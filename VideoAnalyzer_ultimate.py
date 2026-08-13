import cv2
import csv
import html
import math
import os
import shutil
import subprocess
import wave

from array import array
from datetime import timedelta
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# ==================================================
# 必裝項目
# Purpose:
# 1. pip install opencv-python (OpenCV)
# 2. pip install pillow (Pillow)
# 3. winget install ffmpeg (FFmpeg)
# 4. pip install openai-whisper (OpenAI Whisper)
# 5. pip install torch (Torch（PyTorch）)

#完整安裝指令（一次完成）
#pip install opencv-python pillow openai-whisper torch
#winget install ffmpeg (在PowerShell 裡打上, 安裝完之後：關閉 PowerShell,重新開啟 PowerShell, 測試：ffmpeg -version 應該看到：ffmpeg version 7.x, 再測：ffprobe -version 應該看到：ffprobe version 7.x)
# ==================================================

# ==================================================
#以下跟請AI做文件:
# 我上傳的是一段與 Fortinet Support Engineer 進行故障排除錄影後產生的分析資料。
#
# 附件包括：
# 1. transcript.txt，完整語音逐字稿
# 2. transcript_segments.csv，包含逐字稿時間戳記
# 3. index.csv，包含 Keyframe 檔名及影片時間點
# 4. 所有 Contact Sheet 圖片，提供影片操作流程總覽
# 5. ai_analysis_package.md，包含預期的分析結構
#
# 請先完整分析所有附件，並依照時間順序還原 Support Engineer 的故障排除流程。
#
# 請建立一份可直接放入技術知識庫或 Confluence 的 Markdown Troubleshooting Runbook，內容必須包括：
#
# # Fortinet Troubleshooting Runbook
#
# ## 1. Purpose
# ## 2. Scope
# ## 3. Issue Summary
# ## 4. Symptoms
# ## 5. Impact Assessment
# ## 6. Environment and Affected Components
# ## 7. Investigation Timeline
# ## 8. Initial Verification
# ## 9. GUI Checks
# ## 10. CLI Commands and Outputs
# ## 11. Log Evidence
# ## 12. Troubleshooting Decision Points
# ## 13. Root Cause Analysis
# ## 14. Remediation
# ## 15. Post-Recovery Validation
# ## 16. Rollback Considerations
# ## 17. Escalation Criteria
# ## 18. Preventive Actions
# ## 19. Reusable SOP
# ## 20. Related CLI Commands
# ## 21. References and Evidence Mapping
#
# 要求：
# - 所有步驟必須按照影片時間顺序排列。
# - 將 Transcript 與 Keyframe 的時間戳記互相對應。
# - 列出影片中實際出現的 Fortinet CLI 指令。
# - 不要猜測或編造沒有出現在附件中的指令、輸出、設定、根因或修復動作。
# - 清楚區分「已確認事實」、「Support Engineer 的說明」和「尚未確認的可能原因」。
# - 對每個技術步驟說明執行目的、觀察結果及下一個決策。
# - 保留重要的錯誤訊息、Log Message、Tunnel 名稱、Interface 名稱和設定值。
# - 如果 Contact Sheet 中的 CLI、Log 或設定文字太小，請列出需要我補充的原始 keyframe 檔名。
# - 如果證據不足以確認 Root Cause，請明確標示為未確認，不要自行推論。
# - 輸出使用專業英文，格式為 Markdown。
# - 內容要適合資料中心 Network Operations、Incident Response 和後續知識轉移使用。
#
# 請先提供：
# 1. 影片內容與問題的初步判斷
# 2. 調查流程的時間線
# 3. 需要補充的原始 Keyframe 清單
#
# 然後直接產生目前證據可支持的完整 Runbook。
# ==================================================



# ==================================================
# Fortinet Support Troubleshooting Video Analyzer
# Ultimate Edition
#
# Functions:
#
# 1. Validate input video
# 2. Validate FFmpeg and FFprobe
# 3. Detect whether an audio stream exists
# 4. Extract audio to WAV
# 5. Detect whether the audio is effectively silent
# 6. Generate transcript using OpenAI Whisper
# 7. Generate TXT, SRT and transcript CSV
# 8. Extract keyframes using visual change detection
# 9. Generate Contact Sheets
# 10. Generate an HTML report
# 11. Generate an AI analysis package
# 12. Generate upload instructions
# 13. Generate processing summary
#
# ==================================================


# ==================================================
# FFmpeg Settings
# ==================================================

FFMPEG_BIN_DIR = Path(
    r"C:\Users\yi-chang.chen\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0-full_build\bin"
)

FFMPEG_EXE = FFMPEG_BIN_DIR / "ffmpeg.exe"
FFPROBE_EXE = FFMPEG_BIN_DIR / "ffprobe.exe"

# Make FFmpeg available to OpenAI Whisper.
# Whisper internally calls "ffmpeg" rather than using FFMPEG_EXE.
os.environ["PATH"] = (
    str(FFMPEG_BIN_DIR)
    + os.pathsep
    + os.environ.get("PATH", "")
)


# ==================================================
# User Settings
# ==================================================

# Change this path when analysing a different video.
video_file = Path(
    r"C:\Users\yi-chang.chen\Downloads"
    r"\video_with_sound.mp4"
)

# Change this path if a different output folder is required.
output_dir = Path(
    r"C:\Users\yi-chang.chen\Downloads"
    r"\video_with_sound"
)


# ==================================================
# Keyframe Detection Settings
#密集 CLI 操作 要擷取影片時可以用以下參數
#check_every_seconds = 0.5
#change_threshold = 2.5
#minimum_gap_seconds = 1
# ==================================================

# Check the video every three seconds.
check_every_seconds = 1

# Lower value produces more Keyframes.
# Higher value produces fewer Keyframes.
change_threshold = 4.0

# Prevent very similar screenshots being saved too close together.
minimum_gap_seconds = 2

# Comparison image width.
# This does not reduce the saved Keyframe resolution.
resize_width = 320

# Always retain the first video frame.
save_first_frame = True

# True removes the previous output folder before each run.
clean_output_folder = True


# ==================================================
# Contact Sheet Settings
# ==================================================

# The script aims to create approximately this number of sheets.
target_contact_sheet_count = 4

thumb_width = 320
thumb_height = 180

cols = 4
max_rows_per_sheet = 6

padding = 10
header_height = 50
thumbnail_label_height = 24

max_images_per_sheet = (
    cols * max_rows_per_sheet
)


# ==================================================
# Audio and Whisper Settings
# ==================================================

enable_audio_processing = True

# Available Whisper models:
#
# tiny
# base
# small
# medium
# large
#
# small is a practical balance for Fortinet recordings.
whisper_model_name = "small"

# Use "en" for English.
# Use None for automatic language detection.
whisper_language = "en"

# Audio is converted to 16 kHz mono WAV.
audio_sample_rate = 16000

# Audio with RMS lower than this is treated as silent.
silence_rms_threshold = 50


# ==================================================
# Report File Settings
# ==================================================

html_report_name = "report.html"
ai_package_name = "ai_analysis_package.md"
upload_instruction_name = "upload_instructions.txt"
summary_name = "processing_summary.txt"
error_log_name = "errors.log"


# ==================================================
# General Helper Functions
# ==================================================

def format_timestamp(seconds):
    total_seconds = max(
        0,
        int(seconds)
    )

    return str(
        timedelta(seconds=total_seconds)
    )


def format_srt_timestamp(seconds):
    total_milliseconds = max(
        0,
        int(round(seconds * 1000))
    )

    hours = (
        total_milliseconds
        // 3_600_000
    )

    remainder = (
        total_milliseconds
        % 3_600_000
    )

    minutes = (
        remainder
        // 60_000
    )

    remainder = (
        remainder
        % 60_000
    )

    whole_seconds = (
        remainder
        // 1000
    )

    milliseconds = (
        remainder
        % 1000
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{whole_seconds:02d},"
        f"{milliseconds:03d}"
    )


def write_text_file(file_path, content):
    Path(file_path).write_text(
        content,
        encoding="utf-8"
    )


def append_error(error_log_file, section, error):
    message = (
        f"\nSection: {section}\n"
        f"Error type: {type(error).__name__}\n"
        f"Error detail: {error}\n"
        + ("=" * 70)
        + "\n"
    )

    with open(
        error_log_file,
        "a",
        encoding="utf-8"
    ) as log_file:
        log_file.write(message)


def safe_folder_reset(folder_path):
    folder_path = Path(folder_path)

    if (
        clean_output_folder
        and folder_path.exists()
    ):
        shutil.rmtree(folder_path)

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )


def run_command(command_list):
    """
    Run an external process without shell=True.

    Using an argument list avoids Windows quoting problems
    when folders or filenames contain spaces.
    """

    try:
        result = subprocess.run(
            [
                str(item)
                for item in command_list
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False
        )

        return (
            result.returncode,
            result.stdout,
            result.stderr
        )

    except Exception as error:
        return (
            1,
            "",
            str(error)
        )


# ==================================================
# Input and FFmpeg Validation Functions
# ==================================================

def validate_input_files():
    errors = []

    if not video_file.is_file():
        errors.append(
            f"Video file not found:\n{video_file}"
        )

    if enable_audio_processing:

        if not FFMPEG_EXE.is_file():
            errors.append(
                f"ffmpeg.exe not found:\n{FFMPEG_EXE}"
            )

        if not FFPROBE_EXE.is_file():
            errors.append(
                f"ffprobe.exe not found:\n{FFPROBE_EXE}"
            )

    if errors:
        raise FileNotFoundError(
            "\n\n".join(errors)
        )


def test_ffmpeg():
    print("")
    print("==================================================")
    print("FFmpeg Validation")
    print("==================================================")
    print("")

    print(
        f"FFmpeg path             : "
        f"{FFMPEG_EXE}"
    )

    print(
        f"FFprobe path            : "
        f"{FFPROBE_EXE}"
    )

    print(
        f"Whisper ffmpeg path     : "
        f"{shutil.which('ffmpeg')}"
    )

    print(
        f"Whisper ffprobe path    : "
        f"{shutil.which('ffprobe')}"
    )

    print("")

    if not enable_audio_processing:
        print("Audio processing is disabled.")
        return False

    if not shutil.which("ffmpeg"):
        print(
            "FFmpeg cannot be found through "
            "the Python process PATH."
        )
        return False

    if not shutil.which("ffprobe"):
        print(
            "FFprobe cannot be found through "
            "the Python process PATH."
        )
        return False

    return_code, stdout, stderr = run_command(
        [
            FFPROBE_EXE,
            "-version"
        ]
    )

    if return_code != 0:
        print("FFprobe validation failed.")

        if stderr:
            print(stderr)

        return False

    output_lines = stdout.splitlines()

    if output_lines:
        print(output_lines[0])

    print("FFmpeg validation successful.")

    return True


# ==================================================
# Audio Functions
# ==================================================

def has_audio_stream(input_video):
    command = [
        FFPROBE_EXE,
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "csv=p=0",
        input_video
    ]

    return_code, stdout, stderr = run_command(
        command
    )

    if return_code != 0:
        print("Audio stream detection failed.")

        if stderr:
            print(stderr)

        return False

    return bool(stdout.strip())


def extract_audio(
    input_video,
    output_audio
):
    command = [
        FFMPEG_EXE,
        "-y",
        "-i",
        input_video,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        str(audio_sample_rate),
        "-ac",
        "1",
        output_audio
    ]

    return_code, stdout, stderr = run_command(
        command
    )

    if return_code != 0:
        print("Audio extraction failed.")

        if stderr:
            print(stderr)

        return False

    if not Path(output_audio).is_file():
        print(
            "FFmpeg completed, but audio.wav "
            "was not created."
        )
        return False

    return True


def calculate_wav_rms(wav_path):
    wav_path = Path(wav_path)

    if not wav_path.is_file():
        return 0.0

    total_square = 0
    total_samples = 0

    with wave.open(
        str(wav_path),
        "rb"
    ) as wav_file:

        sample_width = (
            wav_file.getsampwidth()
        )

        if sample_width != 2:
            raise ValueError(
                "Expected a 16-bit WAV file. "
                f"Sample width was {sample_width} byte(s)."
            )

        while True:
            raw_data = wav_file.readframes(
                65536
            )

            if not raw_data:
                break

            samples = array("h")
            samples.frombytes(raw_data)

            for sample in samples:
                total_square += (
                    sample * sample
                )

            total_samples += len(samples)

    if total_samples == 0:
        return 0.0

    mean_square = (
        total_square
        / total_samples
    )

    return math.sqrt(mean_square)


# ==================================================
# Image Functions
# ==================================================

def resize_for_compare(
    frame,
    width=320
):
    height = int(
        frame.shape[0]
        * width
        / frame.shape[1]
    )

    return cv2.resize(
        frame,
        (width, height),
        interpolation=cv2.INTER_AREA
    )


def frame_difference_score(
    frame_a,
    frame_b
):
    gray_a = cv2.cvtColor(
        frame_a,
        cv2.COLOR_BGR2GRAY
    )

    gray_b = cv2.cvtColor(
        frame_b,
        cv2.COLOR_BGR2GRAY
    )

    difference = cv2.absdiff(
        gray_a,
        gray_b
    )

    return float(
        difference.mean()
    )


def load_default_font(size=16):
    possible_fonts = [
        Path(
            r"C:\Windows\Fonts\arial.ttf"
        ),
        Path(
            r"C:\Windows\Fonts\segoeui.ttf"
        )
    ]

    for font_path in possible_fonts:

        if font_path.is_file():

            try:
                return ImageFont.truetype(
                    str(font_path),
                    size
                )

            except Exception:
                pass

    return ImageFont.load_default()


def create_thumbnail_with_padding(
    image_path,
    target_width,
    target_height
):
    with Image.open(
        image_path
    ) as source_image:

        image = source_image.convert(
            "RGB"
        )

        image.thumbnail(
            (
                target_width,
                target_height
            ),
            Image.Resampling.LANCZOS
        )

        canvas = Image.new(
            "RGB",
            (
                target_width,
                target_height
            ),
            color="white"
        )

        x_position = (
            target_width
            - image.width
        ) // 2

        y_position = (
            target_height
            - image.height
        ) // 2

        canvas.paste(
            image,
            (
                x_position,
                y_position
            )
        )

    return canvas


# ==================================================
# STEP 0
# Validate Input and Prepare Output Folders
# ==================================================

print("")
print("==================================================")
print("Fortinet Video Analyzer Ultimate")
print("==================================================")
print("")

validate_input_files()

ffmpeg_ready = test_ffmpeg()

if (
    enable_audio_processing
    and not ffmpeg_ready
):
    print("")
    print(
        "FFmpeg is unavailable. "
        "The script will continue as visual-only."
    )
    print("")

safe_folder_reset(
    output_dir
)

output_path = output_dir

contact_sheet_path = (
    output_path
    / "ContactSheets"
)

audio_path = (
    output_path
    / "Audio"
)

transcript_path = (
    output_path
    / "Transcript"
)

error_log_file = (
    output_path
    / error_log_name
)

contact_sheet_path.mkdir(
    parents=True,
    exist_ok=True
)

audio_path.mkdir(
    parents=True,
    exist_ok=True
)

transcript_path.mkdir(
    parents=True,
    exist_ok=True
)

write_text_file(
    error_log_file,
    "Fortinet Video Analyzer Error Log\n"
    + ("=" * 70)
    + "\n"
)


# ==================================================
# STEP 1
# Audio Detection and Whisper Transcript
# ==================================================

audio_stream_detected = False
audible_audio_detected = False
transcript_available = False

transcript_segments = []
audio_rms = 0.0

audio_file = (
    audio_path
    / "audio.wav"
)

transcript_txt_file = (
    transcript_path
    / "transcript.txt"
)

transcript_srt_file = (
    transcript_path
    / "transcript.srt"
)

transcript_csv_file = (
    transcript_path
    / "transcript_segments.csv"
)

print("")
print("==================================================")
print("STEP 1 - Audio Detection and Transcript")
print("==================================================")
print("")

if (
    enable_audio_processing
    and ffmpeg_ready
):

    audio_stream_detected = (
        has_audio_stream(
            video_file
        )
    )

    if audio_stream_detected:

        print("Audio stream detected.")
        print("Extracting audio...")

        audio_extracted = (
            extract_audio(
                video_file,
                audio_file
            )
        )

        if audio_extracted:

            print(
                f"Audio extracted          : "
                f"{audio_file}"
            )

            try:
                audio_rms = (
                    calculate_wav_rms(
                        audio_file
                    )
                )

                print(
                    f"Audio RMS                : "
                    f"{audio_rms:.2f}"
                )

                print(
                    f"Silence threshold        : "
                    f"{silence_rms_threshold}"
                )

                audible_audio_detected = (
                    audio_rms
                    >= silence_rms_threshold
                )

            except Exception as error:

                print(
                    "Audio RMS calculation failed."
                )

                print(
                    f"Error type: "
                    f"{type(error).__name__}"
                )

                print(
                    f"Error detail: "
                    f"{error}"
                )

                append_error(
                    error_log_file,
                    "Audio RMS calculation",
                    error
                )

                # If audio exists, try Whisper.
                audible_audio_detected = True

            if audible_audio_detected:

                print("Audible audio detected.")
                print(
                    "Running Whisper transcription..."
                )

                print(
                    f"Whisper ffmpeg path      : "
                    f"{shutil.which('ffmpeg')}"
                )

                print(
                    f"Whisper ffprobe path     : "
                    f"{shutil.which('ffprobe')}"
                )

                try:
                    if not shutil.which(
                        "ffmpeg"
                    ):
                        raise FileNotFoundError(
                            "Whisper cannot find "
                            "ffmpeg.exe through PATH."
                        )

                    import whisper

                    print(
                        f"Loading Whisper model    : "
                        f"{whisper_model_name}"
                    )

                    model = whisper.load_model(
                        whisper_model_name
                    )

                    whisper_options = {
                        "verbose": False,
                        "fp16": False
                    }

                    if whisper_language:

                        whisper_options[
                            "language"
                        ] = whisper_language

                    result = model.transcribe(
                        str(audio_file),
                        **whisper_options
                    )

                    transcript_text = (
                        result
                        .get(
                            "text",
                            ""
                        )
                        .strip()
                    )

                    transcript_segments = (
                        result.get(
                            "segments",
                            []
                        )
                    )

                    write_text_file(
                        transcript_txt_file,
                        transcript_text
                    )

                    with open(
                        transcript_srt_file,
                        "w",
                        encoding="utf-8"
                    ) as srt_file:

                        for (
                            segment_number,
                            segment
                        ) in enumerate(
                            transcript_segments,
                            start=1
                        ):

                            start_time = (
                                format_srt_timestamp(
                                    segment["start"]
                                )
                            )

                            end_time = (
                                format_srt_timestamp(
                                    segment["end"]
                                )
                            )

                            segment_text = (
                                segment[
                                    "text"
                                ].strip()
                            )

                            srt_file.write(
                                f"{segment_number}\n"
                            )

                            srt_file.write(
                                f"{start_time} --> "
                                f"{end_time}\n"
                            )

                            srt_file.write(
                                f"{segment_text}\n\n"
                            )

                    with open(
                        transcript_csv_file,
                        "w",
                        newline="",
                        encoding="utf-8-sig"
                    ) as csv_file:

                        transcript_fieldnames = [
                            "segment",
                            "start",
                            "end",
                            "start_timestamp",
                            "end_timestamp",
                            "text"
                        ]

                        transcript_writer = (
                            csv.DictWriter(
                                csv_file,
                                fieldnames=(
                                    transcript_fieldnames
                                )
                            )
                        )

                        transcript_writer.writeheader()

                        for (
                            segment_number,
                            segment
                        ) in enumerate(
                            transcript_segments,
                            start=1
                        ):

                            transcript_writer.writerow({
                                "segment":
                                    segment_number,

                                "start":
                                    segment["start"],

                                "end":
                                    segment["end"],

                                "start_timestamp":
                                    format_timestamp(
                                        segment["start"]
                                    ),

                                "end_timestamp":
                                    format_timestamp(
                                        segment["end"]
                                    ),

                                "text":
                                    segment[
                                        "text"
                                    ].strip()
                            })

                    transcript_available = bool(
                        transcript_text
                        or transcript_segments
                    )

                    print(
                        f"Transcript created       : "
                        f"{transcript_txt_file}"
                    )

                    print(
                        f"SRT created              : "
                        f"{transcript_srt_file}"
                    )

                    print(
                        f"Transcript CSV created   : "
                        f"{transcript_csv_file}"
                    )

                except ImportError as error:

                    print(
                        "OpenAI Whisper is not installed "
                        "in the active Python environment."
                    )

                    print(
                        "Install it using:"
                    )

                    print(
                        "python -m pip install "
                        "openai-whisper"
                    )

                    print(
                        f"Error detail: {error}"
                    )

                    append_error(
                        error_log_file,
                        "Whisper import",
                        error
                    )

                except Exception as error:

                    print(
                        "Whisper transcription failed."
                    )

                    print(
                        "Visual processing will continue."
                    )

                    print(
                        f"Error type: "
                        f"{type(error).__name__}"
                    )

                    print(
                        f"Error detail: "
                        f"{error}"
                    )

                    append_error(
                        error_log_file,
                        "Whisper transcription",
                        error
                    )

            else:

                print(
                    "The video contains an audio stream, "
                    "but the audio is effectively silent."
                )

                print(
                    "Whisper transcription was skipped."
                )

        else:

            print(
                "Audio extraction failed. "
                "Continuing as visual-only."
            )

    else:

        print("No audio stream detected.")

        print(
            "Continuing as visual-only."
        )

else:

    print(
        "Audio processing is disabled or "
        "FFmpeg is unavailable."
    )

    print(
        "Continuing as visual-only."
    )


# ==================================================
# STEP 2
# Extract Keyframes
# ==================================================

print("")
print("==================================================")
print("STEP 2 - Extract Keyframes")
print("==================================================")
print("")

video_capture = cv2.VideoCapture(
    str(video_file)
)

if not video_capture.isOpened():

    raise RuntimeError(
        f"Cannot open video file:\n"
        f"{video_file}"
    )

fps = video_capture.get(
    cv2.CAP_PROP_FPS
)

if fps <= 0:

    video_capture.release()

    raise RuntimeError(
        "Invalid FPS detected. "
        "The video may be unreadable."
    )

total_frames = int(
    video_capture.get(
        cv2.CAP_PROP_FRAME_COUNT
    )
)

duration_seconds = (
    total_frames
    / fps
)

check_interval_frames = max(
    1,
    int(
        round(
            fps
            * check_every_seconds
        )
    )
)

minimum_gap_frames = max(
    1,
    int(
        round(
            fps
            * minimum_gap_seconds
        )
    )
)

print(
    f"Video file              : "
    f"{video_file}"
)

print(
    f"Output folder           : "
    f"{output_dir}"
)

print(
    f"FPS                     : "
    f"{fps:.2f}"
)

print(
    f"Total frames            : "
    f"{total_frames}"
)

print(
    f"Duration                : "
    f"{format_timestamp(duration_seconds)}"
)

print(
    f"Check every             : "
    f"{check_every_seconds} seconds"
)

print(
    f"Change threshold        : "
    f"{change_threshold}"
)

print(
    f"Minimum screenshot gap  : "
    f"{minimum_gap_seconds} seconds"
)

print("")

previous_compare_frame = None

last_saved_frame_number = (
    -minimum_gap_frames
)

saved_count = 0
index_rows = []

frame_number = 0

while True:

    success, frame = (
        video_capture.read()
    )

    if not success:
        break

    if (
        frame_number
        % check_interval_frames
        != 0
    ):
        frame_number += 1
        continue

    timestamp_seconds = (
        frame_number
        / fps
    )

    timestamp_text = (
        format_timestamp(
            timestamp_seconds
        )
    )

    compare_frame = (
        resize_for_compare(
            frame,
            resize_width
        )
    )

    should_save = False
    reason = ""
    difference_score = None

    if previous_compare_frame is None:

        if save_first_frame:

            should_save = True
            reason = "first_frame"

    else:

        difference_score = (
            frame_difference_score(
                previous_compare_frame,
                compare_frame
            )
        )

        enough_gap = (
            frame_number
            - last_saved_frame_number
        ) >= minimum_gap_frames

        if (
            difference_score
            >= change_threshold
            and enough_gap
        ):

            should_save = True

            reason = (
                f"scene_change_score_"
                f"{difference_score:.2f}"
            )

    if should_save:

        filename = (
            f"keyframe_"
            f"{saved_count:04d}_"
            f"{int(timestamp_seconds):06d}s.png"
        )

        keyframe_file = (
            output_path
            / filename
        )

        save_success = cv2.imwrite(
            str(keyframe_file),
            frame
        )

        if not save_success:

            print(
                f"Warning: Unable to save "
                f"{keyframe_file}"
            )

        else:

            index_rows.append({
                "number":
                    saved_count + 1,

                "image":
                    filename,

                "timestamp":
                    timestamp_text,

                "timestamp_seconds":
                    round(
                        timestamp_seconds,
                        3
                    ),

                "frame_number":
                    frame_number,

                "difference_score":
                    (
                        ""
                        if difference_score is None
                        else round(
                            difference_score,
                            2
                        )
                    ),

                "reason":
                    reason
            })

            print(
                f"Saved: {filename} "
                f"at {timestamp_text} "
                f"reason={reason}"
            )

            saved_count += 1

            last_saved_frame_number = (
                frame_number
            )

    previous_compare_frame = (
        compare_frame
    )

    frame_number += 1

video_capture.release()


# ==================================================
# Write Keyframe Index CSV
# ==================================================

index_csv_file = (
    output_path
    / "index.csv"
)

with open(
    index_csv_file,
    "w",
    newline="",
    encoding="utf-8-sig"
) as csv_file:

    keyframe_fieldnames = [
        "number",
        "image",
        "timestamp",
        "timestamp_seconds",
        "frame_number",
        "difference_score",
        "reason"
    ]

    keyframe_writer = csv.DictWriter(
        csv_file,
        fieldnames=keyframe_fieldnames
    )

    keyframe_writer.writeheader()
    keyframe_writer.writerows(
        index_rows
    )

print("")

print(
    f"Total keyframes saved   : "
    f"{saved_count}"
)

print(
    f"Index file              : "
    f"{index_csv_file}"
)


# ==================================================
# STEP 3
# Build Contact Sheets
# ==================================================

print("")
print("==================================================")
print("STEP 3 - Build Contact Sheets")
print("==================================================")
print("")

keyframe_images = sorted(
    output_path.glob(
        "keyframe_*.png"
    )
)

if not keyframe_images:

    raise RuntimeError(
        "No keyframe images were found. "
        "Contact Sheets cannot be created."
    )

images_per_sheet = math.ceil(
    len(keyframe_images)
    / target_contact_sheet_count
)

images_per_sheet = min(
    images_per_sheet,
    max_images_per_sheet
)

sheet_count = math.ceil(
    len(keyframe_images)
    / images_per_sheet
)

print(
    f"Images found            : "
    f"{len(keyframe_images)}"
)

print(
    f"Target sheet count      : "
    f"{target_contact_sheet_count}"
)

print(
    f"Actual sheet count      : "
    f"{sheet_count}"
)

print(
    f"Images per sheet        : "
    f"{images_per_sheet}"
)

print("")

title_font = (
    load_default_font(18)
)

label_font = (
    load_default_font(13)
)

contact_sheet_files = []

for sheet_number in range(
    sheet_count
):

    print(
        f"Creating sheet "
        f"{sheet_number + 1}/"
        f"{sheet_count}"
    )

    start_index = (
        sheet_number
        * images_per_sheet
    )

    end_index = (
        start_index
        + images_per_sheet
    )

    batch = keyframe_images[
        start_index:end_index
    ]

    actual_rows = math.ceil(
        len(batch)
        / cols
    )

    sheet_width = (
        cols
        * thumb_width
        + (cols + 1)
        * padding
    )

    sheet_height = (
        header_height
        + actual_rows
        * thumb_height
        + (actual_rows + 1)
        * padding
    )

    contact_sheet = Image.new(
        "RGB",
        (
            sheet_width,
            sheet_height
        ),
        color="white"
    )

    draw = ImageDraw.Draw(
        contact_sheet
    )

    sheet_title = (
        "Fortinet Video Keyframes | "
        f"Sheet {sheet_number + 1}/"
        f"{sheet_count} | "
        f"Images {start_index + 1}-"
        f"{start_index + len(batch)}"
    )

    draw.text(
        (
            padding,
            15
        ),
        sheet_title,
        fill="black",
        font=title_font
    )

    for (
        local_index,
        image_file
    ) in enumerate(batch):

        global_index = (
            start_index
            + local_index
        )

        image_number = (
            global_index
            + 1
        )

        try:

            thumbnail = (
                create_thumbnail_with_padding(
                    image_file,
                    thumb_width,
                    thumb_height
                )
            )

            row_number = (
                local_index
                // cols
            )

            column_number = (
                local_index
                % cols
            )

            x_position = (
                padding
                + column_number
                * (
                    thumb_width
                    + padding
                )
            )

            y_position = (
                header_height
                + padding
                + row_number
                * (
                    thumb_height
                    + padding
                )
            )

            contact_sheet.paste(
                thumbnail,
                (
                    x_position,
                    y_position
                )
            )

            if global_index < len(
                index_rows
            ):

                timestamp = (
                    index_rows[
                        global_index
                    ]["timestamp"]
                )

            else:

                timestamp = "unknown"

            label = (
                f"{image_number}. "
                f"{image_file.name} | "
                f"{timestamp}"
            )

            draw.rectangle(
                [
                    x_position,
                    y_position,
                    x_position
                    + thumb_width,
                    y_position
                    + thumbnail_label_height
                ],
                fill="white"
            )

            draw.text(
                (
                    x_position + 5,
                    y_position + 4
                ),
                label,
                fill="red",
                font=label_font
            )

        except Exception as error:

            print(
                f"Error processing image: "
                f"{image_file}"
            )

            print(
                f"Error detail: {error}"
            )

            append_error(
                error_log_file,
                (
                    "Contact Sheet image "
                    f"{image_file}"
                ),
                error
            )

    contact_sheet_file = (
        contact_sheet_path
        / (
            f"Sheet_"
            f"{sheet_number + 1:02d}.png"
        )
    )

    contact_sheet.save(
        contact_sheet_file,
        format="PNG"
    )

    contact_sheet_files.append(
        contact_sheet_file
    )

    print(
        f"Created: "
        f"{contact_sheet_file}"
    )

print("")

print(
    "Contact Sheet generation completed."
)

print(
    f"Contact Sheets folder   : "
    f"{contact_sheet_path}"
)


# ==================================================
# STEP 4
# Generate HTML Report
# ==================================================

print("")
print("==================================================")
print("STEP 4 - Generate HTML Report")
print("==================================================")
print("")

html_file = (
    output_path
    / html_report_name
)


def html_escape(value):
    return html.escape(
        str(value),
        quote=True
    )


html_parts = [
    "<!DOCTYPE html>",
    "<html lang='en'>",
    "<head>",
    "<meta charset='utf-8'>",
    (
        "<meta name='viewport' "
        "content='width=device-width, initial-scale=1'>"
    ),
    "<title>Fortinet Video Analyzer Report</title>",
    """
<style>
body {
    font-family: Arial, sans-serif;
    margin: 24px;
    background: #f5f5f5;
    color: #222;
}

h1 {
    color: #1f4e3d;
}

h2 {
    color: #333;
    border-bottom: 1px solid #ccc;
    padding-bottom: 6px;
}

.summary {
    background: white;
    border: 1px solid #ddd;
    padding: 16px;
    margin-bottom: 20px;
}

.grid {
    display: grid;
    grid-template-columns:
        repeat(auto-fill, minmax(380px, 1fr));
    gap: 16px;
}

.card {
    background: white;
    border: 1px solid #ddd;
    padding: 10px;
}

.card img {
    display: block;
    width: 100%;
    height: auto;
    border: 1px solid #ccc;
}

.meta {
    font-size: 13px;
    margin-top: 8px;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

.badge {
    display: inline-block;
    background: #e8f3ee;
    color: #1f4e3d;
    padding: 2px 6px;
    border-radius: 4px;
    margin-right: 4px;
}

code {
    background: #eee;
    padding: 2px 4px;
}

pre {
    white-space: pre-wrap;
    background: #222;
    color: #eee;
    padding: 12px;
    overflow-x: auto;
}

a {
    color: #175cd3;
    text-decoration: none;
}
</style>
""",
    "</head>",
    "<body>",
    "<h1>Fortinet Video Analyzer Report</h1>",
    "<div class='summary'>",
    "<h2>Summary</h2>",
    (
        "<p><strong>Video file:</strong> "
        + html_escape(video_file)
        + "</p>"
    ),
    (
        "<p><strong>Output folder:</strong> "
        + html_escape(output_dir)
        + "</p>"
    ),
    (
        "<p><strong>Duration:</strong> "
        + html_escape(
            format_timestamp(
                duration_seconds
            )
        )
        + "</p>"
    ),
    (
        "<p><strong>FPS:</strong> "
        + html_escape(
            f"{fps:.2f}"
        )
        + "</p>"
    ),
    (
        "<p><strong>Total frames:</strong> "
        + html_escape(
            total_frames
        )
        + "</p>"
    ),
    (
        "<p><strong>Total keyframes:</strong> "
        + html_escape(
            saved_count
        )
        + "</p>"
    ),
    (
        "<p><strong>Audio stream detected:</strong> "
        + html_escape(
            audio_stream_detected
        )
        + "</p>"
    ),
    (
        "<p><strong>Audible audio detected:</strong> "
        + html_escape(
            audible_audio_detected
        )
        + "</p>"
    ),
    (
        "<p><strong>Audio RMS:</strong> "
        + html_escape(
            f"{audio_rms:.2f}"
        )
        + "</p>"
    ),
    (
        "<p><strong>Transcript available:</strong> "
        + html_escape(
            transcript_available
        )
        + "</p>"
    ),
    (
        "<p><strong>Change threshold:</strong> "
        + html_escape(
            change_threshold
        )
        + "</p>"
    ),
    (
        "<p><strong>Check every:</strong> "
        + html_escape(
            check_every_seconds
        )
        + " seconds</p>"
    ),
    (
        "<p><strong>Minimum screenshot gap:</strong> "
        + html_escape(
            minimum_gap_seconds
        )
        + " seconds</p>"
    ),
    "</div>"
]


# ==================================================
# HTML Transcript Preview
# ==================================================

if (
    transcript_available
    and transcript_txt_file.is_file()
):

    transcript_preview = (
        transcript_txt_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    )

    html_parts.extend([
        "<h2>Transcript Preview</h2>",
        "<pre>",
        html.escape(
            transcript_preview[:5000]
        ),
        "</pre>"
    ])


# ==================================================
# HTML Contact Sheets
# ==================================================

html_parts.extend([
    "<h2>Contact Sheets</h2>",
    "<div class='grid'>"
])

for contact_sheet_file in contact_sheet_files:

    relative_path = (
        contact_sheet_file
        .relative_to(output_path)
        .as_posix()
    )

    safe_path = html_escape(relative_path)
    safe_name = html_escape(contact_sheet_file.name)

    contact_sheet_card = (
        "<div class='card'>"
        f"{safe_path}"
        f"{safe_path}"
        "</a>"
        "<div class='meta'>"
        f"<strong>{safe_name}</strong>"
        "</div>"
        "</div>"
    )

    html_parts.append(contact_sheet_card)

html_parts.extend([
    "</div>",
    "<h2>Keyframes</h2>",
    "<div class='grid'>"
])


# ==================================================
# HTML Keyframes
# ==================================================

for keyframe_row in index_rows:

    image_name = keyframe_row["image"]

    safe_image_path = html_escape(image_name)
    safe_image_name = html_escape(image_name)

    safe_timestamp = html_escape(
        keyframe_row["timestamp"]
    )

    safe_reason = html_escape(
        keyframe_row["reason"]
    )

    safe_score = html_escape(
        keyframe_row.get(
            "difference_score",
            ""
        )
    )

    safe_seconds = html_escape(
        keyframe_row["timestamp_seconds"]
    )

    safe_frame_number = html_escape(
        keyframe_row["frame_number"]
    )

    safe_number = html_escape(
        keyframe_row["number"]
    )

    keyframe_card = (
        "<div class='card'>"
        f"{safe_image_path}"
        f"{safe_image_path}"
        "</a>"
        "<div class='meta'>"
        f"<span class='badge'>#{safe_number}</span>"
        f"<strong>{safe_image_name}</strong><br>"
        f"Timestamp: <code>{safe_timestamp}</code><br>"
        f"Seconds: <code>{safe_seconds}</code><br>"
        f"Frame: <code>{safe_frame_number}</code><br>"
        f"Difference score: <code>{safe_score}</code><br>"
        f"Reason: <code>{safe_reason}</code>"
        "</div>"
        "</div>"
    )

    html_parts.append(keyframe_card)

html_parts.extend([
    "</div>",
    "</body>",
    "</html>"
])

write_text_file(
    html_file,
    "\n".join(html_parts)
)

print(
    f"HTML report created     : "
    f"{html_file}"
)


# ==================================================
# STEP 5
# Generate AI Analysis Package
# ==================================================

print("")
print("==================================================")
print("STEP 5 - Generate AI Analysis Package")
print("==================================================")
print("")

ai_package_file = (
    output_path
    / ai_package_name
)

upload_instruction_file = (
    output_path
    / upload_instruction_name
)

package_lines = [
    "# Fortinet Support Troubleshooting Video Analysis Package",
    "",
    "## Purpose",
    "",
    (
        "This package converts a Fortinet Support "
        "troubleshooting recording into visual and "
        "transcript evidence for creating a structured "
        "troubleshooting runbook."
    ),
    "",
    "## Video Metadata",
    "",
    f"- Video file: `{video_file}`",
    f"- Duration: `{format_timestamp(duration_seconds)}`",
    f"- FPS: `{fps:.2f}`",
    f"- Total frames: `{total_frames}`",
    f"- Total keyframes: `{saved_count}`",
    f"- Contact Sheets: `{len(contact_sheet_files)}`",
    f"- Audio stream detected: `{audio_stream_detected}`",
    f"- Audible audio detected: `{audible_audio_detected}`",
    f"- Audio RMS: `{audio_rms:.2f}`",
    f"- Transcript available: `{transcript_available}`",
    "",
    "## Generated Files",
    "",
    (
        "- `index.csv`: Keyframe index with timestamps, "
        "difference scores and extraction reasons"
    ),
    (
        "- `report.html`: Local visual report with "
        "clickable Contact Sheets and Keyframes"
    ),
    (
        "- `ContactSheets/Sheet_*.png`: "
        "Visual overview of the recording"
    ),
    (
        "- `keyframe_*.png`: "
        "Original full-resolution screenshots"
    ),
    (
        "- `ai_analysis_package.md`: "
        "Instructions for generating the Runbook"
    ),
    (
        "- `upload_instructions.txt`: "
        "Recommended upload procedure"
    ),
    (
        "- `processing_summary.txt`: "
        "Processing results"
    ),
    (
        "- `errors.log`: "
        "Processing errors and diagnostic information"
    )
]

if audio_file.is_file():

    package_lines.append(
        "- `Audio/audio.wav`: "
        "Extracted mono 16 kHz WAV audio"
    )

if transcript_available:

    package_lines.extend([
        "",
        "## Transcript Files",
        "",
        (
            "- `Transcript/transcript.txt`: "
            "Full transcript for AI analysis"
        ),
        (
            "- `Transcript/transcript.srt`: "
            "Timestamped subtitle file"
        ),
        (
            "- `Transcript/transcript_segments.csv`: "
            "Timestamped transcript segments"
        )
    ])

package_lines.extend([
    "",
    "## Recommended Upload Set",
    ""
])

if transcript_available:

    package_lines.extend([
        "For a recording with audible audio, upload:",
        "",
        "1. `Transcript/transcript.txt`",
        "2. Every PNG file under `ContactSheets`",
        "3. `ai_analysis_package.md`",
        (
            "4. `index.csv` when precise timestamp "
            "mapping is required"
        ),
        "",
        (
            "If CLI, logs or GUI text is too small in a "
            "Contact Sheet, upload the requested original "
            "`keyframe_*.png` files."
        )
    ])

else:

    package_lines.extend([
        "For a silent or visual-only recording, upload:",
        "",
        "1. Every PNG file under `ContactSheets`",
        "2. `ai_analysis_package.md`",
        (
            "3. `index.csv` when precise timestamp "
            "mapping is required"
        ),
        "",
        (
            "If CLI, logs or GUI text is too small in a "
            "Contact Sheet, upload the requested original "
            "`keyframe_*.png` files."
        )
    ])

package_lines.extend([
    "",
    "## Prompt To Use With Copilot",
    "",
    "```text",
    (
        "Please analyse this Fortinet Support "
        "troubleshooting recording package."
    ),
    "",
    (
        "Create a complete Troubleshooting Runbook "
        "in Markdown."
    ),
    "",
    "Include:",
    "1. Issue summary",
    "2. Scope and affected environment",
    "3. Observed symptoms",
    "4. Impact assessment",
    "5. Investigation timeline",
    "6. Fortinet GUI pages reviewed",
    "7. CLI commands used",
    "8. Relevant CLI output",
    "9. Key log messages",
    "10. Evidence collected",
    "11. Troubleshooting decision points",
    "12. Root cause analysis",
    "13. Remediation steps",
    "14. Post-recovery validation",
    "15. Escalation criteria",
    "16. Preventive actions",
    "17. Reusable SOP",
    "",
    (
        "Clearly distinguish confirmed evidence, "
        "support engineer statements and assumptions."
    ),
    "",
    (
        "Do not invent commands, results, root causes "
        "or recovery actions that are not present in "
        "the supplied evidence."
    ),
    "",
    (
        "Keep the output operationally practical for "
        "a data centre network engineering team."
    ),
    "```",
    "",
    "## Required Runbook Structure",
    "",
    "```markdown",
    "# Fortinet Troubleshooting Runbook",
    "",
    "## 1. Purpose",
    "## 2. Scope",
    "## 3. Issue Summary",
    "## 4. Symptoms",
    "## 5. Impact Assessment",
    "## 6. Investigation Timeline",
    "## 7. GUI Checks",
    "## 8. CLI Checks",
    "## 9. Log Evidence",
    "## 10. Evidence and Decision Points",
    "## 11. Root Cause Analysis",
    "## 12. Remediation",
    "## 13. Post-Recovery Validation",
    "## 14. Rollback Considerations",
    "## 15. Escalation Criteria",
    "## 16. Preventive Actions",
    "## 17. Related CLI Commands",
    "## 18. References",
    "```"
])

write_text_file(
    ai_package_file,
    "\n".join(package_lines)
)


# ==================================================
# STEP 5A
# Generate Upload Instructions
# ==================================================

upload_instruction_lines = [
    "Fortinet Video Analyzer Upload Instructions",
    "",
    "VIDEO WITH AUDIO",
    "",
    "Upload these files first:",
    "",
    "1. Transcript/transcript.txt",
    "2. Every ContactSheets/Sheet_*.png file",
    "3. ai_analysis_package.md",
    "",
    "Upload if requested:",
    "",
    "4. index.csv",
    "5. Specific original keyframe_*.png files",
    "",
    "VIDEO WITHOUT AUDIBLE AUDIO",
    "",
    "Upload these files first:",
    "",
    "1. Every ContactSheets/Sheet_*.png file",
    "2. ai_analysis_package.md",
    "",
    "Upload if requested:",
    "",
    "3. index.csv",
    "4. Specific original keyframe_*.png files",
    "",
    "LOCAL REVIEW FILES",
    "",
    (
        "- report.html provides a clickable local "
        "report of Contact Sheets and Keyframes."
    ),
    (
        "- Transcript/transcript.srt provides "
        "timestamped subtitles."
    ),
    (
        "- Transcript/transcript_segments.csv provides "
        "timestamped transcript rows."
    ),
    (
        "- Audio/audio.wav normally does not need "
        "to be uploaded."
    ),
    (
        "- errors.log contains diagnostic information "
        "if any processing step fails."
    )
]

write_text_file(
    upload_instruction_file,
    "\n".join(upload_instruction_lines)
)

print(
    f"AI package created      : "
    f"{ai_package_file}"
)

print(
    f"Upload guide created    : "
    f"{upload_instruction_file}"
)


# ==================================================
# STEP 6
# Generate Processing Summary
# ==================================================

print("")
print("==================================================")
print("STEP 6 - Generate Processing Summary")
print("==================================================")
print("")

summary_file = (
    output_path
    / summary_name
)

summary_lines = [
    "Fortinet Video Analyzer Processing Summary",
    "",
    f"Video file: {video_file}",
    f"Output folder: {output_dir}",
    f"Duration: {format_timestamp(duration_seconds)}",
    f"FPS: {fps:.2f}",
    f"Total video frames: {total_frames}",
    f"Keyframes created: {saved_count}",
    f"Contact Sheets created: {len(contact_sheet_files)}",
    f"Audio stream detected: {audio_stream_detected}",
    f"Audible audio detected: {audible_audio_detected}",
    f"Audio RMS: {audio_rms:.2f}",
    f"Transcript created: {transcript_available}",
    f"Whisper model: {whisper_model_name}",
    f"Whisper language: {whisper_language}",
    f"Whisper ffmpeg path: {shutil.which('ffmpeg')}",
    f"Whisper ffprobe path: {shutil.which('ffprobe')}",
    "",
    "Generated files:",
    "",
    f"Keyframe index: {index_csv_file}",
    f"HTML report: {html_file}",
    f"AI analysis package: {ai_package_file}",
    f"Upload instructions: {upload_instruction_file}",
    f"Error log: {error_log_file}"
]

if audio_file.is_file():

    summary_lines.append(
        f"Extracted audio: {audio_file}"
    )

if transcript_available:

    summary_lines.extend([
        f"Transcript: {transcript_txt_file}",
        f"SRT subtitles: {transcript_srt_file}",
        f"Transcript CSV: {transcript_csv_file}"
    ])

write_text_file(
    summary_file,
    "\n".join(summary_lines)
)

print(
    f"Summary created         : "
    f"{summary_file}"
)


# ==================================================
# Completed
# ==================================================

print("")
print("==================================================")
print("Completed")
print("==================================================")
print("")

print(
    f"Keyframes folder        : "
    f"{output_path}"
)

print(
    f"Contact Sheets folder   : "
    f"{contact_sheet_path}"
)

print(
    f"Contact Sheets created  : "
    f"{len(contact_sheet_files)}"
)

print(
    f"CSV index               : "
    f"{index_csv_file}"
)

print(
    f"HTML report             : "
    f"{html_file}"
)

print(
    f"AI package              : "
    f"{ai_package_file}"
)

print(
    f"Upload instructions     : "
    f"{upload_instruction_file}"
)

print(
    f"Processing summary      : "
    f"{summary_file}"
)

print(
    f"Error log               : "
    f"{error_log_file}"
)

if audio_file.is_file():

    print(
        f"Audio file              : "
        f"{audio_file}"
    )

else:

    print(
        "Audio file              : "
        "Not created"
    )

if transcript_available:

    print(
        f"Transcript              : "
        f"{transcript_txt_file}"
    )

    print(
        f"SRT subtitle            : "
        f"{transcript_srt_file}"
    )

    print(
        f"Transcript CSV          : "
        f"{transcript_csv_file}"
    )

else:

    print(
        "Transcript              : "
        "Not available"
    )

print("")
print("Recommended upload:")

if transcript_available:

    print(
        "1. Transcript/transcript.txt"
    )

    print(
        "2. Every PNG file inside ContactSheets"
    )

    print(
        "3. ai_analysis_package.md"
    )

else:

    print(
        "1. Every PNG file inside ContactSheets"
    )

    print(
        "2. ai_analysis_package.md"
    )

print(
    "4. Requested full-resolution "
    "Keyframes, if required"
)