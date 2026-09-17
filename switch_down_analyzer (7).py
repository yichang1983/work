#!/usr/bin/env python3
"""
FortiSwitch "Switch-Down" Analyzer  ·  STANDALONE (uplink + SiteOps email)
==========================================================================
For when a managed FortiSwitch is DOWN / unreachable. Nothing to do with
STP-loop analysis. Give it ONE file (or several) containing the collections
below, and it reports DOWN switches, the CAPWAP disconnect timeline, each
switch's last events before it dropped, link flaps, DMI optical alarms, ISL
timeouts, the UPLINK switch (Switch / Serial / IP) for each row — plus TWO
one-click email options on the CAPWAP timeline / down-switch tables:

  * "send email"    -> opens Outlook via mailto (quick, plain text)
  * "download .eml" -> downloads a full-HTML draft (bold, bullets, image
                       placeholder, signature). Double-click it and Outlook
                       opens it as an editable draft (X-Unsent: 1).

Both auto-fill Site / Device / Serial; you add the ServiceNow / PagerDuty ID.

Uplink resolution — two independent sources
-------------------------------------------
  * get-physical-conn standard : switch-to-switch topology (UP switches). The
    `_FlInK1_MLAG0_` side is the child; the other side is its uplink/parent.
  * ISL timeouts (central log)  : a DOWN switch DISAPPEARS from get-physical-conn,
    so its uplink is taken from the ISL timeout — the *reporting* switch is the
    uplink, trunk(<serial-suffix>-N) names the down switch, portNN is the uplink
    switch's port.

>>> BEFORE RUNNING — collect these on the FortiGate and save into ONE file <<<
    execute switch-controller get-conn-status
    execute switch-controller get-physical-conn standard
    execute log filter reset
    execute log filter device disk
    execute log filter category event
    execute log filter field subtype switch-controller
    execute log filter view-lines 1000
    execute log display

Usage
-----
    python switch_down_analyzer.py                       # GUI: pick file(s)
    python switch_down_analyzer.py evidence.txt          # one combined file
    python switch_down_analyzer.py conn.txt central.txt physconn.txt
    #   optional:  --out report.html   --no-open
"""
from __future__ import annotations
import argparse
import html
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

LOGID = {
    "0115032695": ("link",        "FortiSwitch link (port up/down · DMI optical)"),
    "0115032696": ("stp",         "STP role / state change"),
    "0115032697": ("isl",         "ISL timing-out on trunk member"),
    "0115032699": ("ntp",         "NTP time-sync (noise)"),
    "0115032606": ("capwap-down", "CAPWAP Tunnel DOWN — switch lost management"),
    "0115032605": ("capwap-up",   "CAPWAP Tunnel UP — switch recovered"),
    "0115032622": ("connected",   "Switch connected via FortiLink"),
    "0115022904": ("caputp-leave","CAPUTP session leave (echo timeout)"),
    "0115022871": ("nac-sync",    "NAC MAC cache sync"),
    "0115022892": ("sync-done",   "Switch config sync complete"),
    "0100001401": ("link", "Physical port DOWN"),
    "0100001400": ("link", "Physical port UP"),
    "0105008255": ("stp",  "STP role change"),
    "0105008254": ("stp",  "STP state change"),
}
NOISE_KINDS = {"ntp", "nac-sync", "sync-done", "connected"}
SERIAL_RE = re.compile(r"^[A-Z][0-9A-Z]{9,}$")

# --- SiteOps device-down email templates ----------------------------------- #
EMAIL_SUBJECT = "{SITE} \u2013 {DEVICE} down (S/N {SERIAL}) \u2013 {INCIDENT_OR_PAGERDUTY_ID}"

EMAIL_BODY = """Hi {SITE} SiteOps,

We were paged that the following network device is currently down:

- Device: {DEVICE}
- Serial Number: {SERIAL}
- Ticket: {SERVICE_NOW_INCIDENT} (please add updates here)

The switch currently appears as follows:
[Insert image here]

Could you please:
- Confirm whether any planned maintenance is/was in progress. If yes, please include the change reference (e.g., CHG00xxxxx).
- If no maintenance, kindly perform:
  1. Before reboot: take clear photos of power PSU LEDs, system/alarm LEDs, and uplink ports (link/activity).
  2. Power cycle the device once.
  3. Wait 5 minutes, then take after-reboot photos of the same LEDs/ports.
  4. Share the photos in your reply.

Optional quick checks while onsite (if safe to do so):
- Verify power feeds/PDUs are on and PSUs are seated; check for fan/alarm indicators.
- Visually confirm uplink/SFP/SFP+ connectivity (avoid disturbing client patching).
- Note any audible alarms or module fault LEDs.

Please reply with:
- Maintenance yes/no + reference
- Photos (before/after)
- Any observations (power, LEDs, cabling, ambient conditions)
- Time actions were performed

Regards,
Yi-Chang Chen
Senior Network Engineer, Global
One Stonecutter Street
London, EC4A 4AH
United Kingdom
yi-chang.chen@vantage-dc.com
vantage-dc.com
"""

# HTML version for the .eml (keeps bold / bullets / image placeholder / signature)
EMAIL_BODY_HTML = """<div style="font-family:Calibri,Segoe UI,Arial,sans-serif;font-size:11pt;color:#201f1e">
<p><b>Hi {SITE} SiteOps,</b></p>
<p><b>We were paged that the following network device is currently down:</b></p>
<ul>
<li>Device: {DEVICE}</li>
<li>Serial Number: {SERIAL}</li>
<li>Ticket: {SERVICE_NOW_INCIDENT} (please add updates here)</li>
</ul>
<p><b>The switch currently appears as follows:</b><br><b>[Insert image here]</b></p>
<p><b>Could you please:</b></p>
<ul>
<li>Confirm whether any planned maintenance is/was in progress. If yes, please include the change reference (e.g., CHG00xxxxx).</li>
<li>If no maintenance, kindly perform:
<ol>
<li>Before reboot: take clear photos of power PSU LEDs, system/alarm LEDs, and uplink ports (link/activity).</li>
<li>Power cycle the device once.</li>
<li>Wait 5 minutes, then take after-reboot photos of the same LEDs/ports.</li>
<li>Share the photos in your reply.</li>
</ol></li>
</ul>
<p><b>Optional quick checks while onsite (if safe to do so):</b></p>
<ul>
<li>Verify power feeds/PDUs are on and PSUs are seated; check for fan/alarm indicators.</li>
<li>Visually confirm uplink/SFP/SFP+ connectivity (avoid disturbing client patching).</li>
<li>Note any audible alarms or module fault LEDs.</li>
</ul>
<p><b>Please reply with:</b></p>
<ul>
<li>Maintenance yes/no + reference</li>
<li>Photos (before/after)</li>
<li>Any observations (power, LEDs, cabling, ambient conditions)</li>
<li>Time actions were performed</li>
</ul>
<p>Regards,<br>
<b>Yi-Chang Chen</b><br>
<b>Senior Network Engineer, Global</b><br>
One Stonecutter Street<br>
London, EC4A 4AH<br>
United Kingdom<br>
<a href="mailto:yi-chang.chen@vantage-dc.com">yi-chang.chen@vantage-dc.com</a><br>
<a href="http://www.vantage-dc.com">vantage-dc.com</a></p>
</div>"""


def read_text(p: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return p.read_text(encoding=enc, errors="ignore")
        except Exception:
            continue
    return p.read_text(errors="ignore")


def kvq(line: str, key: str) -> str:
    m = re.search(rf'{key}="([^"]*)"', line)
    return m.group(1) if m else ""


def kv_any(line: str, key: str) -> str:
    m = re.search(rf'{key}="([^"]*)"', line)
    if m:
        return m.group(1)
    m = re.search(rf'{key}=(\S+)', line)
    return m.group(1) if m else ""


def esc(x) -> str:
    return html.escape(str(x))


def attr(x) -> str:
    return html.escape(str(x), quote=True)


def looks_serial(tok: str) -> bool:
    return bool(SERIAL_RE.match(tok)) and "-" not in tok


def site_of(name: str, serial: str = "") -> str:
    if name and "-" in name:
        return name.split("-", 1)[0]
    if name:
        return name
    return serial or ""


# --------------------------------------------------------------------------- #
@dataclass
class ConnSwitch:
    serial: str
    name: str = ""
    status: str = ""
    ip: str = ""
    up: bool = True


def parse_conn_status(text: str) -> Tuple[List[ConnSwitch], Optional[Tuple[int, int, int]]]:
    out: List[ConnSwitch] = []
    counts = None
    serial_re = re.compile(r"\b([A-Z]{1,6}[0-9A-Z]{6,}\d{2,})\b")
    ip_re = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")
    up_re = re.compile(r"\b(Up|Down|Authorized/(?:up|down)|Discovered|Offline)\b", re.I)
    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        s = line.strip()
        if not s:
            continue
        if "logid=" in line or "eventtime=" in line or "subtype=" in line:
            continue
        if "<<" in line or ">>" in line or "(port" in line or "get-physical-conn" in line:
            continue
        mh = re.search(r"Managed[- ]Switches?:?\s*(\d+).*?UP:?\s*(\d+).*?DOWN:?\s*(\d+)", s, re.I)
        if mh:
            counts = (int(mh.group(1)), int(mh.group(2)), int(mh.group(3)))
            continue
        if s.lower().startswith(("switch-id", "swid", "fortiswitch", "managed", "name ", "status", "flags")):
            continue
        msn = serial_re.search(s)
        if not msn:
            continue
        serial = msn.group(1)
        mip = ip_re.search(s)
        mstat = up_re.search(s)
        status = mstat.group(1) if mstat else ""
        up = not (("down" in status.lower()) or ("offline" in status.lower()))
        name = ""
        for t in reversed(s.split()):
            if t == serial or ip_re.match(t) or up_re.match(t) or t.replace("-", "").isdigit():
                continue
            if re.match(r"^\d+\.\d+", t):
                continue
            name = t
            break
        mname = re.search(r"\b([A-Z]{2,5}\d{0,3}-[A-Za-z0-9_-]+)\b", s)
        if mname and mname.group(1) != serial:
            name = mname.group(1)
        out.append(ConnSwitch(serial=serial, name=name, status=status,
                              ip=(mip.group(1) if mip else ""), up=up))
    return out, counts


# --------------------------------------------------------------------------- #
@dataclass
class CEvent:
    date: str; time: str; ts: str
    logid: str; kind: str; meaning: str
    name: str; sn: str; port: str
    action: str; status: str; level: str; msg: str
    raw: str = ""


@dataclass
class Central:
    total: int = 0
    noise: int = 0
    events: List[CEvent] = field(default_factory=list)
    link: List[CEvent] = field(default_factory=list)
    stp: List[CEvent] = field(default_factory=list)
    isl: List[CEvent] = field(default_factory=list)
    dmi: List[CEvent] = field(default_factory=list)
    capwap_down: List[CEvent] = field(default_factory=list)
    capwap_up: List[CEvent] = field(default_factory=list)
    flap: Counter = field(default_factory=Counter)
    dmi_raise: Counter = field(default_factory=Counter)
    span: Tuple[str, str] = ("", "")


def parse_central(text: str) -> Central:
    c = Central()
    times: List[str] = []
    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        m = re.search(r'logid="(\d+)"', line)
        if not m:
            continue
        c.total += 1
        lid = m.group(1)
        kind, meaning = LOGID.get(lid, ("other", "other switch-controller event"))
        if kind in NOISE_KINDS:
            c.noise += 1
            continue
        date = kv_any(line, "date"); time = kv_any(line, "time")
        if date or time:
            times.append(f"{date} {time}".strip())
        ev = CEvent(date=date, time=time, ts=f"{date} {time}".strip(),
                    logid=lid, kind=kind, meaning=meaning,
                    name=kvq(line, "name"), sn=kvq(line, "sn"),
                    port=kvq(line, "switchphysicalport"),
                    action=kvq(line, "action"), status=kvq(line, "status"),
                    level=kvq(line, "level"), msg=kvq(line, "msg"),
                    raw=line.strip())
        c.events.append(ev)
        if kind == "link":
            if ev.action in ("port-down", "port-up") or ev.status in ("down", "up"):
                c.link.append(ev)
                if ev.status == "down" or ev.action == "port-down":
                    c.flap[(ev.name, ev.port)] += 1
            if "DMI_RX_POWER_LOW" in ev.msg or "DMI_RX_POWER" in ev.msg:
                c.dmi.append(ev)
                if "Raised" in ev.msg:
                    c.dmi_raise[(ev.name, ev.port)] += 1
        elif kind == "stp":
            c.stp.append(ev)
        elif kind == "isl":
            c.isl.append(ev)
        elif kind == "capwap-down":
            c.capwap_down.append(ev)
        elif kind == "capwap-up":
            c.capwap_up.append(ev)
    if times:
        ts_sorted = sorted(t for t in times if t.strip())
        c.span = (ts_sorted[0], ts_sorted[-1])
    c.link.sort(key=lambda e: e.ts)
    c.capwap_down.sort(key=lambda e: e.ts)
    return c


def last_events_before(c: Central, name: str, ts: str, n: int = 5) -> List[CEvent]:
    rel = [e for e in c.link + c.stp + c.dmi + c.isl
           if e.name == name and (not ts or e.ts <= ts)]
    rel.sort(key=lambda e: e.ts)
    return rel[-n:]


# --------------------------------------------------------------------------- #
CONN_LINE = re.compile(r"^(\S+)\(([^)]*)\)\s*<<-+>>\s*(\S+)\(([^)]*)\)\s*$")


def _split_port(field: str) -> Tuple[str, str]:
    if "/" in field:
        p, lbl = field.split("/", 1)
        return p.strip(), lbl.strip()
    return field.strip(), ""


def parse_physical_conn(text: str) -> Dict[str, List[Tuple[str, str, str]]]:
    uplinks: Dict[str, List[Tuple[str, str, str]]] = {}
    in_tier2 = False
    seen_any = False
    for raw in text.splitlines():
        line = raw.rstrip("\r\n").strip()
        if not line:
            continue
        if line.startswith("Tier 2+"):
            in_tier2 = True; seen_any = True; continue
        if line.startswith(("Tier 1", "FortiGate(s)")) or "FortiLink interface" in line:
            in_tier2 = line.startswith("Tier 2+"); continue
        if not in_tier2:
            continue
        m = CONN_LINE.match(line)
        if not m:
            continue
        a, af, b, bf = m.group(1), m.group(2), m.group(3), m.group(4)
        ap, al = _split_port(af)
        bp, bl = _split_port(bf)
        if al == "_FlInK1_ICL0_" or bl == "_FlInK1_ICL0_":
            continue
        child = parent = child_port = parent_port = None
        if al == "_FlInK1_MLAG0_":
            child, child_port, parent, parent_port = a, ap, b, bp
        elif bl == "_FlInK1_MLAG0_":
            child, child_port, parent, parent_port = b, bp, a, ap
        else:
            def suffix_match(label, other):
                core = re.sub(r"-\d+$", "", label)
                return bool(core) and other.endswith(core)
            if bl and suffix_match(bl, a):
                child, child_port, parent, parent_port = a, ap, b, bp
            elif al and suffix_match(al, b):
                child, child_port, parent, parent_port = b, bp, a, ap
            else:
                continue
        if not child or not parent:
            continue
        uplinks.setdefault(child, [])
        entry = (parent, parent_port, child_port)
        if entry not in uplinks[child]:
            uplinks[child].append(entry)
    return uplinks if seen_any else {}


def build_isl_uplinks(c: Central) -> Dict[str, List[Tuple[str, str, str]]]:
    out: Dict[str, List[Tuple[str, str, str]]] = {}
    for e in c.isl:
        mt = re.search(r"trunk\(([^)]+)\)", e.msg)
        if not mt:
            continue
        core = re.sub(r"-\d+$", "", mt.group(1))
        mp = re.search(r"\b(port\d+)\b", e.msg)
        port = mp.group(1) if mp else (e.port or "")
        out.setdefault(core, [])
        rec = (e.name, e.sn, port)
        if rec not in out[core]:
            out[core].append(rec)
    return out


# --------------------------------------------------------------------------- #
CSS = """
:root{--bg:#0f1220;--card:#1a1f35;--ink:#e8ecf4;--mut:#9aa4bf;--line:#2a3150}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--ink);
font:14px/1.55 -apple-system,Segoe UI,Roboto,Arial,sans-serif}
.wrap{max-width:1440px;margin:0 auto;padding:26px 20px 90px}
h1{font-size:22px;margin:0 0 2px} h2{font-size:15px;margin:22px 0 6px;color:#cfe0ff}
.sub{color:var(--mut);margin:0 0 18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:12px 0;overflow:hidden}
.verdict{border-left:6px solid;padding:16px 18px;border-radius:12px;font-size:15px}
.chips{display:flex;gap:12px;flex-wrap:wrap}
.chip{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:104px;text-align:center;flex:1}
.chip-v{font-size:22px;font-weight:700} .chip-l{color:var(--mut);font-size:12px}
.tscroll{overflow-x:auto;max-width:100%}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;white-space:nowrap}
td.wrap,th.wrap{white-space:normal}
th{color:var(--mut);font-weight:600}
.upcol{background:#12182b}  th.upcol{color:#7fb0ff}
table.isl{table-layout:fixed}
table.isl td,table.isl th{vertical-align:top}
table.isl td.detail,table.isl th.detail{white-space:normal;overflow-wrap:anywhere}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;color:#fff;font-weight:700;font-size:11px}
.src{display:inline-block;font-size:9.5px;font-weight:700;border-radius:4px;padding:0 4px;margin-left:4px;vertical-align:middle}
.src.isl{background:#5a2a12;color:#ffd0a8} .src.topo{background:#173a2a;color:#a8ecc4}
code{background:#0c0f1c;border:1px solid var(--line);border-radius:6px;padding:1px 6px;color:#c9d4ff}
.mut{color:var(--mut)} .miss{color:#8a94b0;font-style:italic}
.cmd{background:#0c0f1c;border:1px solid var(--line);border-radius:10px;padding:12px 14px;white-space:pre-wrap;color:#c9d4ff;font-family:ui-monospace,Consolas,monospace;font-size:12px}
.bar{height:9px;border-radius:5px;display:inline-block;vertical-align:middle}
.warn{background:#3a1414;border:1px solid #b00020;border-radius:10px;padding:10px 14px;color:#ffd7d7;font-size:12.5px;margin:10px 0}
.topbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 18px}
.topbar .sub{margin:0}
.exportbtn{cursor:pointer;margin-left:auto;border:1px solid #34518c;background:#16233f;color:#bcd4ff;border-radius:8px;padding:7px 16px;font-size:12.5px;font-weight:600}
.exportbtn:hover{border-color:#4a6dc0;background:#1b2c50}
.mailbtn{cursor:pointer;display:inline-block;border:1px solid #2f5233;background:#12291a;color:#8ee6a2;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;white-space:nowrap;margin:1px 0}
.mailbtn:hover{border-color:#3f8a55;background:#173a24}
.emlbtn{cursor:pointer;display:inline-block;border:1px solid #4a4a8c;background:#1a1a3a;color:#c9c0ff;border-radius:6px;padding:3px 10px;font-size:11px;font-weight:600;white-space:nowrap;margin:1px 0}
.emlbtn:hover{border-color:#6a6ad0;background:#242452}
th.mailcol,td.mailcol{background:#12211a}
#alllogs{display:none}
.logtoggle{cursor:pointer;color:#7fb0ff;font-size:11.5px;user-select:none;white-space:nowrap}
.logtoggle:hover{text-decoration:underline}
.logpanel{background:#0a0d18;border:1px solid #2a3150;border-radius:10px;margin:6px 0 10px;padding:10px 12px}
.logpanel[hidden]{display:none}
.loghead{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:8px;font-size:11.5px;color:#9aa4bf}
.loghead .lbl{font-weight:600;color:#c9d4ff}
.fbtn{cursor:pointer;border:1px solid #2a3150;background:#141a30;color:#c9d4ff;border-radius:6px;padding:2px 10px;font-size:11px}
.fbtn:hover{border-color:#3a4a8c} .fbtn.on{background:#2b3566;border-color:#4a5da0;color:#fff}
.copybtn{cursor:pointer;margin-left:auto;border:1px solid #2f5233;background:#12291a;color:#8ee6a2;border-radius:6px;padding:2px 12px;font-size:11px;font-weight:600}
.copybtn:hover{border-color:#3f8a55}
.logbox{max-height:320px;overflow:auto;background:#080b14;border:1px solid #1c2440;border-radius:8px;
padding:8px 10px;font-family:ui-monospace,Consolas,monospace;font-size:11.5px;line-height:1.55;
white-space:pre-wrap;word-break:break-all;color:#c6d2f0}
.logbox .ln{display:block;padding:1px 2px;border-bottom:1px dashed #141c34}
.logbox .ln:last-child{border-bottom:none}
.logbox .down{color:#ff8f8f} .logbox .up{color:#8ee6a2} .logbox .dmi{color:#ffcf7a} .logbox .stp{color:#c9b3ff}
.logbox.f-down .ln:not(.down){display:none}
.logbox.f-up   .ln:not(.up){display:none}
.logbox.f-dmi  .ln:not(.dmi){display:none}
.logbox.f-stp  .ln:not(.stp){display:none}
.qs{background:#111a30;border:1px solid #24325c;border-radius:14px;padding:18px 20px;margin:22px 0 8px}
.qs h3{margin:0 0 4px;font-size:15px;color:#cfe0ff} .qs h4{margin:14px 0 4px;font-size:13px;color:#8ee6ff}
.qs ol{margin:6px 0 0 20px;padding:0} .qs li{margin:4px 0}
.qs .step{display:inline-block;min-width:20px;height:20px;line-height:20px;text-align:center;border-radius:50%;background:#2b3566;color:#fff;font-weight:700;font-size:11px;margin-right:6px}
.qs .kbd{display:inline-block;border:1px solid #2f5233;background:#12291a;color:#8ee6a2;border-radius:5px;padding:0 6px;font-size:11px;font-weight:600}
.qs .kbd.blue{border-color:#34518c;background:#16233f;color:#bcd4ff}
.qs .kbd.violet{border-color:#4a4a8c;background:#1a1a3a;color:#c9c0ff}
.qs .kbd.plain{border-color:#2a3150;background:#141a30;color:#c9d4ff}
.foot{color:var(--mut);font-size:12px;margin-top:24px}
"""

JS = """
var MAIL_SUBJECT=%%SUBJECT%%;
var MAIL_BODY=%%BODY%%;
var MAIL_BODY_HTML=%%BODYHTML%%;
function toggleLog(id, el){var p=document.getElementById(id);if(!p)return;p.hidden=!p.hidden;
 el.textContent=p.hidden?'\u25B6 show full log':'\u25BC hide log';}
function visLines(panel){var out=[];panel.querySelectorAll('.logbox .ln').forEach(function(n){
 if(getComputedStyle(n).display!=='none')out.push(n);});return out;}
function updCopy(panel,cls){var cb=panel.querySelector('.copybtn');if(!cb)return;
 var n=visLines(panel).length;cb.textContent='\U0001F4CB copy '+(cls?cls:'all')+' ('+n+')';}
function filt(btn,cls){var panel=btn.closest('.logpanel');var box=panel.querySelector('.logbox');
 box.className='logbox'+(cls?' f-'+cls:'');panel.querySelectorAll('.fbtn').forEach(function(b){b.classList.toggle('on',b===btn);});updCopy(panel,cls);}
function copyLog(btn){var panel=btn.closest('.logpanel');
 var text=visLines(panel).map(function(n){return n.textContent;}).join('\\n');
 var done=function(){var t=btn.textContent;btn.textContent='\u2705 copied';setTimeout(function(){btn.textContent=t;},1200);};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,function(){fallback(text,done);});}else{fallback(text,done);}}
function fallback(text,done){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';
 document.body.appendChild(ta);ta.focus();ta.select();try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(ta);}
function exportAll(btn){var holder=document.getElementById('alllogs');var text=holder?holder.textContent:'';
 var fn=(holder&&holder.getAttribute('data-fn'))||'switch_down_logs.txt';
 try{var blob=new Blob([text],{type:'text/plain;charset=utf-8'});var url=URL.createObjectURL(blob);
 var a=document.createElement('a');a.href=url;a.download=fn;document.body.appendChild(a);a.click();document.body.removeChild(a);
 setTimeout(function(){URL.revokeObjectURL(url);},1500);var t=btn.textContent;btn.textContent='\u2705 exported';setTimeout(function(){btn.textContent=t;},1400);}
 catch(e){var w=window.open('','_blank');if(w){w.document.write('<pre>'+text.replace(/[&<>]/g,function(ch){return ch==='&'?'&amp;':ch==='<'?'&lt;':'&gt;';})+'</pre>');}}}
function fill(t,d){return t.replace(/\\{SITE\\}/g,d.site).replace(/\\{DEVICE\\}/g,d.device).replace(/\\{SERIAL\\}/g,d.serial);}
function btnData(btn){return {site:btn.getAttribute('data-site')||'',device:btn.getAttribute('data-device')||'',serial:btn.getAttribute('data-serial')||''};}
function sendMail(btn){
 var d=btnData(btn);var subj=fill(MAIL_SUBJECT,d);var body=fill(MAIL_BODY,d);
 var href='mailto:?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(body);
 if(href.length>2000){
   var full='Subject: '+subj+'\\n\\n'+body;
   if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(full);}
   window.location.href='mailto:?subject='+encodeURIComponent(subj);
   var t=btn.textContent;btn.textContent='\u2709 opened (body copied)';setTimeout(function(){btn.textContent=t;},1600);
   return;
 }
 window.location.href=href;
 var o=btn.textContent;btn.textContent='\u2709 opening…';setTimeout(function(){btn.textContent=o;},1400);
}
function dlEml(btn){
 var d=btnData(btn);var subj=fill(MAIL_SUBJECT,d);var bodyHtml=fill(MAIL_BODY_HTML,d);
 // RFC822 .eml with X-Unsent:1 so Outlook opens it as an editable draft, HTML kept
 var eml='';
 eml+='To: \\r\\n';
 eml+='Subject: '+subj+'\\r\\n';
 eml+='X-Unsent: 1\\r\\n';
 eml+='Content-Type: text/html; charset=utf-8\\r\\n';
 eml+='Content-Transfer-Encoding: 8bit\\r\\n';
 eml+='\\r\\n';
 eml+='<html><body>'+bodyHtml+'</body></html>\\r\\n';
 var safe=(d.device||'device').replace(/[^A-Za-z0-9._-]/g,'_');
 var fn='SiteOps_'+safe+'_down.eml';
 try{
   var blob=new Blob([eml],{type:'message/rfc822'});
   var url=URL.createObjectURL(blob);
   var a=document.createElement('a');a.href=url;a.download=fn;document.body.appendChild(a);a.click();document.body.removeChild(a);
   setTimeout(function(){URL.revokeObjectURL(url);},1500);
   var t=btn.textContent;btn.textContent='\u2705 .eml saved';setTimeout(function(){btn.textContent=t;},1600);
 }catch(e){ alert('Could not create .eml: '+e); }
}
"""


def build_report(conn, counts, c: Central, uplinks_topo, files):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    down_conn = [s for s in conn if not s.up]
    dmi_top = c.dmi_raise.most_common(15)
    flap_top = c.flap.most_common(15)

    id_by_serial: Dict[str, Tuple[str, str]] = {}
    id_by_name: Dict[str, Tuple[str, str]] = {}
    for s in conn:
        if s.serial:
            id_by_serial[s.serial] = (s.name, s.ip)
        if s.name:
            id_by_name[s.name] = (s.serial, s.ip)
    for e in c.events:
        if e.sn and e.sn not in id_by_serial:
            id_by_serial[e.sn] = (e.name, "")
        if e.name and e.name not in id_by_name:
            id_by_name[e.name] = (e.sn, "")

    def resolve_identity(tok: str) -> Tuple[str, str, str]:
        if tok in id_by_serial:
            nm, ip = id_by_serial[tok]; return (nm or tok, tok, ip)
        if tok in id_by_name:
            sr, ip = id_by_name[tok]; return (tok, sr, ip)
        if looks_serial(tok):
            return ("", tok, "")
        return (tok, "", "")

    isl_uplinks = build_isl_uplinks(c)

    def resolve_uplink(name: str, serial: str) -> List[dict]:
        seen = set(); rows = []
        if serial:
            for core, entries in isl_uplinks.items():
                if serial.endswith(core):
                    for rn, rs, port in entries:
                        r_name, r_serial, r_ip = resolve_identity(rn or rs)
                        key = r_serial or r_name or rn
                        if key in seen:
                            continue
                        seen.add(key)
                        rows.append({"name": r_name or rn, "serial": r_serial or rs,
                                     "ip": r_ip, "port": port, "src": "ISL"})
        for tok in (serial, name):
            if tok and tok in uplinks_topo:
                for ptok, pport, cport in uplinks_topo[tok]:
                    r_name, r_serial, r_ip = resolve_identity(ptok)
                    key = r_serial or r_name or ptok
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append({"name": r_name or ptok, "serial": r_serial,
                                 "ip": r_ip, "port": pport, "src": "topo"})
        return rows

    def uplink_cells(name: str, serial: str) -> Tuple[str, str, str]:
        ups = resolve_uplink(name, serial)
        if not ups:
            return ("<span class='mut'>—</span>", "<span class='mut'>—</span>", "<span class='mut'>—</span>")
        sw = "<br>".join(
            f"<code>{esc(u['name'] or '?')}</code>"
            + (f"<span class='mut'>:{esc(u['port'])}</span>" if u['port'] else "")
            + f"<span class='src {u['src'].lower()}'>{esc(u['src'])}</span>"
            for u in ups)
        sr = "<br>".join((esc(u['serial']) if u['serial'] else "<span class='mut'>—</span>") for u in ups)
        ip = "<br>".join((esc(u['ip']) if u['ip'] else "<span class='mut'>—</span>") for u in ups)
        return (sw, sr, ip)

    def dash(x) -> str:
        return esc(x) if x else "<span class='mut'>—</span>"

    def _cls(e: CEvent) -> str:
        if e.status == "down" or e.action == "port-down": return "down"
        if e.status == "up" or e.action == "port-up": return "up"
        if "DMI_RX_POWER" in e.msg: return "dmi"
        if e.kind == "stp": return "stp"
        return ""

    _counter = [0]

    def make_drawer(events, label):
        evs = sorted(events, key=lambda e: e.ts)
        if not evs:
            return ("<span class='mut'>—</span>", "")
        _counter[0] += 1
        pid = f"log_{_counter[0]}"
        nd = sum(1 for e in evs if _cls(e) == "down"); nu = sum(1 for e in evs if _cls(e) == "up")
        ndmi = sum(1 for e in evs if _cls(e) == "dmi"); nstp = sum(1 for e in evs if _cls(e) == "stp")
        lines = "".join(f"<span class='ln {_cls(e)}'>{esc(e.raw)}</span>" for e in evs)
        btns = [f"<span class='fbtn on' onclick=\"filt(this,'')\">All ({len(evs)})</span>"]
        if nd:   btns.append(f"<span class='fbtn' onclick=\"filt(this,'down')\">🔴 down ({nd})</span>")
        if nu:   btns.append(f"<span class='fbtn' onclick=\"filt(this,'up')\">🟢 up ({nu})</span>")
        if ndmi: btns.append(f"<span class='fbtn' onclick=\"filt(this,'dmi')\">🟡 optical ({ndmi})</span>")
        if nstp: btns.append(f"<span class='fbtn' onclick=\"filt(this,'stp')\">🟣 STP ({nstp})</span>")
        copy = f"<span class='copybtn' onclick=\"copyLog(this)\">\U0001F4CB copy all ({len(evs)})</span>"
        toggle = f"<span class='logtoggle' onclick=\"toggleLog('{pid}',this)\">\u25B6 show full log</span>"
        panel = (f"<div id='{pid}' class='logpanel' hidden><div class='loghead'>"
                 f"<span class='lbl'>{esc(label)}</span><span class='mut'>· {len(evs)} lines</span>"
                 f"{''.join(btns)}{copy}</div><div class='logbox'>{lines}</div></div>")
        return (toggle, panel)

    def ev_for_switch(name, sn):
        return [e for e in c.events if (name and e.name == name) or (sn and e.sn == sn)]

    def ev_for_port(name, port):
        return [e for e in c.events if e.name == name and e.port == port]

    def sn_for(name, sn=""):
        if sn: return sn
        if name in id_by_name: return id_by_name[name][0]
        return ""

    def ip_for(name, sn=""):
        if name in id_by_name and id_by_name[name][1]:
            return id_by_name[name][1]
        if sn in id_by_serial and id_by_serial[sn][1]:
            return id_by_serial[sn][1]
        s2 = sn_for(name, sn)
        if s2 in id_by_serial and id_by_serial[s2][1]:
            return id_by_serial[s2][1]
        return ""

    def mail_cell(name, serial):
        st = site_of(name, serial)
        d = f"data-site=\"{attr(st)}\" data-device=\"{attr(name or serial)}\" data-serial=\"{attr(serial)}\""
        return (f"<span class='mailbtn' onclick=\"sendMail(this)\" {d}>\u2709 send email</span><br>"
                f"<span class='emlbtn' onclick=\"dlEml(this)\" {d}>\u2B07 download .eml</span>")

    down_events = [e for e in c.link if e.status == "down" or e.action == "port-down"]

    def port_span(events, name, port):
        tss = sorted(x.ts for x in events if x.name == name and x.port == port and x.ts)
        return (tss[0], tss[-1]) if tss else ("", "")

    cap_unrec = [e for e in c.capwap_down if e.name not in {u.name for u in c.capwap_up}]
    if down_conn or cap_unrec:
        names = [s.name or s.serial for s in down_conn] or [e.name for e in cap_unrec]
        verdict = (f"{len(down_conn) or len(cap_unrec)} switch(es) DOWN / unrecovered: "
                   f"{', '.join(names[:6])}{'…' if len(names) > 6 else ''}. "
                   f"Uplink switch shown per row; use 'send email' / 'download .eml' to page SiteOps.")
        vcls = "CRITICAL"
    elif c.capwap_down:
        verdict = f"{len(c.capwap_down)} CAPWAP tunnel-down event(s), all recovered. Investigate flaps/optical below."
        vcls = "HIGH"
    elif dmi_top:
        p = dmi_top[0][0]
        verdict = f"Optical alarms present: {p[0]} {p[1]} raised DMI_RX_POWER_LOW. Clean/reseat fibre & SFP."
        vcls = "HIGH"
    elif flap_top:
        p = flap_top[0][0]
        verdict = f"No switch down; chronic flapping on {p[0]} {p[1]} ({flap_top[0][1]}×)."
        vcls = "MEDIUM"
    else:
        verdict = "No DOWN switches, CAPWAP drops, flaps or optical alarms in the provided evidence."
        vcls = "OK"

    RC = {"CRITICAL": "#b00020", "HIGH": "#e8590c", "MEDIUM": "#f0a202", "LOW": "#2b8a3e", "OK": "#868e96"}

    def chip(l, v, col):
        return (f'<div class="chip"><div class="chip-v" style="color:{col}">{v}</div>'
                f'<div class="chip-l">{l}</div></div>')

    P = [f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Switch-Down Analyzer</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>FortiSwitch Switch-Down Analyzer</h1>
<div class="topbar"><p class="sub">Generated {esc(ts)} · source <code>{esc(', '.join(files) or '-')}</code></p>
<span class="exportbtn" onclick="exportAll(this)">\u2B07 export all logs (.txt)</span></div>
<div class="card verdict" style="border-color:{RC[vcls]}">
<b style="color:{RC[vcls]}">VERDICT · {vcls}</b><br>{esc(verdict)}</div>
"""]

    total_sw = counts[0] if counts else len(conn)
    up_sw = counts[1] if counts else sum(1 for s in conn if s.up)
    down_sw = counts[2] if counts else len(down_conn)
    P.append('<div class="chips">')
    P.append(chip("Managed", total_sw or "—", '#c9d4ff'))
    P.append(chip("UP", up_sw if conn or counts else "—", '#2b8a3e'))
    P.append(chip("DOWN", down_sw if (conn or counts) else "—", RC['CRITICAL'] if down_sw else '#2b8a3e'))
    P.append(chip("CAPWAP drops", len(c.capwap_down), RC['CRITICAL'] if c.capwap_down else '#2b8a3e'))
    P.append(chip("Optical alarms", sum(c.dmi_raise.values()), RC['CRITICAL'] if c.dmi_raise else '#2b8a3e'))
    P.append(chip("Link flaps", sum(c.flap.values()), RC['HIGH'] if c.flap else '#2b8a3e'))
    P.append(chip("Topo links", sum(len(v) for v in uplinks_topo.values()), '#c9d4ff' if uplinks_topo else '#868e96'))
    P.append('</div>')

    ev_conn = "✅ get-conn-status" if conn else "<span class='miss'>⬜ get-conn-status</span>"
    ev_log = "✅ central log" if c.total else "<span class='miss'>⬜ central log</span>"
    ev_pc = "✅ get-physical-conn" if uplinks_topo else "<span class='miss'>⬜ get-physical-conn (topology uplinks)</span>"
    P.append(f'<div class="card"><b>Evidence detected</b><br>{ev_conn} &nbsp; {ev_log} &nbsp; {ev_pc}')
    if c.total:
        P.append(f'<br><span class="mut">{c.total} switch-controller events · {c.noise} NTP-noise filtered '
                 f'({c.noise*100//max(c.total,1)}%) · span <code>{esc(c.span[0])}</code> → <code>{esc(c.span[1])}</code>'
                 f' · uplink source tags: <span class="src isl">ISL</span> (from ISL timeout, for DOWN switches) '
                 f'<span class="src topo">topo</span> (from get-physical-conn)</span>')
    P.append('</div>')

    # ---- ① DOWN switches ----
    if conn:
        P.append('<h2>① Switch connection status <span class="mut">(get-conn-status)</span></h2><div class="card">')
        if down_conn:
            panels = []
            P.append('<div class="tscroll"><table><tr><th>Switch</th><th>Serial</th><th>IP</th><th>Status</th>'
                     '<th class="wrap">Last events before it went down</th><th>Full log</th>'
                     '<th class="upcol">Uplink Switch</th><th class="upcol">Uplink Serial</th><th class="upcol">Uplink IP</th>'
                     '<th class="mailcol">Email</th></tr>')
            for s in down_conn:
                key = s.name or s.serial
                last = last_events_before(c, key, "", 5) or last_events_before(c, s.serial, "", 5)
                lasttxt = "<br>".join(
                    f"<span class='mut'>{esc(x.ts)}</span> {esc(x.port)} {esc(x.action or x.status or x.kind)}"
                    for x in last) or "<span class='miss'>no matching events</span>"
                tog, pan = make_drawer(ev_for_switch(s.name, s.serial), s.name or s.serial)
                panels.append(pan)
                usw, usr, uip = uplink_cells(s.name, s.serial)
                P.append(f"<tr><td><code>{esc(s.name or '?')}</code></td><td>{dash(s.serial)}</td><td>{dash(s.ip)}</td>"
                         f"<td><span class='pill' style='background:{RC['CRITICAL']}'>{esc(s.status or 'Down')}</span></td>"
                         f"<td class='wrap'>{lasttxt}</td><td>{tog}</td>"
                         f"<td class='upcol'>{usw}</td><td class='upcol'>{usr}</td><td class='upcol'>{uip}</td>"
                         f"<td class='mailcol'>{mail_cell(s.name, s.serial)}</td></tr>")
            P.append("</table></div>")
            P.append("".join(panels))
        else:
            P.append(f"<span class='mut'>All {len(conn)} managed switch(es) report UP.</span>")
        P.append("</div>")
    else:
        P.append('<div class="warn">No get-conn-status section detected. Paste '
                 '<code>execute switch-controller get-conn-status</code> into the same file.</div>')

    # ---- ⓪ CAPWAP timeline ----
    if c.capwap_down:
        P.append('<h2>⓪ CAPWAP disconnect timeline <span class="mut">(who lost management first)</span></h2><div class="card">')
        panels = []
        P.append('<div class="tscroll"><table><tr><th>#</th><th>Date/Time</th><th>Switch</th><th>Serial</th><th>IP</th>'
                 '<th>Recovered?</th><th class="wrap">Last events before down</th><th>Full log</th>'
                 '<th class="upcol">Uplink Switch</th><th class="upcol">Uplink Serial</th><th class="upcol">Uplink IP</th>'
                 '<th class="mailcol">Email</th></tr>')
        up_names = {e.name for e in c.capwap_up}
        for i, e in enumerate(c.capwap_down, 1):
            last = last_events_before(c, e.name, e.ts, 4)
            lasttxt = "<br>".join(
                f"<span class='mut'>{esc(x.ts)}</span> {esc(x.port)} {esc(x.action or x.status or x.kind)}"
                for x in last) or "<span class='mut'>—</span>"
            rec = "✅ up again" if e.name in up_names else "⚠ still down"
            flag = " 🥇 FIRST" if i == 1 else ""
            tog, pan = make_drawer(ev_for_switch(e.name, e.sn), e.name)
            panels.append(pan)
            e_sn = e.sn or sn_for(e.name)
            usw, usr, uip = uplink_cells(e.name, e_sn)
            P.append(f"<tr><td>{i}{flag}</td><td><b>{esc(e.ts)}</b></td><td><code>{esc(e.name)}</code></td>"
                     f"<td>{dash(sn_for(e.name, e.sn))}</td><td>{dash(ip_for(e.name, e.sn))}</td>"
                     f"<td>{rec}</td><td class='wrap'>{lasttxt}</td><td>{tog}</td>"
                     f"<td class='upcol'>{usw}</td><td class='upcol'>{usr}</td><td class='upcol'>{uip}</td>"
                     f"<td class='mailcol'>{mail_cell(e.name, e_sn)}</td></tr>")
        P.append("</table></div>")
        P.append("".join(panels))
        P.append("<span class='mut'>Uplink = the switch/port this down switch connects up to (ISL for DOWN switches, "
                 "topo from get-physical-conn). <b>send email</b> = quick Outlook mailto (plain text). "
                 "<b>download .eml</b> = full-format draft (bold, bullets, image placeholder, signature) — "
                 "double-click it and Outlook opens an editable draft. Site/Device/Serial auto-filled; add the "
                 "ServiceNow / PagerDuty ID.</span></div>")

    # ---- ② optical ----
    if dmi_top:
        P.append('<h2>② Optical / SFP alarms <span class="mut">(DMI_RX_POWER_LOW)</span></h2><div class="card">')
        panels = []; maxn = dmi_top[0][1]
        P.append('<div class="tscroll"><table><tr><th>Switch</th><th>Serial</th><th>IP</th><th>Port</th><th>Raised ×</th>'
                 '<th>First raised</th><th>Last raised</th><th></th><th>Full log</th>'
                 '<th class="upcol">Uplink Switch</th><th class="upcol">Uplink Serial</th><th class="upcol">Uplink IP</th></tr>')
        for (name, port), n in dmi_top:
            f0, f1 = port_span(c.dmi, name, port)
            tog, pan = make_drawer(ev_for_port(name, port), f"{name} {port}"); panels.append(pan)
            usw, usr, uip = uplink_cells(name, sn_for(name))
            P.append(f"<tr><td><code>{esc(name)}</code></td><td>{dash(sn_for(name))}</td><td>{dash(ip_for(name))}</td>"
                     f"<td><code>{esc(port)}</code></td><td><b>{n}</b></td><td>{dash(f0)}</td><td>{dash(f1)}</td>"
                     f"<td><span class='bar' style='width:{int(160*n/maxn)}px;background:#b00020'></span></td><td>{tog}</td>"
                     f"<td class='upcol'>{usw}</td><td class='upcol'>{usr}</td><td class='upcol'>{uip}</td></tr>")
        P.append("</table></div>")
        P.append("".join(panels))
        P.append("<span class='mut'>Same MLAG pair on both members ⇒ suspect shared fibre / patch panel / SFP batch.</span></div>")

    # ---- ③ flap ranking ----
    if flap_top:
        P.append('<h2>③ Link-flap ranking <span class="mut">(port-down count)</span></h2><div class="card">')
        panels = []; maxn = flap_top[0][1]
        P.append('<div class="tscroll"><table><tr><th>#</th><th>Switch</th><th>Serial</th><th>IP</th><th>Port</th><th>Down ×</th>'
                 '<th>First down</th><th>Last down</th><th></th><th>Optical?</th><th>Full log</th>'
                 '<th class="upcol">Uplink Switch</th><th class="upcol">Uplink Serial</th><th class="upcol">Uplink IP</th></tr>')
        for i, ((name, port), n) in enumerate(flap_top, 1):
            f0, f1 = port_span(down_events, name, port)
            opt = "🔴 DMI" if c.dmi_raise.get((name, port)) else ""
            tog, pan = make_drawer(ev_for_port(name, port), f"{name} {port}"); panels.append(pan)
            usw, usr, uip = uplink_cells(name, sn_for(name))
            P.append(f"<tr><td>{i}</td><td><code>{esc(name)}</code></td><td>{dash(sn_for(name))}</td><td>{dash(ip_for(name))}</td>"
                     f"<td><code>{esc(port)}</code></td><td><b>{n}</b></td><td>{dash(f0)}</td><td>{dash(f1)}</td>"
                     f"<td><span class='bar' style='width:{int(110*n/maxn)}px;background:#e8590c'></span></td><td>{opt}</td><td>{tog}</td>"
                     f"<td class='upcol'>{usw}</td><td class='upcol'>{usr}</td><td class='upcol'>{uip}</td></tr>")
        P.append("</table></div>")
        P.append("".join(panels)); P.append("</div>")

    # ---- ④ ISL timeouts ----
    if c.isl:
        P.append('<h2>④ ISL timeouts <span class="mut">(these reveal uplinks of DOWN switches)</span></h2>'
                 '<div class="card"><div class="tscroll"><table class="isl">'
                 '<colgroup><col style="width:160px"><col style="width:190px"><col style="width:150px">'
                 '<col style="width:110px"><col></colgroup>'
                 '<tr><th>Date/Time</th><th>Switch (uplink)</th><th>Serial</th><th>IP</th>'
                 '<th class="detail">Detail — trunk names the DOWN switch</th></tr>')
        for e in c.isl[:25]:
            detail = e.msg.strip() or e.meaning
            P.append(f"<tr><td>{esc(e.ts)}</td><td><code>{esc(e.name)}</code></td>"
                     f"<td>{dash(sn_for(e.name, e.sn))}</td><td>{dash(ip_for(e.name, e.sn))}</td>"
                     f"<td class='detail'>{esc(detail)}</td></tr>")
        P.append("</table></div></div>")

    # ---- ⑤ next actions ----
    sw, pt = (dmi_top[0][0] if dmi_top else (flap_top[0][0] if flap_top else ("<switch>", "<port>")))
    P.append(f"""<h2>⑤ Next actions</h2><div class="card">
<div class="cmd"># re-collect this evidence
execute switch-controller get-conn-status
execute switch-controller get-physical-conn standard
execute log filter reset
execute log filter device disk
execute log filter category event
execute log filter field subtype switch-controller
execute log filter view-lines 1000
execute log display

# for a flagged switch:port (optical / cable)
get switch module summary                                   # RX power / LOS
diagnose switch physical-ports port-stats list {esc(pt)}    # CRC/errors
diagnose switch physical-ports cable-diag {esc(pt)}         # Ok/Open/Short
diagnose switch-controller switch-info port-stats {esc(sw)} # per-switch errors</div>
<span class="mut">A DOWN switch can't be SSH'd — its uplink switch/port (shown above) is where you trace the fibre.
Use <b>send email</b> (quick) or <b>download .eml</b> (full format) to page SiteOps.</span></div>""")

    # ---- Quick-start footer ----
    P.append("""<div class="qs">
<h3>📘 Quick start — how to use this tool</h3>
<h4>① Collect the evidence on the FortiGate</h4>
<div class="cmd">execute switch-controller get-conn-status
execute switch-controller get-physical-conn standard
execute log filter reset
execute log filter device disk
execute log filter category event
execute log filter field subtype switch-controller
execute log filter view-lines 1000
execute log display</div>
<span class="mut">Copy all outputs into ONE file (or several). get-conn-status gives the UP/DOWN list + IP;
get-physical-conn gives the switch-to-switch topology (uplinks of UP switches); the log gives the timeline,
optical alarms, flaps and ISL timeouts (which reveal uplinks of DOWN switches).</span>
<h4>② Run / upload</h4>
<ol>
<li><span class="step">A</span><b>GUI:</b> <span class="kbd plain">python switch_down_analyzer.py</span> then pick the file(s).</li>
<li><span class="step">B</span><b>CLI:</b> <span class="kbd plain">python switch_down_analyzer.py conn.txt central.txt physconn.txt</span></li>
</ol>
<h4>③ Uplink switch + one-click SiteOps email</h4>
<ol style="list-style:none;margin-left:0">
<li><b>topo</b> <span class="src topo">topo</span> — from get-physical-conn (the <code>_FlInK1_MLAG0_</code> side is the child; the other side is its uplink).</li>
<li><b>ISL</b> <span class="src isl">ISL</span> — a DOWN switch is absent from get-physical-conn, so its uplink is read from the ISL timeout.</li>
<li><span class="mailbtn">✉ send email</span> — quick Outlook draft via mailto (<b>plain text</b>: fast, but no bold/bullets).</li>
<li><span class="emlbtn">⬇ download .eml</span> — a <b>full-HTML</b> draft file (bold, bullets, image placeholder, signature). Double-click it → Outlook opens an editable draft (<code>X-Unsent: 1</code>). Site/Device/Serial auto-filled; add the ticket / PagerDuty ID and paste a screenshot.</li>
</ol>
<h4>④ Three ways to read / take the logs</h4>
<ol>
<li><span class="step">1</span><b>Drill</b> — <span class="kbd" style="border-color:#34518c;background:#16233f;color:#7fb0ff">▶ show full log</span> opens a full-width colour-coded panel.</li>
<li><span class="step">2</span><b>Filter + copy</b> — click a type (e.g. <span class="kbd plain">🔴 down</span>) then <span class="kbd">📋 copy down (N)</span> copies only what you see.</li>
<li><span class="step">3</span><b>Export</b> — <span class="kbd blue">⬇ export all logs (.txt)</span> saves the full chronological log with a summary header.</li>
</ol>
</div>
<p class="foot">Standalone Switch-Down analyzer · full date/time + serial + IP + UPLINK switch (topology + ISL) ·
one-click SiteOps email (mailto + full-HTML .eml) · expandable log with per-type filters and filtered copy ·
export-all · NTP noise filtered. Heuristic aid; validate before any action.</p>""")

    # ---- hidden export holder ----
    export_events = sorted(c.events, key=lambda e: e.ts)
    hdr = ["# FortiSwitch Switch-Down Analyzer — exported log",
           f"# generated: {ts}", f"# source: {', '.join(files) or '-'}",
           f"# time span: {c.span[0]} -> {c.span[1]}",
           f"# events: {len(export_events)} (NTP noise excluded: {c.noise})"]
    if conn:
        d = [s for s in conn if not s.up]
        hdr.append(f"# conn-status: {len(conn)} managed, DOWN={len(d)}"
                   + ((": " + ", ".join(f"{(s.name or s.serial)}[{s.serial}/{s.ip or 'no-ip'}]" for s in d)) if d else ""))
    hdr.append("# " + "-" * 60)
    export_text = "\n".join(hdr) + "\n" + "\n".join(e.raw for e in export_events) + "\n"
    fn = f"switch_down_logs_{datetime.now():%Y%m%d_%H%M%S}.txt"
    P.append(f'<div id="alllogs" data-fn="{esc(fn)}">{esc(export_text)}</div>')

    js = (JS.replace("%%SUBJECT%%", json.dumps(EMAIL_SUBJECT))
            .replace("%%BODY%%", json.dumps(EMAIL_BODY))
            .replace("%%BODYHTML%%", json.dumps(EMAIL_BODY_HTML)))
    P.append(f"<script>{js}</script>\n</div></body></html>")
    return "".join(P)


# --------------------------------------------------------------------------- #
def pick_files():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox
    except Exception:
        return []
    r = tk.Tk(); r.withdraw()
    messagebox.showinfo(
        "Switch-Down Analyzer",
        "Upload the evidence file(s). Include ALL of:\n"
        "  execute switch-controller get-conn-status\n"
        "  execute switch-controller get-physical-conn standard\n"
        "  execute log filter reset\n"
        "  execute log filter device disk\n"
        "  execute log filter category event\n"
        "  execute log filter field subtype switch-controller\n"
        "  execute log filter view-lines 1000\n"
        "  execute log display\n\n"
        "One combined file, or several files.")
    return list(filedialog.askopenfilenames(title="Select evidence file(s)"))


def main():
    ap = argparse.ArgumentParser(description="Standalone FortiSwitch Switch-Down analyzer (uplink + email)")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--out"); ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()

    files = a.files or pick_files()
    if not files:
        print("No file provided."); return

    blob = "\n".join(read_text(Path(f)) for f in files)
    conn, counts = parse_conn_status(blob)
    central = parse_central(blob)
    uplinks_topo = parse_physical_conn(blob)

    if not conn and not central.total:
        print("Could not find get-conn-status OR central switch-controller log."); return

    names = [Path(f).name for f in files]
    report = build_report(conn, counts, central, uplinks_topo, names)
    out = Path(a.out) if a.out else Path(files[0]).with_name(
        f"switch_down_report_{datetime.now():%Y%m%d_%H%M%S}.html")
    out.write_text(report, encoding="utf-8")

    print("=" * 74); print("SWITCH-DOWN ANALYSIS")
    if conn:
        down = [s for s in conn if not s.up]
        print(f"  conn-status: {len(conn)} switches, DOWN={len(down)}"
              + (": " + ", ".join(f"{(s.name or s.serial)}[{s.serial}/{s.ip or 'no-ip'}]" for s in down) if down else ""))
    print(f"  physical-conn: {sum(len(v) for v in uplinks_topo.values())} uplink edges parsed "
          f"({len(uplinks_topo)} child switches)")
    if central.total:
        print(f"  central log: {central.total} events, NTP filtered {central.noise}  "
              f"CAPWAP-down={len(central.capwap_down)} flaps={sum(central.flap.values())} "
              f"optical={sum(central.dmi_raise.values())} ISL={len(central.isl)}")
    print("-" * 74); print(f"Report: {out}")
    if not a.no_open:
        try:
            import webbrowser; webbrowser.open(out.resolve().as_uri())
        except Exception:
            pass


if __name__ == "__main__":
    main()
