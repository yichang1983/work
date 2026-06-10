import re

# 請在此處貼上您完整的 diagnose user device list 輸出
raw_data = r"""
  vd root/0  e0:dc:a0:eb:ce:5a  gen 766  req OHUSA/3e
    created 88407659s  gen 765  seen 22s  ENG_LAND  gen 329
    ip 10.210.144.62  src arp
  vd root/0  e0:dc:a0:eb:ce:5b  gen 1655203  req OHUSA/3e
    created 88407520s  gen 1528  seen 22s  ENG_LAND  gen 196077
  vd root/0  e0:dc:a0:eb:cf:46  gen 1150436  req OHUSA/3e
    created 88407689s  gen 10  seen 15s  ENG_LAND  gen 184712
    ip 10.210.144.71  src arp
  vd root/0  e0:dc:a0:eb:cf:47  gen 1655189  req OHUSA/3e
    created 88407522s  gen 1363  seen 19s  ENG_LAND  gen 196066
  vd root/0  e0:dc:a0:eb:cf:6a  gen 1150437  req OHUSA/3e
    created 88407666s  gen 558  seen 19s  ENG_LAND  gen 184713
    ip 10.210.144.72  src arp
  vd root/0  e0:dc:a0:eb:cf:6b  gen 1655190  req OHUSA/3e
    created 88407522s  gen 1364  seen 19s  ENG_LAND  gen 196067
  vd root/0  e0:dc:a0:eb:cd:b4  gen 1150441  req OHUSA/3e
    created 88407671s  gen 36  seen 2s  ENG_LAND  gen 184715
    ip 10.210.144.70  src arp
  vd root/0  e0:dc:a0:eb:cd:b5  gen 1655187  req OHUSA/3e
    created 88407522s  gen 1360  seen 19s  ENG_LAND  gen 196064
  vd root/0  e0:dc:a0:eb:cf:78  gen 978  req OHUSA/3e
    created 88407679s  gen 22  seen 11s  ENG_LAND  gen 22
    ip 10.210.144.67  src arp
  vd root/0  e0:dc:a0:eb:cf:79  gen 1655202  req OHUSA/3e
    created 88407520s  gen 1527  seen 22s  ENG_LAND  gen 196076
  vd root/0  e0:dc:a0:eb:d4:2c  gen 1655201  req OHUSA/3e
    created 88407681s  gen 19  seen 0s  ENG_LAND  gen 196075
    ip 10.210.144.68  src arp
  vd root/0  e0:dc:a0:eb:d4:2d  gen 1655204  req OHUSA/3e
    created 88407520s  gen 1529  seen 22s  ENG_LAND  gen 196078
  vd root/0  e0:dc:a0:eb:d3:c8  gen 104  req OHUSA/3e
    created 88407678s  gen 23  seen 17s  ENG_LAND  gen 23
    ip 10.210.144.57  src arp
  vd root/0  e0:dc:a0:eb:d3:c9  gen 1655205  req OHUSA/3e
    created 88407520s  gen 1530  seen 22s  ENG_LAND  gen 196079
  vd root/0  00:50:56:5c:1e:d1  gen 11277219  req OHUSA/3e
    created 83886200s  gen 44624  seen 21s  ESXMGMT  gen 358286
  vd root/0  e0:23:ff:d4:e5:19  gen 1041  req 0
    created 88407604s  gen 1041  seen 22s  fortilink  gen 432
  vd root/0  00:50:56:58:b2:7c  gen 12429606  req OHUSA/3e
    created 83886320s  gen 44621  seen 21s  ESXMGMT  gen 391415
  vd root/0  e0:23:ff:d4:ea:03  gen 1060  req 0
    created 88407604s  gen 1058  seen 22s  fortilink  gen 447
  vd root/0  e0:23:ff:d4:e4:cf  gen 3552  req 0
    created 88407604s  gen 1043  seen 22s  fortilink  gen 1645
  vd root/0  00:50:56:5b:54:58  gen 11280586  req OHUSA/3e
    created 83886321s  gen 44612  seen 22s  ESXMGMT  gen 358453
  vd root/0  00:50:56:5c:31:c0  gen 11281513  req OHUSA/3e
    created 83886320s  gen 44622  seen 21s  ESXMGMT  gen 358496
  vd root/0  e0:23:ff:d4:ea:4d  gen 1051  req 0
    created 88407604s  gen 1050  seen 22s  fortilink  gen 440
  vd root/0  58:38:79:9e:93:29  gen 15424693  req OUA/34
    created 67152236s  gen 204781  seen 22s  CORP_PRINTERS  gen 448824
    ip 10.210.72.44  src arp
    hardware vendor 'Ricoh'  src dhcp  id 329  weight 128
    type 'Printer'  src dhcp  id 329  weight 128
    os 'Android'  src tcp  id 1652  weight 128
    host 'RNP5838799E9329'  src dhcp
  vd root/0  00:50:56:5c:44:ba  gen 12429924  req HU/18
    created 70868224s  gen 161276  seen 22s  default  gen 391425
  vd root/0  00:50:56:5d:28:64  gen 12430620  req OHUSA/3e
    created 83886320s  gen 44619  seen 22s  ESXMGMT  gen 391450
  vd root/0  00:50:56:5e:19:5e  gen 12430627  req OHUSA/3e
    created 83886321s  gen 44613  seen 22s  ESXMGMT  gen 391457
  vd root/0  00:50:56:5b:88:e9  gen 12429604  req OHUSA/3e
    created 83886321s  gen 44607  seen 22s  ESXMGMT  gen 391413
  vd root/0  00:50:56:5a:ba:04  gen 12429600  req HU/18
    created 70773348s  gen 162468  seen 22s  default  gen 391409
  vd root/0  fe:4e:33:9f:21:d5  gen 15466488  req OUA/34
    created 19350013s  gen 7921552  seen 1s  Guest  gen 449610
    ip 172.176.0.45  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '15'  src dhcp  id 6732  weight 230
    host 'S25-Ultra-korisnika-Antun'  src dhcp
  vd root/0  00:50:56:59:e3:c3  gen 12430622  req HU/18
    created 59202849s  gen 298501  seen 22s  default  gen 391452
  vd root/0  00:50:56:5c:83:71  gen 12430694  req HU/18
    created 70768424s  gen 162571  seen 22s  default  gen 391458
  vd root/0  00:50:56:5e:54:82  gen 12429999  req OHUSA/3e
    created 83886321s  gen 44610  seen 22s  ESXMGMT  gen 391428
  vd root/0  ee:a9:2a:c8:fb:29  gen 15042103  req OUA/34
    created 15840298s  gen 9150272  seen 766670s  Guest  gen 441701
    ip 172.176.0.8  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:60:33:83  gen 15463212  req OHUSA/3e
    created 88407657s  gen 826  seen 22s  CORP_SERVERS  gen 358490
    ip 10.210.0.35  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  cc:3f:1d:02:bc:a5  gen 1643195  req OHUSA/3e
    created 88407524s  gen 1343  seen 20s  ENG_LANB  gen 195630
    ip 10.210.136.86  src arp
  vd root/0  00:1f:d1:34:0f:b1  gen 13357380  req OHUSA/3e
    created 8987493s  gen 11520296  seen 0s  SECURITY_ExtDev  gen 412266
    ip 10.210.48.182  src arp
  vd root/0  00:50:56:5e:8d:0c  gen 12430000  req OHUSA/3e
    created 83886140s  gen 44627  seen 22s  ESXMGMT  gen 391429
  vd root/0  00:1f:d1:34:19:c0  gen 12359668  req OHUSA/3e
    created 10628756s  gen 11008782  seen 0s  SECURITY_ExtDev  gen 389483
    ip 10.210.48.178  src mac
  vd root/0  10:df:fc:10:f1:00  gen 13128488  req OHUSA/3e
    created 88407524s  gen 1273  seen 20s  ENG_LAND  gen 196119
    ip 10.210.144.125  src arp
  vd root/0  10:df:fc:10:f1:03  gen 13494760  req OHUSA/3e
    created 88407524s  gen 1341  seen 20s  ENG_LANC  gen 313412
    ip 10.210.140.185  src arp
  vd root/0  10:df:fc:10:f1:04  gen 13494745  req OHUSA/3e
    created 88407520s  gen 1479  seen 22s  ENG_LAND  gen 215141
    ip 10.210.144.122  src arp
  vd root/0  10:df:fc:10:f1:05  gen 13494736  req OHUSA/3e
    created 88407524s  gen 1276  seen 20s  ENG_LAND  gen 196124
    ip 10.210.144.124  src arp
  vd root/0  10:df:fc:10:f1:08  gen 13494743  req OHUSA/3e
    created 88407524s  gen 1257  seen 20s  ENG_LAND  gen 214630
    ip 10.210.144.178  src arp
  vd root/0  10:df:fc:10:f1:0a  gen 13494759  req OHUSA/3e
    created 88407524s  gen 1346  seen 20s  ENG_LAND  gen 313613
    ip 10.210.144.152  src arp
  vd root/0  10:df:fc:10:f1:0c  gen 13494756  req OHUSA/3e
    created 88407523s  gen 1354  seen 20s  ENG_LANC  gen 215522
    ip 10.210.140.155  src arp
  vd root/0  10:df:fc:10:f1:14  gen 13494754  req OHUSA/3e
    created 88407524s  gen 1348  seen 20s  ENG_LAND  gen 313614
    ip 10.210.144.151  src arp
  vd root/0  10:df:fc:10:f1:1e  gen 13494766  req OHUSA/3e
    created 88407524s  gen 1339  seen 20s  ENG_LANC  gen 313411
    ip 10.210.140.184  src arp
  vd root/0  10:df:fc:10:f1:41  gen 13127916  req OHUSA/3e
    created 88407520s  gen 1474  seen 22s  ENG_LANC  gen 215510
    ip 10.210.140.152  src arp
  vd root/0  10:df:fc:10:f1:4f  gen 13494752  req OHUSA/3e
    created 88407503s  gen 1597  seen 20s  ENG_LANC  gen 313410
    ip 10.210.140.182  src arp
  vd root/0  e4:30:22:3a:87:ea  gen 493  req OHUSA/3e
    created 88407667s  gen 459  seen 3s  SECURITY_ExtDev  gen 218
    ip 10.210.48.154  src mac
  vd root/0  10:df:fc:10:f2:65  gen 13494737  req OHUSA/3e
    created 88407522s  gen 1429  seen 19s  ENG_LAND  gen 313616
    ip 10.210.144.155  src arp
  vd root/0  10:df:fc:10:f0:b5  gen 13494768  req OHUSA/3e
    created 88407524s  gen 1280  seen 20s  ENG_LAND  gen 214625
    ip 10.210.144.181  src arp
  vd root/0  10:df:fc:10:f0:e2  gen 13494765  req OHUSA/3e
    created 88407520s  gen 1477  seen 22s  ENG_LAND  gen 215140
    ip 10.210.144.121  src arp
  vd root/0  10:df:fc:10:f0:e3  gen 13127918  req OHUSA/3e
    created 88407520s  gen 1473  seen 22s  ENG_LANC  gen 215512
    ip 10.210.140.151  src arp
  vd root/0  10:df:fc:10:f0:e4  gen 13494769  req OHUSA/3e
    created 88407503s  gen 1595  seen 20s  ENG_LANC  gen 313409
    ip 10.210.140.181  src arp
  vd root/0  10:df:fc:10:f0:e9  gen 13127911  req OHUSA/3e
    created 88407524s  gen 1293  seen 20s  ENG_LANC  gen 214965
    ip 10.210.140.122  src arp
  vd root/0  e4:a7:a0:93:db:1d  gen 15436897  req OUA/34
    created 31166766s  gen 4525068  seen 40835s  Guest  gen 449066
    ip 172.176.0.19  src arp
    type 'Computer'  src http  id 1403  weight 100
    os 'Android'  src http  id 1074  weight 130
    host 'antumnos'  src dhcp
  vd root/0  10:df:fc:10:f0:f3  gen 13494748  req OHUSA/3e
    created 88407524s  gen 1289  seen 20s  ENG_LANC  gen 214961
    ip 10.210.140.125  src arp
  vd root/0  10:df:fc:10:f0:f6  gen 13494761  req OHUSA/3e
    created 88407523s  gen 1351  seen 20s  ENG_LANC  gen 215521
    ip 10.210.140.154  src arp
  vd root/0  10:df:fc:10:f2:fc  gen 13494747  req OHUSA/3e
    created 88407522s  gen 1427  seen 19s  ENG_LAND  gen 313615
    ip 10.210.144.154  src arp
  vd root/0  00:1f:d1:35:0d:ca  gen 12359741  req OHUSA/3e
    created 10622692s  gen 11012187  seen 0s  SECURITY_ExtDev  gen 389484
    ip 10.210.48.177  src mac
  vd root/0  44:a3:bb:5a:3a:b1  gen 15090380  req OUA/34
    created 702144s  gen 15090346  seen 701386s  CORP WIRELESS  gen 442557
    ip 10.210.68.74  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'VDC-83LPW64'  src dhcp
  vd root/0  10:df:fc:10:fe:22  gen 13494750  req OHUSA/3e
    created 88407524s  gen 1286  seen 20s  ENG_LANC  gen 214960
    ip 10.210.140.124  src arp
  vd root/0  10:df:fc:10:fd:f8  gen 13128485  req OHUSA/3e
    created 88407522s  gen 1372  seen 18s  ENG_LAND  gen 215134
    ip 10.210.144.118  src arp
  vd root/0  10:df:fc:10:fd:f9  gen 13883641  req OHUSA/3e
    created 88407522s  gen 1366  seen 19s  ENG_LANC  gen 214818
    ip 10.210.140.118  src arp
  vd root/0  10:df:fc:10:fd:fe  gen 13350472  req OHUSA/3e
    created 88407522s  gen 1370  seen 18s  ENG_LAND  gen 215132
    ip 10.210.144.119  src arp
  vd root/0  44:a3:bb:5b:33:8a  gen 15426606  req OHUSA/3e
    created 82100s  gen 15426606  seen 81628s  CORP WIRELESS  gen 448861
  vd root/0  00:50:56:5f:a0:ab  gen 11279836  req HU/18
    created 70859997s  gen 161418  seen 22s  default  gen 358405
  vd root/0  44:a3:bb:5a:60:95  gen 15364624  req OA/24
    created 38189261s  gen 3290874  seen 160831s  CORP WIRELESS  gen 447663
    ip 10.210.68.81  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-I6I6N5S'  src dhcp
    user 'Sotirios.Drimis'  src kerberos
  vd root/0  4a:01:17:f1:35:36  gen 14181569  req OUA/34
    created 2260668s  gen 14181564  seen 2260304s  CORP WIRELESS  gen 427047
    ip 10.210.68.34  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  e4:30:22:39:e2:08  gen 238710  req OHUSA/3e
    created 88407667s  gen 500  seen 5s  SECURITY_ExtDev  gen 119966
    ip 10.210.48.136  src mac
  vd root/0  00:50:56:5e:d0:97  gen 11277391  req OHUSA/3e
    created 83886320s  gen 44618  seen 22s  ESXMGMT  gen 358296
  vd root/0  00:50:56:60:b3:79  gen 15463052  req OHUSA/3e
    created 88407604s  gen 1064  seen 22s  CORP_SERVERS  gen 358299
    ip 10.210.0.21  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  5e:a5:b5:98:22:b5  gen 14328074  req OUA/34
    created 2022812s  gen 14318098  seen 1992971s  Guest  gen 429210
    ip 172.176.0.4  src arp
    hardware vendor 'Apple'  src http  id 1743  weight 220
    type 'Phone'  src http  id 1743  weight 220
    family 'iPhone'  src http  id 1743  weight 220
    os 'iOS'  src http  id 1743  weight 220
    software version '26.4.2'  src http  id 1743  weight 220
    host 'iPhone'  src dhcp
  vd root/0  ac:64:17:b4:4a:11  gen 962  req OHUSA/3e
    created 88407689s  gen 8  seen 18s  ENG_LAND  gen 8
    ip 10.210.144.173  src arp
  vd root/0  ac:64:17:b4:4a:12  gen 1654739  req OHUSA/3e
    created 88407522s  gen 1399  seen 18s  ENG_LAND  gen 195968
  vd root/0  b8:a4:4f:0f:5c:8a  gen 11145  req OHUA/3c
    created 88407667s  gen 487  seen 10s  SECURITY_Int&CP  gen 231
    ip 10.210.40.22  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  e6:a9:57:f7:35:68  gen 11992884  req OUA/34
    created 88407593s  gen 1112  seen 12s  Guest  gen 379147
    ip 172.176.0.9  src mac
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'A52s-5G'  src dhcp  id 182  weight 232
    software version '12'  src dhcp  id 133  weight 255
    host 'Galaxy-A52s-5G'  src dhcp
  vd root/0  00:50:56:5f:f6:8b  gen 11281507  req OHUSA/3e
    created 83886140s  gen 44626  seen 22s  ESXMGMT  gen 358491
  vd root/0  22:35:1c:a1:5b:49  gen 14781312  req OUA/34
    created 7000357s  gen 12079192  seen 1211650s  Guest  gen 437306
    ip 172.176.0.35  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:62:c8:80  gen 15467470  req OHUSA/3e
    created 88405648s  gen 1756  seen 22s  VMWare_VMotion  gen 449629
    ip 10.210.7.23  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  aa:90:46:ca:53:82  gen 14379574  req OUA/34
    created 2791401s  gen 13874361  seen 1910341s  CORP WIRELESS  gen 430244
    ip 10.210.68.70  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:62:cb:8e  gen 15467468  req OHUSA/3e
    created 88405648s  gen 1758  seen 22s  VMWare_VMotion  gen 449628
    ip 10.210.7.27  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:64:8c:cf  gen 15467466  req OHUSA/3e
    created 88405648s  gen 1752  seen 22s  VMWare_VMotion  gen 449627
    ip 10.210.7.25  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  e8:1c:ba:b3:ba:00  gen 1644334  req 0
    created 88407524s  gen 1299  seen 20s  fortilink  gen 195780
  vd root/0  e8:1c:ba:b3:b9:d6  gen 1644055  req 0
    created 88407524s  gen 1258  seen 20s  fortilink  gen 195735
  vd root/0  e8:1c:ba:b3:b9:e4  gen 1566  req 0
    created 88407506s  gen 1566  seen 8s  fortilink  gen 818
  vd root/0  e8:1c:ba:b3:b9:f2  gen 1643695  req 0
    created 88407524s  gen 1275  seen 20s  fortilink  gen 195692
  vd root/0  e8:1c:ba:b3:c1:0e  gen 1644338  req 0
    created 88407524s  gen 1283  seen 20s  fortilink  gen 195784
  vd root/0  e8:1c:ba:b3:bf:cc  gen 1292  req 0
    created 88407524s  gen 1292  seen 20s  fortilink  gen 550
  vd root/0  e8:1c:ba:b3:c1:c4  gen 1277  req 0
    created 88407524s  gen 1277  seen 20s  fortilink  gen 535
  vd root/0  ac:64:17:b5:9d:33  gen 1654740  req OHUSA/3e
    created 88407522s  gen 1400  seen 18s  ENG_LAND  gen 195969
  vd root/0  ac:64:17:b5:9d:35  gen 1654737  req OHUSA/3e
    created 88407522s  gen 1395  seen 18s  ENG_LAND  gen 195966
  vd root/0  e8:1c:ba:b3:c8:2a  gen 1644473  req 0
    created 88407505s  gen 1583  seen 20s  fortilink  gen 195795
  vd root/0  ac:64:17:b5:9f:38  gen 1654938  req OHUSA/3e
    created 88407520s  gen 1492  seen 22s  ENG_LAND  gen 196010
  vd root/0  ac:64:17:b5:9d:be  gen 1655196  req OHUSA/3e
    created 88407524s  gen 1267  seen 20s  ENG_LANC  gen 196073
  vd root/0  ac:64:17:b5:9d:d0  gen 1654849  req OHUSA/3e
    created 88407524s  gen 1327  seen 20s  ENG_LANC  gen 195978
  vd root/0  ac:64:17:b5:a3:75  gen 1654726  req OHUSA/3e
    created 88407520s  gen 1483  seen 22s  ENG_LAND  gen 195955
  vd root/0  ac:64:17:b5:a3:76  gen 1654728  req OHUSA/3e
    created 88407520s  gen 1486  seen 22s  ENG_LAND  gen 195957
  vd root/0  ac:64:17:ba:04:c9  gen 1654927  req OHUSA/3e
    created 88407522s  gen 1402  seen 20s  ENG_LAND  gen 195999
  vd root/0  ac:64:17:ba:04:cb  gen 1654928  req OHUSA/3e
    created 88407522s  gen 1403  seen 20s  ENG_LAND  gen 196000
  vd root/0  3c:ec:ef:4f:bd:8d  gen 84836  req 0
    created 88407659s  gen 769  seen 0s  TegRepTransNet  gen 330
    ip 10.210.104.22  src mac
    server smb
  vd root/0  3c:ec:ef:4f:bd:93  gen 84839  req 0
    created 88407659s  gen 749  seen 22s  TegRepTransNet  gen 323
    ip 10.210.104.26  src mac
    server smb
  vd root/0  3c:ec:ef:4f:bd:af  gen 84838  req 0
    created 88407659s  gen 764  seen 2s  TegRepTransNet  gen 328
    ip 10.210.104.24  src mac
    server smb
  vd root/0  00:50:56:66:83:fd  gen 15467491  req OHUSA/3e
    created 88405648s  gen 1751  seen 22s  VMWare_VMotion  gen 449630
    ip 10.210.7.21  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:67:69:c8  gen 15464895  req OHUSA/3e
    created 88407660s  gen 662  seen 22s  CORP_SERVERS  gen 391427
    ip 10.210.0.31  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  ac:64:17:b6:9a:2e  gen 1654996  req OHUSA/3e
    created 88407505s  gen 1573  seen 20s  ENG_LAND  gen 196025
  vd root/0  ac:64:17:b6:9b:8c  gen 9180318  req OHUSA/3e
    created 88407503s  gen 1600  seen 22s  ENG_LANC  gen 313586
  vd root/0  12:56:e6:4e:a4:a6  gen 15458175  req OUA/34
    created 26723833s  gen 5735835  seen 20s  Guest  gen 449454
    ip 172.176.0.43  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.5'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  8e:98:91:71:f0:09  gen 14942275  req OUA/34
    created 53630416s  gen 983852  seen 953771s  CORP WIRELESS  gen 440165
    ip 10.210.68.15  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S2 Ultra'  src dhcp  id 6732  weight 230
    software version '14'  src http  id 997  weight 230
    host 'Tony-s-S22-Ultra'  src dhcp
  vd root/0  e4:1f:d5:9c:60:ee  gen 14782725  req OA/24
    created 34325386s  gen 3840530  seen 1122747s  CORP WIRELESS  gen 437349
    ip 10.210.68.45  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'VDC-FR2MW84'  src dhcp
    user 'mfrei'  src kerberos
  vd root/0  da:e6:80:de:d0:f1  gen 15191525  req OHUSA/3e
    created 1065474s  gen 14878496  seen 519179s  Guest  gen 444369
    ip 172.176.0.40  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
  vd root/0  66:09:66:da:05:8f  gen 14989525  req OUA/34
    created 37363786s  gen 3402425  seen 870222s  Guest  gen 440915
    ip 172.176.0.18  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.4'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  d6:6f:cd:d3:ca:c8  gen 14546409  req OHUA/3c
    created 4076868s  gen 13202005  seen 1636679s  Guest  gen 433363
    ip 172.176.0.40  src arp
    hardware vendor 'Apple'  src dhcp  id 4670  weight 130
    type 'Mobile Generic'  src dhcp  id 4670  weight 130
    os 'iOS'  src dhcp  id 4670  weight 130
  vd root/0  ac:64:17:b9:71:68  gen 976  req OHUSA/3e
    created 88407680s  gen 21  seen 22s  ENG_LAND  gen 21
    ip 10.210.144.108  src arp
  vd root/0  ac:64:17:b9:71:69  gen 1655008  req OHUSA/3e
    created 88407520s  gen 1525  seen 22s  ENG_LAND  gen 196035
  vd root/0  00:50:56:67:ac:82  gen 15467294  req OHUSA/3e
    created 88405602s  gen 1767  seen 22s  VMWare_VMotion  gen 449620
    ip 10.210.7.35  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  28:2e:89:a2:5c:82  gen 15461069  req OUA/34
    created 30355098s  gen 4756773  seen 1785s  Guest  gen 449511
    ip 172.176.0.40  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'LAP25012'  src dhcp
  vd root/0  f6:35:1c:44:25:30  gen 15453171  req OUA/34
    created 31998741s  gen 4302224  seen 29386s  CORP WIRELESS  gen 449349
    ip 10.210.68.23  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  ac:64:17:b8:a5:bc  gen 1655009  req OHUSA/3e
    created 88407520s  gen 1526  seen 22s  ENG_LAND  gen 196036
  vd root/0  ac:64:17:b8:a5:be  gen 1655007  req OHUSA/3e
    created 88407520s  gen 1523  seen 22s  ENG_LAND  gen 196034
  vd root/0  86:22:34:5a:b7:da  gen 14831400  req OUA/34
    created 88407662s  gen 647  seen 1121126s  CORP WIRELESS  gen 438174
    ip 10.210.68.39  src arp
    hardware vendor 'Apple'  src dns  id 4849  weight 230
    type 'Phone'  src dns  id 4849  weight 230
    family 'iPhone'  src dns  id 4849  weight 230
    os 'iOS'  src dns  id 4849  weight 230
    hardware version '13 Pro Max'  src dns  id 4849  weight 230
    software version '16.6'  src http  id 905  weight 230
    host 'iPhone-von-Manuel'  src dns
  vd root/0  2e:13:89:15:3f:b1  gen 15452946  req OUA/34
    created 34776s  gen 15450669  seen 23741s  CORP WIRELESS  gen 449338
    ip 10.210.68.34  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '13'  src dhcp  id 191  weight 130
    host 'Ciulei-s-A71'  src dhcp
  vd root/0  b8:a4:4f:18:12:08  gen 11140  req OHUA/3c
    created 88407667s  gen 427  seen 3s  SECURITY_ExtDev  gen 202
    ip 10.210.48.23  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  b8:a4:4f:18:11:99  gen 11128  req OHUA/3c
    created 88407667s  gen 436  seen 5s  SECURITY_ExtDev  gen 207
    ip 10.210.48.24  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  b8:a4:4f:18:11:9a  gen 14641521  req OHUA/3c
    created 88407667s  gen 445  seen 0s  SECURITY_ExtDev  gen 435043
    ip 10.210.48.13  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  b8:a4:4f:18:11:9c  gen 11182  req OHUA/3c
    created 88407667s  gen 434  seen 13s  SECURITY_Int&CP  gen 206
    ip 10.210.40.20  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  b8:a4:4f:18:11:a4  gen 5267  req OHUA/3c
    created 88407667s  gen 490  seen 8s  SECURITY_Int&CP  gen 232
    ip 10.210.40.18  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  b8:a4:4f:18:11:a5  gen 11162  req OHUA/3c
    created 88407667s  gen 467  seen 5s  SECURITY_ExtDev  gen 222
    ip 10.210.48.21  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  28:92:00:0b:ef:e6  gen 15288092  req OA/24
    created 24738288s  gen 6279732  seen 342057s  CORP WIRELESS  gen 446204
    ip 10.210.68.84  src mac
    os 'Windows'  src dhcp  id 6502  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'WIN-LS5I9VLB1TH'  src dhcp
    user 'mcelebic'  src kerberos
  vd root/0  b8:a4:4f:18:11:ac  gen 14641514  req OHUA/3c
    created 88407667s  gen 465  seen 5s  SECURITY_ExtDev  gen 435040
    ip 10.210.48.15  src mac
    hardware vendor 'Axis'  src onvif  id 4316  weight 230
    type 'IP Camera'  src onvif  id 4316  weight 230
    family 'IP Camera'  src onvif  id 4316  weight 230
    hardware version 'A8004-VE'  src onvif  id 4316  weight 230
  vd root/0  28:2e:89:a2:7b:18  gen 15456982  req OUA/34
    created 23020954s  gen 6810850  seen 41s  Guest  gen 449425
    ip 172.176.0.41  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'LAP25013'  src dhcp
  vd root/0  00:50:56:67:cb:42  gen 15467297  req OHUSA/3e
    created 88405645s  gen 1761  seen 22s  VMWare_VMotion  gen 449622
    ip 10.210.7.33  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  ac:64:17:b9:99:5d  gen 700  req OHUSA/3e
    created 88407659s  gen 699  seen 13s  ENG_LANC  gen 298
    ip 10.210.140.108  src arp
  vd root/0  ac:64:17:b9:99:5e  gen 1655213  req OHUSA/3e
    created 88407520s  gen 1510  seen 22s  ENG_LANC  gen 196086
  vd root/0  00:50:56:68:b2:9c  gen 15465337  req OHUSA/3e
    created 88407604s  gen 1054  seen 22s  CORP_SERVERS  gen 391448
    ip 10.210.0.27  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  e4:1f:d5:9d:95:4a  gen 15435381  req OA/24
    created 16359138s  gen 8964974  seen 33048s  CORP WIRELESS  gen 449031
    ip 10.210.68.52  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'VDC-3PXLW84'  src dhcp
    user 'jtexugo'  src kerberos
  vd root/0  ac:64:17:b9:9f:5c  gen 110  req OHUA/3c
    created 88407671s  gen 32  seen 12s  ENG_LANC  gen 26
    ip 10.210.140.168  src arp
    hardware vendor 'Siemens'  src fortiguard  id 0  weight 108
    type 'Industry'  src fortiguard  id 0  weight 108
    family 'Industrial Device'  src fortiguard  id 0  weight 108
    hardware version 'SIMATIC'  src fortiguard  id 0  weight 108
  vd root/0  ac:64:17:b9:9f:5d  gen 1654869  req OHUSA/3e
    created 88407520s  gen 1469  seen 20s  ENG_LANC  gen 195993
  vd root/0  ac:64:17:b9:9f:76  gen 968  req OHUSA/3e
    created 88407686s  gen 12  seen 20s  ENG_LANC  gen 12
    ip 10.210.140.138  src arp
  vd root/0  ac:64:17:b9:9f:77  gen 1655317  req OHUSA/3e
    created 88407524s  gen 1324  seen 20s  ENG_LANC  gen 196106
  vd root/0  ac:64:17:b9:9f:d9  gen 918  req OHUSA/3e
    created 88407644s  gen 917  seen 20s  ENG_LAND  gen 378
    ip 10.210.144.138  src arp
  vd root/0  ac:64:17:b9:9f:da  gen 1654929  req OHUSA/3e
    created 88407522s  gen 1405  seen 20s  ENG_LAND  gen 196001
  vd root/0  ac:64:17:b7:e3:b2  gen 1654868  req OHUSA/3e
    created 88407520s  gen 1467  seen 20s  ENG_LANC  gen 195992
  vd root/0  ac:64:17:b7:e3:b4  gen 1654871  req OHUSA/3e
    created 88407520s  gen 1471  seen 20s  ENG_LANC  gen 195995
  vd root/0  c2:a6:fb:87:a0:89  gen 14543601  req OUA/34
    created 1649230s  gen 14539072  seen 1636582s  Guest  gen 433208
    ip 172.176.0.47  src arp
    hardware vendor 'Samsung'  src http  id 1788  weight 220
    type 'Phone'  src http  id 1788  weight 220
    family 'Galaxy'  src http  id 1788  weight 220
    os 'Android'  src http  id 1788  weight 220
    software version '14'  src http  id 1788  weight 220
    host 'Ciaran-s-S23-FE'  src dhcp
  vd root/0  00:50:56:6a:7f:c3  gen 15422866  req OHUSA/3e
    created 88407660s  gen 660  seen 22s  CORP_SERVERS  gen 391408
    ip 10.210.0.33  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  f4:96:34:b3:90:43  gen 15392260  req OUA/34
    created 88357299s  gen 2877  seen 126066s  Guest  gen 448156
    ip 172.176.0.23  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-VUHDOGA'  src dhcp
  vd root/0  e0:23:ff:e7:93:c1  gen 1026  req 0
    created 88407605s  gen 1026  seen 23s  fortilink  gen 420
  vd root/0  e0:23:ff:e7:94:cf  gen 1008  req 0
    created 88407605s  gen 1007  seen 18s  fortilink  gen 404
  vd root/0  00:50:56:68:ca:78  gen 15464246  req OHUSA/3e
    created 88407604s  gen 1062  seen 22s  CORP_SERVERS  gen 358404
    ip 10.210.0.23  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  e0:23:ff:e7:96:cd  gen 1013  req 0
    created 88407605s  gen 1012  seen 23s  fortilink  gen 408
  vd root/0  00:0d:8d:03:47:4c  gen 15272591  req OHUSA/3e
    created 88407504s  gen 1590  seen 18s  ENG_LANA  gen 196048
    ip 10.210.132.223  src arp
  vd root/0  00:0d:8d:03:47:55  gen 15462353  req OHUSA/3e
    created 88407521s  gen 1450  seen 22s  ENG_LANA  gen 196046
    ip 10.210.132.224  src arp
  vd root/0  00:0d:8d:03:47:56  gen 15453030  req OHUSA/3e
    created 88407507s  gen 1556  seen 22s  ENG_LANA  gen 196051
    ip 10.210.132.222  src arp
  vd root/0  00:0d:8d:03:47:ab  gen 15439200  req OHUSA/3e
    created 88407522s  gen 1376  seen 22s  ENG_LANA  gen 196049
    ip 10.210.132.221  src arp
  vd root/0  00:0d:8d:03:47:ac  gen 15451834  req OHUSA/3e
    created 88407522s  gen 1357  seen 19s  ENG_LANA  gen 196056
    ip 10.210.132.220  src arp
  vd root/0  ac:64:17:b9:c2:ae  gen 1655318  req OHUSA/3e
    created 88407524s  gen 1325  seen 20s  ENG_LANC  gen 196107
  vd root/0  ac:64:17:b9:c2:b0  gen 1655314  req OHUSA/3e
    created 88407524s  gen 1319  seen 20s  ENG_LANC  gen 196103
  vd root/0  7c:1e:b3:ed:1b:68  gen 15246046  req OUA/34
    created 46663774s  gen 2056006  seen 1s  CORP_WKS  gen 445389
    ip 10.210.64.21  src arp
    hardware vendor 'Yealink'  src sip  id 3394  weight 220
    type 'IP Phone'  src sip  id 3394  weight 220
    family 'T'  src sip  id 3394  weight 220
    os 'Linux'  src tcp  id 1624  weight 90
    hardware version 'T58W'  src sip  id 3396  weight 200
    host '2N® IP Phone D7A'  src dhcp
  vd root/0  ac:64:17:b9:ce:51  gen 1655209  req OHUSA/3e
    created 88407520s  gen 1505  seen 22s  ENG_LANC  gen 196082
  vd root/0  ac:64:17:b9:ce:53  gen 1655212  req OHUSA/3e
    created 88407520s  gen 1509  seen 22s  ENG_LANC  gen 196085
  vd root/0  00:50:56:6b:81:dd  gen 15467311  req OHUSA/3e
    created 88405645s  gen 1763  seen 22s  VMWare_VMotion  gen 449624
    ip 10.210.7.29  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  ac:64:17:b9:d0:81  gen 3395222  req OHUSA/3e
    created 88407524s  gen 1303  seen 20s  ENG_LANC  gen 214830
  vd root/0  ac:64:17:b9:d0:83  gen 3395223  req OHUSA/3e
    created 88407524s  gen 1304  seen 20s  ENG_LANC  gen 214831
  vd root/0  1a:71:55:b5:d4:13  gen 15385444  req OUA/34
    created 41427309s  gen 2842764  seen 163533s  CORP WIRELESS  gen 448026
    ip 10.210.68.13  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '14'  src http  id 997  weight 230
    host 'SM-L315F'  src dhcp
  vd root/0  a4:a4:d3:be:a6:fe  gen 14575668  req OHUA/3c
    created 88407597s  gen 1089  seen 74s  Guest  gen 408543
    ip 172.176.0.24  src arp
    os 'KaiOS'  src http  id 1357  weight 130
    software version '2.5.1'  src http  id 1357  weight 130
  vd root/0  00:50:56:6a:b8:d6  gen 15465535  req OHUSA/3e
    created 88407604s  gen 1061  seen 22s  CORP_SERVERS  gen 358282
    ip 10.210.0.29  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:6c:7f:9b  gen 15462496  req OHUSA/3e
    created 88407604s  gen 1049  seen 22s  CORP_SERVERS  gen 358451
    ip 10.210.0.25  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  d2:ea:af:ad:ff:5b  gen 14426646  req OUA/34
    created 7618259s  gen 11932829  seen 1817006s  Guest  gen 431127
    ip 172.176.0.42  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.7.6'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:6c:a8:d0  gen 15467295  req OHUSA/3e
    created 88405645s  gen 1765  seen 22s  VMWare_VMotion  gen 449621
    ip 10.210.7.31  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:0d:8d:06:46:c0  gen 15294168  req OHUSA/3e
    created 88407522s  gen 1440  seen 20s  ENG_LANA  gen 195770
    ip 10.210.132.204  src arp
  vd root/0  00:0d:8d:06:46:f4  gen 15417771  req OHUSA/3e
    created 88407522s  gen 1422  seen 19s  ENG_LANA  gen 195745
    ip 10.210.132.205  src arp
  vd root/0  00:0d:8d:06:51:2e  gen 15451832  req OHUSA/3e
    created 88407522s  gen 1421  seen 19s  ENG_LANB  gen 195744
    ip 10.210.136.205  src arp
  vd root/0  e4:1f:d5:9e:ff:2f  gen 15232480  req OA/24
    created 29653980s  gen 4957247  seen 432970s  CORP WIRELESS  gen 445094
    ip 10.210.68.64  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-0E0PQSR'  src dhcp
    user 'erikgeert.mollema'  src kerberos
  vd root/0  e4:1f:d5:9e:ff:34  gen 15460467  req OA/24
    created 36738118s  gen 3490209  seen 1s  CORP WIRELESS  gen 449499
    ip 10.210.68.11  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-RN4GGAV'  src dhcp
    user 'aman.singh'  src kerberos
  vd root/0  e4:1f:d5:9e:fe:85  gen 14798518  req OUA/34
    created 1547945s  gen 14598419  seen 1206633s  CORP WIRELESS  gen 437640
    ip 10.210.68.53  src arp
    os 'Windows'  src http  id 1077  weight 130
    host 'VDC-HFLMW84'  src dhcp
  vd root/0  00:0d:8d:06:66:63  gen 15444743  req OHUSA/3e
    created 88407522s  gen 1437  seen 20s  ENG_LANB  gen 195768
    ip 10.210.136.204  src arp
  vd root/0  c2:2b:fb:fa:29:0c  gen 14127635  req OHUA/3c
    created 2350881s  gen 14127627  seen 2342929s  CORP WIRELESS  gen 426253
    ip 10.210.68.24  src arp
    hardware vendor 'Apple'  src dhcp  id 4670  weight 130
    type 'Mobile Generic'  src dhcp  id 4670  weight 130
    os 'iOS'  src dhcp  id 4670  weight 130
  vd root/0  56:af:b5:b8:36:ca  gen 15451223  req OUA/34
    created 33800s  gen 15451221  seen 23741s  CORP WIRELESS  gen 449305
    ip 10.210.68.36  src arp
    hardware vendor 'Samsung'  src dhcp  id 182  weight 232
    type 'Phone'  src dhcp  id 182  weight 232
    family 'Galaxy'  src dhcp  id 182  weight 232
    os 'Android'  src dhcp  id 182  weight 232
    hardware version 'S21-Ultra-5G'  src dhcp  id 182  weight 232
    software version '15'  src dhcp  id 182  weight 232
    host 'Galaxy-S21-Ultra-5G'  src dhcp
  vd root/0  70:9c:d1:52:99:aa  gen 14476610  req OUA/34
    created 1755301s  gen 14474925  seen 1749160s  Guest  gen 432054
    ip 172.176.0.30  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'MUC-1801050711'  src dhcp
  vd root/0  46:b3:67:ec:e8:f3  gen 15288731  req OUA/34
    created 6169030s  gen 12353112  seen 353978s  Guest  gen 446217
    ip 172.176.0.30  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.3.1'  src http  id 902  weight 230
    host 'Adams-iPhone'  src dns
  vd root/0  f6:91:af:e5:a4:a3  gen 15456832  req OUA/34
    created 15836207s  gen 9151382  seen 21039s  CORP WIRELESS  gen 449423
    ip 10.210.68.46  src arp
    hardware vendor 'Apple'  src dhcp  id 2675  weight 180
    type 'Phone'  src dhcp  id 2675  weight 180
    family 'iPhone'  src dhcp  id 2675  weight 180
    os 'iOS'  src dhcp  id 2675  weight 180
    host 'iPhone'  src dhcp
  vd root/0  d4:76:a0:f5:7f:c0  gen 9910221  req OUA/34
    created 88407659s  gen 685  seen 0s  WIRELESS_APs  gen 291
    ip 10.210.96.28  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21037550'  src capwap
  vd root/0  d4:76:a0:f5:88:00  gen 8521356  req OUA/34
    created 88407659s  gen 677  seen 0s  WIRELESS_APs  gen 287
    ip 10.210.96.36  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21037616'  src capwap
  vd root/0  a8:43:a4:e5:15:1d  gen 14334526  req OUA/34
    created 14885565s  gen 9523163  seen 1991378s  Guest  gen 429469
    ip 172.176.0.3  src mac
    os 'Android'  src dhcp  id 191  weight 130
    software version '11'  src dhcp  id 191  weight 130
    host 'Android'  src dns
  vd root/0  c8:4b:d6:94:d5:75  gen 5837727  req OUSA/36
    created 88388649s  gen 2213  seen 21s  NET_MANAGEMENT  gen 253981
    ip 10.210.100.151  src mac
    host 'ZRH11-SEC-Secondary-iDRAC01-FO'  src dns
  vd root/0  c8:4b:d6:94:d9:65  gen 10676408  req OUA/34
    created 88392769s  gen 2054  seen 22s  NET_MANAGEMENT  gen 344608
    ip 10.210.100.142  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'ZRH11-SEC-Primary-iDRAC02'  src dns
  vd root/0  c8:4b:d6:94:d9:89  gen 3598  req OUA/34
    created 88392769s  gen 2056  seen 22s  NET_MANAGEMENT  gen 962
    ip 10.210.100.141  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'ZRH11-SEC-Primary-iDRAC01'  src dns
  vd root/0  ac:1d:df:91:8f:7f  gen 15399767  req OHUSA/3e
    created 88407529s  gen 1225  seen 22s  ENG_LANC  gen 488
    ip 10.210.140.31  src mac
  vd root/0  c8:4b:d6:94:ea:5d  gen 10676410  req OUA/34
    created 88388648s  gen 2215  seen 22s  NET_MANAGEMENT  gen 344609
    ip 10.210.100.152  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'ZRH11-SEC-Secondary-iDRAC02-FO'  src dns
  vd root/0  d6:e1:1f:0f:c2:93  gen 15077096  req OUA/34
    created 724454s  gen 15077094  seen 696966s  Guest  gen 442279
    ip 172.176.0.26  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  8a:b0:91:23:0e:ac  gen 15324503  req OUA/34
    created 88337346s  gen 3021  seen 252147s  Guest  gen 446909
    ip 172.176.0.8  src arp
    hardware vendor 'Samsung'  src http  id 993  weight 255
    type 'Phone'  src http  id 993  weight 255
    family 'Galaxy'  src http  id 993  weight 255
    os 'Android'  src http  id 993  weight 255
    hardware version 'S'  src http  id 1094  weight 230
    software version '12'  src http  id 993  weight 255
    host 'Julie-s-S21'  src dhcp
  vd root/0  ac:64:17:cb:22:36  gen 9180823  req OHUSA/3e
    created 88407524s  gen 1308  seen 20s  ENG_LAND  gen 313605
  vd root/0  ac:64:17:cb:22:37  gen 9180822  req OHUSA/3e
    created 88407524s  gen 1305  seen 20s  ENG_LAND  gen 313604
  vd root/0  ac:64:17:cb:22:5c  gen 3417618  req OHUSA/3e
    created 88407522s  gen 1373  seen 18s  ENG_LAND  gen 215135
  vd root/0  ac:64:17:cb:22:5d  gen 3417616  req OHUSA/3e
    created 88407522s  gen 1371  seen 18s  ENG_LAND  gen 215133
  vd root/0  ac:64:17:cb:28:8a  gen 9168493  req OHUSA/3e
    created 88407524s  gen 1285  seen 20s  ENG_LANC  gen 313404
  vd root/0  ac:64:17:cb:28:8b  gen 9168490  req OHUSA/3e
    created 88407524s  gen 1281  seen 20s  ENG_LANC  gen 313401
  vd root/0  ac:64:17:cb:29:71  gen 3454165  req OHUSA/3e
    created 88407522s  gen 1379  seen 18s  ENG_LANC  gen 215504
  vd root/0  ac:64:17:cb:29:72  gen 3454166  req OHUSA/3e
    created 88407522s  gen 1382  seen 18s  ENG_LANC  gen 215505
  vd root/0  ac:64:17:cb:28:b0  gen 3395038  req OHUSA/3e
    created 88407522s  gen 1368  seen 19s  ENG_LANC  gen 214816
  vd root/0  ac:64:17:cb:28:b1  gen 3395037  req OHUSA/3e
    created 88407522s  gen 1365  seen 19s  ENG_LANC  gen 214815
  vd root/0  ac:64:17:cb:28:f2  gen 9168423  req OHUSA/3e
    created 88407505s  gen 1585  seen 20s  ENG_LANC  gen 313400
  vd root/0  ac:64:17:cb:28:f3  gen 9168420  req OHUSA/3e
    created 88407505s  gen 1581  seen 20s  ENG_LANC  gen 313397
  vd root/0  ac:64:17:cb:2f:46  gen 3417426  req OHUSA/3e
    created 88407524s  gen 1313  seen 20s  ENG_LAND  gen 215126
  vd root/0  ac:64:17:cb:2f:47  gen 3417424  req OHUSA/3e
    created 88407524s  gen 1311  seen 20s  ENG_LAND  gen 215124
  vd root/0  ac:64:17:cb:2f:4f  gen 9180831  req OHUSA/3e
    created 88407522s  gen 1384  seen 18s  ENG_LAND  gen 313608
  vd root/0  ac:64:17:cb:2f:50  gen 9180832  req OHUSA/3e
    created 88407522s  gen 1388  seen 18s  ENG_LAND  gen 313609
  vd root/0  d6:3c:a5:26:b4:21  gen 14241844  req OUA/34
    created 2172742s  gen 14233378  seen 2157500s  CORP WIRELESS  gen 427849
    ip 10.210.68.57  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  ce:fe:df:d5:a1:9b  gen 15241181  req OUA/34
    created 28882648s  gen 5157080  seen 433154s  CORP WIRELESS  gen 445084
    ip 10.210.68.61  src arp
    hardware vendor 'Apple'  src dns  id 4616  weight 230
    type 'Phone'  src dns  id 4616  weight 230
    family 'iPhone'  src dns  id 4616  weight 230
    os 'iOS'  src dns  id 4616  weight 230
    hardware version '12'  src dns  id 4616  weight 230
    software version '18.5'  src http  id 929  weight 230
    host 'iPhone-Vantage'  src dns
  vd root/0  ac:64:17:ca:99:62  gen 3454327  req OHUSA/3e
    created 88407522s  gen 1390  seen 22s  ENG_LANC  gen 215517
  vd root/0  ac:64:17:ca:99:63  gen 3454329  req OHUSA/3e
    created 88407522s  gen 1392  seen 22s  ENG_LANC  gen 215519
  vd root/0  ac:64:17:ce:2d:00  gen 3404507  req OHUSA/3e
    created 88407524s  gen 1295  seen 20s  ENG_LANC  gen 214964
  vd root/0  ac:64:17:ce:2d:01  gen 3404506  req OHUSA/3e
    created 88407524s  gen 1291  seen 20s  ENG_LANC  gen 214963
  vd root/0  ac:64:17:ce:2d:3b  gen 3404265  req OHUSA/3e
    created 88407524s  gen 1288  seen 20s  ENG_LANC  gen 214958
  vd root/0  ac:64:17:ce:2d:3c  gen 3404266  req OHUSA/3e
    created 88407524s  gen 1290  seen 20s  ENG_LANC  gen 214959
  vd root/0  6e:a6:35:19:c9:78  gen 15277562  req OUA/34
    created 48990116s  gen 1740907  seen 346547s  Guest  gen 445973
    ip 172.176.0.33  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'S20'  src dhcp  id 182  weight 232
    software version '13'  src dhcp  id 133  weight 255
    host 'Galaxy-S20'  src dhcp
  vd root/0  fe:20:fd:31:1b:d9  gen 15202428  req OUA/34
    created 12625223s  gen 10216009  seen 512113s  CORP WIRELESS  gen 444579
    ip 10.210.68.29  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  08:8e:90:bb:14:99  gen 15457806  req OUA/34
    created 88407597s  gen 1091  seen 15s  Guest  gen 449438
    ip 172.176.0.10  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'LAP22114'  src dhcp
  vd root/0  ac:64:17:d0:0c:ae  gen 3384082  req OHUSA/3e
    created 88407524s  gen 1298  seen 20s  ENG_LAND  gen 214636
  vd root/0  ac:64:17:d0:0c:af  gen 3384081  req OHUSA/3e
    created 88407524s  gen 1297  seen 20s  ENG_LAND  gen 214635
  vd root/0  00:80:f4:aa:b0:e4  gen 1654741  req OHUSA/3e
    created 88407637s  gen 951  seen 18s  ENG_LAND  gen 195970
    ip 10.210.144.170  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  00:80:f4:aa:b0:fe  gen 1202  req OHUSA/3e
    created 88407690s  gen 4  seen 22s  ENG_LANC  gen 4
    ip 10.210.140.130  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  de:23:04:f6:cc:60  gen 14548613  req OUA/34
    created 1651444s  gen 14537525  seen 1633948s  Guest  gen 433399
    ip 172.176.0.38  src arp
    hardware vendor 'Google'  src dhcp  id 6466  weight 220
    type 'Phone'  src dhcp  id 6466  weight 220
    family 'Pixel'  src dhcp  id 6466  weight 220
    os 'Android'  src dhcp  id 6466  weight 220
    hardware version '4a'  src dhcp  id 6466  weight 220
    software version '1'  src dhcp  id 6466  weight 220
    host 'Pixel-4a'  src dhcp
  vd root/0  00:80:f4:aa:cf:94  gen 1138  req OHUSA/3e
    created 88407681s  gen 18  seen 20s  ENG_LAND  gen 18
    ip 10.210.144.100  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  00:80:f4:aa:cf:b6  gen 138  req OHUA/3c
    created 88407668s  gen 100  seen 22s  ENG_LAND  gen 56
    ip 10.210.144.130  src arp
    hardware vendor 'Schneider Elect'  src fortiguard  id 0  weight 127
    type 'Network'  src fortiguard  id 0  weight 127
    family 'Gateway'  src fortiguard  id 0  weight 127
    os 'Android'  src fortiguard  id 0  weight 127
  vd root/0  00:80:f4:aa:cf:f2  gen 1151  req OHUSA/3e
    created 88407677s  gen 25  seen 13s  ENG_LAND  gen 25
    ip 10.210.144.160  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  46:9d:e6:28:86:c6  gen 15232393  req OUA/34
    created 460883s  gen 15232391  seen 448586s  Guest  gen 445090
    ip 172.176.0.34  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  ac:64:17:ce:b2:36  gen 1655469  req OHUSA/3e
    created 88407524s  gen 1272  seen 20s  ENG_LAND  gen 196122
  vd root/0  ac:64:17:ce:b2:37  gen 1655470  req OHUSA/3e
    created 88407524s  gen 1274  seen 20s  ENG_LAND  gen 196123
  vd root/0  00:80:f4:aa:ef:16  gen 1094  req OHUSA/3e
    created 88407689s  gen 9  seen 20s  ENG_LANC  gen 9
    ip 10.210.140.160  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  ac:64:17:ce:b2:9c  gen 3417839  req OHUSA/3e
    created 88407520s  gen 1478  seen 22s  ENG_LAND  gen 215138
  vd root/0  ac:64:17:ce:b2:9d  gen 3417840  req OHUSA/3e
    created 88407520s  gen 1480  seen 22s  ENG_LAND  gen 215139
  vd root/0  00:80:f4:aa:f0:1e  gen 964  req OHUSA/3e
    created 88407629s  gen 963  seen 20s  ENG_LANC  gen 396
    ip 10.210.140.100  src arp
    hardware vendor 'Telemecanique'  src mac  id 0  weight 120
  vd root/0  ac:64:17:ce:b2:b4  gen 3454315  req OHUSA/3e
    created 88407523s  gen 1353  seen 20s  ENG_LANC  gen 215514
  vd root/0  ac:64:17:ce:b2:b5  gen 3454316  req OHUSA/3e
    created 88407523s  gen 1355  seen 20s  ENG_LANC  gen 215515
  vd root/0  ac:64:17:ce:b2:bd  gen 9180821  req OHUSA/3e
    created 88407524s  gen 1350  seen 20s  ENG_LAND  gen 313603
  vd root/0  ac:64:17:ce:b2:bf  gen 9180820  req OHUSA/3e
    created 88407524s  gen 1349  seen 20s  ENG_LAND  gen 313602
  vd root/0  e8:62:be:97:c2:e6  gen 15091723  req OUA/34
    created 2356819s  gen 14124230  seen 690855s  Guest  gen 442586
    ip 172.176.0.19  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'ZRH-YME7HWQSQNC'  src dhcp
  vd root/0  e0:3e:cb:f8:99:94  gen 14161479  req OUA/34
    created 24718433s  gen 6284526  seen 2294366s  Guest  gen 426773
    ip 172.176.0.4  src mac
    hardware vendor 'Hisense'  src http  id 5302  weight 180
    type 'Television'  src http  id 5302  weight 180
    family 'TV'  src http  id 5302  weight 180
    os 'Linux'  src ssdp  id 6076  weight 128
    hardware version 'SmartTV'  src http  id 5302  weight 180
    host 'SmartTV-cc12280045af'  src dns
  vd root/0  e2:0a:01:62:18:5d  gen 14537301  req OUA/34
    created 1651767s  gen 14537299  seen 1636556s  Guest  gen 433174
    ip 172.176.0.19  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:a0:03:ee:cc:d6  gen 6873268  req OHUSA/3e
    created 88407666s  gen 542  seen 22s  ENG_LANB  gen 271946
    ip 10.210.136.111  src arp
  vd root/0  00:a0:03:ee:d2:94  gen 14384521  req OHUSA/3e
    created 88407667s  gen 525  seen 11s  ENG_LANA  gen 430350
    ip 10.210.132.111  src arp
  vd root/0  00:a0:03:ee:d2:98  gen 12659199  req OHUA/3c
    created 88407669s  gen 42  seen 20s  ENG_LANA  gen 396300
    ip 10.210.132.112  src arp
    hardware vendor 'Siemens'  src fortiguard  id 0  weight 178
    type 'Industry'  src fortiguard  id 0  weight 178
    family 'Industrial Device'  src fortiguard  id 0  weight 178
    os 'Windows CE'  src fortiguard  id 0  weight 178
    hardware version 'POL648'  src fortiguard  id 0  weight 178
  vd root/0  de:a6:74:fe:9b:f3  gen 15460816  req OUA/34
    created 52887891s  gen 1108720  seen 13553s  Guest  gen 449507
    ip 172.176.0.19  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '14'  src dhcp  id 191  weight 130
    host 'Zenfone-9'  src dhcp
  vd root/0  56:31:ec:4c:3e:57  gen 15086931  req OUSA/36
    created 724446s  gen 15077097  seen 701831s  Guest  gen 442488
    ip 172.176.0.27  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  70:08:10:62:c9:e2  gen 14229925  req OUA/34
    created 2182241s  gen 14228080  seen 2178870s  Guest  gen 427782
    ip 172.176.0.33  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'ZRH-3I6S6GRK2Z4'  src dhcp
  vd root/0  7e:3b:71:54:54:97  gen 15001422  req OUA/34
    created 4612408s  gen 12979297  seen 853129s  CORP WIRELESS  gen 441082
    ip 10.210.68.34  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  70:08:10:63:e9:85  gen 14928586  req OUA/34
    created 980050s  gen 14928253  seen 976771s  Guest  gen 439909
    ip 172.176.0.43  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'ZRH-XIS171ON75O'  src dhcp
  vd root/0  28:0c:50:60:ec:49  gen 14490623  req OUA/34
    created 1729593s  gen 14490614  seen 1727795s  CORP WIRELESS  gen 432338
    ip 10.210.68.50  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'VDC-C08RXC4'  src dhcp
  vd root/0  d6:0e:10:b3:42:6f  gen 15414215  req OUA/34
    created 725835s  gen 15076301  seen 105286s  CORP WIRELESS  gen 448599
    ip 10.210.68.72  src mac
    hardware vendor 'Samsung'  src http  id 1093  weight 230
    type 'Phone'  src http  id 1093  weight 230
    family 'Galaxy'  src http  id 1093  weight 230
    os 'Android'  src http  id 1093  weight 230
    hardware version 'A'  src http  id 1093  weight 230
    software version '16'  src http  id 1093  weight 230
    host 'A54-von-Sandro'  src dhcp
  vd root/0  ac:64:17:d6:72:c2  gen 3383995  req OHUSA/3e
    created 88407524s  gen 1256  seen 20s  ENG_LAND  gen 214626
  vd root/0  ac:64:17:d6:72:c3  gen 3383996  req OHUSA/3e
    created 88407524s  gen 1259  seen 20s  ENG_LAND  gen 214627
  vd root/0  ac:64:17:d6:71:eb  gen 3383964  req OHUSA/3e
    created 88407524s  gen 1279  seen 20s  ENG_LAND  gen 214624
  vd root/0  ac:64:17:d6:71:ec  gen 3383963  req OHUSA/3e
    created 88407524s  gen 1278  seen 20s  ENG_LAND  gen 214623
  vd root/0  ac:64:17:d6:89:2e  gen 9168495  req OHUSA/3e
    created 88407503s  gen 1598  seen 20s  ENG_LANC  gen 313406
  vd root/0  ac:64:17:d6:89:2f  gen 9168494  req OHUSA/3e
    created 88407503s  gen 1594  seen 20s  ENG_LANC  gen 313405
  vd root/0  ac:64:17:d6:88:bc  gen 9168592  req OHUSA/3e
    created 88407524s  gen 1342  seen 20s  ENG_LANC  gen 313408
  vd root/0  ac:64:17:d6:88:bd  gen 9168591  req OHUSA/3e
    created 88407524s  gen 1338  seen 20s  ENG_LANC  gen 313407
  vd root/0  5a:58:61:bd:93:30  gen 15452607  req OUA/34
    created 57209090s  gen 354206  seen 8s  Guest  gen 449329
    ip 172.176.0.32  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'A41'  src dhcp  id 182  weight 232
    software version '12'  src dhcp  id 133  weight 255
    host 'Galaxy-A41'  src dhcp
  vd root/0  02:03:ea:f6:d9:20  gen 15285179  req OUA/34
    created 72376835s  gen 145576  seen 349203s  CORP WIRELESS  gen 446139
    ip 10.210.68.50  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    hardware version '14 Pro Max'  src dns  id 5006  weight 230
    software version '17.3.1'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  ac:64:17:d4:df:52  gen 3454209  req OHUSA/3e
    created 88407520s  gen 1472  seen 22s  ENG_LANC  gen 215509
  vd root/0  ac:64:17:d4:df:53  gen 3454211  req OHUSA/3e
    created 88407520s  gen 1475  seen 22s  ENG_LANC  gen 215511
  vd root/0  ac:64:17:d4:df:6f  gen 9180827  req OHUSA/3e
    created 88407522s  gen 1430  seen 19s  ENG_LAND  gen 313607
  vd root/0  ac:64:17:d4:df:70  gen 9180826  req OHUSA/3e
    created 88407522s  gen 1426  seen 19s  ENG_LAND  gen 313606
  vd root/0  00:50:56:8b:02:0f  gen 4739729  req OUA/34
    created 54857385s  gen 746614  seen 22s  ENG_LANA  gen 233915
    ip 10.210.132.14  src arp
    os 'Windows'  src ssdp  id 1612  weight 128
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-ENGWKS-01'  src dns
  vd root/0  78:ac:44:14:04:42  gen 12429603  req OHUSA/3e
    created 88407654s  gen 869  seen 22s  ESXMGMT  gen 391412
    ip 10.210.8.33  src mac
  vd root/0  1a:1c:85:c9:6c:2e  gen 15307209  req OUA/34
    created 50019019s  gen 1578848  seen 294092s  Guest  gen 446566
    ip 172.176.0.29  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.0.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  78:ac:44:14:05:74  gen 11281511  req OHUSA/3e
    created 88407575s  gen 1160  seen 21s  ESXMGMT  gen 358494
    ip 10.210.8.35  src mac
  vd root/0  b6:c3:0a:00:c4:fe  gen 15330032  req OUA/34
    created 3023837s  gen 13741636  seen 199751s  Guest  gen 447007
    ip 172.176.0.25  src arp
    hardware vendor 'Apple'  src dns  id 4626  weight 230
    type 'Tablet'  src dns  id 4626  weight 230
    family 'iPad'  src dns  id 4626  weight 230
    os 'iPadOS'  src dns  id 4626  weight 230
    hardware version 'iPad'  src dns  id 4626  weight 230
    software version '18.6.2'  src http  id 930  weight 230
    host 'iPad'  src dhcp
  vd root/0  00:50:56:8b:1a:63  gen 273072  req OHA/2c
    created 88407666s  gen 536  seen 0s  ENG_SERVERS  gen 137991
    ip 10.210.4.20  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src http  id 1403  weight 100
    os 'Debian'  src http  id 1403  weight 100
    user 'puppetsso'  src kerberos
  vd root/0  00:50:56:8b:1d:60  gen 162632  req OHA/2c
    created 88407666s  gen 551  seen 0s  ENG_SERVERS  gen 83994
    ip 10.210.4.21  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src ssh  id 1613  weight 128
    os 'Ubuntu'  src ssh  id 1613  weight 128
    user 'puppetsso'  src kerberos
  vd root/0  70:88:4d:02:b2:da  gen 14894993  req OUA/34
    created 88407619s  gen 979  seen 22s  CORP WIRELESS  gen 439342
    ip 10.210.68.32  src mwbs
    hardware vendor 'Ricoh'  src dns  id 875  weight 150
    type 'Printer'  src dns  id 875  weight 150
    host 'RNP70884D02B2DA'  src mwbs
  vd root/0  00:50:56:8b:22:46  gen 607  req 0
    created 88407663s  gen 605  seen 0s  VMWare_MGT  gen 263
    ip 10.210.6.40  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
    server smb
  vd root/0  22:28:42:67:1e:8a  gen 14781063  req OUA/34
    created 5299634s  gen 12690407  seen 1211753s  Guest  gen 437308
    ip 172.176.0.32  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'KillAri'  src dhcp
  vd root/0  a6:df:55:aa:21:bd  gen 15076685  req OUA/34
    created 3044771s  gen 13729918  seen 724805s  CORP WIRELESS  gen 442267
    ip 10.210.68.46  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:8b:2a:36  gen 4739731  req OUA/34
    created 54857385s  gen 746616  seen 22s  ENG_LANC  gen 233917
    ip 10.210.140.14  src arp
    os 'Windows'  src ssdp  id 1612  weight 128
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-ENGWKS-01'  src dns
  vd root/0  b4:b1:5a:0e:70:04  gen 14518455  req OHUSA/3e
    created 88407529s  gen 1226  seen 22s  ENG_LANC  gen 1077
    ip 10.210.140.35  src arp
  vd root/0  b4:b1:5a:0e:70:19  gen 14781546  req OHUSA/3e
    created 88407529s  gen 1227  seen 22s  ENG_LANC  gen 1080
    ip 10.210.140.25  src arp
  vd root/0  b4:b1:5a:0e:70:34  gen 14581682  req OHUSA/3e
    created 88407527s  gen 1238  seen 22s  ENG_LAND  gen 196273
    ip 10.210.144.25  src arp
  vd root/0  b4:b1:5a:0e:71:19  gen 14531329  req OHUSA/3e
    created 88407529s  gen 1223  seen 22s  ENG_LANC  gen 1074
    ip 10.210.140.37  src arp
  vd root/0  b4:b1:5a:0e:6f:9c  gen 14851480  req OHUSA/3e
    created 88407527s  gen 1232  seen 22s  ENG_LAND  gen 196269
    ip 10.210.144.37  src arp
  vd root/0  b4:b1:5a:0e:6f:a3  gen 14523860  req OHUSA/3e
    created 88407529s  gen 1221  seen 22s  ENG_LANC  gen 1071
    ip 10.210.140.36  src arp
  vd root/0  b4:b1:5a:0e:6f:bc  gen 15464080  req OHUSA/3e
    created 88407527s  gen 1236  seen 22s  ENG_LAND  gen 196271
    ip 10.210.144.35  src arp
  vd root/0  b4:b1:5a:0e:6f:c6  gen 14528071  req OHUSA/3e
    created 88407527s  gen 1233  seen 22s  ENG_LAND  gen 196270
    ip 10.210.144.36  src arp
  vd root/0  e4:30:22:67:23:39  gen 238707  req OHUSA/3e
    created 88407668s  gen 250  seen 7s  SECURITY_CAMERA  gen 119963
    ip 10.210.32.130  src mac
  vd root/0  56:17:ed:c6:66:86  gen 15000346  req OUA/34
    created 856014s  gen 15000340  seen 855650s  CORP WIRELESS  gen 441064
    ip 10.210.68.14  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S2 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'S22-Ultra-von-misel'  src dhcp
  vd root/0  6a:ce:64:e2:33:da  gen 15422008  req OUA/34
    created 1751433s  gen 14477331  seen 83412s  Guest  gen 448762
    ip 172.176.0.21  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  da:0a:d8:41:b4:18  gen 15419969  req OUA/34
    created 22217380s  gen 7048895  seen 87104s  Guest  gen 448720
    ip 172.176.0.40  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.0.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  4a:70:25:13:f1:a0  gen 15462581  req OUA/34
    created 9601118s  gen 11324003  seen 10411s  Guest  gen 449538
    ip 172.176.0.21  src mac
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '16'  src http  id 997  weight 230
    host 'Bill-s-S23'  src dhcp
  vd root/0  00:50:56:8b:81:e4  gen 4739732  req OUA/34
    created 54857385s  gen 746617  seen 22s  ENG_LAND  gen 233918
    ip 10.210.144.14  src arp
    os 'Windows'  src ssdp  id 1612  weight 128
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-ENGWKS-01'  src dns
  vd root/0  26:eb:17:f0:8a:7e  gen 14379439  req OUA/34
    created 2791375s  gen 13874393  seen 1896290s  CORP WIRELESS  gen 430239
    ip 10.210.68.51  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:8b:91:48  gen 1696  req OUA/34
    created 88407584s  gen 1141  seen 22s  VMWare_MGT  gen 471
    ip 10.210.6.34  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-SQL-01'  src mwbs
  vd root/0  06:4b:46:9f:4e:f8  gen 15458312  req OUA/34
    created 25407933s  gen 6100354  seen 18337s  CORP WIRELESS  gen 449455
    ip 10.210.68.78  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'SM-L705F'  src dhcp
  vd root/0  d4:76:a0:18:f7:8b  gen 1023  req 0
    created 88407605s  gen 1019  seen 23s  fortilink  gen 414
  vd root/0  00:50:56:8b:c5:5d  gen 746515  req OA/24
    created 88407668s  gen 56  seen 0s  ENG_SERVERS  gen 173090
    ip 10.210.4.14  src mac
    hardware vendor 'Microsoft'  src fortiguard  id 0  weight 213
    type 'Home & Office'  src fortiguard  id 0  weight 213
    family 'IP Phone'  src fortiguard  id 0  weight 213
    os 'Windows'  src fortiguard  id 0  weight 213
    hardware version 'Lync'  src fortiguard  id 0  weight 213
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-ENGWKS-01'  src mwbs
    user 'christopher.dodd'  src kerberos
  vd root/0  78:ac:44:13:ec:ec  gen 12430621  req OHUSA/3e
    created 88407644s  gen 919  seen 12s  ESXMGMT  gen 391451
    ip 10.210.8.27  src mac
  vd root/0  78:ac:44:13:f0:86  gen 11279825  req OHUSA/3e
    created 88407646s  gen 909  seen 12s  ESXMGMT  gen 358400
    ip 10.210.8.23  src mac
  vd root/0  78:ac:44:13:f5:96  gen 11277218  req OHUA/3c
    created 88407641s  gen 936  seen 22s  ESXMGMT  gen 358285
    ip 10.210.8.29  src mac
    os 'Fedora'  src dhcp  id 787  weight 128
  vd root/0  78:ac:44:13:fa:00  gen 217164  req HU/18
    created 88407604s  gen 1048  seen 22s  default  gen 110735
  vd root/0  78:ac:44:13:fa:1e  gen 11280585  req OHUSA/3e
    created 88407568s  gen 1168  seen 13s  ESXMGMT  gen 358452
    ip 10.210.8.25  src mac
  vd root/0  d4:76:a0:1b:de:36  gen 1531  req 0
    created 88407520s  gen 1531  seen 22s  fortilink  gen 789
  vd root/0  00:50:56:8b:dc:a2  gen 4739730  req OUA/34
    created 54857385s  gen 746615  seen 22s  ENG_LANB  gen 233916
    ip 10.210.136.14  src arp
    os 'Windows'  src ssdp  id 1612  weight 128
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-ENGWKS-01'  src dns
  vd root/0  78:ac:44:13:fb:96  gen 298507  req HU/18
    created 88407604s  gen 1052  seen 22s  default  gen 150265
  vd root/0  78:ac:44:13:fb:98  gen 298508  req HU/18
    created 64728965s  gen 236078  seen 22s  default  gen 150266
  vd root/0  78:ac:44:13:fb:b6  gen 12430006  req OHUSA/3e
    created 88407652s  gen 875  seen 21s  ESXMGMT  gen 391434
    ip 10.210.8.31  src mac
  vd root/0  78:ac:44:13:f9:fe  gen 335902  req HU/18
    created 70611942s  gen 164574  seen 22s  default  gen 159391
  vd root/0  00:50:56:8b:e7:bf  gen 8464  req OA/24
    created 88407663s  gen 601  seen 0s  VMWare_MGT  gen 262
    ip 10.210.6.41  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-DC02'  src mwbs
    user 'kburlakow'  src kerberos
  vd root/0  d4:76:a0:1b:ee:04  gen 1533  req 0
    created 88407520s  gen 1533  seen 20s  fortilink  gen 791
  vd root/0  64:b5:c6:55:aa:06  gen 14470200  req OHUSA/3e
    created 3837633s  gen 13308508  seen 1763201s  Guest  gen 431912
    ip 172.176.0.5  src arp
  vd root/0  3e:0e:83:0b:93:19  gen 15451885  req OUA/34
    created 30260556s  gen 4782085  seen 1850s  Guest  gen 449319
    ip 172.176.0.26  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    hardware version '14 Pro'  src dns  id 5005  weight 230
    software version '18.4.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  3a:62:4d:8e:d2:c7  gen 15411357  req OUA/34
    created 39937584s  gen 3043034  seen 109850s  CORP WIRELESS  gen 448527
    ip 10.210.68.65  src none
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '15'  src http  id 997  weight 230
    host 'Steve-s-S25-Ultra'  src dhcp
  vd root/0  4e:06:a2:56:7a:5a  gen 15420016  req OUA/34
    created 58751619s  gen 303513  seen 87141s  Guest  gen 448722
    ip 172.176.0.41  src arp
    hardware vendor 'Apple'  src dns  id 5005  weight 230
    type 'Phone'  src dns  id 5005  weight 230
    family 'iPhone'  src dns  id 5005  weight 230
    os 'iOS'  src dns  id 5005  weight 230
    hardware version '14 Pro'  src dns  id 5005  weight 230
    software version '18.0'  src http  id 905  weight 230
    host 'Radus-iPhone'  src dns
  vd root/0  28:39:26:9b:a8:df  gen 15467554  req OUA/34
    created 88372170s  gen 2734  seen 0s  Guest  gen 449626
    ip 172.176.0.27  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'LAPTOP-50CAD648'  src dhcp
  vd root/0  26:e9:90:78:29:5e  gen 15454108  req OUA/34
    created 40026338s  gen 3030645  seen 1824s  CORP WIRELESS  gen 449364
    ip 10.210.68.21  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '18.5.0'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:0f:e5:0c:f9:d8  gen 15291398  req OHUSA/3e
    created 1743355s  gen 14482276  seen 22s  SECURITY_CP  gen 432176
    ip 10.210.42.19  src mac
  vd root/0  00:0f:e5:0c:f9:da  gen 15293437  req OUSA/36
    created 88407528s  gen 1231  seen 21s  SECURITY_CP  gen 432370
    ip 10.210.42.22  src mac
    host 'MAC000FE5010000'  src dns
  vd root/0  00:0f:e5:0c:f9:dc  gen 15291399  req OUSA/36
    created 88407605s  gen 1034  seen 22s  SECURITY_CP  gen 433133
    ip 10.210.42.25  src mac
    host 'MAC000FE5010000'  src dns
  vd root/0  00:0f:e5:0c:f9:dd  gen 15291397  req OUSA/36
    created 88407527s  gen 1243  seen 21s  SECURITY_CP  gen 433107
    ip 10.210.42.28  src mac
    host 'MAC000FE5010000'  src dns
  vd root/0  00:0f:e5:0c:f9:e4  gen 14534021  req OUSA/36
    created 88407527s  gen 1242  seen 1654596s  SECURITY_CP  gen 196266
    ip 10.210.42.25  src none
    host 'MAC000FE5010000'  src dns
  vd root/0  f8:d0:27:2a:08:00  gen 15282262  req OUSA/36
    created 366742s  gen 15282260  seen 336411s  CORP WIRELESS  gen 446081
    ip 10.210.68.3  src arp
    host 'EPSON2A0800'  src dhcp
  vd root/0  0e:a0:3d:12:8e:39  gen 14374122  req OUA/34
    created 10733969s  gen 10971586  seen 1924442s  Guest  gen 430157
    ip 172.176.0.35  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S2 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Gabi-s-S22-Ultra'  src dhcp
  vd root/0  5e:3f:90:56:35:ff  gen 13824195  req OUA/34
    created 4325980s  gen 13096994  seen 2320052s  CORP WIRELESS  gen 420818
    ip 10.210.68.70  src arp
    hardware vendor 'Apple'  src dns  id 3122  weight 180
    type 'Tablet'  src dns  id 3122  weight 180
    family 'iPad'  src dns  id 3122  weight 180
    os 'iPadOS'  src dns  id 3122  weight 180
    host 'iPad'  src dhcp
  vd root/0  78:ac:44:1e:9b:b6  gen 11277397  req OHUSA/3e
    created 88407567s  gen 1170  seen 12s  ESXMGMT  gen 358302
    ip 10.210.8.21  src mac
  vd root/0  00:be:43:92:33:99  gen 10948968  req OUA/34
    created 88407656s  gen 853  seen 4s  CORP_WKS  gen 349959
    ip 10.210.64.20  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'D-ZRH11-OPS'  src dns
  vd root/0  c6:cf:07:88:70:51  gen 15421102  req OUA/34
    created 9409051s  gen 11394996  seen 63686s  Guest  gen 448749
    ip 172.176.0.43  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'Lenovo-Idea-Tab-Pro'  src dhcp
  vd root/0  00:1c:9e:01:73:80  gen 908  req OHUSA/3e
    created 88407646s  gen 907  seen 16s  Fire_Alarm  gen 374
    ip 192.168.3.2  src mac
  vd root/0  00:be:43:91:79:1f  gen 11205980  req OA/24
    created 88407664s  gen 593  seen 0s  SECURITY_CP  gen 356126
    ip 10.210.42.15  src tcp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'D-ZRH11-SEC01-1'  src mwbs
    user 'agim.januzi'  src kerberos
  vd root/0  00:be:43:91:78:cd  gen 11362192  req OA/24
    created 88407664s  gen 591  seen 0s  SECURITY_CP  gen 360589
    ip 10.210.42.14  src tcp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'D-ZRH11-SEC02-1'  src mwbs
    user 'octavian.solomes'  src kerberos
  vd root/0  00:80:a3:e3:06:74  gen 11075409  req OHUSA/3e
    created 52544269s  gen 1166137  seen 22s  ENG_LAND  gen 353279
    ip 10.210.144.30  src arp
  vd root/0  00:80:a3:e3:16:07  gen 11074814  req OHUSA/3e
    created 52544710s  gen 1166039  seen 12s  ENG_LANC  gen 353257
    ip 10.210.140.30  src arp
  vd root/0  2c:7b:a0:38:21:dd  gen 15355712  req OUA/34
    created 4464914s  gen 13040503  seen 221516s  Guest  gen 447498
    ip 172.176.0.15  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'ZRH-0D83ZUBJ3TK'  src dhcp
  vd root/0  36:1a:10:d9:0c:4c  gen 15464179  req OUA/34
    created 37484715s  gen 3386588  seen 47s  Guest  gen 449568
    ip 172.176.0.44  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.4'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  12:dd:e5:e8:10:02  gen 15336757  req OUA/34
    created 72297819s  gen 146285  seen 252189s  Guest  gen 447136
    ip 172.176.0.13  src arp
    hardware vendor 'Samsung'  src http  id 993  weight 255
    type 'Phone'  src http  id 993  weight 255
    family 'Galaxy'  src http  id 993  weight 255
    os 'Android'  src http  id 993  weight 255
    hardware version 'S'  src http  id 1094  weight 230
    software version '13'  src http  id 993  weight 255
    host 'Julie-s-S21'  src dhcp
  vd root/0  3a:57:ae:1e:09:1a  gen 15069237  req OUSA/36
    created 2615154s  gen 13973858  seen 732122s  Guest  gen 442122
    ip 172.176.0.19  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  3a:f1:7f:d0:9f:5a  gen 15194456  req OUA/34
    created 25933933s  gen 5949964  seen 525143s  CORP WIRELESS  gen 444426
    ip 10.210.68.49  src mac
    hardware vendor 'Samsung'  src dhcp  id 6704  weight 230
    type 'Phone'  src dhcp  id 6704  weight 230
    family 'Galaxy'  src dhcp  id 6704  weight 230
    os 'Android'  src dhcp  id 6704  weight 230
    hardware version 'Z Fold7'  src dhcp  id 6704  weight 230
    software version '16'  src dhcp  id 6704  weight 230
    host 'Michael-s-Z-Fold7'  src dhcp
  vd root/0  62:61:da:3c:ca:2f  gen 14585145  req OUSA/36
    created 1570653s  gen 14585144  seen 1570288s  CORP WIRELESS  gen 434045
    host 'iPad'  src dhcp
  vd root/0  3a:3a:9e:7a:66:eb  gen 15380007  req OUA/34
    created 42137424s  gen 2743625  seen 172240s  CORP WIRELESS  gen 447662
    ip 10.210.68.75  src mac
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '15'  src http  id 997  weight 230
    host 'To-S25-Ultra-tou-tes-DRIMIS'  src dhcp
  vd root/0  5a:3b:9b:1e:9e:bb  gen 15075990  req OHUSA/3e
    created 726272s  gen 15075983  seen 725706s  CORP WIRELESS  gen 442242
    ip 10.210.68.71  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
  vd root/0  3e:73:28:9f:ae:b2  gen 15450557  req OUA/34
    created 11866296s  gen 10535503  seen 23417s  Guest  gen 449284
    ip 172.176.0.22  src arp
    hardware vendor 'Samsung'  src http  id 979  weight 255
    type 'Phone'  src http  id 979  weight 255
    family 'Galaxy'  src http  id 979  weight 255
    os 'Android'  src http  id 979  weight 255
    hardware version 'A'  src http  id 1093  weight 230
    software version '14'  src http  id 979  weight 255
    host 'A34-de-vera'  src dhcp
  vd root/0  22:57:c7:9f:45:51  gen 14627211  req OUA/34
    created 1498497s  gen 14627192  seen 1497931s  CORP WIRELESS  gen 434737
    ip 10.210.68.14  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Steve-s-S25-Ultra'  src dhcp
  vd root/0  00:50:56:a3:00:2a  gen 1686040  req OUA/34
    created 88407668s  gen 142  seen 0s  VMWare_MGT  gen 59
    ip 10.210.6.220  src mac  ip6 ad2:6dc::  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-MEP-01'  src mwbs
  vd root/0  00:50:56:a3:00:89  gen 1698  req OUA/34
    created 88407663s  gen 624  seen 0s  VMWare_MGT  gen 269
    ip 10.210.6.94  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-GEN-MC'  src mwbs
  vd root/0  5e:20:28:d6:7b:66  gen 14547732  req OHUA/3c
    created 1635558s  gen 14547730  seen 1591211s  Guest  gen 433390
    ip 172.176.0.2  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '10'  src dhcp  id 191  weight 130
  vd root/0  00:50:56:a3:16:58  gen 1683  req OUA/34
    created 88407668s  gen 66  seen 4s  VMWare_MGT  gen 42
    ip 10.210.6.120  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 146
    type 'Server'  src fortiguard  id 0  weight 146
    family 'Virtual Machine'  src fortiguard  id 0  weight 146
    os 'Windows'  src fortiguard  id 0  weight 146
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 146
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-APP-FED'  src mwbs
  vd root/0  00:50:56:a3:12:e0  gen 15467355  req OHSA/2e
    created 32661202s  gen 4144798  seen 12s  ESXMGMT  gen 224057
    ip 10.210.8.20  src mac
    user 'svc-vmware-ro'  src kerberos
  vd root/0  00:50:56:a3:1a:62  gen 4186525  req OHUSA/3e
    created 32484684s  gen 4186525  seen 21s  ENG_SERVERS  gen 224635
  vd root/0  00:50:56:a3:1c:47  gen 14742987  req OUA/34
    created 88407662s  gen 637  seen 3s  VMWare_MGT  gen 83989
    ip 10.210.6.113  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-GEN-SQL-F'  src mwbs
  vd root/0  da:d0:35:eb:7e:71  gen 15451896  req OUA/34
    created 22131868s  gen 7075205  seen 2s  Guest  gen 449321
    ip 172.176.0.28  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '15'  src dhcp  id 6732  weight 230
    host 'Corrado-s-S25-Ultra'  src dhcp
  vd root/0  00:50:56:a3:1b:b1  gen 5451837  req OHUSA/3e
    created 88407657s  gen 806  seen 21s  ENG_LAND  gen 83995
    ip 10.210.144.11  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:1b:e3  gen 95097  req OUA/34
    created 88407668s  gen 85  seen 0s  VMWare_MGT  gen 51052
    ip 10.210.6.110  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 141
    type 'Server'  src fortiguard  id 0  weight 141
    family 'Virtual Machine'  src fortiguard  id 0  weight 141
    os 'Windows'  src fortiguard  id 0  weight 141
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 141
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-GEN-APP'  src mwbs
  vd root/0  00:50:56:a3:1e:c7  gen 14795616  req OUA/34
    created 88407668s  gen 102  seen 0s  VMWare_MGT  gen 138065
    ip 10.210.6.111  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 213
    type 'Server'  src fortiguard  id 0  weight 213
    family 'Virtual Machine'  src fortiguard  id 0  weight 213
    os 'Windows'  src fortiguard  id 0  weight 213
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 213
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-GEN-SQL'  src mwbs
  vd root/0  00:50:56:a3:21:96  gen 277205  req OHUSA/3e
    created 88407616s  gen 986  seen 6s  ENG_LANA  gen 137993
    ip 10.210.132.20  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:2c:3d  gen 162618  req OUA/34
    created 88407664s  gen 596  seen 0s  VMWare_MGT  gen 83993
    ip 10.210.6.100  src tcp
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-AUTH01'  src mwbs
  vd root/0  00:50:56:a3:2e:0f  gen 45419  req OHA/2c
    created 88407662s  gen 627  seen 0s  ENG_SERVERS  gen 270
    ip 10.210.4.32  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src ssh  id 1613  weight 128
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    user 'puppetsso'  src kerberos
  vd root/0  00:50:56:a3:2f:57  gen 10261185  req OHUSA/3e
    created 88407657s  gen 804  seen 21s  ENG_LANC  gen 83998
    ip 10.210.140.11  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:31:43  gen 51328  req OHA/2c
    created 88407666s  gen 544  seen 2s  ENG_SERVERS  gen 251
    ip 10.210.4.25  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src http  id 1403  weight 100
    os 'Debian'  src http  id 1403  weight 100
    user 'puppetsso'  src kerberos
  vd root/0  ec:8e:77:49:49:27  gen 14934166  req OUA/34
    created 5201615s  gen 12730985  seen 969324s  CORP WIRELESS  gen 440001
    ip 10.210.68.24  src arp
    os 'Windows'  src http  id 6752  weight 130
    software version '11 Enterprise'  src http  id 6752  weight 130
    host 'dinm5CG5062LL9'  src dhcp
  vd root/0  00:50:56:a3:35:4b  gen 3418068  req OUA/34
    created 37257535s  gen 3417858  seen 0s  VMWare_MGT  gen 215144
    ip 10.210.6.114  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'WIN-3ECGEUCC34S'  src dhcp
  vd root/0  00:50:56:a3:32:e0  gen 273071  req OHUSA/3e
    created 88407616s  gen 989  seen 22s  ENG_LANB  gen 137990
    ip 10.210.136.20  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:35:bd  gen 162613  req OUA/34
    created 88407668s  gen 52  seen 0s  VMWare_MGT  gen 83992
    ip 10.210.6.51  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 137
    type 'Server'  src fortiguard  id 0  weight 137
    family 'Virtual Machine'  src fortiguard  id 0  weight 137
    os 'Windows'  src fortiguard  id 0  weight 137
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 137
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-BC'  src mwbs
  vd root/0  00:50:56:a3:38:fb  gen 1625  req OUA/34
    created 88407663s  gen 622  seen 7s  VMWare_MGT  gen 268
    ip 10.210.6.115  src tcp
    hardware vendor 'VMware'  src mac  id 0  weight 120
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH1-GEN-WTN01'  src mwbs
  vd root/0  38:b4:d3:e1:0b:62  gen 3302238  req OUSA/36
    created 88407655s  gen 863  seen 22s  CORP WIRELESS  gen 354
    ip 10.210.68.63  src mac
    host 'bosch-dishwasher-011070523016001694'  src dns
  vd root/0  6c:3c:8c:6d:c6:d4  gen 1657424  req HU/18
    created 80953967s  gen 69863  seen 22s  Nessus  gen 196296
  vd root/0  00:50:56:a3:57:2c  gen 4186524  req OHUSA/3e
    created 32484684s  gen 4186524  seen 21s  ENG_SERVERS  gen 224634
  vd root/0  28:0c:50:83:32:f4  gen 15151712  req OHUSA/3e
    created 601584s  gen 15151712  seen 601284s  CORP WIRELESS  gen 443637
  vd root/0  00:50:56:a3:5b:7c  gen 62577  req OHA/2c
    created 88407662s  gen 645  seen 0s  ENG_SERVERS  gen 278
    ip 10.210.4.17  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src http  id 1403  weight 100
    os 'Debian'  src http  id 1403  weight 100
    user 'puppetsso'  src kerberos
  vd root/0  00:50:56:a3:5c:ef  gen 9190547  req OHUSA/3e
    created 88407616s  gen 991  seen 0s  ENG_LANC  gen 137989
    ip 10.210.140.20  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:6b:63  gen 4186899  req OUA/34
    created 32484686s  gen 4186521  seen 0s  VMWare_MGT  gen 224633
    ip 10.210.6.70  src arp
    os 'Ubuntu'  src dhcp  id 3255  weight 128
    host 'tenable-tf4zu1y8'  src dhcp
  vd root/0  00:50:56:a3:6a:91  gen 283371  req OHUSA/3e
    created 88407657s  gen 810  seen 9s  ENG_LANA  gen 83997
    ip 10.210.132.11  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:6d:70  gen 14446752  req OHA/2c
    created 88407662s  gen 642  seen 1s  ENG_SERVERS  gen 150942
    ip 10.210.4.30  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src ssh  id 1613  weight 128
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    user 'puppetsso'  src kerberos
  vd root/0  00:50:56:a3:6e:7e  gen 162634  req OHUSA/3e
    created 88407657s  gen 807  seen 22s  ENG_LANB  gen 83996
    ip 10.210.136.11  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  98:59:7a:f2:23:5d  gen 14237321  req OUA/34
    created 2165895s  gen 14237310  seen 2162245s  CORP WIRELESS  gen 427921
    ip 10.210.68.67  src arp
    type 'Desktop'  src dhcp  id 6502  weight 130
    os 'Windows'  src dhcp  id 6502  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'DESKTOP-AGFK3J5'  src dhcp
  vd root/0  7c:c2:55:2b:0b:ca  gen 1657418  req OHUSA/3e
    created 67221631s  gen 204068  seen 22s  WIRELESS_APs  gen 196290
    ip 10.210.215.6  src arp
  vd root/0  00:50:56:a3:82:32  gen 3738772  req OUA/34
    created 34980658s  gen 3738746  seen 11s  VMWare_MGT  gen 219772
    ip 10.210.6.75  src arp
    os 'Ubuntu'  src dhcp  id 3255  weight 128
    host 'adlumin-forwarder'  src dhcp
  vd root/0  00:50:56:a3:96:e8  gen 1558  req OUA/34
    created 88407668s  gen 69  seen 0s  VMWare_MGT  gen 43
    ip 10.210.6.112  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 183
    type 'Server'  src fortiguard  id 0  weight 183
    family 'Virtual Machine'  src fortiguard  id 0  weight 183
    os 'Windows'  src fortiguard  id 0  weight 183
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 183
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-GEN-APP-F'  src mwbs
  vd root/0  00:50:56:a3:9b:b4  gen 162612  req OUA/34
    created 88407668s  gen 54  seen 3s  VMWare_MGT  gen 83991
    ip 10.210.6.52  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 234
    type 'Server'  src fortiguard  id 0  weight 234
    family 'Virtual Machine'  src fortiguard  id 0  weight 234
    os 'Windows'  src fortiguard  id 0  weight 234
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 234
    software version '10'  src http  id 1444  weight 130
    host 'ZRH11-TRAKA'  src mwbs
  vd root/0  00:50:56:a3:9c:a8  gen 2731  req OHUA/3c
    created 88407662s  gen 631  seen 0s  ENG_SERVERS  gen 272
    ip 10.210.4.45  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src ssh  id 1613  weight 128
    os 'Ubuntu'  src ssh  id 1613  weight 128
  vd root/0  00:50:56:a3:9e:89  gen 95099  req OUA/34
    created 88407668s  gen 87  seen 22s  SECURITY_CAMERA  gen 51053
    ip 10.210.32.5  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 129
    type 'Server'  src fortiguard  id 0  weight 129
    family 'Virtual Machine'  src fortiguard  id 0  weight 129
    os 'Windows'  src fortiguard  id 0  weight 129
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 129
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'ZRH11-GEN-APP'  src mwbs
  vd root/0  00:50:56:a3:b8:68  gen 5645571  req OHUSA/3e
    created 88407616s  gen 985  seen 22s  ENG_LAND  gen 137992
    ip 10.210.144.20  src arp
    hardware vendor 'VMware'  src mac  id 0  weight 120
  vd root/0  00:50:56:a3:c0:57  gen 3471259  req OA/24
    created 36873215s  gen 3470700  seen 0s  ENG_SERVERS  gen 215749
    ip 10.210.4.15  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'VANTADM-J01DAJV'  src dhcp
    user 'puppetsso'  src kerberos
  vd root/0  00:50:56:a3:ca:8a  gen 4186523  req OHUSA/3e
    created 32484686s  gen 4186520  seen 22s  ENG_SERVERS  gen 224632
    ip 192.168.3.3  src arp
  vd root/0  00:0a:5c:81:9b:9a  gen 15442023  req OHUSA/3e
    created 88407498s  gen 1622  seen 22s  ENG_LANA  gen 195540
    ip 10.210.132.92  src arp
  vd root/0  00:50:56:a3:e3:34  gen 14446759  req OHA/2c
    created 88407662s  gen 639  seen 0s  ENG_SERVERS  gen 274
    ip 10.210.4.31  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src ssh  id 1613  weight 128
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    user 'puppetsso'  src kerberos
  vd root/0  02:2b:30:ac:36:7e  gen 15430730  req OUA/34
    created 18544820s  gen 8227557  seen 34024s  Guest  gen 448933
    ip 172.176.0.3  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.7'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:a3:e6:71  gen 1702  req OUA/34
    created 88407669s  gen 38  seen 10s  VMWare_MGT  gen 29
    ip 10.210.6.121  src mac
    hardware vendor 'VMware'  src fortiguard  id 0  weight 134
    type 'Server'  src fortiguard  id 0  weight 134
    family 'Virtual Machine'  src fortiguard  id 0  weight 134
    os 'Windows'  src fortiguard  id 0  weight 134
    hardware version 'Virtual Machine'  src fortiguard  id 0  weight 134
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-SQL-FED'  src mwbs
  vd root/0  00:50:56:a3:fb:cb  gen 50682  req OHA/2c
    created 88407666s  gen 533  seen 0s  ENG_SERVERS  gen 246
    ip 10.210.4.24  src mac
    hardware vendor 'VMware'  src mac  id 0  weight 120
    type 'Computer'  src http  id 1403  weight 100
    os 'Debian'  src http  id 1403  weight 100
    user 'puppetsso'  src kerberos
  vd root/0  b6:f8:0d:e9:3b:5c  gen 15229599  req OUA/34
    created 465780s  gen 15229597  seen 465036s  CORP WIRELESS  gen 445015
    ip 10.210.68.83  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S3 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'I-s-S23-Ultra'  src dhcp
  vd root/0  00:0a:5c:81:d3:0f  gen 15418761  req OHUSA/3e
    created 88407605s  gen 1017  seen 23s  ENG_LANA  gen 272542
    ip 10.210.132.40  src arp
  vd root/0  00:0a:5c:81:d3:18  gen 15442048  req OHUSA/3e
    created 88407522s  gen 1439  seen 20s  ENG_LANB  gen 214826
    ip 10.210.136.27  src arp
  vd root/0  00:0a:5c:81:d2:b5  gen 15343723  req OHUSA/3e
    created 88407521s  gen 1452  seen 22s  ENG_LANA  gen 214825
    ip 10.210.132.90  src arp
  vd root/0  00:0a:5c:81:d2:b7  gen 15343726  req OHUSA/3e
    created 88407520s  gen 1545  seen 22s  ENG_LANB  gen 195588
    ip 10.210.136.90  src arp
  vd root/0  00:0a:5c:81:d2:b8  gen 15434603  req OHUSA/3e
    created 88407521s  gen 1459  seen 19s  ENG_LANB  gen 195572
    ip 10.210.136.91  src arp
  vd root/0  00:0a:5c:81:d2:cc  gen 15432803  req OHUSA/3e
    created 88407522s  gen 1423  seen 19s  ENG_LANB  gen 214822
    ip 10.210.136.28  src arp
  vd root/0  00:0a:5c:81:d2:cd  gen 15440106  req OHUSA/3e
    created 88407605s  gen 1014  seen 23s  ENG_LANA  gen 272539
    ip 10.210.132.38  src arp
  vd root/0  00:0a:5c:81:d2:d0  gen 15384654  req OHUSA/3e
    created 88407500s  gen 1618  seen 18s  ENG_LANA  gen 195679
    ip 10.210.132.91  src arp
  vd root/0  00:0a:5c:81:d2:d1  gen 15242752  req OHUSA/3e
    created 88407522s  gen 1420  seen 19s  ENG_LANB  gen 195743
    ip 10.210.136.30  src arp
  vd root/0  00:0a:5c:81:d2:d3  gen 15440071  req OHUSA/3e
    created 88407605s  gen 1016  seen 23s  ENG_LANA  gen 272541
    ip 10.210.132.39  src arp
  vd root/0  00:0a:5c:81:d2:d5  gen 15242774  req OHUSA/3e
    created 88407522s  gen 1445  seen 18s  ENG_LANA  gen 195815
    ip 10.210.132.27  src arp
  vd root/0  00:0a:5c:81:d2:dd  gen 15442020  req OHUSA/3e
    created 88407605s  gen 1018  seen 23s  ENG_LANB  gen 8902
    ip 10.210.136.40  src arp
  vd root/0  ee:2c:bb:b9:74:4c  gen 15250078  req OUA/34
    created 429402s  gen 15250076  seen 429392s  Guest  gen 445465
    ip 172.176.0.32  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'S24-korisnika-Marko'  src dhcp
  vd root/0  00:0a:5c:81:e6:05  gen 15369612  req OHUSA/3e
    created 88407605s  gen 1030  seen 23s  ENG_LANA  gen 7883
    ip 10.210.132.36  src arp
  vd root/0  00:0a:5c:81:e6:0d  gen 15418753  req OHUSA/3e
    created 88407522s  gen 1425  seen 19s  ENG_LANB  gen 195748
    ip 10.210.136.29  src arp
  vd root/0  10:3d:1c:e7:b6:e8  gen 15232294  req OUA/34
    created 461026s  gen 15232290  seen 459647s  Guest  gen 445082
    ip 172.176.0.32  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'AMP-CL81549'  src dhcp
  vd root/0  2c:ea:7f:9e:20:c6  gen 229693  req OUA/34
    created 88378996s  gen 2620  seen 21s  SECURITY_NVR  gen 116367
    ip 10.210.44.73  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-FKRQMF3'  src dhcp
  vd root/0  00:0a:5c:81:e6:6e  gen 15442028  req OHUSA/3e
    created 88407522s  gen 1414  seen 18s  ENG_LANA  gen 195803
    ip 10.210.132.28  src arp
  vd root/0  2c:ea:7f:9e:20:cc  gen 15467635  req OA/24
    created 88407668s  gen 140  seen 2s  SECURITY_NVR  gen 370145
    ip 10.210.44.27  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR02'  src mwbs
    user 's-rdenny'  src kerberos
  vd root/0  2c:ea:7f:9e:20:cd  gen 12450585  req OA/24
    created 62400604s  gen 262469  seen 5s  SECURITY_NVR  gen 370147
    ip 10.210.44.18  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'WIN-2C6M5M0431R'  src dhcp
    user 't-rarellano'  src kerberos
  vd root/0  00:0a:5c:81:e6:74  gen 15434599  req OHUSA/3e
    created 88407605s  gen 1021  seen 23s  ENG_LANB  gen 8925
    ip 10.210.136.39  src arp
  vd root/0  00:0a:5c:81:e6:76  gen 15220928  req OHUSA/3e
    created 88407605s  gen 1022  seen 23s  ENG_LANB  gen 214824
    ip 10.210.136.38  src arp
  vd root/0  00:0a:5c:81:e6:78  gen 15418760  req OHUSA/3e
    created 88407522s  gen 1415  seen 18s  ENG_LANA  gen 195804
    ip 10.210.132.30  src arp
  vd root/0  00:0a:5c:81:e6:84  gen 15434600  req OHUSA/3e
    created 88407605s  gen 1027  seen 23s  ENG_LANA  gen 7946
    ip 10.210.132.37  src arp
  vd root/0  00:0a:5c:81:e6:89  gen 15436492  req OHUSA/3e
    created 88407605s  gen 1009  seen 23s  ENG_LANB  gen 7855
    ip 10.210.136.35  src arp
  vd root/0  00:0a:5c:81:e6:8a  gen 15440105  req OHUSA/3e
    created 88407605s  gen 1028  seen 23s  ENG_LANA  gen 7833
    ip 10.210.132.35  src arp
  vd root/0  00:0a:5c:81:e6:8f  gen 15283835  req OHUSA/3e
    created 88407522s  gen 1447  seen 18s  ENG_LANA  gen 195817
    ip 10.210.132.26  src arp
  vd root/0  00:0a:5c:81:e6:90  gen 15411734  req OHUSA/3e
    created 88407605s  gen 1010  seen 23s  ENG_LANB  gen 7920
    ip 10.210.136.36  src arp
  vd root/0  00:0a:5c:81:e6:95  gen 15330341  req OHUSA/3e
    created 88407522s  gen 1419  seen 18s  ENG_LANA  gen 195807
    ip 10.210.132.29  src arp
  vd root/0  00:0a:5c:81:e6:9d  gen 15440089  req OHUSA/3e
    created 88407522s  gen 1448  seen 18s  ENG_LANA  gen 195818
    ip 10.210.132.25  src arp
  vd root/0  00:0a:5c:81:e5:e6  gen 15145079  req OHUSA/3e
    created 88407522s  gen 1436  seen 20s  ENG_LANB  gen 195767
    ip 10.210.136.26  src arp
  vd root/0  00:0a:5c:81:e5:e9  gen 15411733  req OHUSA/3e
    created 88407605s  gen 1011  seen 23s  ENG_LANB  gen 214823
    ip 10.210.136.37  src arp
  vd root/0  00:0a:5c:81:e5:f1  gen 15432802  req OHUSA/3e
    created 88407522s  gen 1441  seen 20s  ENG_LANB  gen 195771
    ip 10.210.136.25  src arp
  vd root/0  2c:ea:7f:9e:25:de  gen 262436  req OUA/34
    created 88377737s  gen 2649  seen 22s  SECURITY_NVR  gen 133057
    ip 10.210.44.71  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-CKRQMF3'  src dhcp
  vd root/0  2c:ea:7f:9e:25:e4  gen 11721979  req OA/24
    created 88407667s  gen 514  seen 22s  SECURITY_NVR  gen 370387
    ip 10.210.44.14  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01    '  src kerberos
    user 'sd-hkraiem'  src kerberos
  vd root/0  2c:ea:7f:9e:25:e5  gen 15467638  req OA/24
    created 88407667s  gen 513  seen 0s  SECURITY_NVR  gen 370386
    ip 10.210.44.14  src none
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01'  src mwbs
    user 'sd-hkraiem'  src kerberos
  vd root/0  84:b1:e2:6f:0d:96  gen 15423657  req OUA/34
    created 4691607s  gen 12946057  seen 87884s  Guest  gen 448793
    ip 172.176.0.25  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'STS37-JF'  src dhcp
  vd root/0  2c:ea:7f:9e:36:4b  gen 262432  req OUA/34
    created 88377835s  gen 2647  seen 5s  SECURITY_NVR  gen 133055
    ip 10.210.44.70  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-8KRQMF3'  src dhcp
  vd root/0  2c:ea:7f:9e:36:51  gen 12843488  req OA/24
    created 88407667s  gen 509  seen 17s  SECURITY_NVR  gen 400326
    ip 10.210.44.12  src tcp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR04'  src mwbs
    user 't-rarellano'  src kerberos
  vd root/0  2c:ea:7f:9e:36:52  gen 15467622  req OA/24
    created 88407669s  gen 48  seen 0s  SECURITY_NVR  gen 150874
    ip 10.210.44.22  src none
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR04'  src mwbs
    user 'ps-tziller'  src kerberos
  vd root/0  2c:ea:7f:9e:37:7b  gen 229694  req 0
    created 88378888s  gen 2624  seen 2s  SECURITY_NVR  gen 116368
    host 'iDRAC-7KRQMF3'  src dhcp
  vd root/0  2c:ea:7f:9e:37:81  gen 11704785  req OA/24
    created 88407668s  gen 160  seen 21s  SECURITY_NVR  gen 369639
    ip 10.210.44.16  src tcp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR03'  src mwbs
    user 'tziller'  src kerberos
  vd root/0  2c:ea:7f:9e:37:82  gen 15467628  req OA/24
    created 88407667s  gen 406  seen 14s  SECURITY_NVR  gen 369637
    ip 10.210.44.26  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR03'  src dns
    user 'ps-tziller'  src kerberos
  vd root/0  76:e3:93:21:8e:95  gen 15450299  req OUA/34
    created 11866859s  gen 10535341  seen 21981s  Guest  gen 449277
    ip 172.176.0.16  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S4 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'S24-Ultra-de-vera'  src dhcp
  vd root/0  be:ee:8f:0d:f9:3e  gen 15423085  req OUA/34
    created 14966690s  gen 9487103  seen 88971s  Guest  gen 448784
    ip 172.176.0.12  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.4.0'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  3e:d8:48:61:ba:90  gen 14926631  req OUA/34
    created 1068308s  gen 14876853  seen 954131s  CORP WIRELESS  gen 439863
    ip 10.210.68.50  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'A52s-5G'  src dhcp  id 182  weight 232
    software version '14'  src dhcp  id 133  weight 255
    host 'Galaxy-A52s-5G'  src dhcp
  vd root/0  b2:4e:a5:57:8a:21  gen 15245991  req OUA/34
    created 11346781s  gen 10749574  seen 436632s  CORP WIRELESS  gen 445386
    ip 10.210.68.44  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S2 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Bogdan-s-S22-Ultra'  src dhcp
  vd root/0  dc:05:75:05:94:d3  gen 3884939  req OHUSA/3e
    created 88407529s  gen 1222  seen 22s  ENG_LANC  gen 1072
    ip 10.210.140.26  src arp
  vd root/0  66:3d:bd:01:4b:92  gen 15465456  req OUA/34
    created 4869195s  gen 12870472  seen 2847s  Guest  gen 449591
    ip 172.176.0.29  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.7'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  dc:05:75:05:b9:9c  gen 7321053  req OHUSA/3e
    created 88407527s  gen 1237  seen 22s  ENG_LAND  gen 196272
    ip 10.210.144.26  src arp
  vd root/0  00:0e:be:0c:14:ad  gen 11914290  req OHUSA/3e
    created 88407522s  gen 1410  seen 19s  ENG_LANB  gen 196060
    ip 10.210.136.200  src arp
  vd root/0  00:0e:be:0c:14:ae  gen 1655126  req OHUSA/3e
    created 88407522s  gen 1358  seen 1821647s  ENG_LANA  gen 196057
    ip 10.210.132.245  src arp
  vd root/0  0c:bf:15:02:08:4a  gen 12359020  req OUA/34
    created 88407662s  gen 644  seen 20s  SECURITY_CP  gen 389458
    ip 10.210.42.29  src arp
    os 'Windows'  src dhcp  id 848  weight 128
    host 'SCL0CBF1502084A'  src dhcp
  vd root/0  0c:bf:15:02:08:60  gen 2419  req OUA/34
    created 88407662s  gen 630  seen 2s  SECURITY_CP  gen 271
    ip 10.210.42.26  src arp
    os 'Windows'  src dhcp  id 848  weight 128
    host 'SCL0CBF15020860'  src dhcp
  vd root/0  0c:bf:15:02:07:8c  gen 2417  req OUA/34
    created 88407666s  gen 540  seen 21s  SECURITY_CP  gen 249
    ip 10.210.42.23  src arp
    os 'Windows'  src dhcp  id 848  weight 128
    host 'SCL0CBF1502078C'  src dhcp
  vd root/0  00:0a:75:1f:df:07  gen 13860588  req OHUSA/3e
    created 88407520s  gen 1537  seen 22s  ENG_LAND  gen 194984
    ip 10.210.144.60  src arp
  vd root/0  00:0a:75:1f:df:0e  gen 15152996  req OHUSA/3e
    created 88407520s  gen 1534  seen 22s  ENG_LANC  gen 196661
    ip 10.210.140.65  src arp
  vd root/0  0c:bf:15:02:07:ea  gen 2416  req OUA/34
    created 88407664s  gen 590  seen 3s  SECURITY_CP  gen 257
    ip 10.210.42.20  src arp
    os 'Windows'  src dhcp  id 848  weight 128
    host 'SCL0CBF150207EA'  src dhcp
  vd root/0  00:0a:75:1f:df:2c  gen 15253053  req OHUSA/3e
    created 88407520s  gen 1532  seen 22s  ENG_LANC  gen 196308
    ip 165.26.78.148  src mac
  vd root/0  00:0a:75:1f:df:69  gen 13222302  req OHUSA/3e
    created 88407520s  gen 1536  seen 22s  ENG_LAND  gen 191690
    ip 10.210.144.65  src arp
  vd root/0  00:0a:75:1f:de:d3  gen 15251426  req OHUSA/3e
    created 88407520s  gen 1539  seen 22s  ENG_LANC  gen 196311
    ip 10.210.140.55  src arp
  vd root/0  0c:bf:15:02:11:ac  gen 15467338  req OUA/34
    created 4165696s  gen 13164928  seen 262s  SECURITY_CP  gen 449625
    ip 10.210.42.21  src arp
    os 'Windows'  src dhcp  id 848  weight 128
    host 'SCL0CBF150211AC'  src dhcp
  vd root/0  82:9d:48:98:f3:96  gen 15075854  req OUA/34
    created 726489s  gen 15075851  seen 725406s  CORP WIRELESS  gen 442237
    ip 10.210.68.48  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:0e:be:0a:ec:0c  gen 1655099  req OHUSA/3e
    created 88407521s  gen 1449  seen 372021s  ENG_LANA  gen 196045
    ip 10.210.132.249  src arp
  vd root/0  00:0e:be:0a:ea:97  gen 14479696  req OHUSA/3e
    created 88407522s  gen 1377  seen 1217984s  ENG_LANA  gen 196050
    ip 10.210.132.246  src arp
  vd root/0  00:0e:be:0a:ea:a0  gen 1655101  req OHUSA/3e
    created 88407504s  gen 1589  seen 631864s  ENG_LANA  gen 196047
    ip 10.210.132.248  src arp
  vd root/0  00:0a:f5:95:52:03  gen 14943922  req OHUA/3c
    created 1223596s  gen 14789013  seen 952931s  CORP WIRELESS  gen 440199
    ip 10.210.68.51  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '13'  src dhcp  id 191  weight 130
  vd root/0  00:0a:5c:91:26:05  gen 11996806  req OHUSA/3e
    created 88407527s  gen 1248  seen 11s  ENG_LANB  gen 508
    ip 10.210.136.97  src arp
  vd root/0  20:bb:c6:0f:48:1d  gen 936928  req OHUSA/3e
    created 88407524s  gen 1262  seen 18s  ENG_LANC  gen 520
    ip 10.210.140.105  src arp
  vd root/0  20:bb:c6:0f:48:1e  gen 1655197  req OHUSA/3e
    created 88407524s  gen 1270  seen 20s  ENG_LANC  gen 196074
  vd root/0  16:f0:f3:f1:ea:bf  gen 14386498  req OUSA/36
    created 1917341s  gen 14379440  seen 1896290s  CORP WIRELESS  gen 430398
    ip 10.210.68.62  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  ce:9f:d8:d0:3b:ca  gen 15211887  req OUA/34
    created 36383570s  gen 3541427  seen 466991s  Guest  gen 444712
    ip 172.176.0.13  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '17.5.1'  src http  id 902  weight 230
    host 'Africcii'  src dns
  vd root/0  00:0a:5c:91:54:53  gen 11994853  req OHUSA/3e
    created 88407526s  gen 1250  seen 11s  ENG_LANB  gen 196291
    ip 10.210.136.96  src arp
  vd root/0  00:0a:5c:91:56:56  gen 11994832  req OHUSA/3e
    created 88407526s  gen 1251  seen 11s  ENG_LANB  gen 196292
    ip 10.210.136.95  src arp
  vd root/0  56:ec:c1:6b:2b:17  gen 15270981  req OUA/34
    created 2202861s  gen 14216451  seen 388286s  Guest  gen 445833
    ip 172.176.0.3  src arp
    hardware vendor 'Samsung'  src http  id 979  weight 255
    type 'Phone'  src http  id 979  weight 255
    family 'Galaxy'  src http  id 979  weight 255
    os 'Android'  src http  id 979  weight 255
    hardware version 'A'  src http  id 1093  weight 230
    software version '16'  src http  id 979  weight 255
    host 'A56-von-Akif'  src dhcp
  vd root/0  b6:2c:2a:de:79:bb  gen 15464776  req OUA/34
    created 69928693s  gen 172662  seen 23s  Guest  gen 449579
    ip 172.176.0.4  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'S24-Ultra'  src dhcp  id 182  weight 232
    software version '14'  src dhcp  id 133  weight 255
    host 'Galaxy-S24-Ultra'  src dhcp
  vd root/0  ea:4f:8b:35:c0:a4  gen 15454793  req OUA/34
    created 4344684s  gen 13089282  seen 25543s  CORP WIRELESS  gen 449381
    ip 10.210.68.10  src mac
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S1 Ultra'  src dhcp  id 6732  weight 230
    software version '15'  src dhcp  id 6732  weight 230
    host 'Angie-s-S21-Ultra'  src dhcp
  vd root/0  2a:fd:77:65:ae:b5  gen 15008678  req OUA/34
    created 2507140s  gen 14037430  seen 841377s  Guest  gen 441219
    ip 172.176.0.11  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '15'  src dhcp  id 191  weight 130
    host 'Nothing-phone-1'  src dhcp
  vd root/0  f6:97:1b:5a:d8:38  gen 15392326  req OUA/34
    created 35799249s  gen 3621393  seen 121219s  Guest  gen 448157
    ip 172.176.0.21  src arp
    hardware vendor 'Apple'  src dhcp  id 3847  weight 230
    type 'Computer'  src dhcp  id 3847  weight 230
    family 'Mac'  src dhcp  id 3847  weight 230
    os 'macOS'  src dhcp  id 3847  weight 230
    hardware version 'MacBook Pro'  src dns  id 2654  weight 150
    software version '10.15.7'  src http  id 1883  weight 220
    host 'Ronaks-MacBook-Pro'  src dns
  vd root/0  5e:82:cc:24:b2:10  gen 14546213  req OUA/34
    created 1742632s  gen 14482692  seen 1636525s  Guest  gen 433361
    ip 172.176.0.37  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  00:0a:5c:90:f8:25  gen 11979609  req OHUSA/3e
    created 88407527s  gen 1246  seen 11s  ENG_LANB  gen 196283
    ip 10.210.136.98  src arp
  vd root/0  d2:86:29:c1:cb:e9  gen 15467298  req OUA/34
    created 5707698s  gen 12522718  seen 11s  Guest  gen 449623
    ip 172.176.0.3  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '16'  src http  id 997  weight 230
    host 'SM-L500'  src dhcp
  vd root/0  0e:d1:4b:9a:48:4c  gen 15276528  req OUA/34
    created 9154326s  gen 11460998  seen 377555s  Guest  gen 445956
    ip 172.176.0.29  src arp
    hardware vendor 'Apple'  src dhcp  id 2675  weight 180
    type 'Phone'  src dhcp  id 2675  weight 180
    family 'iPhone'  src dhcp  id 2675  weight 180
    os 'iOS'  src dhcp  id 2675  weight 180
    host 'iPhone'  src dhcp
  vd root/0  0e:59:0e:d4:12:53  gen 15275792  req OHUSA/3e
    created 464055s  gen 15230583  seen 378445s  CORP WIRELESS  gen 445934
  vd root/0  30:05:05:3e:d4:42  gen 15410746  req OA/24
    created 74244245s  gen 130054  seen 85531s  CORP WIRELESS  gen 448504
    ip 10.210.68.27  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'D1BM69Y3'  src dhcp
    user 'Adrian.Huppin'  src kerberos
  vd root/0  00:0a:75:32:5e:fd  gen 14197306  req OHUSA/3e
    created 88407520s  gen 1535  seen 22s  ENG_LAND  gen 178963
    ip 10.210.144.55  src arp
  vd root/0  2a:e4:60:a6:dc:68  gen 15450825  req OUA/34
    created 9787082s  gen 11268087  seen 3155s  Guest  gen 449288
    ip 172.176.0.25  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  36:e1:16:e4:4e:fe  gen 15459432  req OUA/34
    created 16707392s  gen 8859687  seen 13373s  Guest  gen 449476
    ip 172.176.0.6  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '16'  src http  id 997  weight 230
    host 'NabucoGalaxy22'  src dhcp
  vd root/0  02:c9:26:5a:f5:35  gen 15456660  req OUA/34
    created 5285250s  gen 12696450  seen 22438s  Guest  gen 449412
    ip 172.176.0.31  src arp
    hardware vendor 'Apple'  src dhcp  id 2675  weight 180
    type 'Phone'  src dhcp  id 2675  weight 180
    family 'iPhone'  src dhcp  id 2675  weight 180
    os 'iOS'  src dhcp  id 2675  weight 180
    host 'iPhone'  src dhcp
  vd root/0  ca:1e:46:a3:0f:85  gen 15234057  req OUA/34
    created 28882418s  gen 5157138  seen 432610s  CORP WIRELESS  gen 445083
    ip 10.210.68.60  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  bc:03:58:5e:b3:c5  gen 15465120  req OA/24
    created 68975908s  gen 183600  seen 1s  CORP WIRELESS  gen 449588
    ip 10.210.68.19  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'D38H5GY3'  src dhcp
    user 'adrian.stoian'  src kerberos
  vd root/0  46:bb:a2:04:f5:96  gen 15416506  req OUA/34
    created 8614518s  gen 11657232  seen 101348s  Guest  gen 448652
    ip 172.176.0.33  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'S25-Ultra-korisnika-mira'  src dhcp
  vd root/0  94:b6:09:0c:2c:63  gen 14538219  req OUA/34
    created 1650290s  gen 14538214  seen 1636533s  Guest  gen 433200
    ip 172.176.0.42  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'Ciaran_Keyes'  src dhcp
  vd root/0  1a:70:63:b1:03:d0  gen 14525917  req OUA/34
    created 13884064s  gen 9798427  seen 1654916s  Guest  gen 432931
    ip 172.176.0.23  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  9c:50:d1:b6:51:eb  gen 15396090  req OUA/34
    created 88403571s  gen 1810  seen 22s  CORP WIRELESS  gen 448025
    ip 10.210.68.8  src tcp
    os 'Android'  src dhcp  id 191  weight 130
    software version '6.0.1'  src dhcp  id 191  weight 130
    host 'android-eec08cdcdbab458'  src dhcp
  vd root/0  5e:c4:8e:1e:5c:c5  gen 15467577  req OUA/34
    created 9695022s  gen 11290590  seen 22s  CORP WIRELESS  gen 449631
    ip 10.210.68.82  src arp
    hardware vendor 'Apple'  src dhcp  id 3829  weight 200
    type 'Tablet'  src dhcp  id 3829  weight 200
    family 'iPad'  src dhcp  id 3829  weight 200
    os 'iPadOS'  src dhcp  id 3829  weight 200
    host 'iPad'  src dhcp
  vd root/0  0e:2c:d8:bc:ce:63  gen 15436040  req OUA/34
    created 64976929s  gen 233737  seen 33751s  Guest  gen 449046
    ip 172.176.0.14  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '17.5'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  92:54:54:a7:7c:9f  gen 14927894  req OUA/34
    created 8320835s  gen 11736350  seen 974128s  CORP WIRELESS  gen 439894
    ip 10.210.68.3  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.3.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  b8:a4:4f:6e:7f:d6  gen 3226019  req OHUA/3c
    created 39842137s  gen 3057451  seen 22s  SECURITY_CAMERA  gen 212515
    ip 10.210.32.175  src ssdp
    hardware vendor 'Axis'  src onvif  id 4314  weight 200
    type 'Network Generic'  src onvif  id 4314  weight 200
    family 'Network Device'  src onvif  id 4314  weight 200
    os 'Linux'  src ssdp  id 6076  weight 128
    hardware version 'P3267-LV'  src onvif  id 4316  weight 180
  vd root/0  38:8d:3d:11:0e:a9  gen 14959927  req OUA/34
    created 9967611s  gen 11227079  seen 925920s  Guest  gen 440455
    ip 172.176.0.32  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'ZRH-YX9POJSCFVT'  src dhcp
  vd root/0  9e:ee:06:3a:5d:19  gen 15368586  req OHUSA/3e
    created 196419s  gen 15368586  seen 195599s  CORP WIRELESS  gen 447734
  vd root/0  ec:7f:ec:3d:fc:23  gen 15017602  req OHUA/3c
    created 830588s  gen 15015141  seen 824366s  Guest  gen 441307
    ip 172.176.0.39  src arp
    hardware vendor 'Apple'  src dns  id 1713  weight 180
    type 'Media Player'  src dns  id 1713  weight 180
    family 'TV'  src dns  id 1713  weight 180
    os 'tvOS'  src dns  id 1713  weight 180
  vd root/0  66:54:cd:d0:90:77  gen 14126637  req OUA/34
    created 4320938s  gen 13099202  seen 2351396s  CORP WIRELESS  gen 426222
    ip 10.210.68.98  src arp
    hardware vendor 'Google'  src dhcp  id 6462  weight 255
    type 'Phone'  src dhcp  id 6462  weight 255
    family 'Pixel'  src dhcp  id 6462  weight 255
    os 'Android'  src dhcp  id 6462  weight 255
    hardware version '9'  src dhcp  id 6466  weight 220
    software version '1'  src dhcp  id 6462  weight 255
    host 'Pixel-9'  src dhcp
  vd root/0  c6:3a:5d:05:ec:f2  gen 15459340  req OUA/34
    created 3041489s  gen 13731900  seen 923s  CORP WIRELESS  gen 449475
    ip 10.210.68.42  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.7'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  22:1c:46:61:d8:db  gen 15458899  req OUA/34
    created 2528512s  gen 14024861  seen 14s  Guest  gen 449469
    ip 172.176.0.2  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  14:dd:9c:89:61:08  gen 10390971  req OHUA/3c
    created 17642640s  gen 8518693  seen 22s  CORP WIRELESS  gen 339393
    ip 10.210.68.12  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '13'  src dhcp  id 191  weight 130
  vd root/0  e4:30:22:a8:0f:4d  gen 12359904  req OHUSA/3e
    created 27932016s  gen 5403741  seen 3s  SECURITY_ExtDev  gen 389495
    ip 10.210.48.175  src mac
  vd root/0  e4:30:22:a8:0f:4e  gen 11671677  req OHUSA/3e
    created 27931043s  gen 5403989  seen 3s  SECURITY_ExtDev  gen 368667
    ip 10.210.48.176  src mac
  vd root/0  1a:2c:e3:c8:c7:36  gen 15451140  req OUA/34
    created 71138813s  gen 158286  seen 3625s  CORP WIRELESS  gen 449295
    ip 10.210.68.25  src mac
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S4 Ultra'  src dhcp  id 6732  weight 230
    software version '14'  src http  id 997  weight 230
    host 'S24-Ultra-korisnika-Tihomir'  src dhcp
  vd root/0  92:63:e1:80:bb:f4  gen 15075860  req OHUSA/3e
    created 726481s  gen 15075857  seen 726007s  CORP WIRELESS  gen 442239
    ip 10.210.68.70  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
  vd root/0  8c:53:e6:ed:38:bc  gen 14843986  req OUA/34
    created 1130542s  gen 14842044  seen 1125847s  Guest  gen 438443
    ip 172.176.0.45  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'LAP24135'  src dhcp
  vd root/0  34:6d:9c:00:3d:94  gen 11979651  req OHUSA/3e
    created 88407655s  gen 861  seen 11s  ENG_LANB  gen 196044
    ip 10.210.136.120  src arp
  vd root/0  34:6d:9c:00:43:05  gen 15442041  req OHUSA/3e
    created 88407642s  gen 928  seen 22s  ENG_LANA  gen 438387
    ip 10.210.132.120  src arp
  vd root/0  28:e9:8e:67:5a:8a  gen 15442877  req OHUSA/3e
    created 88407524s  gen 1345  seen 20s  ENG_LANB  gen 196055
    ip 10.210.136.85  src arp
  vd root/0  82:8f:37:67:b0:c7  gen 15411402  req OUA/34
    created 56791741s  gen 383722  seen 101203s  CORP WIRELESS  gen 448528
    ip 10.210.68.66  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  2e:af:e9:8f:b9:1b  gen 15459054  req OUA/34
    created 48073515s  gen 1870661  seen 6124s  Guest  gen 449471
    ip 172.176.0.18  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S4 Ultra'  src dhcp  id 6732  weight 230
    software version '14'  src http  id 997  weight 230
    host 'S24-Ultra-korisnika-Boris'  src dhcp
  vd root/0  76:42:f7:e6:03:68  gen 14695608  req OUA/34
    created 7856220s  gen 11868119  seen 1371134s  Guest  gen 436016
    ip 172.176.0.8  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.2'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  fc:6d:77:25:2d:a3  gen 15088907  req OUA/34
    created 7548744s  gen 11948557  seen 699885s  Guest  gen 442527
    ip 172.176.0.21  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'loukasHP'  src dhcp
  vd root/0  96:4d:dd:73:6d:df  gen 15451318  req OUA/34
    created 2366408s  gen 14118899  seen 32989s  CORP WIRELESS  gen 449306
    ip 10.210.68.90  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  0e:1c:b9:77:57:c7  gen 15425358  req OUA/34
    created 4922420s  gen 12847751  seen 83129s  CORP WIRELESS  gen 448834
    ip 10.210.68.7  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  e0:2b:e9:38:11:bb  gen 14497316  req OUA/34
    created 1729567s  gen 14490633  seen 1718873s  Guest  gen 432447
    ip 172.176.0.24  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'VDC-6CH64D3'  src dhcp
  vd root/0  b2:e9:15:0c:e8:63  gen 14241848  req OUA/34
    created 2172785s  gen 14233310  seen 2157441s  CORP WIRELESS  gen 427846
    ip 10.210.68.14  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  9a:bd:19:81:01:88  gen 14379466  req OUA/34
    created 2791391s  gen 13874370  seen 1896290s  CORP WIRELESS  gen 430238
    ip 10.210.68.33  src arp
    hardware vendor 'Apple'  src http  id 6085  weight 230
    type 'Computer'  src http  id 6085  weight 230
    family 'Mac'  src http  id 6085  weight 230
    os 'macOS'  src http  id 6085  weight 230
    hardware version 'MacBook Pro'  src dns  id 2654  weight 150
    software version '26.2'  src http  id 6085  weight 230
    host 'Mac'  src dhcp
  vd root/0  ca:3d:e8:46:db:eb  gen 14901359  req OUA/34
    created 2202892s  gen 14216438  seen 1026723s  Guest  gen 439456
    ip 172.176.0.7  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S4 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Akif-s-S24-Ultra'  src dhcp
  vd root/0  00:12:ea:15:0d:14  gen 15455241  req OHUSA/3e
    created 88407573s  gen 1162  seen 22s  ENG_LANA  gen 449384
    ip 10.210.132.235  src arp
  vd root/0  00:12:ea:15:0d:18  gen 8372354  req OHUSA/3e
    created 88407595s  gen 1108  seen 18s  ENG_LANA  gen 296389
    ip 10.210.132.236  src arp
  vd root/0  00:12:ea:0e:f0:9f  gen 12986609  req OHUSA/3e
    created 88407652s  gen 879  seen 22s  ENG_LANA  gen 403718
    ip 10.210.132.232  src arp
  vd root/0  00:12:ea:15:0d:1e  gen 4369453  req OHUSA/3e
    created 88407578s  gen 1158  seen 18s  ENG_LANA  gen 227873
    ip 10.210.132.237  src arp
  vd root/0  00:12:ea:15:0d:22  gen 7949758  req OHUSA/3e
    created 88407621s  gen 972  seen 22s  ENG_LANA  gen 288973
    ip 10.210.132.233  src arp
  vd root/0  00:12:ea:15:0d:42  gen 9487006  req OHUSA/3e
    created 88407638s  gen 946  seen 19s  ENG_LANA  gen 301340
    ip 10.210.132.230  src arp
  vd root/0  00:12:ea:15:0d:46  gen 3403612  req OHUSA/3e
    created 88407649s  gen 888  seen 19s  ENG_LANA  gen 214828
    ip 10.210.132.231  src arp
  vd root/0  00:12:ea:15:0d:48  gen 8372869  req OHUSA/3e
    created 88407603s  gen 1068  seen 22s  ENG_LANA  gen 296412
    ip 10.210.132.238  src arp
  vd root/0  00:12:ea:0e:f3:8f  gen 1748615  req OHUSA/3e
    created 88407655s  gen 865  seen 22s  ENG_LANA  gen 147606
    ip 10.210.132.239  src arp
  vd root/0  00:12:ea:15:12:92  gen 15411769  req OHUSA/3e
    created 88407591s  gen 1119  seen 22s  ENG_LANA  gen 448548
    ip 10.210.132.234  src arp
  vd root/0  de:0d:e6:e5:01:cb  gen 15085770  req OUA/34
    created 8409239s  gen 11710697  seen 697438s  Guest  gen 442235
    ip 172.176.0.14  src mac
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'S25-Ultra-von-L'  src dhcp
  vd root/0  44:6f:f8:ae:f5:16  gen 15405993  req OUSA/36
    created 1045222s  gen 14889911  seen 6s  Guest  gen 448377
    ip 172.176.0.7  src arp
    host '9HE-CH-VAA1176A'  src dhcp
  vd root/0  44:6f:f8:ae:f4:5f  gen 14890933  req OUSA/36
    created 1044218s  gen 14890476  seen 44s  Guest  gen 439277
    ip 172.176.0.36  src arp
    host '9HE-CH-VAA1283A'  src dhcp
  vd root/0  44:6f:f8:ae:f6:61  gen 14890946  req OUSA/36
    created 1044736s  gen 14890147  seen 58s  Guest  gen 439279
    ip 172.176.0.35  src arp
    host '9HE-CH-VAA1862A'  src dhcp
  vd root/0  44:6f:f8:ae:f7:de  gen 14890771  req OUSA/36
    created 1043907s  gen 14890769  seen 59s  Guest  gen 439273
    ip 172.176.0.37  src arp
    host '9HE-CH-VAA1835A'  src dhcp
  vd root/0  b8:a4:4f:81:87:98  gen 11274592  req OHUA/3c
    created 14863301s  gen 9528757  seen 22s  SECURITY_CAMERA  gen 326333
    ip 10.210.32.173  src arp
    hardware vendor 'Axis'  src onvif  id 4314  weight 200
    type 'Network Generic'  src onvif  id 4314  weight 200
    family 'Network Device'  src onvif  id 4314  weight 200
    os 'Linux'  src ssdp  id 6076  weight 128
    hardware version 'Q6318-LE'  src onvif  id 4316  weight 180
  vd root/0  3e:1f:54:d5:52:c2  gen 14779861  req OUA/34
    created 54821388s  gen 757165  seen 18s  CORP WIRELESS  gen 437283
    ip 10.210.68.33  src arp
    hardware vendor 'Apple'  src http  id 930  weight 230
    type 'Tablet'  src http  id 930  weight 230
    family 'iPad'  src http  id 930  weight 230
    os 'iPadOS'  src http  id 930  weight 230
    hardware version 'Air'  src dns  id 4605  weight 230
    software version '17.5.1'  src http  id 930  weight 230
    host 'iPad'  src dns
  vd root/0  36:a9:e4:25:95:0c  gen 15195145  req OUA/34
    created 526730s  gen 15194643  seen 525024s  CORP WIRELESS  gen 444429
    ip 10.210.68.80  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  c8:94:02:ca:ce:b7  gen 14826337  req OUA/34
    created 2959131s  gen 13778582  seen 1157373s  Guest  gen 438064
    ip 172.176.0.19  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'ZRH-5CG15128TK'  src dhcp
  vd root/0  0c:29:8f:06:fc:0a  gen 15110510  req OUSA/36
    created 29882781s  gen 4897730  seen 638527s  Guest  gen 442881
    ip 172.176.0.23  src arp
    host 'Tesla'  src dhcp
  vd root/0  42:65:eb:52:cb:79  gen 15150399  req OUA/34
    created 2993685s  gen 13758392  seen 383731s  CORP WIRELESS  gen 443616
    ip 10.210.68.16  src arp
    hardware vendor 'Apple'  src http  id 930  weight 230
    type 'Tablet'  src http  id 930  weight 230
    family 'iPad'  src http  id 930  weight 230
    os 'iPadOS'  src http  id 930  weight 230
    software version '16.3'  src http  id 930  weight 230
    host 'iPad-von-Levi'  src dns
  vd root/0  00:0e:8c:ff:ff:01  gen 13494744  req OHUSA/3e
    created 37419091s  gen 3395049  seen 19s  ENG_LANC  gen 214817
    ip 10.210.140.119  src arp
  vd root/0  1e:18:fc:be:95:6d  gen 15451545  req OUA/34
    created 10974175s  gen 10876419  seen 84s  Guest  gen 449308
    ip 172.176.0.38  src arp
    hardware vendor 'Samsung'  src http  id 990  weight 255
    type 'Phone'  src http  id 990  weight 255
    family 'Galaxy'  src http  id 990  weight 255
    os 'Android'  src http  id 990  weight 255
    hardware version 'On'  src http  id 1783  weight 230
    software version '16'  src http  id 990  weight 255
    host 'Galaxy-XCover7'  src dhcp
  vd root/0  0c:7a:15:4e:cf:4b  gen 15433942  req OUA/34
    created 58755104s  gen 303467  seen 65571s  Guest  gen 448999
    ip 172.176.0.6  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'Derico'  src dhcp
  vd root/0  3a:39:a7:12:08:88  gen 15079988  req OUA/34
    created 2187807s  gen 14224994  seen 689995s  Guest  gen 442345
    ip 172.176.0.34  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  64:07:f6:3f:80:15  gen 15026445  req OUA/34
    created 88407690s  gen 5  seen 0s  CORP WIRELESS  gen 441470
    ip 10.210.68.4  src mac
    hardware vendor 'Samsung'  src ssdp  id 6854  weight 180
    type 'Television'  src ssdp  id 6854  weight 180
    family 'Smart TV'  src ssdp  id 6854  weight 180
    os 'Tizen'  src fortiguard  id 0  weight 139
    host 'Display 1'  src dhcp
  vd root/0  64:07:f6:3f:7f:d9  gen 15026470  req OUA/34
    created 88407690s  gen 6  seen 0s  CORP WIRELESS  gen 441471
    ip 10.210.68.2  src mac
    hardware vendor 'Samsung'  src ssdp  id 6854  weight 180
    type 'Television'  src ssdp  id 6854  weight 180
    family 'Smart TV'  src ssdp  id 6854  weight 180
    os 'Tizen'  src fortiguard  id 0  weight 139
    host 'Display 2'  src dhcp
  vd root/0  00:30:d6:22:5e:26  gen 15363210  req OHUSA/3e
    created 88407498s  gen 1621  seen 22s  ENG_LANC  gen 279660
    ip 10.210.140.86  src arp
  vd root/0  00:30:d6:22:5e:2f  gen 15464950  req OHUSA/3e
    created 88407521s  gen 1454  seen 22s  ENG_LANC  gen 279632
    ip 10.210.140.76  src arp
  vd root/0  00:30:d6:22:5d:92  gen 15278230  req OHUSA/3e
    created 88407521s  gen 1457  seen 19s  ENG_LAND  gen 279648
    ip 10.210.144.81  src arp
  vd root/0  00:30:d6:22:5d:c7  gen 14948692  req OHUSA/3e
    created 88407520s  gen 1548  seen 22s  ENG_LAND  gen 279641
    ip 10.210.144.76  src arp
  vd root/0  00:30:d6:22:5d:ca  gen 15398445  req OHUSA/3e
    created 88407500s  gen 1615  seen 18s  ENG_LANC  gen 279647
    ip 10.210.140.81  src arp
  vd root/0  00:30:d6:22:5d:d8  gen 15251141  req OHUSA/3e
    created 88407522s  gen 1431  seen 18s  ENG_LAND  gen 279644
    ip 10.210.144.86  src arp
  vd root/0  36:07:13:b0:01:24  gen 14831908  req OUA/34
    created 60594917s  gen 283026  seen 1147987s  Guest  gen 438183
    ip 172.176.0.40  src mac
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'S22-Ultra'  src dhcp  id 182  weight 232
    software version '14'  src dhcp  id 133  weight 255
    host 'Galaxy-S22-Ultra'  src dhcp
  vd root/0  f6:86:55:7b:7c:a7  gen 15460065  req OUA/34
    created 1754612s  gen 14475387  seen 18s  Guest  gen 449488
    ip 172.176.0.39  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  5c:fb:3a:7f:5c:dd  gen 15385213  req OUA/34
    created 941822s  gen 14950879  seen 164106s  Guest  gen 448022
    ip 172.176.0.18  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'Bari-Soliman'  src dhcp
  vd root/0  5c:88:16:af:1b:29  gen 933  req OHUSA/3e
    created 88407641s  gen 932  seen 19s  ENG_LANA  gen 385
    ip 10.210.132.210  src arp
  vd root/0  5c:88:16:af:1b:db  gen 960  req OHUSA/3e
    created 88407632s  gen 959  seen 7s  ENG_LANA  gen 395
    ip 10.210.132.214  src arp
  vd root/0  5c:88:16:af:1c:c3  gen 859  req OHUSA/3e
    created 88407656s  gen 858  seen 18s  ENG_LANA  gen 352
    ip 10.210.132.213  src arp
  vd root/0  5c:88:16:af:1c:e2  gen 849  req OHUSA/3e
    created 88407657s  gen 848  seen 22s  ENG_LANA  gen 349
    ip 10.210.132.212  src arp
  vd root/0  5c:88:16:ac:91:0e  gen 950  req OHUSA/3e
    created 88407638s  gen 949  seen 22s  ENG_LANA  gen 392
    ip 10.210.132.171  src arp
  vd root/0  5c:88:16:ac:91:13  gen 894  req OHUSA/3e
    created 88407648s  gen 893  seen 8s  ENG_LANA  gen 367
    ip 10.210.132.175  src arp
  vd root/0  5c:88:16:ac:91:14  gen 941  req OHUSA/3e
    created 88407638s  gen 940  seen 12s  ENG_LANA  gen 388
    ip 10.210.132.172  src arp
  vd root/0  5c:88:16:ac:94:20  gen 235935  req OHUSA/3e
    created 88407638s  gen 947  seen 0s  ENG_LANA  gen 118703
    ip 10.210.132.173  src arp
  vd root/0  5c:88:16:ac:92:6c  gen 235938  req OHUSA/3e
    created 88407647s  gen 901  seen 22s  ENG_LANA  gen 118706
    ip 10.210.132.174  src arp
  vd root/0  5c:88:16:ac:93:86  gen 235928  req OHUSA/3e
    created 88407678s  gen 24  seen 22s  ENG_LANA  gen 118702
    ip 10.210.132.170  src arp
  vd root/0  00:01:29:79:39:11  gen 15442012  req OUA/34
    created 88407522s  gen 1435  seen 18s  ENG_LAND  gen 195973
    ip 10.210.144.85  src mac
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'agentsmith'  src dns
  vd root/0  00:01:29:79:38:9f  gen 15440101  req OUA/34
    created 88407520s  gen 1547  seen 22s  ENG_LAND  gen 195590
    ip 10.210.144.75  src mac
    os 'Windows'  src http  id 1444  weight 130
    software version '10'  src http  id 1444  weight 130
    host 'agentsmith'  src dns
  vd root/0  00:01:29:79:38:ad  gen 15442021  req OUSA/36
    created 88407521s  gen 1455  seen 22s  ENG_LANC  gen 196081
    ip 10.210.140.75  src arp
    host 'agentsmith'  src dns
  vd root/0  00:01:29:79:38:c5  gen 15440111  req OUA/34
    created 88407498s  gen 1623  seen 22s  ENG_LANC  gen 195987
    ip 10.210.140.85  src mac
    os 'Windows'  src http  id 6752  weight 130
    software version '11 Enterprise'  src http  id 6752  weight 130
    host 'agentsmith'  src dns
  vd root/0  00:01:29:79:38:dd  gen 12429817  req OUSA/36
    created 88407521s  gen 1460  seen 19s  ENG_LAND  gen 314753
    ip 10.210.144.80  src arp
    host 'agentsmith'  src dns
  vd root/0  00:01:29:79:38:df  gen 15434601  req OHUA/3c
    created 88407500s  gen 1617  seen 18s  ENG_LANC  gen 195678
    ip 10.210.140.80  src arp
    os 'Windows'  src http  id 6752  weight 130
    software version '11 Enterprise'  src http  id 6752  weight 130
  vd root/0  d0:57:7e:83:26:bf  gen 14234486  req OUA/34
    created 2170915s  gen 14234482  seen 2161344s  CORP WIRELESS  gen 427880
    ip 10.210.68.71  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host '360-WIN11-EMS'  src dhcp
  vd root/0  5c:88:16:ae:a8:e0  gen 915  req OHUSA/3e
    created 88407645s  gen 914  seen 22s  ENG_LANA  gen 377
    ip 10.210.132.211  src arp
  vd root/0  ac:f2:3c:c5:35:91  gen 15120364  req OUA/34
    created 10233477s  gen 11131874  seen 639032s  Guest  gen 443034
    ip 172.176.0.18  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'LAPTOP-FPIM4D0N'  src dhcp
  vd root/0  e6:a6:32:2f:a3:0a  gen 15451750  req OUA/34
    created 13680990s  gen 9846112  seen 17256s  CORP WIRELESS  gen 449310
    ip 10.210.68.5  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.1.0'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  98:fa:2e:4d:ee:2c  gen 15050432  req OUA/34
    created 769839s  gen 15050427  seen 769822s  Guest  gen 441835
    ip 172.176.0.14  src arp
    hardware vendor 'Sony'  src http  id 1287  weight 220
    type 'Game Console'  src http  id 1287  weight 220
    family 'PlayStation'  src http  id 1287  weight 220
    os 'Orbis OS'  src http  id 1287  weight 220
    hardware version '5'  src dhcp  id 2795  weight 200
    host 'PS5-51C526'  src dns
  vd root/0  8c:ec:7b:8b:e7:8c  gen 15002107  req OUA/34
    created 10255640s  gen 11125542  seen 809761s  Guest  gen 441095
    ip 172.176.0.23  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.7.1'  src http  id 929  weight 230
    host 'AmansiPone12Pro'  src dhcp
  vd root/0  74:78:a6:68:91:b6  gen 457311  req HU/18
    created 56082849s  gen 457311  seen 21s  WIRELESS_APs  gen 166668
  vd root/0  00:62:0b:c7:1f:c0  gen 3632  req OUA/34
    created 88377979s  gen 2644  seen 0s  VMWare_MGT  gen 1217
    ip 10.210.6.11  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR02'  src dhcp
  vd root/0  00:62:0b:c7:1f:c1  gen 11345  req OA/24
    created 88377491s  gen 2653  seen 0s  VMWare_MGT  gen 1221
    ip 10.210.6.11  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR02'  src dhcp
    user 'ps-pbrinkmann'  src kerberos
  vd root/0  ee:cc:3a:d8:68:b9  gen 15451897  req OUSA/36
    created 4956667s  gen 12832807  seen 32336s  Guest  gen 449320
    ip 172.176.0.27  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  be:71:b8:30:a1:8a  gen 14942148  req OUA/34
    created 54812216s  gen 759837  seen 956331s  Guest  gen 440164
    ip 172.176.0.13  src mac
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S2 Ultra'  src dhcp  id 6732  weight 230
    software version '14'  src http  id 997  weight 230
    host 'Tony-s-S22-Ultra'  src dhcp
  vd root/0  00:62:0b:c9:03:30  gen 2334804  req OUA/34
    created 88378039s  gen 2643  seen 0s  VMWare_MGT  gen 1216
    ip 10.210.6.10  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01'  src dhcp
  vd root/0  00:62:0b:c9:03:31  gen 2334811  req OUA/34
    created 88377547s  gen 2651  seen 0s  VMWare_MGT  gen 1220
    ip 10.210.6.10  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01'  src dhcp
  vd root/0  00:62:0b:c5:b2:60  gen 3740  req OUA/34
    created 88378819s  gen 2627  seen 0s  VMWare_MGT  gen 1747
    ip 10.210.6.15  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR02-FO'  src dhcp
  vd root/0  00:62:0b:c5:b2:61  gen 3739  req OUA/34
    created 88378819s  gen 2629  seen 0s  VMWare_MGT  gen 1746
    ip 10.210.6.15  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR02-FO'  src dhcp
  vd root/0  d2:7d:4a:35:3b:76  gen 15246011  req OUA/34
    created 13329634s  gen 9945004  seen 436632s  CORP WIRELESS  gen 445387
    ip 10.210.68.17  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  72:dc:cb:85:d1:8b  gen 14862446  req OUA/34
    created 5596918s  gen 12567784  seen 1094104s  CORP WIRELESS  gen 438785
    ip 10.210.68.37  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  a6:de:16:42:64:d9  gen 15410632  req OA/24
    created 74233501s  gen 130176  seen 105346s  CORP WIRELESS  gen 448503
    ip 10.210.68.28  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '14'  src http  id 997  weight 230
    host 'S23-von-Leo'  src dhcp
    user 'Adrian.Huppin'  src kerberos
  vd root/0  00:62:0b:c6:db:70  gen 3603  req OUA/34
    created 88378819s  gen 2626  seen 0s  VMWare_MGT  gen 1648
    ip 10.210.6.14  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01-FO'  src dhcp
  vd root/0  00:62:0b:c6:db:71  gen 3602  req OUA/34
    created 88378819s  gen 2628  seen 0s  VMWare_MGT  gen 1209
    ip 10.210.6.14  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'ZRH11-GNVR01-FO'  src dhcp
  vd root/0  00:1b:08:6d:51:29  gen 14792347  req OHUSA/3e
    created 1217967s  gen 14792269  seen 22s  ENG_LANA  gen 437533
    ip 10.210.132.246  src arp
  vd root/0  00:1b:08:6d:51:2f  gen 14933546  req OHUSA/3e
    created 971158s  gen 14933501  seen 18s  ENG_LANA  gen 439991
    ip 10.210.132.253  src arp
  vd root/0  00:1b:08:6d:51:3e  gen 14127219  req OHUSA/3e
    created 2856613s  gen 13837324  seen 10s  ENG_LANA  gen 426242
    ip 10.210.132.252  src arp
  vd root/0  00:1b:08:6d:51:44  gen 14435636  req OHUSA/3e
    created 1821555s  gen 14435498  seen 6s  ENG_LANA  gen 431305
    ip 10.210.132.245  src arp
  vd root/0  00:1b:08:6d:50:6f  gen 14386203  req OHUSA/3e
    created 1905999s  gen 14386048  seen 19s  ENG_LANA  gen 430384
    ip 10.210.132.250  src arp
  vd root/0  00:1b:08:6d:50:76  gen 14529829  req OHUSA/3e
    created 1664615s  gen 14529405  seen 14s  ENG_LANA  gen 433005
    ip 10.210.132.251  src arp
  vd root/0  00:1b:08:6d:50:79  gen 15184019  req OHUSA/3e
    created 545308s  gen 15184018  seen 2s  ENG_LANA  gen 444208
    ip 10.210.132.254  src arp
  vd root/0  00:1b:08:6d:50:83  gen 15279469  req OHUSA/3e
    created 371990s  gen 15279468  seen 22s  ENG_LANA  gen 446020
    ip 10.210.132.249  src arp
  vd root/0  00:1b:08:6d:50:86  gen 15133144  req OHUSA/3e
    created 631839s  gen 15133068  seen 7s  ENG_LANA  gen 443278
    ip 10.210.132.248  src arp
  vd root/0  00:1b:08:6d:50:89  gen 14071889  req OHUSA/3e
    created 2447391s  gen 14071754  seen 22s  ENG_LANA  gen 425294
    ip 10.210.132.247  src arp
  vd root/0  74:04:f1:ea:06:19  gen 14940326  req OUA/34
    created 975709s  gen 14930769  seen 959115s  CORP WIRELESS  gen 440127
    ip 10.210.68.62  src arp
    type 'Desktop'  src dhcp  id 6502  weight 130
    os 'Windows'  src dhcp  id 6502  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'DESKTOP-5RC6S73'  src dhcp
  vd root/0  1a:c1:77:b6:00:04  gen 15450540  req OHUA/3c
    created 1245123s  gen 14776575  seen 3268s  Guest  gen 449283
    ip 172.176.0.11  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.5.0'  src http  id 902  weight 230
  vd root/0  3e:ec:ef:4f:bd:8c  gen 8939969  req OHUSA/3e
    created 88407604s  gen 1040  seen 22s  TegRepTransNet  gen 309127
  vd root/0  3e:ec:ef:4f:bd:8d  gen 8939970  req OHUSA/3e
    created 88407604s  gen 1055  seen 22s  TegRepTransNet  gen 309128
  vd root/0  3e:ec:ef:4f:bd:92  gen 8935215  req OHUSA/3e
    created 88407604s  gen 1039  seen 22s  TegRepTransNet  gen 309076
  vd root/0  3e:ec:ef:4f:bd:93  gen 8935216  req OHUSA/3e
    created 88407604s  gen 1065  seen 22s  TegRepTransNet  gen 309077
  vd root/0  3e:ec:ef:4f:bd:ae  gen 8935126  req OHUSA/3e
    created 88407604s  gen 1038  seen 22s  TegRepTransNet  gen 309069
  vd root/0  74:04:f1:e9:f5:2f  gen 15411592  req OA/24
    created 56791382s  gen 383745  seen 101203s  CORP WIRELESS  gen 448539
    ip 10.210.68.68  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'Steve_VDC'  src dhcp
    user 'Steve.Kargel'  src kerberos
  vd root/0  e0:23:ff:85:05:0e  gen 3477015  req OUA/34
    created 88407379s  gen 1654  seen 0s  ENG_LAND  gen 215840
    ip 192.168.1.99  src arp
    hardware vendor 'Fortinet'  src dhcp  id 160  weight 220
    type 'Network Generic'  src dhcp  id 160  weight 220
    family 'FortiSwitchRugged'  src dhcp  id 160  weight 220
    os 'FortiSwitchRugged OS'  src dhcp  id 160  weight 220
    hardware version '112D-POE'  src dhcp  id 160  weight 220
    host 'SR12DPTD20001622'  src dhcp
  vd root/0  e0:23:ff:85:05:0f  gen 1654942  req OHUSA/3e
    created 88407520s  gen 1497  seen 22s  ENG_LAND  gen 196014
  vd root/0  e0:23:ff:85:05:62  gen 1655875  req 0
    created 88407524s  gen 1287  seen 20s  fortilink  gen 196161
  vd root/0  e0:23:ff:85:05:70  gen 1642730  req 0
    created 88407524s  gen 1330  seen 20s  fortilink  gen 195553
  vd root/0  e0:23:ff:85:07:4c  gen 1318  req 0
    created 88407524s  gen 1318  seen 20s  fortilink  gen 576
  vd root/0  e0:23:ff:85:07:68  gen 1438  req 0
    created 88407522s  gen 1438  seen 20s  fortilink  gen 696
  vd root/0  e0:23:ff:85:0a:16  gen 1306  req 0
    created 88407524s  gen 1306  seen 20s  fortilink  gen 564
  vd root/0  e0:23:ff:85:04:e4  gen 1643364  req 0
    created 88407524s  gen 1268  seen 20s  fortilink  gen 195657
  vd root/0  e0:23:ff:85:08:64  gen 1340  req 0
    created 88407524s  gen 1340  seen 11s  fortilink  gen 598
  vd root/0  e0:23:ff:85:07:92  gen 1310  req 0
    created 88407524s  gen 1310  seen 20s  fortilink  gen 568
  vd root/0  e0:23:ff:85:09:52  gen 1462  req 0
    created 88407520s  gen 1462  seen 10s  fortilink  gen 720
  vd root/0  e0:23:ff:85:07:ae  gen 1352  req 0
    created 88407523s  gen 1352  seen 20s  fortilink  gen 610
  vd root/0  e0:23:ff:85:09:7c  gen 1575  req 0
    created 88407505s  gen 1575  seen 20s  fortilink  gen 827
  vd root/0  e0:23:ff:85:0b:74  gen 1656260  req 0
    created 88407503s  gen 1596  seen 20s  fortilink  gen 196191
  vd root/0  e0:23:ff:85:0f:02  gen 3477024  req OUA/34
    created 88407590s  gen 1122  seen 20s  ENG_LAND  gen 215842
    ip 192.168.1.99  src arp
    hardware vendor 'Fortinet'  src dhcp  id 160  weight 220
    type 'Network Generic'  src dhcp  id 160  weight 220
    family 'FortiSwitchRugged'  src dhcp  id 160  weight 220
    os 'FortiSwitchRugged OS'  src dhcp  id 160  weight 220
    hardware version '112D-POE'  src dhcp  id 160  weight 220
    host 'SR12DPTD20001804'  src dhcp
  vd root/0  e0:23:ff:85:0f:03  gen 1654995  req OHUSA/3e
    created 88407505s  gen 1572  seen 20s  ENG_LAND  gen 196024
  vd root/0  e0:23:ff:85:0b:90  gen 1344  req 0
    created 88407524s  gen 1344  seen 20s  fortilink  gen 602
  vd root/0  e0:23:ff:85:0a:be  gen 1347  req 0
    created 88407524s  gen 1347  seen 20s  fortilink  gen 605
  vd root/0  e0:23:ff:85:09:ec  gen 1644491  req 0
    created 88407524s  gen 1302  seen 20s  fortilink  gen 195812
  vd root/0  e0:23:ff:85:0c:8c  gen 14641501  req 0
    created 88407523s  gen 1356  seen 20s  fortilink  gen 435036
  vd root/0  e0:23:ff:85:0e:5a  gen 12389331  req OUA/34
    created 88407638s  gen 944  seen 11s  ENG_LANC  gen 390308
    ip 192.168.1.99  src arp
    hardware vendor 'Fortinet'  src dhcp  id 160  weight 220
    type 'Network Generic'  src dhcp  id 160  weight 220
    family 'FortiSwitchRugged'  src dhcp  id 160  weight 220
    os 'FortiSwitchRugged OS'  src dhcp  id 160  weight 220
    hardware version '112D-POE'  src dhcp  id 160  weight 220
    host 'SR12DPTD20001792'  src dhcp
  vd root/0  e0:23:ff:85:0e:5b  gen 1654852  req OHUSA/3e
    created 88407524s  gen 1332  seen 20s  ENG_LANC  gen 195981
  vd root/0  e0:23:ff:85:0d:96  gen 1401  req 0
    created 88407522s  gen 1401  seen 20s  fortilink  gen 659
  vd root/0  e0:23:ff:85:10:44  gen 1643187  req 0
    created 88407522s  gen 1413  seen 19s  fortilink  gen 195624
  vd root/0  e0:23:ff:85:10:52  gen 1643699  req 0
    created 88407522s  gen 1428  seen 11s  fortilink  gen 195696
  vd root/0  e0:23:ff:85:0e:d8  gen 14641640  req OUA/34
    created 88407419s  gen 1644  seen 4s  ENG_LANC  gen 435046
    hardware vendor 'Fortinet'  src dhcp  id 160  weight 220
    type 'Network Generic'  src dhcp  id 160  weight 220
    family 'FortiSwitchRugged'  src dhcp  id 160  weight 220
    os 'FortiSwitchRugged OS'  src dhcp  id 160  weight 220
    hardware version '112D-POE'  src dhcp  id 160  weight 220
    host 'SR12DPTD20001801'  src dhcp
  vd root/0  e0:23:ff:85:0e:d9  gen 1655191  req OHUSA/3e
    created 88407524s  gen 1261  seen 20s  ENG_LANC  gen 196068
  vd root/0  e0:23:ff:85:13:38  gen 1359  req 0
    created 88407522s  gen 1359  seen 19s  fortilink  gen 617
  vd root/0  e0:23:ff:85:0f:fe  gen 1643367  req 0
    created 88407522s  gen 1361  seen 19s  fortilink  gen 195660
  vd root/0  e0:23:ff:85:13:7e  gen 1644198  req 0
    created 88407522s  gen 1424  seen 19s  fortilink  gen 195747
  vd root/0  3a:34:7b:c7:1a:dc  gen 15286615  req OUA/34
    created 1015951s  gen 14907462  seen 358141s  Guest  gen 446179
    ip 172.176.0.3  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  e0:23:ff:85:16:9c  gen 1644330  req 0
    created 88407522s  gen 1369  seen 19s  fortilink  gen 195776
  vd root/0  e0:23:ff:85:1b:18  gen 1642448  req 0
    created 88407522s  gen 1433  seen 18s  fortilink  gen 195518
  vd root/0  e0:23:ff:85:19:66  gen 1418  req 0
    created 88407522s  gen 1418  seen 18s  fortilink  gen 676
  vd root/0  e0:23:ff:85:18:94  gen 1642867  req 0
    created 88407521s  gen 1461  seen 19s  fortilink  gen 195574
  vd root/0  e0:23:ff:85:1c:bc  gen 1644215  req 0
    created 88407522s  gen 1374  seen 1s  fortilink  gen 195761
  vd root/0  e0:23:ff:85:1c:d8  gen 1398  req 0
    created 88407522s  gen 1398  seen 10s  fortilink  gen 656
  vd root/0  e0:23:ff:85:23:3e  gen 1644478  req 0
    created 88407522s  gen 1380  seen 18s  fortilink  gen 195800
  vd root/0  e0:23:ff:85:21:b6  gen 1443  req 0
    created 88407522s  gen 1443  seen 18s  fortilink  gen 701
  vd root/0  e0:23:ff:85:25:36  gen 14641506  req 0
    created 88407522s  gen 1383  seen 18s  fortilink  gen 435037
  vd root/0  e0:23:ff:85:23:84  gen 1644217  req 0
    created 88407522s  gen 1385  seen 2s  fortilink  gen 195763
  vd root/0  e0:23:ff:85:27:12  gen 1644495  req 0
    created 88407522s  gen 1446  seen 18s  fortilink  gen 195816
  vd root/0  e0:23:ff:85:27:20  gen 1588  req 0
    created 88407504s  gen 1588  seen 18s  fortilink  gen 837
  vd root/0  e0:23:ff:85:27:66  gen 1616  req 0
    created 88407500s  gen 1616  seen 15s  fortilink  gen 861
  vd root/0  e0:23:ff:85:27:82  gen 1389  req 0
    created 88407522s  gen 1389  seen 22s  fortilink  gen 647
  vd root/0  e0:23:ff:85:2b:02  gen 1375  req 0
    created 88407522s  gen 1375  seen 22s  fortilink  gen 633
  vd root/0  e0:23:ff:85:2b:1e  gen 1453  req 0
    created 88407521s  gen 1453  seen 22s  fortilink  gen 711
  vd root/0  e0:23:ff:85:2b:9c  gen 1555  req 0
    created 88407507s  gen 1555  seen 1s  fortilink  gen 809
  vd root/0  e0:23:ff:85:2f:1c  gen 1541  req 0
    created 88407520s  gen 1541  seen 22s  fortilink  gen 799
  vd root/0  e0:23:ff:85:2e:4a  gen 1643009  req 0
    created 88407520s  gen 1546  seen 22s  fortilink  gen 195589
  vd root/0  e0:23:ff:85:2f:54  gen 1619  req 0
    created 88407498s  gen 1619  seen 22s  fortilink  gen 864
  vd root/0  e0:23:ff:85:2b:e2  gen 1451  req 0
    created 88407521s  gen 1451  seen 22s  fortilink  gen 709
  vd root/0  ae:d4:e2:3f:aa:9a  gen 14126578  req OUA/34
    created 2352820s  gen 14126524  seen 2350736s  CORP WIRELESS  gen 426220
    ip 10.210.68.97  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  e0:23:ff:85:37:a4  gen 1643523  req 0
    created 88407503s  gen 1606  seen 22s  fortilink  gen 195671
  vd root/0  e0:23:ff:85:36:e0  gen 1498  req 0
    created 88407520s  gen 1498  seen 22s  fortilink  gen 756
  vd root/0  e0:23:ff:85:37:ce  gen 1643191  req 0
    created 88407520s  gen 1549  seen 22s  fortilink  gen 195627
  vd root/0  e0:23:ff:85:39:8e  gen 1643706  req 0
    created 88407520s  gen 1481  seen 22s  fortilink  gen 195703
  vd root/0  e0:23:ff:85:39:b8  gen 1522  req 0
    created 88407520s  gen 1522  seen 10s  fortilink  gen 780
  vd root/0  e0:23:ff:85:3a:98  gen 1512  req 0
    created 88407520s  gen 1512  seen 22s  fortilink  gen 770
  vd root/0  e0:23:ff:85:3c:66  gen 1476  req 0
    created 88407520s  gen 1476  seen 22s  fortilink  gen 734
  vd root/0  e0:23:ff:85:39:d4  gen 9523277  req OUA/34
    created 88407503s  gen 1604  seen 22s  ENG_LANC  gen 320107
    ip 192.168.1.99  src arp
    hardware vendor 'Fortinet'  src dhcp  id 160  weight 220
    type 'Network Generic'  src dhcp  id 160  weight 220
    family 'FortiSwitchRugged'  src dhcp  id 160  weight 220
    os 'FortiSwitchRugged OS'  src dhcp  id 160  weight 220
    hardware version '112D-POE'  src dhcp  id 160  weight 220
    host 'SR12DPTD20002587'  src dhcp
  vd root/0  e0:23:ff:85:39:d5  gen 9180325  req OHUSA/3e
    created 88407503s  gen 1611  seen 22s  ENG_LANC  gen 313593
  vd root/0  e0:23:ff:85:3b:f6  gen 1642459  req 0
    created 88407520s  gen 1490  seen 22s  fortilink  gen 195526
  vd root/0  92:8b:96:fb:e8:ec  gen 15234802  req OUA/34
    created 460958s  gen 15232338  seen 448789s  Guest  gen 445085
    ip 172.176.0.33  src mac
    hardware vendor 'Samsung'  src dhcp  id 182  weight 232
    type 'Phone'  src dhcp  id 182  weight 232
    family 'Galaxy'  src dhcp  id 182  weight 232
    os 'Android'  src dhcp  id 182  weight 232
    hardware version 'S24-Ultra'  src dhcp  id 182  weight 232
    software version '16'  src dhcp  id 182  weight 232
    host 'Galaxy-S24-Ultra'  src dhcp
  vd root/0  8e:20:12:5a:73:5d  gen 15467008  req OUA/34
    created 4322480s  gen 13098572  seen 1542s  Guest  gen 449619
    ip 172.176.0.8  src arp
    hardware vendor 'Apple'  src dns  id 5005  weight 230
    type 'Phone'  src dns  id 5005  weight 230
    family 'iPhone'  src dns  id 5005  weight 230
    os 'iOS'  src dns  id 5005  weight 230
    hardware version '14 Pro'  src dns  id 5005  weight 230
    host 'iPhone'  src dhcp
  vd root/0  36:01:2c:83:6e:f1  gen 15452517  req OUA/34
    created 55581506s  gen 537781  seen 12s  Guest  gen 449324
    ip 172.176.0.30  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    hardware version '11'  src dns  id 4940  weight 230
    software version '17.5.1'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  4c:eb:bd:a4:e6:cd  gen 15384647  req OUA/34
    created 8080002s  gen 11804234  seen 162332s  CORP WIRELESS  gen 448008
    ip 10.210.68.14  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'LAPTOP-41CH83MV'  src dhcp
  vd root/0  00:24:ae:08:5d:19  gen 350197  req OHUSA/3e
    created 68405262s  gen 190208  seen 14s  SECURITY_READER  gen 160314
    ip 10.210.36.36  src arp
  vd root/0  00:24:ae:08:5d:55  gen 350349  req OHUSA/3e
    created 68419913s  gen 190066  seen 12s  SECURITY_READER  gen 160317
    ip 10.210.36.32  src arp
  vd root/0  00:24:ae:08:5d:5b  gen 12359410  req OHUSA/3e
    created 68432403s  gen 189911  seen 1s  SECURITY_READER  gen 389473
    ip 10.210.36.34  src arp
  vd root/0  00:24:ae:08:5d:60  gen 965555  req OHUSA/3e
    created 68411627s  gen 190131  seen 1s  SECURITY_READER  gen 179153
    ip 10.210.36.39  src arp
  vd root/0  00:24:ae:08:5d:6f  gen 348735  req OHUSA/3e
    created 68409045s  gen 190158  seen 1s  SECURITY_READER  gen 160312
    ip 10.210.36.31  src arp
  vd root/0  00:24:ae:08:5d:7d  gen 348556  req OHUSA/3e
    created 68400581s  gen 190281  seen 12s  SECURITY_READER  gen 160316
    ip 10.210.36.30  src arp
  vd root/0  00:24:ae:08:5d:83  gen 350656  req OHUSA/3e
    created 68441531s  gen 189794  seen 0s  SECURITY_READER  gen 160320
    ip 10.210.36.38  src arp
  vd root/0  00:24:ae:08:5d:8a  gen 12359563  req OHUSA/3e
    created 12804059s  gen 10134854  seen 0s  SECURITY_READER  gen 389476
    ip 10.210.36.35  src arp
  vd root/0  00:24:ae:08:5d:b3  gen 350742  req OHUSA/3e
    created 68445735s  gen 189743  seen 0s  SECURITY_READER  gen 160319
    ip 10.210.36.33  src arp
  vd root/0  00:24:ae:08:5d:ed  gen 348736  req OHUSA/3e
    created 68418653s  gen 190078  seen 15s  SECURITY_READER  gen 160315
    ip 10.210.36.37  src arp
  vd root/0  80:19:34:6f:27:78  gen 15212007  req OUA/34
    created 35571526s  gen 3654358  seen 468296s  Guest  gen 444713
    ip 172.176.0.14  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'Africcii'  src dhcp
  vd root/0  fe:f8:62:c5:31:9f  gen 15450278  req OUA/34
    created 6408751s  gen 12273450  seen 5943s  Guest  gen 449276
    ip 172.176.0.15  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.3.1'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:90:0b:c1:a5:da  gen 7875212  req OHUA/3c
    created 28445038s  gen 5276296  seen 22s  VMWare_MGT  gen 288105
    ip 10.210.6.71  src arp
    os 'Linux'  src tcp  id 1624  weight 90
  vd root/0  5e:e2:80:87:ff:68  gen 15199634  req OUA/34
    created 5457728s  gen 12624496  seen 516757s  Guest  gen 444533
    ip 172.176.0.43  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.7'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  fa:e1:a1:5d:93:e3  gen 15462685  req OUA/34
    created 4322635s  gen 13098498  seen 1282s  CORP WIRELESS  gen 449539
    ip 10.210.68.30  src mac
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  ae:da:4f:4f:2a:84  gen 15244891  req OUA/34
    created 5974711s  gen 12418847  seen 179446s  CORP WIRELESS  gen 445361
    ip 10.210.68.20  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.4.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  a2:69:fc:43:ed:e5  gen 15459438  req OUA/34
    created 87962714s  gen 7163  seen 4646s  Guest  gen 449478
    ip 172.176.0.5  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '16.6.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  2c:6d:c1:72:54:70  gen 14481638  req OUA/34
    created 15135801s  gen 9414819  seen 1734142s  Guest  gen 432083
    ip 172.176.0.34  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'Purple'  src dhcp
  vd root/0  ae:bd:19:df:8e:a8  gen 15407581  req OUA/34
    created 29756778s  gen 4929849  seen 83788s  CORP WIRELESS  gen 448424
    ip 10.210.68.18  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'A12'  src dhcp  id 182  weight 232
    software version '13'  src dhcp  id 133  weight 255
    host 'Galaxy-A12'  src dhcp
  vd root/0  e0:23:ff:94:75:5d  gen 855  req 0
    created 88407669s  gen 46  seen 0s  L3_Link  gen 33
    type 'Router'  src ttl  id 0  weight 0
  vd root/0  e0:23:ff:94:75:5e  gen 473782  req OUA/34
    created 88407690s  gen 2  seen 1s  L3_Link  gen 2
    ip 172.30.75.8  src lldp
    host 'ZRH11-DSW-M2'  src lldp
  vd root/0  ae:7f:e4:8c:fe:ea  gen 15451822  req OUA/34
    created 16351845s  gen 8966868  seen 31847s  CORP WIRELESS  gen 449317
    ip 10.210.68.79  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  e0:23:ff:94:7a:f3  gen 1653496  req 0
    created 51317766s  gen 1366995  seen 2s  L3_Link  gen 191482
    type 'Router'  src ttl  id 0  weight 0
  vd root/0  e0:23:ff:94:7a:f4  gen 473542  req OUA/34
    created 88407691s  gen 1  seen 1s  L3_Link  gen 167069
    ip 172.30.75.7  src lldp
    hardware vendor 'Fortinet'  src lldp  id 1478  weight 255
    type 'Network Generic'  src lldp  id 1478  weight 255
    family 'FortiSwitch'  src lldp  id 1478  weight 255
    os 'FortiSwitch OS'  src lldp  id 1478  weight 255
    hardware version '1024D'  src lldp  id 1478  weight 255
    software version '6.4.5 Build 0461'  src lldp  id 1478  weight 255
    host 'ZRH11-DSW-M1'  src lldp
  vd root/0  2c:ea:7f:fd:5a:b8  gen 150052  req OUA/34
    created 88407658s  gen 792  seen 21s  ESXMGMT  gen 337
    ip 10.210.8.34  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX17'  src dns
  vd root/0  2c:ea:7f:fd:5c:b0  gen 298509  req OUA/34
    created 88407658s  gen 795  seen 22s  ESXMGMT  gen 150267
    ip 10.210.8.32  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX16'  src dns
  vd root/0  2c:ea:7f:fd:65:f2  gen 150054  req OUA/34
    created 88407658s  gen 785  seen 21s  ESXMGMT  gen 336
    ip 10.210.8.30  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX15'  src dns
  vd root/0  ea:6b:51:cb:e1:e0  gen 14894217  req OUA/34
    created 87036975s  gen 15509  seen 4s  CORP WIRELESS  gen 439331
    ip 10.210.68.22  src arp
    hardware vendor 'Apple'  src http  id 930  weight 230
    type 'Tablet'  src http  id 930  weight 230
    family 'iPad'  src http  id 930  weight 230
    os 'iPadOS'  src http  id 930  weight 230
    hardware version 'Air'  src dns  id 4605  weight 230
    software version '16.6'  src http  id 930  weight 230
    host 'Joaos-iPad'  src dns
  vd root/0  e0:23:ff:9a:00:4d  gen 2182  req 0
    created 88407527s  gen 1247  seen 21s  fortilink  gen 507
    host 'S448DFTF20003200'  src capwap
  vd root/0  52:3c:65:bc:35:94  gen 15381181  req OUA/34
    created 1136728s  gen 14838416  seen 170138s  CORP WIRELESS  gen 447948
    ip 10.210.68.55  src mac
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S5 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'To-S25-Ultra-tou-tes-DRIMIS'  src dhcp
  vd root/0  e0:23:ff:9a:05:5d  gen 1656841  req 0
    created 88407527s  gen 1240  seen 22s  fortilink  gen 196264
  vd root/0  e0:23:ff:9a:07:43  gen 1245  req 0
    created 88407527s  gen 1244  seen 21s  fortilink  gen 505
  vd root/0  e0:23:ff:9a:0b:0f  gen 2131  req 0
    created 88407526s  gen 1253  seen 12s  fortilink  gen 512
    host 'S448DFTF20003251'  src capwap
  vd root/0  ce:44:96:e5:59:30  gen 14235162  req OUA/34
    created 2169573s  gen 14235160  seen 2161627s  Guest  gen 427893
    ip 172.176.0.12  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  2c:ea:7f:fd:99:e8  gen 150034  req OUA/34
    created 88407658s  gen 793  seen 22s  ESXMGMT  gen 338
    ip 10.210.8.36  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX18'  src dns
  vd root/0  2c:ea:7f:fd:bb:d8  gen 150030  req OUA/34
    created 88407658s  gen 780  seen 22s  ESXMGMT  gen 333
    ip 10.210.8.22  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX11'  src dns
  vd root/0  2c:ea:7f:fd:c1:4e  gen 298390  req OUA/34
    created 88407656s  gen 856  seen 22s  ESXMGMT  gen 150217
    ip 10.210.8.24  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX12'  src dns
  vd root/0  2c:ea:7f:fd:be:d2  gen 298484  req OUA/34
    created 88407658s  gen 796  seen 16s  ESXMGMT  gen 150249
    ip 10.210.8.28  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX14'  src dns
  vd root/0  2c:ea:7f:fd:bf:c2  gen 150047  req OUA/34
    created 88407658s  gen 783  seen 10s  ESXMGMT  gen 335
    ip 10.210.8.26  src mac
    hardware vendor 'Dell'  src dhcp  id 173  weight 128
    type 'Server'  src dhcp  id 173  weight 128
    family 'DRAC'  src dhcp  id 173  weight 128
    host 'iDRAC-ZRH11CORPESX13'  src dns
  vd root/0  4a:83:68:75:a7:d0  gen 14223348  req OUSA/36
    created 2362268s  gen 14121118  seen 2180018s  CORP WIRELESS  gen 427690
    ip 10.210.68.94  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Markos-Iphone'  src dns
  vd root/0  0e:95:a9:83:2f:89  gen 15392154  req OUA/34
    created 88278082s  gen 3874  seen 121345s  Guest  gen 448154
    ip 172.176.0.22  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '16.1.1'  src http  id 929  weight 230
    host 'Rons-iPhone'  src dns
  vd root/0  82:9b:6d:07:0a:fa  gen 15111263  req OUA/34
    created 2171503s  gen 14234168  seen 405348s  CORP WIRELESS  gen 442891
    ip 10.210.68.69  src arp
    hardware vendor 'Apple'  src dns  id 4605  weight 230
    type 'Tablet'  src dns  id 4605  weight 230
    family 'iPad'  src dns  id 4605  weight 230
    os 'iPadOS'  src dns  id 4605  weight 230
    hardware version 'Air'  src dns  id 4605  weight 230
    host 'iPad'  src dhcp
  vd root/0  6c:94:66:04:72:bb  gen 15319662  req OUA/34
    created 2885559s  gen 13820716  seen 293112s  Guest  gen 446801
    ip 172.176.0.18  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'ZRH-5CG13790NP.ant.amazon.com'  src dhcp
  vd root/0  6c:94:66:03:ad:0e  gen 14499646  req OUA/34
    created 1715061s  gen 14499640  seen 1714029s  Guest  gen 432484
    ip 172.176.0.14  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1444  weight 120
    host 'ZRH-IBRELA08'  src dhcp
  vd root/0  6c:94:66:06:59:a5  gen 15093547  req OHUSA/3e
    created 697121s  gen 15093546  seen 697116s  Guest  gen 442614
    ip 10.13.57.22  src arp
  vd root/0  e0:23:ff:99:e0:73  gen 1224  req 0
    created 88407529s  gen 1224  seen 0s  fortilink  gen 487
  vd root/0  d6:0c:bc:bc:7b:be  gen 15461966  req OUA/34
    created 6744559s  gen 12162523  seen 10831s  CORP WIRELESS  gen 449521
    ip 10.210.68.45  src mac
    hardware vendor 'Samsung'  src http  id 1093  weight 230
    type 'Phone'  src http  id 1093  weight 230
    family 'Galaxy'  src http  id 1093  weight 230
    os 'Android'  src http  id 1093  weight 230
    hardware version 'A'  src http  id 1093  weight 230
    software version '13'  src http  id 1093  weight 230
    host 'A32-de-Joseph'  src dhcp
  vd root/0  e0:23:ff:99:ef:37  gen 1656856  req 0
    created 88407529s  gen 1228  seen 22s  fortilink  gen 196265
  vd root/0  e0:23:ff:99:ef:6d  gen 1230  req 0
    created 88407528s  gen 1230  seen 22s  fortilink  gen 493
  vd root/0  e0:23:ff:99:f2:61  gen 1235  req 0
    created 88407528s  gen 1234  seen 22s  fortilink  gen 497
  vd root/0  e0:23:ff:99:f4:47  gen 1239  req 0
    created 88407527s  gen 1239  seen 22s  fortilink  gen 501
  vd root/0  e0:23:ff:99:f5:c1  gen 1252  req 0
    created 88407526s  gen 1252  seen 22s  fortilink  gen 511
  vd root/0  d4:76:a0:a1:5e:43  gen 1031  req 0
    created 88407605s  gen 1031  seen 19s  fortilink  gen 425
  vd root/0  a0:02:a5:c9:0e:14  gen 15294113  req OUA/34
    created 6168975s  gen 12353137  seen 343456s  Guest  gen 446345
    ip 172.176.0.39  src arp
    os 'Windows'  src http  id 7124  weight 130
    software version '11'  src http  id 7124  weight 130
    host 'STS930'  src dhcp
  vd root/0  b4:0e:de:e0:72:f2  gen 15407688  req OA/24
    created 88407663s  gen 616  seen 84390s  CORP WIRELESS  gen 448428
    ip 10.210.68.43  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-U4DKHPJ'  src dhcp
    user 'cpop'  src kerberos
  vd root/0  22:6c:d4:53:86:96  gen 15347518  req OUA/34
    created 88396523s  gen 1912  seen 37331s  Guest  gen 447350
    ip 172.176.0.2  src arp
    hardware vendor 'Apple'  src http  id 930  weight 230
    type 'Tablet'  src http  id 930  weight 230
    family 'iPad'  src http  id 930  weight 230
    os 'iPadOS'  src http  id 930  weight 230
    hardware version 'iPad'  src dns  id 4626  weight 230
    software version '16.6'  src http  id 930  weight 230
    host 'iPad'  src dns
  vd root/0  b4:0e:de:e0:a9:0c  gen 15452580  req OA/24
    created 43487417s  gen 2546609  seen 0s  CORP WIRELESS  gen 449327
    ip 10.210.68.35  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-33N72HC'  src dhcp
    user 'levi.mueller'  src kerberos
  vd root/0  00:50:06:17:fe:64  gen 15330359  req OUSA/36
    created 88407605s  gen 1020  seen 23s  ENG_LANA  gen 130805
    ip 10.210.132.103  src mac
    host 'AS-P-17FE64'  src dns
  vd root/0  00:50:06:17:fe:68  gen 15330350  req OUSA/36
    created 88407605s  gen 1024  seen 23s  ENG_LANA  gen 310762
    ip 10.210.132.101  src mac
    host 'AS-P-17FE68'  src dns
  vd root/0  00:50:06:17:fe:7a  gen 15418758  req OUSA/36
    created 88407605s  gen 1025  seen 23s  ENG_LANA  gen 210940
    ip 10.210.132.102  src mac
    host 'AS-P-17FE7A'  src dns
  vd root/0  0a:a1:40:ca:13:cb  gen 14538182  req OUA/34
    created 1650322s  gen 14538180  seen 1636578s  Guest  gen 433199
    ip 172.176.0.41  src arp
    hardware vendor 'Google'  src dhcp  id 6466  weight 220
    type 'Phone'  src dhcp  id 6466  weight 220
    family 'Pixel'  src dhcp  id 6466  weight 220
    os 'Android'  src dhcp  id 6466  weight 220
    hardware version '7a'  src dhcp  id 6466  weight 220
    software version '1'  src dhcp  id 6466  weight 220
    host 'Pixel-7a'  src dhcp
  vd root/0  da:6e:c9:7e:2b:20  gen 15409390  req OUA/34
    created 7247399s  gen 12015800  seen 83729s  CORP WIRELESS  gen 448467
    ip 10.210.68.31  src none
    hardware vendor 'Samsung'  src dhcp  id 182  weight 232
    type 'Phone'  src dhcp  id 182  weight 232
    family 'Galaxy'  src dhcp  id 182  weight 232
    os 'Android'  src dhcp  id 182  weight 232
    hardware version 'S24-Ultra'  src dhcp  id 182  weight 232
    software version '16'  src dhcp  id 182  weight 232
    host 'Galaxy-S24-Ultra'  src dhcp
  vd root/0  58:6c:25:a9:82:5b  gen 15240970  req OUA/34
    created 3747629s  gen 13345750  seen 445435s  Guest  gen 445274
    ip 172.176.0.40  src mac
    os 'Windows'  src http  id 1453  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'MAGNTBWX061'  src dhcp
  vd root/0  b4:0e:de:e0:cf:8b  gen 14772014  req OUA/34
    created 17374232s  gen 8634661  seen 1201469s  CORP WIRELESS  gen 437141
    ip 10.210.68.29  src arp
    type 'Desktop'  src dhcp  id 6502  weight 130
    os 'Windows'  src dhcp  id 6502  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-2BKELOH'  src dhcp
  vd root/0  d8:9b:3b:ef:3b:45  gen 15433322  req OUA/34
    created 70522s  gen 15432662  seen 34618s  Guest  gen 448974
    ip 172.176.0.4  src arp
    hardware vendor 'Huawei'  src dhcp  id 178  weight 220
    type 'Phone'  src dhcp  id 178  weight 220
    family 'Mate'  src dhcp  id 178  weight 220
    os 'Android'  src dhcp  id 178  weight 220
    hardware version '20 '  src dhcp  id 178  weight 220
    software version '10'  src http  id 1365  weight 130
    host 'HUAWEI_Mate_20_lite-6dafb'  src dhcp
  vd root/0  8a:e0:fe:a7:94:47  gen 14119242  req OUA/34
    created 2365775s  gen 14119227  seen 2364723s  Guest  gen 426069
    ip 172.176.0.26  src arp
    hardware vendor 'Apple'  src http  id 1744  weight 220
    type 'Tablet'  src http  id 1744  weight 220
    family 'iPad'  src http  id 1744  weight 220
    os 'iPadOS'  src http  id 1744  weight 220
    software version '17.6.1'  src http  id 1744  weight 220
    host 'Tonys-iPad'  src dns
  vd root/0  32:f9:91:fd:03:cf  gen 15466586  req OUA/34
    created 59108390s  gen 299917  seen 11s  CORP WIRELESS  gen 449611
    ip 10.210.68.6  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.3.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  06:92:f6:d7:fd:79  gen 15196495  req OUA/34
    created 12637069s  gen 10212995  seen 522440s  CORP WIRELESS  gen 444477
    ip 10.210.68.53  src arp
    hardware vendor 'Apple'  src dhcp  id 2675  weight 180
    type 'Phone'  src dhcp  id 2675  weight 180
    family 'iPhone'  src dhcp  id 2675  weight 180
    os 'iOS'  src dhcp  id 2675  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:00:5e:00:01:01  gen 1654093  req OHUA/3c
    created 88407669s  gen 44  seen 0s  L3_Link  gen 32
    ip 10.210.105.3  src mac
    hardware vendor 'HPE Enterprise'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'Switch'  src fortiguard  id 0  weight 255
    os 'HPE ComwareSoftware'  src fortiguard  id 0  weight 255
    hardware version 'HPE514048G4SFP_ELSWJL829A'  src fortiguard  id 0  weight 255
  vd root/0  6e:35:90:7b:22:0f  gen 14537747  req OUA/34
    created 1651091s  gen 14537745  seen 1639565s  Guest  gen 433182
    ip 172.176.0.39  src arp
    hardware vendor 'Samsung'  src dhcp  id 182  weight 232
    type 'Phone'  src dhcp  id 182  weight 232
    family 'Galaxy'  src dhcp  id 182  weight 232
    os 'Android'  src dhcp  id 182  weight 232
    hardware version 'S20-FE-5G'  src dhcp  id 182  weight 232
    software version '13'  src dhcp  id 182  weight 232
    host 'Galaxy-S20-FE-5G'  src dhcp
  vd root/0  fa:52:65:9e:2a:5e  gen 14299073  req OUA/34
    created 69827255s  gen 173900  seen 2053899s  Guest  gen 428903
    ip 172.176.0.8  src mac
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'S10'  src dhcp  id 182  weight 232
    software version '12'  src dhcp  id 133  weight 255
    host 'Kashoku-s-Galaxy-S10'  src dhcp
  vd root/0  00:19:05:18:48:a9  gen 15459681  req OHUSA/3e
    created 88407520s  gen 1543  seen 22s  ENG_LANA  gen 196257
    ip 10.210.132.100  src arp
  vd root/0  9e:83:0a:17:b6:68  gen 15232286  req OUA/34
    created 1066530s  gen 14877823  seen 432310s  CORP WIRELESS  gen 445080
    ip 10.210.68.56  src arp
    hardware vendor 'Apple'  src dns  id 3181  weight 150
    type 'Tablet'  src dns  id 3181  weight 150
    family 'iPad'  src dns  id 3181  weight 150
    os 'iPadOS'  src dns  id 3181  weight 150
    host 'iPad'  src dhcp
  vd root/0  e8:c8:29:40:8b:d4  gen 14891688  req OA/24
    created 56019994s  gen 467626  seen 1s  CORP WIRELESS  gen 439289
    ip 10.210.68.54  src tcp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-HD200G2'  src dhcp
    user 'Tony.Farrell'  src kerberos
  vd root/0  e8:c8:29:42:62:ec  gen 15451345  req OA/24
    created 56005224s  gen 471006  seen 3625s  CORP WIRELESS  gen 449307
    ip 10.210.68.26  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'DESKTOP-JPHHDDM'  src dhcp
    user 'KAndersen'  src kerberos
  vd root/0  06:80:97:5d:63:b1  gen 15458120  req OUA/34
    created 12643171s  gen 10211463  seen 18696s  CORP WIRELESS  gen 449448
    ip 10.210.68.41  src arp
    hardware vendor 'Apple'  src dhcp  id 3828  weight 200
    type 'Phone'  src dhcp  id 3828  weight 200
    family 'iPhone'  src dhcp  id 3828  weight 200
    os 'iOS'  src dhcp  id 3828  weight 200
    host 'iPhone'  src dhcp
  vd root/0  92:54:b8:54:e9:f5  gen 15287130  req OUA/34
    created 6150954s  gen 12359197  seen 354307s  CORP WIRELESS  gen 446183
    ip 10.210.68.76  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    software version '16'  src http  id 997  weight 230
    host 'Javi-s-S22'  src dhcp
  vd root/0  a6:f3:93:50:ac:f8  gen 15464785  req OUA/34
    created 22402002s  gen 6993999  seen 3s  Guest  gen 449580
    ip 172.176.0.14  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '18.6'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  38:87:d5:b6:0f:21  gen 14893154  req OUA/34
    created 1039876s  gen 14893153  seen 1039340s  CORP WIRELESS  gen 439318
    os 'Windows'  src dhcp  id 848  weight 128
    host 'VDC-732TZH3'  src dhcp
  vd root/0  66:fb:97:22:7f:79  gen 15277503  req OUA/34
    created 48131517s  gen 1862433  seen 367366s  Guest  gen 445972
    ip 172.176.0.32  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '16.6.1'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  e8:c8:29:42:d8:17  gen 15411009  req OA/24
    created 64733581s  gen 236018  seen 0s  CORP WIRELESS  gen 448514
    ip 10.210.68.47  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'kandersen'  src dhcp
    user 'KAndersen'  src kerberos
  vd root/0  b8:a4:4f:c8:d2:fd  gen 14641499  req OHUA/3c
    created 41651444s  gen 2810073  seen 5s  SECURITY_ExtDev  gen 435034
    ip 10.210.48.14  src arp
    hardware vendor 'Axis'  src sip  id 6990  weight 255
    type 'Intercom'  src sip  id 6990  weight 255
    family 'Network Video Intercom'  src sip  id 6990  weight 255
    os 'Axis OS'  src sip  id 6990  weight 255
    hardware version '\U1'  src sip  id 6990  weight 255
  vd root/0  b8:a4:4f:c8:d9:5d  gen 14641497  req OHUA/3c
    created 41657729s  gen 2809102  seen 0s  SECURITY_ExtDev  gen 435033
    ip 10.210.48.11  src arp
    hardware vendor 'Axis'  src sip  id 6990  weight 255
    type 'Intercom'  src sip  id 6990  weight 255
    family 'Network Video Intercom'  src sip  id 6990  weight 255
    os 'Axis OS'  src sip  id 6990  weight 255
    hardware version '\U1'  src sip  id 6990  weight 255
  vd root/0  46:b3:e6:50:0d:a1  gen 15303866  req OUA/34
    created 75318656s  gen 120556  seen 323342s  Guest  gen 446497
    ip 172.176.0.8  src arp
    hardware vendor 'Samsung'  src http  id 979  weight 255
    type 'Phone'  src http  id 979  weight 255
    family 'Galaxy'  src http  id 979  weight 255
    os 'Android'  src http  id 979  weight 255
    hardware version 'A'  src http  id 1093  weight 230
    software version '13'  src http  id 979  weight 255
    host 'DONTRA-s-A54'  src dhcp
  vd root/0  b8:a4:4f:cf:5b:64  gen 13238641  req OHUA/3c
    created 4761416s  gen 12916139  seen 9s  SECURITY_ExtDev  gen 402054
    ip 10.210.48.25  src arp
    hardware vendor 'Axis'  src sip  id 6990  weight 255
    type 'Intercom'  src sip  id 6990  weight 255
    family 'Network Video Intercom'  src sip  id 6990  weight 255
    os 'Axis OS'  src sip  id 6990  weight 255
    hardware version '\U1'  src sip  id 6990  weight 255
  vd root/0  be:a8:5c:3b:62:d7  gen 14121021  req OUA/34
    created 2362463s  gen 14121019  seen 2358123s  CORP WIRELESS  gen 426114
    ip 10.210.68.92  src arp
    hardware vendor 'Apple'  src dns  id 2654  weight 150
    type 'Laptop'  src dns  id 2654  weight 150
    family 'Mac'  src dns  id 2654  weight 150
    os 'macOS'  src dns  id 2654  weight 150
    hardware version 'MacBook Air'  src dns  id 2654  weight 150
    host 'Markos-MacBook-Air'  src dns
  vd root/0  b8:a4:4f:ce:92:f7  gen 14641500  req OHUA/3c
    created 41650070s  gen 2810279  seen 3s  SECURITY_ExtDev  gen 435035
    ip 10.210.48.12  src arp
    hardware vendor 'Axis'  src sip  id 6990  weight 255
    type 'Intercom'  src sip  id 6990  weight 255
    family 'Network Video Intercom'  src sip  id 6990  weight 255
    os 'Axis OS'  src sip  id 6990  weight 255
    hardware version '\U1'  src sip  id 6990  weight 255
  vd root/0  b6:06:53:a2:6e:27  gen 15452547  req OHUSA/3e
    created 1245089s  gen 14776592  seen 16446s  Guest  gen 449325
    ip 172.176.0.23  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
  vd root/0  3e:e1:47:51:98:e1  gen 15420531  req OUA/34
    created 36902427s  gen 3466532  seen 65245s  Guest  gen 448740
    ip 172.176.0.22  src mac
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'Z Fold6'  src dhcp  id 6704  weight 230
    software version '14'  src http  id 997  weight 230
    host 'Derick-s-Z-Fold6'  src dhcp
  vd root/0  8c:3b:4a:46:fe:ce  gen 14234529  req OUA/34
    created 2170892s  gen 14234522  seen 2161344s  CORP WIRELESS  gen 427881
    ip 10.210.68.73  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '11 Enterprise'  src http  id 6763  weight 130
    host '360-WIN11-BP'  src dhcp
  vd root/0  16:ab:1c:18:fc:34  gen 15299908  req OUA/34
    created 1199229s  gen 14803229  seen 330826s  Guest  gen 446432
    ip 172.176.0.14  src arp
    hardware vendor 'Samsung'  src http  id 1093  weight 230
    type 'Phone'  src http  id 1093  weight 230
    family 'Galaxy'  src http  id 1093  weight 230
    os 'Android'  src http  id 1093  weight 230
    hardware version 'A'  src http  id 1093  weight 230
    software version '16'  src http  id 1093  weight 230
    host 'DONTRA-s-A56'  src dhcp
  vd root/0  00:15:5d:2c:0c:00  gen 15093307  req OA/24
    created 57901640s  gen 312062  seen 0s  SECURITY_NVR  gen 442613
    ip 10.210.44.22  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'WIN-9RCUSO3LATC'  src dhcp
    user 'ps-lkaczmarski'  src kerberos
  vd root/0  00:15:5d:2c:0e:00  gen 15146795  req OA/24
    created 57901731s  gen 312050  seen 0s  SECURITY_NVR  gen 443560
    ip 10.210.44.24  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'WIN-3ELU0C0N803'  src dhcp
    user 'ps-lkaczmarski'  src kerberos
  vd root/0  96:aa:20:06:26:73  gen 15414230  req OUA/34
    created 725417s  gen 15076553  seen 105946s  CORP WIRELESS  gen 448602
    ip 10.210.68.73  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:15:5d:2c:10:00  gen 11710742  req OA/24
    created 57825491s  gen 313314  seen 0s  SECURITY_NVR  gen 370023
    ip 10.210.44.26  src arp
    os 'Windows'  src http  id 1453  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'WIN-3S7K4DD35QR'  src dhcp
    user 'ps-lkaczmarski'  src kerberos
  vd root/0  00:15:5d:2c:12:00  gen 14189193  req OA/24
    created 57901498s  gen 312065  seen 21s  SECURITY_NVR  gen 427138
    ip 10.210.44.27  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10 / 2016'  src mwbs  id 1489  weight 50
    host 'WIN-D6KNFTG8E8I'  src dhcp
    user 'ps-lkaczmarski'  src kerberos
  vd root/0  5e:5e:c6:48:84:1d  gen 15464111  req OUA/34
    created 6161376s  gen 12355724  seen 7221s  Guest  gen 449576
    ip 172.176.0.42  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    hardware version '11'  src dns  id 4940  weight 230
    software version '26.3.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  5c:88:16:f4:2e:13  gen 15436498  req OHUA/3c
    created 88407671s  gen 34  seen 18s  ENG_LANA  gen 196255
    ip 10.210.132.201  src arp
    hardware vendor 'Rockwell Automa'  src fortiguard  id 0  weight 136
    type 'Industry'  src fortiguard  id 0  weight 136
    family 'Industrial Device'  src fortiguard  id 0  weight 136
    os 'Windows CE'  src fortiguard  id 0  weight 136
  vd root/0  5c:88:16:f4:2d:81  gen 1656714  req OHUSA/3e
    created 88407522s  gen 1417  seen 18s  ENG_LANA  gen 195806
    ip 10.210.132.200  src arp
  vd root/0  4a:6b:e6:d6:bc:fc  gen 14122605  req OUA/34
    created 2359823s  gen 14122600  seen 2356021s  CORP WIRELESS  gen 426142
    ip 10.210.68.96  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  5c:88:16:f4:2e:ce  gen 11917124  req OHUSA/3e
    created 88407616s  gen 993  seen 18s  ENG_LANA  gen 403
    ip 10.210.132.203  src mac
  vd root/0  5c:88:16:f4:2e:ee  gen 1656715  req OHUSA/3e
    created 88407522s  gen 1416  seen 18s  ENG_LANA  gen 195805
    ip 10.210.132.202  src arp
  vd root/0  08:6a:c5:fd:ed:78  gen 15458607  req OA/24
    created 88405899s  gen 1745  seen 0s  CORP WIRELESS  gen 449462
    ip 10.210.68.9  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'VDC-9BB0DK3'  src dns
    user 'nbousslimi'  src kerberos
  vd root/0  00:90:5b:04:2b:56  gen 2552  req OHUSA/3e
    created 88407605s  gen 1029  seen 23s  ENG_LANC  gen 1171
    ip 10.210.140.194  src arp
  vd root/0  00:90:5b:04:2b:57  gen 1654711  req OHUSA/3e
    created 88407522s  gen 1434  seen 18s  ENG_LAND  gen 195953
    ip 10.210.144.38  src arp
  vd root/0  00:90:5b:04:2b:5c  gen 1656768  req OHUSA/3e
    created 88407520s  gen 1540  seen 22s  ENG_LANC  gen 196256
    ip 10.210.140.189  src arp
  vd root/0  c6:9c:20:70:22:09  gen 15447643  req OUA/34
    created 6940073s  gen 12099266  seen 35340s  Guest  gen 449236
    ip 172.176.0.12  src arp
    hardware vendor 'Apple'  src http  id 905  weight 230
    type 'Phone'  src http  id 905  weight 230
    family 'iPhone'  src http  id 905  weight 230
    os 'iOS'  src http  id 905  weight 230
    software version '26.3'  src http  id 905  weight 230
    host 'iPhone'  src dhcp
  vd root/0  00:90:5b:04:3e:5e  gen 1656682  req OHUSA/3e
    created 88407522s  gen 1444  seen 18s  ENG_LAND  gen 196238
    ip 10.210.144.190  src arp
  vd root/0  00:90:5b:04:48:6d  gen 8599096  req OHUSA/3e
    created 61605718s  gen 270301  seen 22s  ENG_LANC  gen 301458
    ip 10.210.140.190  src arp
  vd root/0  00:50:db:02:0f:ee  gen 12030094  req OHUSA/3e
    created 88407522s  gen 1442  seen 10s  ENG_LANB  gen 196237
    ip 10.210.136.104  src mac
  vd root/0  00:50:db:02:23:7e  gen 12030093  req OHUSA/3e
    created 88407521s  gen 1456  seen 7s  ENG_LANB  gen 196006
    ip 10.210.136.103  src mac
  vd root/0  00:50:db:02:45:79  gen 12014648  req OHUSA/3e
    created 88407605s  gen 1015  seen 8s  ENG_LANB  gen 272540
    ip 10.210.136.105  src mac
  vd root/0  ec:8e:77:cd:f6:8b  gen 15289895  req OUA/34
    created 36307218s  gen 3552811  seen 349741s  Guest  gen 446248
    ip 172.176.0.40  src arp
    os 'Windows'  src http  id 1077  weight 130
    software version '10'  src http  id 1453  weight 130
    host 'RatingMatters'  src dhcp
  vd root/0  92:35:69:76:95:d7  gen 15414865  req OUA/34
    created 6040158s  gen 12397100  seen 103185s  CORP WIRELESS  gen 448617
    ip 10.210.68.77  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S6 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Javi-s-S26-Ultra'  src dhcp
  vd root/0  a2:90:89:bc:ee:e9  gen 15437089  req OUA/34
    created 11896561s  gen 10525706  seen 39801s  Guest  gen 449068
    ip 172.176.0.8  src arp
    hardware vendor 'Xiaomi'  src dhcp  id 6583  weight 255
    type 'Phone'  src dhcp  id 6583  weight 255
    family 'Xiaomi'  src dhcp  id 6583  weight 255
    os 'Android'  src dhcp  id 6583  weight 255
    hardware version '11-Lite-5G-NE'  src dhcp  id 6583  weight 255
    software version '14'  src dhcp  id 6583  weight 255
    host 'Xiaomi-11-Lite-5G-NE'  src dhcp
  vd root/0  d4:76:a0:ba:cb:71  gen 12389208  req 0
    created 6062313s  gen 12389208  seen 21s  fortilink  gen 390297
  vd root/0  d4:76:a0:ba:ca:99  gen 238700  req 0
    created 88407605s  gen 1032  seen 21s  fortilink  gen 119959
  vd root/0  5c:88:16:f7:c2:20  gen 113  req OHUA/3c
    created 88407669s  gen 40  seen 0s  ENG_LANA  gen 30
    ip 10.210.132.176  src mac
    hardware vendor 'Rockwell Automa'  src fortiguard  id 0  weight 136
    type 'Industry'  src fortiguard  id 0  weight 136
    family 'Industrial Device'  src fortiguard  id 0  weight 136
    os 'Windows CE'  src fortiguard  id 0  weight 136
  vd root/0  4a:11:c8:2e:b4:63  gen 15405924  req OUA/34
    created 88278237s  gen 3863  seen 121319s  Guest  gen 448375
    ip 172.176.0.8  src arp
    hardware vendor 'Apple'  src dns  id 5005  weight 230
    type 'Phone'  src dns  id 5005  weight 230
    family 'iPhone'  src dns  id 5005  weight 230
    os 'iOS'  src dns  id 5005  weight 230
    hardware version '14 Pro'  src dns  id 5005  weight 230
    software version '16.6'  src http  id 929  weight 230
    host 'Ronaks-iPhone-2'  src dns
  vd root/0  00:30:de:59:c9:27  gen 15467602  req OHUSA/3e
    created 18567023s  gen 8213560  seen 20s  ENG_LANC  gen 449636
  vd root/0  00:30:de:59:c9:2d  gen 15467600  req OHUSA/3e
    created 18566726s  gen 8213785  seen 20s  ENG_LAND  gen 449635
    ip 10.210.144.90  src arp
  vd root/0  00:30:de:59:c7:b1  gen 15467590  req OHUSA/3e
    created 18566732s  gen 8213780  seen 20s  ENG_LAND  gen 449632
    ip 10.210.144.59  src arp
  vd root/0  00:30:de:59:c9:84  gen 15467599  req OHUSA/3e
    created 18566731s  gen 8213781  seen 19s  ENG_LAND  gen 449634
    ip 10.210.144.64  src arp
  vd root/0  00:30:de:59:c9:a2  gen 15467603  req OHUSA/3e
    created 18567022s  gen 8213561  seen 19s  ENG_LANC  gen 449637
    ip 10.210.140.64  src arp
  vd root/0  00:30:de:59:c9:d8  gen 15467593  req OHUSA/3e
    created 18567021s  gen 8213564  seen 19s  ENG_LANC  gen 449633
    ip 10.210.140.69  src arp
  vd root/0  00:30:de:59:c9:f9  gen 1683148  req OHUSA/3e
    created 49420938s  gen 1683147  seen 2s  ENG_LANC  gen 196740
    ip 10.210.140.73  src mac
  vd root/0  72:e1:c5:0f:1f:0e  gen 15423981  req OUA/34
    created 26091147s  gen 5913440  seen 87085s  Guest  gen 448800
    ip 172.176.0.44  src arp
    hardware vendor 'Apple'  src http  id 3271  weight 255
    type 'Laptop'  src http  id 3271  weight 255
    family 'Mac'  src http  id 3271  weight 255
    os 'macOS'  src http  id 3271  weight 255
    hardware version 'MacBook Pro'  src dhcp  id 3684  weight 180
    software version '15.6'  src http  id 3271  weight 255
    host 'MacBookPro'  src dhcp
  vd root/0  14:23:f2:9f:73:30  gen 2114062  req HU/18
    created 80956549s  gen 69847  seen 22s  Nessus  gen 201132
  vd root/0  14:23:f2:9f:73:31  gen 2114061  req HU/18
    created 80956549s  gen 69846  seen 22s  Nessus  gen 201131
  vd root/0  7a:d3:45:93:b9:2a  gen 15460867  req OUA/34
    created 43998398s  gen 2462285  seen 12933s  CORP WIRELESS  gen 449509
    ip 10.210.68.24  src arp
    hardware vendor 'Apple'  src dns  id 5008  weight 230
    type 'Phone'  src dns  id 5008  weight 230
    family 'iPhone'  src dns  id 5008  weight 230
    os 'iOS'  src dns  id 5008  weight 230
    hardware version '12 Pro'  src dns  id 5008  weight 230
    host 'Shaun-iPhone-12'  src dns
  vd root/0  54:3a:d6:db:7d:96  gen 15238577  req OUA/34
    created 88332253s  gen 3106  seen 449424s  CORP WIRELESS  gen 445223
    ip 10.210.68.40  src mac
    hardware vendor 'Samsung'  src ssdp  id 4025  weight 255
    type 'Television'  src ssdp  id 4025  weight 255
    family 'Smart TV'  src ssdp  id 4025  weight 255
    os 'Tizen'  src http  id 1066  weight 230
    hardware version 'QAQ85'  src http  id 5303  weight 230
    software version '6.0'  src http  id 1066  weight 230
    host 'Samsung'  src dhcp
  vd root/0  92:07:76:cc:1f:91  gen 15460287  req OUSA/36
    created 15003s  gen 15460286  seen 14734s  CORP WIRELESS  gen 449497
    host 'Watch'  src dhcp
  vd root/0  e4:30:22:1b:c1:b6  gen 132660  req OHUSA/3e
    created 78377696s  gen 92855  seen 5s  SECURITY_ExtDev  gen 69999
    ip 10.210.48.142  src mac
  vd root/0  e4:30:22:1b:c1:b8  gen 479  req OHUSA/3e
    created 88407667s  gen 478  seen 5s  SECURITY_ExtDev  gen 227
    ip 10.210.48.169  src mac
  vd root/0  e4:30:22:1b:c1:b9  gen 339  req OHUSA/3e
    created 88407668s  gen 338  seen 7s  SECURITY_CAMERA  gen 154
    ip 10.210.32.85  src mac
  vd root/0  e4:30:22:1b:c1:ba  gen 15421277  req OHUSA/3e
    created 88407667s  gen 474  seen 7s  SECURITY_ExtDev  gen 448752
    ip 10.210.48.127  src mac
  vd root/0  e4:30:22:1b:c1:be  gen 426  req OHUSA/3e
    created 88407667s  gen 410  seen 3s  SECURITY_ExtDev  gen 190
    ip 10.210.48.166  src mac
  vd root/0  e4:30:22:1b:c1:bf  gen 484  req OHUSA/3e
    created 88407667s  gen 483  seen 5s  SECURITY_ExtDev  gen 229
    ip 10.210.48.159  src mac
  vd root/0  e4:30:22:1b:c1:c2  gen 477  req OHUSA/3e
    created 88407667s  gen 476  seen 6s  SECURITY_ExtDev  gen 226
    ip 10.210.48.165  src mac
  vd root/0  e4:30:22:1b:c1:c3  gen 6996630  req OHUSA/3e
    created 88407667s  gen 409  seen 3s  SECURITY_ExtDev  gen 274071
    ip 10.210.48.134  src mac
  vd root/0  e4:30:22:1b:c1:c5  gen 6996672  req OHUSA/3e
    created 79151665s  gen 86332  seen 3s  SECURITY_ExtDev  gen 274073
    ip 10.210.48.135  src mac
  vd root/0  e4:30:22:1b:c1:c6  gen 422  req OHUSA/3e
    created 88407667s  gen 414  seen 3s  SECURITY_ExtDev  gen 193
    ip 10.210.48.160  src mac
  vd root/0  e4:30:22:1b:c1:c9  gen 14641516  req OHUSA/3e
    created 88407668s  gen 334  seen 7s  SECURITY_CAMERA  gen 435042
    ip 10.210.32.118  src mac
  vd root/0  e4:30:22:1b:c1:ca  gen 443  req OHUSA/3e
    created 88407667s  gen 442  seen 3s  SECURITY_ExtDev  gen 209
    ip 10.210.48.155  src mac
  vd root/0  e4:30:22:1b:c1:cb  gen 440  req OHUSA/3e
    created 88407667s  gen 416  seen 2s  SECURITY_ExtDev  gen 195
    ip 10.210.48.164  src mac
  vd root/0  e4:30:22:1b:c1:cd  gen 6996894  req OHUSA/3e
    created 88407667s  gen 419  seen 5s  SECURITY_ExtDev  gen 274075
    ip 10.210.48.129  src mac
  vd root/0  e4:30:22:1b:c1:ce  gen 6997034  req OHUSA/3e
    created 88407667s  gen 417  seen 5s  SECURITY_ExtDev  gen 274086
    ip 10.210.48.131  src mac
  vd root/0  e4:30:22:1b:c1:d0  gen 486  req OHUSA/3e
    created 88407667s  gen 485  seen 5s  SECURITY_ExtDev  gen 230
    ip 10.210.48.168  src mac
  vd root/0  e4:30:22:1b:c1:d1  gen 503  req OHUSA/3e
    created 88407667s  gen 418  seen 3s  SECURITY_ExtDev  gen 197
    ip 10.210.48.138  src mac
  vd root/0  e4:30:22:1b:c1:d2  gen 441  req OHUSA/3e
    created 88407667s  gen 423  seen 3s  SECURITY_ExtDev  gen 200
    ip 10.210.48.156  src mac
  vd root/0  e4:30:22:1b:c1:d3  gen 14641515  req OHUSA/3e
    created 7779785s  gen 11889640  seen 6s  SECURITY_ExtDev  gen 435041
    ip 10.210.48.122  src mac
  vd root/0  e4:30:22:1b:c1:d4  gen 14641512  req OHUSA/3e
    created 3727930s  gen 13354463  seen 3s  SECURITY_ExtDev  gen 435038
    ip 10.210.48.121  src mac
  vd root/0  e4:30:22:1b:c1:d5  gen 14641513  req OHUSA/3e
    created 88407667s  gen 452  seen 6s  SECURITY_ExtDev  gen 435039
    ip 10.210.48.120  src mac
  vd root/0  e4:30:22:1a:f8:77  gen 1563548  req OHUSA/3e
    created 88407668s  gen 204  seen 7s  SECURITY_CAMERA  gen 194897
    ip 10.210.32.125  src mac
  vd root/0  e4:30:22:1a:f8:7f  gen 6994883  req OHUSA/3e
    created 88407667s  gen 504  seen 3s  SECURITY_ExtDev  gen 274011
    ip 10.210.48.126  src mac
  vd root/0  12:58:7b:bf:af:3a  gen 15459163  req OUA/34
    created 18871s  gen 15458376  seen 16836s  CORP WIRELESS  gen 449472
    ip 10.210.68.48  src arp
    hardware vendor 'Samsung'  src dhcp  id 6732  weight 230
    type 'Phone'  src dhcp  id 6732  weight 230
    family 'Galaxy'  src dhcp  id 6732  weight 230
    os 'Android'  src dhcp  id 6732  weight 230
    hardware version 'S6 Ultra'  src dhcp  id 6732  weight 230
    software version '16'  src dhcp  id 6732  weight 230
    host 'Javi-s-S26-Ultra'  src dhcp
  vd root/0  ac:1f:6b:3f:0e:70  gen 8936704  req OHUSA/3e
    created 16417873s  gen 8936703  seen 22s  NET_MANAGEMENT  gen 309107
    ip 10.210.100.25  src arp
  vd root/0  ac:1f:6b:3f:11:4d  gen 8938965  req OHUSA/3e
    created 16415847s  gen 8938963  seen 22s  NET_MANAGEMENT  gen 309125
    ip 10.210.100.23  src arp
  vd root/0  00:30:de:61:6d:89  gen 15442013  req OHUSA/3e
    created 49419120s  gen 1683398  seen 22s  ENG_LANC  gen 196743
    ip 10.210.140.72  src mac
  vd root/0  00:30:de:61:6d:8f  gen 15418759  req OHUSA/3e
    created 52624055s  gen 1153031  seen 20s  ENG_LANC  gen 199393
    ip 10.210.140.58  src arp
  vd root/0  00:30:de:61:6d:a7  gen 15451835  req OHUSA/3e
    created 51256596s  gen 1376765  seen 20s  ENG_LAND  gen 199392
    ip 10.210.144.89  src arp
  vd root/0  ac:1f:6b:3f:2c:a1  gen 8940650  req OHUSA/3e
    created 16413730s  gen 8940649  seen 22s  NET_MANAGEMENT  gen 309143
    ip 10.210.100.21  src arp
  vd root/0  00:30:de:60:a9:53  gen 15436497  req OHUSA/3e
    created 49444069s  gen 1679259  seen 19s  ENG_LANC  gen 199397
    ip 10.210.140.68  src arp
  vd root/0  00:30:de:60:a9:7d  gen 15451836  req OHUSA/3e
    created 50110829s  gen 1563606  seen 19s  ENG_LAND  gen 199396
    ip 10.210.144.63  src arp
  vd root/0  00:30:de:60:a9:86  gen 15432811  req OHUSA/3e
    created 53230472s  gen 1050072  seen 20s  ENG_LAND  gen 199384
    ip 10.210.144.58  src arp
  vd root/0  00:30:de:60:a9:8f  gen 15384665  req OHUSA/3e
    created 51945279s  gen 1265031  seen 19s  ENG_LANC  gen 199395
    ip 10.210.140.63  src arp
  vd root/0  c2:3a:1f:27:2d:8c  gen 14525588  req OUA/34
    created 13883903s  gen 9798460  seen 1654683s  Guest  gen 432921
    ip 172.176.0.24  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.2.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  c4:00:ad:7a:4b:c5  gen 2016  req OHUA/3c
    created 88407663s  gen 598  seen 23s  ENG_LANA  gen 261
    ip 10.210.132.115  src arp
    hardware vendor 'Advantech'  src mac  id 0  weight 120
    os 'Windows'  src dhcp  id 848  weight 128
  vd root/0  c4:00:ad:7c:32:60  gen 10382022  req OHUA/3c
    created 88407498s  gen 1620  seen 22s  ENG_LANA  gen 339160
    ip 10.210.132.113  src arp
    hardware vendor 'Advantech'  src mac  id 0  weight 120
    os 'Windows'  src dhcp  id 848  weight 128
  vd root/0  c4:00:ad:7c:32:63  gen 898  req OHUA/3c
    created 88407663s  gen 612  seen 20s  ENG_LANA  gen 264
    ip 10.210.132.114  src arp
    hardware vendor 'Advantech'  src mac  id 0  weight 120
    os 'Windows'  src dhcp  id 848  weight 128
  vd root/0  7e:ba:43:d2:3a:8d  gen 15406845  req OUA/34
    created 1303366s  gen 14741612  seen 121491s  Guest  gen 448402
    ip 172.176.0.19  src arp
    hardware vendor 'Apple'  src dhcp  id 3831  weight 200
    type 'Watch'  src dhcp  id 3831  weight 200
    family 'Watch'  src dhcp  id 3831  weight 200
    os 'watchOS'  src dhcp  id 3831  weight 200
    host 'Watch'  src dhcp
  vd root/0  56:d1:8a:9f:d0:b5  gen 15378011  req OUA/34
    created 42021051s  gen 2760744  seen 149338s  Guest  gen 447891
    ip 172.176.0.14  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '18.1.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  e4:30:22:26:3b:92  gen 333  req OHUSA/3e
    created 88407668s  gen 332  seen 7s  SECURITY_CAMERA  gen 151
    ip 10.210.32.152  src mac
  vd root/0  82:74:3e:ff:f0:5f  gen 15452920  req OUA/34
    created 7919813s  gen 11849119  seen 39s  Guest  gen 449337
    ip 172.176.0.34  src arp
    hardware vendor 'Apple'  src http  id 902  weight 230
    type 'Phone'  src http  id 902  weight 230
    family 'iPhone'  src http  id 902  weight 230
    os 'iOS'  src http  id 902  weight 230
    software version '26.3.1'  src http  id 902  weight 230
    host 'iPhone'  src dhcp
  vd root/0  a2:56:70:9e:d9:1e  gen 14926979  req OUA/34
    created 2360033s  gen 14122497  seen 979232s  CORP WIRELESS  gen 439875
    ip 10.210.68.95  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'Pixel-10-Pro-XL'  src dhcp
  vd root/0  3e:1c:0a:f5:28:a3  gen 15450352  req OUA/34
    created 725310s  gen 15076640  seen 6719s  Guest  gen 449280
    ip 172.176.0.20  src mac
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'S20-5G'  src dhcp  id 182  weight 232
    software version '13'  src dhcp  id 133  weight 255
    host 'Galaxy-S20-5G'  src dhcp
  vd root/0  e4:0d:36:b2:d8:24  gen 14833921  req OUA/34
    created 1144604s  gen 14833902  seen 1125912s  Guest  gen 438225
    ip 172.176.0.41  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'PC-JA'  src dhcp
  vd root/0  10:df:fc:02:07:81  gen 15446034  req OUSA/36
    created 88407524s  gen 1329  seen 20s  ENG_LANC  gen 195980
    ip 10.210.140.173  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  10:df:fc:02:07:a8  gen 15438062  req OHUSA/3e
    created 88407520s  gen 1499  seen 22s  ENG_LAND  gen 196015
    ip 10.210.144.143  src arp
  vd root/0  10:df:fc:02:07:c6  gen 15460652  req OHUSA/3e
    created 88407520s  gen 1501  seen 22s  ENG_LAND  gen 196017
    ip 10.210.144.142  src arp
  vd root/0  10:df:fc:02:07:e4  gen 15460494  req OUSA/36
    created 88407524s  gen 1335  seen 20s  ENG_LANC  gen 195984
    ip 10.210.140.172  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  e4:30:22:28:2e:24  gen 193  req OHUSA/3e
    created 88407668s  gen 192  seen 7s  SECURITY_CAMERA  gen 81
    ip 10.210.32.67  src mac
  vd root/0  e4:30:22:28:2e:26  gen 303  req OHUSA/3e
    created 88407668s  gen 302  seen 7s  SECURITY_CAMERA  gen 136
    ip 10.210.32.151  src mac
  vd root/0  e6:cf:2d:b5:e9:03  gen 15465788  req OUA/34
    created 121789s  gen 15406711  seen 3325s  CORP WIRELESS  gen 449601
    ip 10.210.68.15  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  d4:76:a0:cc:63:b0  gen 10355770  req OUA/34
    created 88407659s  gen 695  seen 0s  WIRELESS_APs  gen 296
    ip 10.210.96.9  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026480'  src capwap
  vd root/0  be:99:02:7e:fe:a6  gen 15211034  req OUA/34
    created 18994578s  gen 8052530  seen 63793s  CORP WIRELESS  gen 444694
    ip 10.210.68.39  src arp
    hardware vendor 'Apple'  src http  id 930  weight 230
    type 'Tablet'  src http  id 930  weight 230
    family 'iPad'  src http  id 930  weight 230
    os 'iPadOS'  src http  id 930  weight 230
    hardware version 'Air'  src dns  id 4628  weight 200
    software version '18.6.2'  src http  id 930  weight 230
    host 'iPad'  src dhcp
  vd root/0  d4:76:a0:cc:63:d0  gen 7671365  req OUA/34
    created 88407659s  gen 704  seen 0s  WIRELESS_APs  gen 301
    ip 10.210.96.49  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026481'  src capwap
  vd root/0  d4:76:a0:cc:66:70  gen 12389289  req OUA/34
    created 88407662s  gen 641  seen 0s  WIRELESS_APs  gen 390302
    ip 10.210.96.40  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026502'  src capwap
  vd root/0  d4:76:a0:cc:65:d0  gen 6971327  req OUA/34
    created 88407659s  gen 701  seen 0s  WIRELESS_APs  gen 299
    ip 10.210.96.55  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026497'  src capwap
  vd root/0  10:df:fc:02:23:23  gen 14405976  req OHUSA/3e
    created 88407520s  gen 1482  seen 15s  ENG_LAND  gen 195954
    ip 10.210.144.161  src arp
  vd root/0  10:df:fc:02:23:24  gen 1654730  req OHUSA/3e
    created 88407520s  gen 1488  seen 22s  ENG_LAND  gen 195959
  vd root/0  10:df:fc:03:02:24  gen 936944  req OHUSA/3e
    created 88407520s  gen 1524  seen 5s  ENG_LAND  gen 782
    ip 10.210.144.102  src arp
  vd root/0  10:df:fc:03:02:25  gen 1655003  req OHUSA/3e
    created 88407520s  gen 1517  seen 22s  ENG_LAND  gen 196030
  vd root/0  d4:76:a0:cc:65:f0  gen 8276147  req OUA/34
    created 88407659s  gen 681  seen 0s  WIRELESS_APs  gen 289
    ip 10.210.96.58  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026498'  src capwap
  vd root/0  d4:76:a0:cc:66:d0  gen 14908276  req OUA/34
    created 88407659s  gen 722  seen 0s  WIRELESS_APs  gen 310
    ip 10.210.96.22  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026505'  src capwap
  vd root/0  10:df:fc:02:25:63  gen 15423630  req OHUSA/3e
    created 88407505s  gen 1570  seen 20s  ENG_LAND  gen 196020
    ip 10.210.144.113  src arp
  vd root/0  10:df:fc:02:23:b3  gen 15445231  req OHUSA/3e
    created 88407506s  gen 1560  seen 20s  ENG_LAND  gen 812
    ip 10.210.144.162  src arp
  vd root/0  10:df:fc:02:23:b4  gen 1654735  req OHUSA/3e
    created 88407506s  gen 1567  seen 20s  ENG_LAND  gen 195964
  vd root/0  10:df:fc:02:26:5f  gen 15448050  req OHUSA/3e
    created 88407505s  gen 1569  seen 20s  ENG_LAND  gen 196023
    ip 10.210.144.112  src arp
  vd root/0  10:df:fc:02:28:48  gen 15442756  req OUSA/36
    created 88407503s  gen 1610  seen 22s  ENG_LANC  gen 313592
    ip 10.210.140.142  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  d4:76:a0:cc:71:30  gen 10058332  req OUA/34
    created 88407659s  gen 725  seen 0s  WIRELESS_APs  gen 311
    ip 10.210.96.15  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026588'  src capwap
  vd root/0  10:df:fc:02:27:8b  gen 15383410  req OUSA/36
    created 88407524s  gen 1263  seen 20s  ENG_LANC  gen 196069
    ip 10.210.140.113  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  10:df:fc:02:27:a0  gen 15454156  req OUSA/36
    created 88407524s  gen 1271  seen 20s  ENG_LANC  gen 529
    ip 10.210.140.112  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  d4:76:a0:cc:71:50  gen 9123085  req OUA/34
    created 88407659s  gen 687  seen 0s  WIRELESS_APs  gen 292
    ip 10.210.96.43  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026589'  src capwap
  vd root/0  d4:76:a0:cc:72:30  gen 6142964  req OUA/34
    created 88407659s  gen 743  seen 0s  WIRELESS_APs  gen 320
    ip 10.210.96.32  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026596'  src capwap
  vd root/0  10:df:fc:02:25:f0  gen 15440597  req OUSA/36
    created 88407503s  gen 1612  seen 22s  ENG_LANC  gen 313594
    ip 10.210.140.143  src arp
    host 'D-ZRH11-SEC02-1'  src mwbs
  vd root/0  d4:76:a0:cc:73:90  gen 12230592  req OUA/34
    created 88407659s  gen 667  seen 0s  WIRELESS_APs  gen 282
    ip 10.210.96.61  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026607'  src capwap
  vd root/0  d4:76:a0:cc:75:50  gen 8910548  req OUA/34
    created 88407659s  gen 720  seen 0s  WIRELESS_APs  gen 309
    ip 10.210.96.27  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026621'  src capwap
  vd root/0  d4:76:a0:cc:75:b0  gen 9664755  req OUA/34
    created 88407659s  gen 669  seen 0s  WIRELESS_APs  gen 200654
    ip 10.210.96.34  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026624'  src capwap
  vd root/0  22:8d:55:9c:49:a7  gen 14126625  req OUA/34
    created 4333950s  gen 13093706  seen 2350917s  CORP WIRELESS  gen 426221
    ip 10.210.68.50  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  12:a5:53:ea:a2:60  gen 15391147  req OUA/34
    created 87209773s  gen 13854  seen 143477s  CORP WIRELESS  gen 448042
    ip 10.210.68.37  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '12'  src dhcp  id 191  weight 130
    host 'jtexugo-Handy'  src dhcp
  vd root/0  d4:76:a0:cc:87:30  gen 9989811  req OUA/34
    created 88407659s  gen 727  seen 0s  WIRELESS_APs  gen 312
    ip 10.210.96.60  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026764'  src capwap
  vd root/0  d4:76:a0:cc:88:50  gen 9456018  req OUA/34
    created 88407659s  gen 741  seen 0s  WIRELESS_APs  gen 319
    ip 10.210.96.13  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026773'  src capwap
  vd root/0  d4:76:a0:cc:88:70  gen 10136271  req OUA/34
    created 88407668s  gen 71  seen 0s  WIRELESS_APs  gen 44
    ip 10.210.96.8  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026774'  src capwap
  vd root/0  d4:76:a0:cc:8b:10  gen 12389315  req OUA/34
    created 88407659s  gen 691  seen 0s  WIRELESS_APs  gen 390306
    ip 10.210.96.16  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026795'  src capwap
  vd root/0  d4:76:a0:cc:87:b0  gen 5565299  req OUA/34
    created 88407659s  gen 729  seen 0s  WIRELESS_APs  gen 119961
    ip 10.210.96.5  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026768'  src capwap
  vd root/0  d4:76:a0:cc:8b:30  gen 10526939  req OUA/34
    created 88407668s  gen 75  seen 0s  WIRELESS_APs  gen 46
    ip 10.210.96.4  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026796'  src capwap
  vd root/0  d4:76:a0:cc:88:b0  gen 10624559  req OUA/34
    created 88407659s  gen 709  seen 0s  WIRELESS_APs  gen 304
    ip 10.210.96.44  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026776'  src capwap
  vd root/0  d4:76:a0:cc:8b:70  gen 10494737  req OUA/34
    created 88407659s  gen 754  seen 0s  WIRELESS_APs  gen 325
    ip 10.210.96.17  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026798'  src capwap
  vd root/0  d4:76:a0:cc:88:f0  gen 6527169  req OUA/34
    created 88407659s  gen 670  seen 0s  WIRELESS_APs  gen 284
    ip 10.210.96.45  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026778'  src capwap
  vd root/0  d4:76:a0:cc:8b:90  gen 6935915  req OUA/34
    created 88407668s  gen 79  seen 0s  WIRELESS_APs  gen 48
    ip 10.210.96.12  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026799'  src capwap
  vd root/0  d4:76:a0:cc:8d:50  gen 12278774  req OUA/34
    created 88407659s  gen 693  seen 0s  WIRELESS_APs  gen 295
    ip 10.210.96.7  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026813'  src capwap
  vd root/0  d4:76:a0:cc:8e:30  gen 10863453  req OUA/34
    created 88407659s  gen 716  seen 0s  WIRELESS_APs  gen 307
    ip 10.210.96.31  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026820'  src capwap
  vd root/0  d4:76:a0:cc:8c:90  gen 7636082  req OUA/34
    created 88407659s  gen 714  seen 0s  WIRELESS_APs  gen 306
    ip 10.210.96.62  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026807'  src capwap
  vd root/0  d4:76:a0:cc:8e:50  gen 9526108  req OUA/34
    created 88407659s  gen 689  seen 0s  WIRELESS_APs  gen 293
    ip 10.210.96.33  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026821'  src capwap
  vd root/0  d4:76:a0:cc:8c:b0  gen 8159562  req OUA/34
    created 88407659s  gen 745  seen 0s  WIRELESS_APs  gen 321
    ip 10.210.96.11  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026808'  src capwap
  vd root/0  d4:76:a0:cc:8d:b0  gen 8262532  req OUA/34
    created 88407659s  gen 697  seen 0s  WIRELESS_APs  gen 297
    ip 10.210.96.56  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026816'  src capwap
  vd root/0  d4:76:a0:cc:8e:90  gen 10169636  req OUA/34
    created 88407659s  gen 731  seen 0s  WIRELESS_APs  gen 314
    ip 10.210.96.54  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026823'  src capwap
  vd root/0  d4:76:a0:cc:8c:f0  gen 7401725  req OUA/34
    created 88407659s  gen 735  seen 0s  WIRELESS_APs  gen 316
    ip 10.210.96.50  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026810'  src capwap
  vd root/0  d4:76:a0:cc:8d:d0  gen 8710053  req OUA/34
    created 88407659s  gen 739  seen 0s  WIRELESS_APs  gen 318
    ip 10.210.96.42  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026817'  src capwap
  vd root/0  d4:76:a0:cc:8e:b0  gen 12259792  req OUA/34
    created 88407659s  gen 718  seen 0s  WIRELESS_APs  gen 308
    ip 10.210.96.51  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026824'  src capwap
  vd root/0  d4:76:a0:cc:91:50  gen 6870104  req OUA/34
    created 88407659s  gen 712  seen 0s  WIRELESS_APs  gen 305
    ip 10.210.96.59  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026845'  src capwap
  vd root/0  0e:81:52:21:6f:b9  gen 15071900  req OUSA/36
    created 2615389s  gen 13973717  seen 732972s  CORP WIRELESS  gen 442175
    ip 10.210.68.19  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  00:80:40:2d:5b:8f  gen 14131746  req OUA/34
    created 2343841s  gen 14131739  seen 2343829s  CORP_WKS  gen 426328
    ip 10.210.64.22  src arp
    os 'Linux'  src tcp  id 1624  weight 90
    host 'ciq2-cross'  src dhcp
  vd root/0  d4:76:a0:cc:9c:10  gen 12389301  req OUA/34
    created 88407659s  gen 706  seen 0s  WIRELESS_APs  gen 390304
    ip 10.210.96.18  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026931'  src capwap
  vd root/0  d4:76:a0:cc:9a:70  gen 8901309  req OUA/34
    created 88407668s  gen 89  seen 0s  WIRELESS_APs  gen 53
    ip 10.210.96.10  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026918'  src capwap
  vd root/0  d4:76:a0:cc:9c:30  gen 11110855  req OUA/34
    created 49591520s  gen 1657257  seen 0s  WIRELESS_APs  gen 196285
    ip 10.210.96.23  src mac
    hardware vendor 'Fortinet'  src dhcp  id 156  weight 220
    type 'Network Generic'  src dhcp  id 156  weight 220
    family 'FortiAP'  src dhcp  id 156  weight 220
    os 'FortiAP OS'  src dhcp  id 156  weight 220
    hardware version 'FP231F'  src dhcp  id 156  weight 220
    host 'FortiAP-231F'  src dns
  vd root/0  d4:76:a0:cc:9c:50  gen 9461957  req OUA/34
    created 88407659s  gen 733  seen 0s  WIRELESS_APs  gen 315
    ip 10.210.96.21  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026933'  src capwap
  vd root/0  d4:76:a0:cc:9d:30  gen 11290421  req OUA/34
    created 88407659s  gen 675  seen 0s  WIRELESS_APs  gen 286
    ip 10.210.96.24  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026940'  src capwap
  vd root/0  d4:76:a0:cc:9c:70  gen 9745082  req OUA/34
    created 88407659s  gen 756  seen 0s  WIRELESS_APs  gen 326
    ip 10.210.96.25  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026934'  src capwap
  vd root/0  d4:76:a0:cc:9d:50  gen 9899195  req OUA/34
    created 88407659s  gen 708  seen 0s  WIRELESS_APs  gen 303
    ip 10.210.96.3  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026941'  src capwap
  vd root/0  d4:76:a0:cc:9c:90  gen 10980887  req OUA/34
    created 88407659s  gen 758  seen 0s  WIRELESS_APs  gen 327
    ip 10.210.96.48  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026935'  src capwap
  vd root/0  d4:76:a0:cc:9e:50  gen 7977878  req OUA/34
    created 88407668s  gen 73  seen 0s  WIRELESS_APs  gen 45
    ip 10.210.96.6  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026949'  src capwap
  vd root/0  d4:76:a0:cc:9f:30  gen 10272271  req OUA/34
    created 88407659s  gen 679  seen 0s  WIRELESS_APs  gen 288
    ip 10.210.96.52  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026956'  src capwap
  vd root/0  d4:76:a0:cc:9d:90  gen 12389308  req OUA/34
    created 88407663s  gen 614  seen 0s  WIRELESS_APs  gen 390305
    ip 10.210.96.38  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026943'  src capwap
  vd root/0  d4:76:a0:cc:9f:50  gen 8640505  req OUA/34
    created 88407659s  gen 683  seen 0s  WIRELESS_APs  gen 290
    ip 10.210.96.26  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026957'  src capwap
  vd root/0  d4:76:a0:cc:9b:f0  gen 9900251  req OUA/34
    created 88407659s  gen 737  seen 0s  WIRELESS_APs  gen 317
    ip 10.210.96.19  src arp
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026930'  src capwap
  vd root/0  d4:76:a0:cc:9c:d0  gen 8704078  req OUA/34
    created 88407659s  gen 747  seen 0s  WIRELESS_APs  gen 322
    ip 10.210.96.30  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026937'  src capwap
  vd root/0  d4:76:a0:cc:9c:f0  gen 9729324  req OUA/34
    created 88407659s  gen 673  seen 0s  WIRELESS_APs  gen 285
    ip 10.210.96.53  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '231F'  src capwap  id 2679  weight 220
    host 'FP231FTF21026938'  src capwap
  vd root/0  d4:76:a0:cc:9e:d0  gen 12389295  req OUA/34
    created 88407668s  gen 83  seen 0s  WIRELESS_APs  gen 390303
    ip 10.210.96.37  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026953'  src capwap
  vd root/0  d4:76:a0:cc:9f:d0  gen 12389319  req OUA/34
    created 88407668s  gen 81  seen 0s  WIRELESS_APs  gen 390307
    ip 10.210.96.39  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-231F'  src fortiguard  id 0  weight 255
    host 'FP231FTF21026961'  src capwap
  vd root/0  04:cb:1d:83:13:59  gen 2407  req OHUA/3c
    created 88407657s  gen 834  seen 14s  SECURITY_ExtDev  gen 347
    ip 10.210.48.20  src arp
    os 'Windows'  src dhcp  id 848  weight 128
  vd root/0  8a:46:a9:31:8a:57  gen 15453243  req OUA/34
    created 9178230s  gen 11452715  seen 27s  Guest  gen 449351
    ip 172.176.0.33  src arp
    hardware vendor 'Apple'  src http  id 929  weight 230
    type 'Phone'  src http  id 929  weight 230
    family 'iPhone'  src http  id 929  weight 230
    os 'iOS'  src http  id 929  weight 230
    software version '26.1'  src http  id 929  weight 230
    host 'iPhone'  src dhcp
  vd root/0  76:a0:50:fa:ba:8d  gen 15463577  req OUA/34
    created 67503526s  gen 200937  seen 7519s  Guest  gen 449557
    ip 172.176.0.17  src arp
    hardware vendor 'Samsung'  src http  id 997  weight 230
    type 'Phone'  src http  id 997  weight 230
    family 'Galaxy'  src http  id 997  weight 230
    os 'Android'  src http  id 997  weight 230
    hardware version 'S3 Ultra'  src dhcp  id 6732  weight 230
    software version '14'  src http  id 997  weight 230
    host 'S23-Ultra-korisnika-Antonio'  src dhcp
  vd root/0  62:4f:4d:a8:3e:3b  gen 14557428  req OUSA/36
    created 2615574s  gen 13973628  seen 1617907s  CORP WIRELESS  gen 433529
    ip 10.210.68.3  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'Watch'  src dhcp
  vd root/0  10:df:fc:02:8a:7f  gen 936939  req OHUSA/3e
    created 88407526s  gen 1254  seen 18s  ENG_LAND  gen 513
    ip 10.210.144.172  src arp
  vd root/0  10:df:fc:02:8a:80  gen 1654738  req OHUSA/3e
    created 88407522s  gen 1396  seen 18s  ENG_LAND  gen 195967
  vd root/0  10:df:fc:02:8e:00  gen 927791  req OHUSA/3e
    created 88407524s  gen 1337  seen 2s  ENG_LANC  gen 595
    ip 10.210.140.165  src arp
  vd root/0  10:df:fc:02:8e:01  gen 1654848  req OHUSA/3e
    created 88407524s  gen 1326  seen 20s  ENG_LANC  gen 195977
  vd root/0  10:df:fc:02:8a:97  gen 936927  req OHUSA/3e
    created 88407503s  gen 1603  seen 13s  ENG_LANC  gen 850
    ip 10.210.140.134  src arp
  vd root/0  10:df:fc:02:8a:98  gen 9180322  req OHUSA/3e
    created 88407503s  gen 1607  seen 22s  ENG_LANC  gen 313590
  vd root/0  10:df:fc:02:8a:a6  gen 936925  req OHUSA/3e
    created 88407503s  gen 1608  seen 3s  ENG_LANC  gen 855
    ip 10.210.140.133  src arp
  vd root/0  10:df:fc:02:8a:a7  gen 9180320  req OHUSA/3e
    created 88407503s  gen 1602  seen 22s  ENG_LANC  gen 313588
  vd root/0  10:df:fc:02:8a:af  gen 936924  req OHUSA/3e
    created 88407520s  gen 1485  seen 14s  ENG_LAND  gen 743
    ip 10.210.144.163  src arp
  vd root/0  10:df:fc:02:8a:b0  gen 1654729  req OHUSA/3e
    created 88407520s  gen 1487  seen 22s  ENG_LAND  gen 195958
  vd root/0  10:df:fc:02:8a:d6  gen 936933  req OHUSA/3e
    created 88407522s  gen 1397  seen 0s  ENG_LAND  gen 655
    ip 10.210.144.171  src arp
  vd root/0  10:df:fc:02:8a:d7  gen 1654736  req OHUSA/3e
    created 88407522s  gen 1394  seen 18s  ENG_LAND  gen 195965
  vd root/0  10:df:fc:02:8a:eb  gen 8857107  req OHUSA/3e
    created 88407506s  gen 1563  seen 10s  ENG_LAND  gen 815
    ip 10.210.144.165  src arp
  vd root/0  10:df:fc:02:8a:ec  gen 1654734  req OHUSA/3e
    created 88407506s  gen 1564  seen 20s  ENG_LAND  gen 195963
  vd root/0  10:df:fc:02:8e:ae  gen 936923  req OHUSA/3e
    created 88407520s  gen 1489  seen 19s  ENG_LAND  gen 747
    ip 10.210.144.164  src arp
  vd root/0  10:df:fc:02:8e:af  gen 1654727  req OHUSA/3e
    created 88407520s  gen 1484  seen 22s  ENG_LAND  gen 195956
  vd root/0  10:df:fc:02:8e:f6  gen 936942  req OHUSA/3e
    created 88407506s  gen 1565  seen 20s  ENG_LAND  gen 817
    ip 10.210.144.166  src arp
  vd root/0  10:df:fc:02:8e:f7  gen 1654732  req OHUSA/3e
    created 88407506s  gen 1561  seen 20s  ENG_LAND  gen 195961
  vd root/0  10:df:fc:02:a0:21  gen 936940  req OHUSA/3e
    created 88407522s  gen 1404  seen 20s  ENG_LAND  gen 662
    ip 10.210.144.132  src arp
  vd root/0  10:df:fc:02:a0:22  gen 1654932  req OHUSA/3e
    created 88407522s  gen 1409  seen 20s  ENG_LAND  gen 196004
  vd root/0  10:df:fc:02:a0:2a  gen 936920  req OHUSA/3e
    created 88407524s  gen 1323  seen 20s  ENG_LANC  gen 581
    ip 10.210.140.132  src arp
  vd root/0  10:df:fc:02:a0:2b  gen 1655313  req OHUSA/3e
    created 88407524s  gen 1315  seen 20s  ENG_LANC  gen 196102
  vd root/0  10:df:fc:02:a0:30  gen 936913  req OHUSA/3e
    created 88407520s  gen 1503  seen 22s  ENG_LAND  gen 761
    ip 10.210.144.134  src arp
  vd root/0  10:df:fc:02:a0:31  gen 1654941  req OHUSA/3e
    created 88407520s  gen 1495  seen 22s  ENG_LAND  gen 196013
  vd root/0  10:df:fc:02:a0:42  gen 936936  req OHUSA/3e
    created 88407520s  gen 1514  seen 14s  ENG_LANC  gen 772
    ip 10.210.140.111  src arp
  vd root/0  10:df:fc:02:a0:43  gen 1655211  req OHUSA/3e
    created 88407520s  gen 1508  seen 22s  ENG_LANC  gen 196084
  vd root/0  10:df:fc:02:9c:cd  gen 936931  req OHUSA/3e
    created 88407536s  gen 1212  seen 20s  ENG_LANC  gen 482
    ip 10.210.140.103  src arp
  vd root/0  10:df:fc:02:9c:ce  gen 1655195  req OHUSA/3e
    created 88407524s  gen 1266  seen 20s  ENG_LANC  gen 196072
  vd root/0  10:df:fc:02:a0:51  gen 936930  req OHUSA/3e
    created 88407505s  gen 1574  seen 20s  ENG_LAND  gen 826
    ip 10.210.144.105  src arp
  vd root/0  10:df:fc:02:a0:52  gen 1654997  req OHUSA/3e
    created 88407505s  gen 1576  seen 20s  ENG_LAND  gen 196026
  vd root/0  10:df:fc:02:a0:57  gen 936914  req OHUSA/3e
    created 88407520s  gen 1506  seen 22s  ENG_LANC  gen 764
    ip 10.210.140.110  src arp
  vd root/0  10:df:fc:02:a0:58  gen 1655215  req OHUSA/3e
    created 88407520s  gen 1515  seen 22s  ENG_LANC  gen 196088
  vd root/0  10:df:fc:02:9e:a4  gen 919436  req OHUSA/3e
    created 88407503s  gen 1599  seen 22s  ENG_LANC  gen 846
    ip 10.210.140.135  src arp
  vd root/0  10:df:fc:02:9e:a5  gen 9180321  req OHUSA/3e
    created 88407503s  gen 1605  seen 22s  ENG_LANC  gen 313589
  vd root/0  10:df:fc:02:a0:69  gen 936943  req OHUSA/3e
    created 88407520s  gen 1496  seen 22s  ENG_LAND  gen 754
    ip 10.210.144.133  src arp
  vd root/0  10:df:fc:02:a0:6a  gen 1654944  req OHUSA/3e
    created 88407520s  gen 1500  seen 22s  ENG_LAND  gen 196016
  vd root/0  10:df:fc:02:a0:6c  gen 936922  req OHUSA/3e
    created 88407520s  gen 1502  seen 22s  ENG_LAND  gen 760
    ip 10.210.144.135  src arp
  vd root/0  10:df:fc:02:a0:6d  gen 1654939  req OHUSA/3e
    created 88407520s  gen 1493  seen 22s  ENG_LAND  gen 196011
  vd root/0  10:df:fc:02:a0:75  gen 936916  req OHUSA/3e
    created 88407524s  gen 1331  seen 7s  ENG_LANC  gen 589
    ip 10.210.140.163  src arp
  vd root/0  10:df:fc:02:a0:76  gen 1654854  req OHUSA/3e
    created 88407524s  gen 1334  seen 20s  ENG_LANC  gen 195983
  vd root/0  10:df:fc:02:a0:78  gen 936932  req OHUSA/3e
    created 88407686s  gen 13  seen 19s  ENG_LANC  gen 1710
    ip 10.210.140.164  src arp
  vd root/0  10:df:fc:02:a0:79  gen 1654853  req OHUSA/3e
    created 88407524s  gen 1333  seen 20s  ENG_LANC  gen 195982
  vd root/0  10:df:fc:02:a0:7e  gen 936918  req OHUSA/3e
    created 88407520s  gen 1513  seen 22s  ENG_LANC  gen 771
    ip 10.210.140.102  src arp
  vd root/0  10:df:fc:02:a0:7f  gen 1655210  req OHUSA/3e
    created 88407520s  gen 1507  seen 22s  ENG_LANC  gen 196083
  vd root/0  10:df:fc:02:a0:84  gen 936919  req OHUSA/3e
    created 88407524s  gen 1269  seen 20s  ENG_LANC  gen 527
    ip 10.210.140.104  src arp
  vd root/0  10:df:fc:02:a0:85  gen 1655193  req OHUSA/3e
    created 88407524s  gen 1264  seen 20s  ENG_LANC  gen 196070
  vd root/0  10:df:fc:02:a0:87  gen 936921  req OHUSA/3e
    created 88407650s  gen 886  seen 3s  ENG_LAND  gen 363
    ip 10.210.144.104  src arp
  vd root/0  10:df:fc:02:a0:88  gen 1655000  req OHUSA/3e
    created 88407505s  gen 1580  seen 20s  ENG_LAND  gen 196029
  vd root/0  00:0e:6b:09:2d:04  gen 15440052  req OHUSA/3e
    created 88407520s  gen 1511  seen 22s  ENG_LANC  gen 196087
    ip 10.210.140.107  src arp
  vd root/0  00:0e:6b:09:2d:07  gen 15436489  req OHUSA/3e
    created 88407524s  gen 1265  seen 20s  ENG_LANC  gen 196071
    ip 10.210.140.106  src arp
  vd root/0  00:0e:6b:09:2c:2a  gen 1654731  req 0
    created 88407520s  gen 1491  seen 22s  ENG_LAND  gen 195960
    ip 10.210.144.167  src arp
    server ftp
  vd root/0  00:0e:6b:09:2c:2b  gen 15440110  req OHUSA/3e
    created 88407506s  gen 1562  seen 20s  ENG_LAND  gen 195962
    ip 10.210.144.168  src arp
  vd root/0  00:0e:6b:09:2c:2e  gen 15436487  req OHUSA/3e
    created 88407503s  gen 1609  seen 22s  ENG_LANC  gen 313591
    ip 10.210.140.136  src arp
  vd root/0  00:0e:6b:09:2d:1e  gen 15384650  req OHUSA/3e
    created 88407505s  gen 1579  seen 20s  ENG_LAND  gen 196028
    ip 10.210.144.106  src arp
  vd root/0  00:0e:6b:09:2d:20  gen 15418752  req OHUSA/3e
    created 88407524s  gen 1321  seen 20s  ENG_LANC  gen 195683
    ip 10.210.140.137  src arp
  vd root/0  00:0e:6b:09:2d:23  gen 1654866  req 0
    created 88407520s  gen 1465  seen 20s  ENG_LANC  gen 195990
    ip 10.210.140.167  src arp
    server ftp
  vd root/0  00:0e:6b:09:2d:24  gen 1654931  req 0
    created 88407522s  gen 1408  seen 20s  ENG_LAND  gen 196003
    ip 10.210.144.137  src arp
    server ftp
  vd root/0  00:0e:6b:09:2d:27  gen 15384653  req OHUSA/3e
    created 88407520s  gen 1518  seen 22s  ENG_LAND  gen 196031
    ip 10.210.144.107  src arp
  vd root/0  42:bb:de:7a:5f:c3  gen 14273795  req OUA/34
    created 2365605s  gen 14119356  seen 2100155s  CORP WIRELESS  gen 428500
    ip 10.210.68.91  src arp
    hardware vendor 'Samsung'  src dhcp  id 133  weight 255
    type 'Phone'  src dhcp  id 133  weight 255
    family 'Galaxy'  src dhcp  id 133  weight 255
    os 'Android'  src dhcp  id 133  weight 255
    hardware version 'A25-5G'  src dhcp  id 182  weight 232
    software version '15'  src dhcp  id 133  weight 255
    host 'Galaxy-A25-5G'  src dhcp
  vd root/0  10:df:fc:02:a0:db  gen 936929  req OHUSA/3e
    created 88407505s  gen 1571  seen 20s  ENG_LAND  gen 823
    ip 10.210.144.103  src arp
  vd root/0  10:df:fc:02:a0:dc  gen 1654998  req OHUSA/3e
    created 88407505s  gen 1578  seen 20s  ENG_LAND  gen 196027
  vd root/0  00:0e:6b:09:2c:b1  gen 15442035  req OHUSA/3e
    created 88407524s  gen 1328  seen 20s  ENG_LANC  gen 195979
    ip 10.210.140.166  src arp
  vd root/0  00:0e:6b:09:2c:b3  gen 15432801  req OHUSA/3e
    created 88407520s  gen 1494  seen 22s  ENG_LAND  gen 196012
    ip 10.210.144.136  src arp
  vd root/0  10:df:fc:02:ab:19  gen 936935  req OHUSA/3e
    created 88407522s  gen 1406  seen 20s  ENG_LAND  gen 664
    ip 10.210.144.140  src arp
  vd root/0  10:df:fc:02:ab:1a  gen 1654933  req OHUSA/3e
    created 88407522s  gen 1411  seen 20s  ENG_LAND  gen 196005
  vd root/0  10:df:fc:02:aa:7d  gen 936917  req OHUSA/3e
    created 88407524s  gen 1317  seen 20s  ENG_LANC  gen 575
    ip 10.210.140.141  src arp
  vd root/0  10:df:fc:02:aa:7e  gen 1655315  req OHUSA/3e
    created 88407524s  gen 1320  seen 20s  ENG_LANC  gen 196104
  vd root/0  00:50:56:50:6a:f5  gen 12429605  req OHUSA/3e
    created 83886321s  gen 44608  seen 21s  ESXMGMT  gen 391414
  vd root/0  10:df:fc:02:cd:90  gen 936926  req OHUSA/3e
    created 88407520s  gen 1468  seen 15s  ENG_LANC  gen 726
    ip 10.210.140.170  src arp
  vd root/0  10:df:fc:02:cd:91  gen 1654865  req OHUSA/3e
    created 88407520s  gen 1463  seen 20s  ENG_LANC  gen 195989
  vd root/0  10:df:fc:02:cd:93  gen 931554  req OHUSA/3e
    created 88407524s  gen 1316  seen 20s  ENG_LANC  gen 574
    ip 10.210.140.140  src arp
  vd root/0  10:df:fc:02:cd:94  gen 1655316  req OHUSA/3e
    created 88407524s  gen 1322  seen 20s  ENG_LANC  gen 196105
  vd root/0  e4:30:22:2c:6b:2a  gen 499  req OHUSA/3e
    created 88407667s  gen 444  seen 3s  SECURITY_ExtDev  gen 210
    ip 10.210.48.161  src mac
  vd root/0  10:df:fc:02:ce:9e  gen 936934  req OHUSA/3e
    created 88407522s  gen 1412  seen 20s  ENG_LAND  gen 670
    ip 10.210.144.141  src arp
  vd root/0  10:df:fc:02:ce:9f  gen 1654930  req OHUSA/3e
    created 88407522s  gen 1407  seen 20s  ENG_LAND  gen 196002
  vd root/0  e4:30:22:2c:6b:2e  gen 463  req OHUSA/3e
    created 88407667s  gen 461  seen 4s  SECURITY_ExtDev  gen 219
    ip 10.210.48.158  src mac
  vd root/0  e4:30:22:2c:6b:35  gen 413  req OHUSA/3e
    created 88407667s  gen 412  seen 5s  SECURITY_ExtDev  gen 192
    ip 10.210.48.149  src mac
  vd root/0  10:df:fc:02:d0:72  gen 936912  req OHUSA/3e
    created 88407520s  gen 1464  seen 20s  ENG_LANC  gen 722
    ip 10.210.140.162  src arp
  vd root/0  10:df:fc:02:d0:73  gen 1654870  req OHUSA/3e
    created 88407520s  gen 1470  seen 20s  ENG_LANC  gen 195994
  vd root/0  00:50:56:51:5d:41  gen 11280587  req OHUSA/3e
    created 83886321s  gen 44614  seen 22s  ESXMGMT  gen 358454
  vd root/0  10:df:fc:02:cd:f6  gen 9263537  req OHUSA/3e
    created 88407686s  gen 14  seen 2s  ENG_LANC  gen 14
    ip 10.210.140.171  src arp
  vd root/0  10:df:fc:02:cd:f7  gen 1654867  req OHUSA/3e
    created 88407520s  gen 1466  seen 20s  ENG_LANC  gen 195991
  vd root/0  ae:7b:93:f7:d2:f3  gen 15463731  req OUA/34
    created 13913366s  gen 9791100  seen 4830s  Guest  gen 449559
    ip 172.176.0.12  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '12'  src dhcp  id 191  weight 130
    host 'Lenovo-Tab-M10-3rd-Gen'  src dhcp
  vd root/0  e4:30:22:2c:6a:bd  gen 454  req OHUSA/3e
    created 88407667s  gen 432  seen 3s  SECURITY_ExtDev  gen 205
    ip 10.210.48.171  src mac
  vd root/0  e4:30:22:2c:6a:d2  gen 425  req OHUSA/3e
    created 88407667s  gen 424  seen 3s  SECURITY_ExtDev  gen 201
    ip 10.210.48.172  src mac
  vd root/0  2a:ed:70:53:81:6e  gen 14934431  req OUSA/36
    created 971614s  gen 14933217  seen 965721s  CORP WIRELESS  gen 440007
    ip 10.210.68.67  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
    host 'iPad'  src dhcp
  vd root/0  00:50:56:50:85:39  gen 12429946  req OHUSA/3e
    created 83886020s  gen 44630  seen 22s  ESXMGMT  gen 391426
  vd root/0  4c:fc:aa:a6:68:79  gen 15436016  req OUSA/36
    created 26767493s  gen 5723103  seen 64048s  Guest  gen 449043
    ip 172.176.0.11  src arp
    host 'Tesla'  src dhcp
  vd root/0  e4:30:22:2e:41:3d  gen 201  req OHUSA/3e
    created 88407668s  gen 200  seen 7s  SECURITY_CAMERA  gen 85
    ip 10.210.32.17  src mac
  vd root/0  e4:30:22:2e:41:3f  gen 275  req OHUSA/3e
    created 88407668s  gen 272  seen 7s  SECURITY_CAMERA  gen 122
    ip 10.210.32.42  src mac
  vd root/0  e4:30:22:2e:41:44  gen 174  req OHUSA/3e
    created 88407668s  gen 173  seen 7s  SECURITY_CAMERA  gen 72
    ip 10.210.32.113  src mac
  vd root/0  e4:30:22:2e:41:45  gen 172  req OHUSA/3e
    created 88407668s  gen 171  seen 7s  SECURITY_CAMERA  gen 71
    ip 10.210.32.114  src mac
  vd root/0  e4:30:22:2e:41:49  gen 373  req OHUSA/3e
    created 88407668s  gen 372  seen 7s  SECURITY_CAMERA  gen 171
    ip 10.210.32.21  src mac
  vd root/0  e4:30:22:2e:41:4b  gen 238709  req OHUSA/3e
    created 88407668s  gen 294  seen 7s  SECURITY_CAMERA  gen 119965
    ip 10.210.32.143  src mac
  vd root/0  e4:30:22:2e:41:5e  gen 369  req OHUSA/3e
    created 88407668s  gen 368  seen 7s  SECURITY_CAMERA  gen 169
    ip 10.210.32.43  src mac
  vd root/0  e4:30:22:2e:41:60  gen 249  req OHUSA/3e
    created 88407668s  gen 248  seen 7s  SECURITY_CAMERA  gen 109
    ip 10.210.32.12  src mac
  vd root/0  e4:30:22:2e:41:76  gen 159  req OHUSA/3e
    created 88407668s  gen 158  seen 7s  SECURITY_CAMERA  gen 64
    ip 10.210.32.22  src mac
  vd root/0  e4:30:22:2e:41:7b  gen 166  req OHUSA/3e
    created 88407668s  gen 165  seen 7s  SECURITY_CAMERA  gen 68
    ip 10.210.32.35  src mac
  vd root/0  e4:30:22:2e:41:82  gen 238717  req OHUSA/3e
    created 88407668s  gen 236  seen 7s  SECURITY_CAMERA  gen 119973
    ip 10.210.32.44  src mac
  vd root/0  e4:30:22:2e:41:85  gen 287  req OHUSA/3e
    created 88407668s  gen 286  seen 7s  SECURITY_CAMERA  gen 128
    ip 10.210.32.45  src mac
  vd root/0  e4:30:22:2e:41:88  gen 365  req OHUSA/3e
    created 88407668s  gen 364  seen 7s  SECURITY_CAMERA  gen 167
    ip 10.210.32.36  src mac
  vd root/0  e4:30:22:2e:41:89  gen 223  req OHUSA/3e
    created 88407668s  gen 222  seen 7s  SECURITY_CAMERA  gen 96
    ip 10.210.32.141  src mac
  vd root/0  e4:30:22:2e:41:8a  gen 178  req OHUSA/3e
    created 88407668s  gen 177  seen 7s  SECURITY_CAMERA  gen 74
    ip 10.210.32.137  src mac
  vd root/0  e4:30:22:2e:41:8b  gen 361  req OHUSA/3e
    created 88407668s  gen 360  seen 7s  SECURITY_CAMERA  gen 165
    ip 10.210.32.109  src mac
  vd root/0  e4:30:22:2e:41:8c  gen 238715  req OHUSA/3e
    created 88407668s  gen 352  seen 7s  SECURITY_CAMERA  gen 119971
    ip 10.210.32.148  src mac
  vd root/0  e4:30:22:2e:41:8d  gen 199  req OHUSA/3e
    created 88407668s  gen 198  seen 7s  SECURITY_CAMERA  gen 84
    ip 10.210.32.110  src mac
  vd root/0  e4:30:22:2e:41:90  gen 239  req OHUSA/3e
    created 88407668s  gen 238  seen 7s  SECURITY_CAMERA  gen 104
    ip 10.210.32.46  src mac
  vd root/0  10:df:fc:02:ef:61  gen 936915  req OHUSA/3e
    created 88407520s  gen 1519  seen 22s  ENG_LAND  gen 777
    ip 10.210.144.111  src arp
  vd root/0  10:df:fc:02:ef:62  gen 1655006  req OHUSA/3e
    created 88407520s  gen 1521  seen 22s  ENG_LAND  gen 196033
  vd root/0  00:50:56:55:01:64  gen 11279826  req OHUSA/3e
    created 83886320s  gen 44617  seen 22s  ESXMGMT  gen 358401
  vd root/0  10:df:fc:02:fd:02  gen 936938  req OHUSA/3e
    created 88407520s  gen 1516  seen 15s  ENG_LAND  gen 774
    ip 10.210.144.110  src arp
  vd root/0  10:df:fc:02:fd:03  gen 1655005  req OHUSA/3e
    created 88407520s  gen 1520  seen 22s  ENG_LAND  gen 196032
  vd root/0  00:50:56:55:14:7c  gen 11281512  req OHUSA/3e
    created 83886200s  gen 44623  seen 21s  ESXMGMT  gen 358495
  vd root/0  00:50:56:50:b9:bd  gen 11279837  req HU/18
    created 64638172s  gen 237378  seen 22s  default  gen 358406
  vd root/0  e4:30:22:2e:67:d2  gen 321  req OHUSA/3e
    created 88407668s  gen 320  seen 7s  SECURITY_CAMERA  gen 145
    ip 10.210.32.108  src mac
  vd root/0  e4:30:22:2e:67:d3  gen 238728  req OHUSA/3e
    created 88407668s  gen 260  seen 7s  SECURITY_CAMERA  gen 119984
    ip 10.210.32.144  src mac
  vd root/0  e4:30:22:2e:67:d4  gen 238730  req OHUSA/3e
    created 88407668s  gen 252  seen 7s  SECURITY_CAMERA  gen 119986
    ip 10.210.32.132  src mac
  vd root/0  00:50:56:54:3d:57  gen 11277217  req OHUSA/3e
    created 83886321s  gen 44609  seen 22s  ESXMGMT  gen 358284
  vd root/0  c6:07:41:18:dc:61  gen 15202178  req OUA/34
    created 533866s  gen 15190582  seen 513314s  CORP WIRELESS  gen 444570
    ip 10.210.68.38  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  88:51:7a:73:d1:0b  gen 15423378  req OHUA/3c
    created 88407595s  gen 1105  seen 114s  Guest  gen 344318
    ip 172.176.0.13  src arp
    os 'KaiOS'  src http  id 1357  weight 130
    software version '2.5.2'  src http  id 1357  weight 130
  vd root/0  4a:8b:50:c2:df:02  gen 14780822  req OUA/34
    created 6076721s  gen 12383974  seen 1217157s  Guest  gen 437302
    ip 172.176.0.28  src arp
    hardware vendor 'Apple'  src dhcp  id 7286  weight 180
    type 'Phone'  src dhcp  id 7286  weight 180
    family 'iPhone'  src dhcp  id 7286  weight 180
    os 'iOS'  src dhcp  id 7286  weight 180
    host 'iPhone'  src dhcp
  vd root/0  00:50:56:56:18:cf  gen 12430619  req OHUSA/3e
    created 83886321s  gen 44611  seen 22s  ESXMGMT  gen 391449
  vd root/0  10:df:fc:0a:32:5c  gen 13127931  req OHUSA/3e
    created 88407524s  gen 1301  seen 20s  ENG_LANC  gen 214833
    ip 10.210.140.116  src arp
  vd root/0  10:df:fc:0a:32:66  gen 13494764  req OHUSA/3e
    created 88407524s  gen 1260  seen 20s  ENG_LANC  gen 196062
    ip 10.210.140.101  src arp
  vd root/0  10:df:fc:0a:32:8e  gen 13494739  req OHUSA/3e
    created 88407505s  gen 1568  seen 20s  ENG_LAND  gen 196022
    ip 10.210.144.101  src arp
  vd root/0  10:df:fc:0a:32:91  gen 13494753  req OHUSA/3e
    created 88407520s  gen 1504  seen 22s  ENG_LAND  gen 196018
    ip 10.210.144.131  src arp
  vd root/0  10:df:fc:0a:32:97  gen 13494751  req OHUSA/3e
    created 88407524s  gen 1336  seen 20s  ENG_LANC  gen 195985
    ip 10.210.140.161  src arp
  vd root/0  10:df:fc:0a:32:a2  gen 13494757  req OHUSA/3e
    created 88407524s  gen 1300  seen 20s  ENG_LANC  gen 214832
    ip 10.210.140.115  src arp
  vd root/0  10:df:fc:0a:31:ea  gen 13494767  req OHUSA/3e
    created 88407503s  gen 1601  seen 22s  ENG_LANC  gen 313587
    ip 10.210.140.131  src arp
  vd root/0  10:df:fc:0a:38:05  gen 13127914  req OHUSA/3e
    created 88407522s  gen 1391  seen 22s  ENG_LANC  gen 215518
    ip 10.210.140.149  src arp
  vd root/0  10:df:fc:0a:38:0c  gen 13494740  req OHUSA/3e
    created 88407522s  gen 1386  seen 18s  ENG_LAND  gen 313617
    ip 10.210.144.148  src arp
  vd root/0  10:df:fc:0a:39:01  gen 13494734  req OHUSA/3e
    created 88407524s  gen 1314  seen 20s  ENG_LAND  gen 215127
    ip 10.210.144.115  src arp
  vd root/0  10:df:fc:0a:39:02  gen 13494735  req OHUSA/3e
    created 88407524s  gen 1312  seen 20s  ENG_LAND  gen 215125
    ip 10.210.144.116  src arp
  vd root/0  10:df:fc:0a:38:28  gen 13494733  req OHUSA/3e
    created 88407505s  gen 1584  seen 20s  ENG_LANC  gen 313399
    ip 10.210.140.175  src arp
  vd root/0  10:df:fc:0a:36:6f  gen 13494755  req OHUSA/3e
    created 88407524s  gen 1307  seen 20s  ENG_LAND  gen 313611
    ip 10.210.144.145  src arp
  vd root/0  10:df:fc:0a:39:20  gen 13494762  req OHUSA/3e
    created 88407524s  gen 1284  seen 20s  ENG_LANC  gen 313403
    ip 10.210.140.178  src arp
  vd root/0  10:df:fc:0a:39:24  gen 13494758  req OHUSA/3e
    created 88407524s  gen 1282  seen 20s  ENG_LANC  gen 313402
    ip 10.210.140.179  src arp
  vd root/0  10:df:fc:0a:38:49  gen 13494746  req OHUSA/3e
    created 88407524s  gen 1309  seen 20s  ENG_LAND  gen 313612
    ip 10.210.144.146  src arp
  vd root/0  10:df:fc:0a:38:8c  gen 13494738  req OHUSA/3e
    created 88407505s  gen 1582  seen 20s  ENG_LANC  gen 313398
    ip 10.210.140.176  src arp
  vd root/0  10:df:fc:0a:37:cc  gen 13494742  req OHUSA/3e
    created 88407524s  gen 1296  seen 20s  ENG_LAND  gen 214634
    ip 10.210.144.175  src arp
  vd root/0  10:df:fc:0a:38:c0  gen 13494732  req OHUSA/3e
    created 88407522s  gen 1387  seen 18s  ENG_LAND  gen 313618
    ip 10.210.144.149  src arp
  vd root/0  10:df:fc:0a:37:e9  gen 13494763  req OHUSA/3e
    created 88407522s  gen 1393  seen 22s  ENG_LANC  gen 215520
    ip 10.210.140.148  src arp
  vd root/0  10:df:fc:0a:38:d0  gen 13127921  req OHUSA/3e
    created 88407522s  gen 1381  seen 18s  ENG_LANC  gen 215507
    ip 10.210.140.145  src arp
  vd root/0  10:df:fc:0a:37:f7  gen 13494749  req OHUSA/3e
    created 37334785s  gen 3406388  seen 20s  ENG_LANC  gen 215000
    ip 10.210.140.121  src mac
  vd root/0  10:df:fc:0a:38:de  gen 13127935  req OHUSA/3e
    created 88407522s  gen 1378  seen 18s  ENG_LANC  gen 215506
    ip 10.210.140.146  src arp
  vd root/0  62:60:11:05:f5:09  gen 14984284  req OUA/34
    created 896283s  gen 14976979  seen 882937s  Guest  gen 440830
    ip 172.176.0.23  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '16'  src dhcp  id 191  weight 130
    host 'A57-von-Sebastian'  src dhcp
  vd root/0  c2:8b:5e:21:ba:32  gen 15451487  req OUA/34
    created 1135086s  gen 14839399  seen 32747s  CORP WIRELESS  gen 449247
    ip 10.210.68.57  src arp
    os 'Android'  src dhcp  id 191  weight 130
    software version '12'  src dhcp  id 191  weight 130
    host 'jtexugo-Handy'  src dhcp
  vd root/0  e4:30:22:30:8a:00  gen 157  req OHUSA/3e
    created 88407668s  gen 156  seen 7s  SECURITY_CAMERA  gen 63
    ip 10.210.32.97  src mac
  vd root/0  e4:30:22:30:8a:02  gen 235  req OHUSA/3e
    created 88407668s  gen 234  seen 7s  SECURITY_CAMERA  gen 102
    ip 10.210.32.98  src mac
  vd root/0  e4:30:22:30:8a:03  gen 203  req OHUSA/3e
    created 88407668s  gen 202  seen 7s  SECURITY_CAMERA  gen 86
    ip 10.210.32.11  src mac
  vd root/0  e4:30:22:30:8a:04  gen 399  req OHUSA/3e
    created 88407668s  gen 398  seen 7s  SECURITY_CAMERA  gen 184
    ip 10.210.32.24  src mac
  vd root/0  e4:30:22:30:8a:05  gen 331  req OHUSA/3e
    created 88407668s  gen 330  seen 7s  SECURITY_CAMERA  gen 150
    ip 10.210.32.99  src mac
  vd root/0  e4:30:22:30:8a:06  gen 379  req OHUSA/3e
    created 88407668s  gen 377  seen 7s  SECURITY_CAMERA  gen 174
    ip 10.210.32.100  src mac
  vd root/0  e4:30:22:30:8a:07  gen 257  req OHUSA/3e
    created 88407668s  gen 256  seen 7s  SECURITY_CAMERA  gen 113
    ip 10.210.32.101  src mac
  vd root/0  e4:30:22:30:8a:08  gen 341  req OHUSA/3e
    created 88407668s  gen 340  seen 7s  SECURITY_CAMERA  gen 155
    ip 10.210.32.102  src mac
  vd root/0  e4:30:22:30:8a:09  gen 255  req OHUSA/3e
    created 88407668s  gen 254  seen 7s  SECURITY_CAMERA  gen 112
    ip 10.210.32.103  src mac
  vd root/0  e4:30:22:30:8a:0a  gen 323  req OHUSA/3e
    created 88407668s  gen 322  seen 7s  SECURITY_CAMERA  gen 146
    ip 10.210.32.39  src mac
  vd root/0  e4:30:22:30:8a:0c  gen 347  req OHUSA/3e
    created 88407668s  gen 346  seen 7s  SECURITY_CAMERA  gen 158
    ip 10.210.32.18  src mac
  vd root/0  e4:30:22:30:8a:0d  gen 274  req OHUSA/3e
    created 88407668s  gen 271  seen 7s  SECURITY_CAMERA  gen 121
    ip 10.210.32.104  src mac
  vd root/0  e4:30:22:30:8a:0f  gen 162  req OHUSA/3e
    created 88407668s  gen 161  seen 7s  SECURITY_CAMERA  gen 66
    ip 10.210.32.105  src mac
  vd root/0  e4:30:22:30:8a:10  gen 247  req OHUSA/3e
    created 88407668s  gen 246  seen 7s  SECURITY_CAMERA  gen 108
    ip 10.210.32.27  src mac
  vd root/0  ea:69:b1:f0:70:4c  gen 14927905  req OHUSA/3e
    created 980620s  gen 14927897  seen 973828s  CORP WIRELESS  gen 439895
    ip 10.210.68.36  src arp
    hardware vendor 'Apple'  src http  id 1715  weight 128
  vd root/0  e4:30:22:30:89:97  gen 217  req OHUSA/3e
    created 88407668s  gen 216  seen 7s  SECURITY_CAMERA  gen 93
    ip 10.210.32.47  src mac
  vd root/0  e4:30:22:30:89:98  gen 279  req OHUSA/3e
    created 88407668s  gen 278  seen 7s  SECURITY_CAMERA  gen 124
    ip 10.210.32.48  src mac
  vd root/0  e4:30:22:30:89:99  gen 265  req OHUSA/3e
    created 88407668s  gen 264  seen 7s  SECURITY_CAMERA  gen 117
    ip 10.210.32.49  src mac
  vd root/0  e4:30:22:30:89:9a  gen 389  req OHUSA/3e
    created 88407668s  gen 388  seen 7s  SECURITY_CAMERA  gen 179
    ip 10.210.32.50  src mac
  vd root/0  e4:30:22:30:89:9b  gen 245  req OHUSA/3e
    created 88407668s  gen 244  seen 7s  SECURITY_CAMERA  gen 107
    ip 10.210.32.28  src mac
  vd root/0  e4:30:22:30:89:9c  gen 311  req OHUSA/3e
    created 88407668s  gen 310  seen 7s  SECURITY_CAMERA  gen 140
    ip 10.210.32.41  src mac
  vd root/0  e4:30:22:30:89:9d  gen 187  req OHUSA/3e
    created 88407668s  gen 186  seen 7s  SECURITY_CAMERA  gen 78
    ip 10.210.32.25  src mac
  vd root/0  e4:30:22:30:89:9e  gen 180  req OHUSA/3e
    created 88407668s  gen 179  seen 7s  SECURITY_CAMERA  gen 75
    ip 10.210.32.51  src mac
  vd root/0  e4:30:22:30:89:9f  gen 285  req OHUSA/3e
    created 88407668s  gen 284  seen 7s  SECURITY_CAMERA  gen 127
    ip 10.210.32.52  src mac
  vd root/0  e4:30:22:30:89:a0  gen 325  req OHUSA/3e
    created 88407668s  gen 324  seen 7s  SECURITY_CAMERA  gen 147
    ip 10.210.32.53  src mac
  vd root/0  e4:30:22:30:89:a1  gen 164  req OHUSA/3e
    created 88407668s  gen 163  seen 7s  SECURITY_CAMERA  gen 67
    ip 10.210.32.16  src mac
  vd root/0  e4:30:22:30:89:a2  gen 401  req OHUSA/3e
    created 88407668s  gen 400  seen 7s  SECURITY_CAMERA  gen 185
    ip 10.210.32.32  src mac
  vd root/0  e4:30:22:30:89:a3  gen 281  req OHUSA/3e
    created 88407668s  gen 280  seen 7s  SECURITY_CAMERA  gen 125
    ip 10.210.32.54  src mac
  vd root/0  e4:30:22:30:89:a4  gen 189  req OHUSA/3e
    created 88407668s  gen 188  seen 7s  SECURITY_CAMERA  gen 79
    ip 10.210.32.30  src mac
  vd root/0  e4:30:22:30:89:a5  gen 381  req OHUSA/3e
    created 88407668s  gen 380  seen 7s  SECURITY_CAMERA  gen 175
    ip 10.210.32.55  src mac
  vd root/0  e4:30:22:30:89:a7  gen 238719  req OHUSA/3e
    created 88407668s  gen 354  seen 7s  SECURITY_CAMERA  gen 119975
    ip 10.210.32.56  src mac
  vd root/0  e4:30:22:30:89:a8  gen 238724  req OHUSA/3e
    created 88407668s  gen 206  seen 7s  SECURITY_CAMERA  gen 119980
    ip 10.210.32.57  src mac
  vd root/0  e4:30:22:30:89:a9  gen 238720  req OHUSA/3e
    created 88407668s  gen 276  seen 7s  SECURITY_CAMERA  gen 119976
    ip 10.210.32.58  src mac
  vd root/0  e4:30:22:30:89:aa  gen 211  req OHUSA/3e
    created 88407668s  gen 210  seen 7s  SECURITY_CAMERA  gen 90
    ip 10.210.32.59  src mac
  vd root/0  e4:30:22:30:89:ab  gen 238714  req OHUSA/3e
    created 88407668s  gen 336  seen 7s  SECURITY_CAMERA  gen 119970
    ip 10.210.32.60  src mac
  vd root/0  e4:30:22:30:89:ac  gen 363  req OHUSA/3e
    created 88407668s  gen 362  seen 7s  SECURITY_CAMERA  gen 166
    ip 10.210.32.61  src mac
  vd root/0  e4:30:22:30:89:ad  gen 229  req OHUSA/3e
    created 88407668s  gen 228  seen 7s  SECURITY_CAMERA  gen 99
    ip 10.210.32.62  src mac
  vd root/0  e4:30:22:30:89:ae  gen 345  req OHUSA/3e
    created 88407668s  gen 344  seen 7s  SECURITY_CAMERA  gen 157
    ip 10.210.32.63  src mac
  vd root/0  e4:30:22:30:89:af  gen 219  req OHUSA/3e
    created 88407668s  gen 218  seen 7s  SECURITY_CAMERA  gen 94
    ip 10.210.32.106  src mac
  vd root/0  e4:30:22:30:89:b0  gen 225  req OHUSA/3e
    created 88407668s  gen 224  seen 7s  SECURITY_CAMERA  gen 97
    ip 10.210.32.64  src mac
  vd root/0  e4:30:22:30:89:b1  gen 391  req OHUSA/3e
    created 88407668s  gen 390  seen 7s  SECURITY_CAMERA  gen 180
    ip 10.210.32.40  src mac
  vd root/0  e4:30:22:30:89:b2  gen 233  req OHUSA/3e
    created 88407668s  gen 231  seen 7s  SECURITY_CAMERA  gen 101
    ip 10.210.32.19  src mac
  vd root/0  e4:30:22:30:89:b4  gen 289  req OHUSA/3e
    created 88407668s  gen 288  seen 7s  SECURITY_CAMERA  gen 129
    ip 10.210.32.23  src mac
  vd root/0  e4:30:22:30:89:b5  gen 259  req OHUSA/3e
    created 88407668s  gen 258  seen 7s  SECURITY_CAMERA  gen 114
    ip 10.210.32.65  src mac
  vd root/0  e4:30:22:30:89:b6  gen 197  req OHUSA/3e
    created 88407668s  gen 196  seen 7s  SECURITY_CAMERA  gen 83
    ip 10.210.32.66  src mac
  vd root/0  e4:30:22:30:89:b8  gen 273  req OHUSA/3e
    created 88407668s  gen 270  seen 7s  SECURITY_CAMERA  gen 120
    ip 10.210.32.68  src mac
  vd root/0  e4:30:22:30:89:b9  gen 292  req OHUSA/3e
    created 88407668s  gen 290  seen 7s  SECURITY_CAMERA  gen 130
    ip 10.210.32.13  src mac
  vd root/0  e4:30:22:30:89:ba  gen 397  req OHUSA/3e
    created 88407668s  gen 396  seen 7s  SECURITY_CAMERA  gen 183
    ip 10.210.32.69  src mac
  vd root/0  e4:30:22:30:89:bb  gen 385  req OHUSA/3e
    created 88407668s  gen 384  seen 7s  SECURITY_CAMERA  gen 177
    ip 10.210.32.34  src mac
  vd root/0  e4:30:22:30:89:bc  gen 227  req OHUSA/3e
    created 88407668s  gen 226  seen 7s  SECURITY_CAMERA  gen 98
    ip 10.210.32.70  src mac
  vd root/0  e4:30:22:30:89:bd  gen 319  req OHUSA/3e
    created 88407668s  gen 318  seen 7s  SECURITY_CAMERA  gen 144
    ip 10.210.32.14  src mac
  vd root/0  e4:30:22:30:89:c0  gen 351  req OHUSA/3e
    created 88407668s  gen 350  seen 7s  SECURITY_CAMERA  gen 160
    ip 10.210.32.128  src mac
  vd root/0  e4:30:22:30:89:c1  gen 307  req OHUSA/3e
    created 88407668s  gen 306  seen 7s  SECURITY_CAMERA  gen 138
    ip 10.210.32.71  src mac
  vd root/0  e4:30:22:30:89:c2  gen 238723  req OHUSA/3e
    created 88407668s  gen 291  seen 7s  SECURITY_CAMERA  gen 119979
    ip 10.210.32.73  src mac
  vd root/0  e4:30:22:30:89:c3  gen 238706  req OHUSA/3e
    created 88407668s  gen 376  seen 7s  SECURITY_CAMERA  gen 119962
    ip 10.210.32.72  src mac
  vd root/0  e4:30:22:30:89:c6  gen 155  req OHUSA/3e
    created 88407668s  gen 154  seen 7s  SECURITY_CAMERA  gen 62
    ip 10.210.32.117  src mac
  vd root/0  e4:30:22:30:89:c7  gen 403  req OHUSA/3e
    created 88407668s  gen 402  seen 7s  SECURITY_CAMERA  gen 186
    ip 10.210.32.74  src mac
  vd root/0  e4:30:22:30:89:c8  gen 170  req OHUSA/3e
    created 88407668s  gen 169  seen 7s  SECURITY_CAMERA  gen 70
    ip 10.210.32.75  src mac
  vd root/0  e4:30:22:30:89:ca  gen 309  req OHUSA/3e
    created 88407668s  gen 308  seen 7s  SECURITY_CAMERA  gen 139
    ip 10.210.32.115  src mac
  vd root/0  e4:30:22:30:89:cb  gen 268  req OHUSA/3e
    created 88407668s  gen 266  seen 7s  SECURITY_CAMERA  gen 118
    ip 10.210.32.77  src mac
  vd root/0  e4:30:22:30:89:cd  gen 315  req OHUSA/3e
    created 88407668s  gen 314  seen 7s  SECURITY_CAMERA  gen 142
    ip 10.210.32.78  src mac
  vd root/0  e4:30:22:30:89:ce  gen 243  req OHUSA/3e
    created 88407668s  gen 242  seen 7s  SECURITY_CAMERA  gen 106
    ip 10.210.32.116  src mac
  vd root/0  e4:30:22:30:89:d0  gen 343  req OHUSA/3e
    created 88407668s  gen 342  seen 7s  SECURITY_CAMERA  gen 156
    ip 10.210.32.79  src mac
  vd root/0  e4:30:22:30:89:d1  gen 301  req OHUSA/3e
    created 88407668s  gen 300  seen 7s  SECURITY_CAMERA  gen 135
    ip 10.210.32.80  src mac
  vd root/0  e4:30:22:30:89:d2  gen 153  req OHUSA/3e
    created 88407668s  gen 152  seen 7s  SECURITY_CAMERA  gen 61
    ip 10.210.32.81  src mac
  vd root/0  e4:30:22:30:89:d3  gen 185  req OHUSA/3e
    created 88407668s  gen 184  seen 7s  SECURITY_CAMERA  gen 77
    ip 10.210.32.82  src mac
  vd root/0  e4:30:22:30:89:d8  gen 387  req OHUSA/3e
    created 88407668s  gen 386  seen 7s  SECURITY_CAMERA  gen 178
    ip 10.210.32.26  src mac
  vd root/0  e4:30:22:30:89:d9  gen 232  req OHUSA/3e
    created 88407668s  gen 230  seen 7s  SECURITY_CAMERA  gen 100
    ip 10.210.32.83  src mac
  vd root/0  e4:30:22:30:89:da  gen 359  req OHUSA/3e
    created 88407668s  gen 358  seen 7s  SECURITY_CAMERA  gen 164
    ip 10.210.32.84  src mac
  vd root/0  e4:30:22:30:89:db  gen 393  req OHUSA/3e
    created 88407668s  gen 392  seen 7s  SECURITY_CAMERA  gen 181
    ip 10.210.32.140  src mac
  vd root/0  e4:30:22:30:89:df  gen 238722  req OHUSA/3e
    created 88407668s  gen 190  seen 7s  SECURITY_CAMERA  gen 119978
    ip 10.210.32.147  src mac
  vd root/0  e4:30:22:30:89:e0  gen 329  req OHUSA/3e
    created 88407668s  gen 328  seen 7s  SECURITY_CAMERA  gen 149
    ip 10.210.32.33  src mac
  vd root/0  e4:30:22:30:89:e1  gen 238718  req OHUSA/3e
    created 88407668s  gen 208  seen 7s  SECURITY_CAMERA  gen 119974
    ip 10.210.32.167  src mac
  vd root/0  e4:30:22:30:89:e2  gen 238729  req OHUSA/3e
    created 88407668s  gen 370  seen 7s  SECURITY_CAMERA  gen 119985
    ip 10.210.32.146  src mac
  vd root/0  e4:30:22:30:89:e3  gen 357  req OHUSA/3e
    created 88407668s  gen 356  seen 7s  SECURITY_CAMERA  gen 163
    ip 10.210.32.86  src mac
  vd root/0  e4:30:22:30:89:e4  gen 405  req OHUSA/3e
    created 88407668s  gen 404  seen 7s  SECURITY_CAMERA  gen 187
    ip 10.210.32.87  src mac
  vd root/0  e4:30:22:30:89:e5  gen 241  req OHUSA/3e
    created 88407668s  gen 240  seen 7s  SECURITY_CAMERA  gen 105
    ip 10.210.32.88  src mac
  vd root/0  e4:30:22:30:89:e7  gen 383  req OHUSA/3e
    created 88407668s  gen 382  seen 7s  SECURITY_CAMERA  gen 176
    ip 10.210.32.89  src mac
  vd root/0  e4:30:22:30:89:e8  gen 299  req OHUSA/3e
    created 88407668s  gen 298  seen 7s  SECURITY_CAMERA  gen 134
    ip 10.210.32.20  src mac
  vd root/0  e4:30:22:30:89:e9  gen 168  req OHUSA/3e
    created 88407668s  gen 167  seen 7s  SECURITY_CAMERA  gen 69
    ip 10.210.32.31  src mac
  vd root/0  e4:30:22:30:89:ea  gen 313  req OHUSA/3e
    created 88407668s  gen 312  seen 7s  SECURITY_CAMERA  gen 141
    ip 10.210.32.112  src mac
  vd root/0  e4:30:22:30:89:eb  gen 327  req OHUSA/3e
    created 88407668s  gen 326  seen 7s  SECURITY_CAMERA  gen 148
    ip 10.210.32.90  src mac
  vd root/0  e4:30:22:30:89:ed  gen 238716  req OHUSA/3e
    created 88407668s  gen 262  seen 7s  SECURITY_CAMERA  gen 119972
    ip 10.210.32.91  src mac
  vd root/0  e4:30:22:30:89:ef  gen 221  req OHUSA/3e
    created 88407668s  gen 220  seen 7s  SECURITY_CAMERA  gen 95
    ip 10.210.32.153  src mac
  vd root/0  e4:30:22:30:89:f1  gen 238726  req OHUSA/3e
    created 88407668s  gen 366  seen 7s  SECURITY_CAMERA  gen 119982
    ip 10.210.32.92  src mac
  vd root/0  e4:30:22:30:89:f2  gen 238712  req OHUSA/3e
    created 88407668s  gen 214  seen 7s  SECURITY_CAMERA  gen 119968
    ip 10.210.32.145  src mac
  vd root/0  e4:30:22:30:89:f5  gen 238711  req OHUSA/3e
    created 88407668s  gen 194  seen 7s  SECURITY_CAMERA  gen 119967
    ip 10.210.32.37  src mac
  vd root/0  e4:30:22:30:89:f6  gen 283  req OHUSA/3e
    created 88407668s  gen 282  seen 7s  SECURITY_CAMERA  gen 126
    ip 10.210.32.93  src mac
  vd root/0  e4:30:22:30:89:f8  gen 349  req OHUSA/3e
    created 88407668s  gen 348  seen 7s  SECURITY_CAMERA  gen 159
    ip 10.210.32.94  src mac
  vd root/0  e4:30:22:30:89:f9  gen 375  req OHUSA/3e
    created 88407668s  gen 374  seen 7s  SECURITY_CAMERA  gen 172
    ip 10.210.32.111  src mac
  vd root/0  e4:30:22:30:89:fa  gen 297  req OHUSA/3e
    created 88407668s  gen 296  seen 7s  SECURITY_CAMERA  gen 133
    ip 10.210.32.29  src mac
  vd root/0  e4:30:22:30:89:fb  gen 176  req OHUSA/3e
    created 88407668s  gen 175  seen 7s  SECURITY_CAMERA  gen 73
    ip 10.210.32.15  src mac
  vd root/0  e4:30:22:30:89:fc  gen 238713  req OHUSA/3e
    created 88407668s  gen 267  seen 7s  SECURITY_CAMERA  gen 119969
    ip 10.210.32.38  src mac
  vd root/0  e4:30:22:30:89:fd  gen 238727  req OHUSA/3e
    created 88407668s  gen 316  seen 7s  SECURITY_CAMERA  gen 119983
    ip 10.210.32.133  src mac
  vd root/0  e4:30:22:30:89:fe  gen 183  req OHUSA/3e
    created 88407668s  gen 182  seen 7s  SECURITY_CAMERA  gen 76
    ip 10.210.32.95  src mac
  vd root/0  e4:30:22:30:89:ff  gen 395  req OHUSA/3e
    created 88407668s  gen 394  seen 7s  SECURITY_CAMERA  gen 182
    ip 10.210.32.96  src mac
  vd root/0  00:50:56:53:d9:ae  gen 12430005  req OHUSA/3e
    created 83886139s  gen 44629  seen 22s  ESXMGMT  gen 391433
  vd root/0  16:8d:35:87:1a:8f  gen 15075856  req OUA/34
    created 726487s  gen 15075853  seen 725706s  CORP WIRELESS  gen 442238
    ip 10.210.68.58  src arp
    hardware vendor 'realme'  src dhcp  id 6441  weight 255
    type 'Phone'  src dhcp  id 6441  weight 255
    family 'Smartphones'  src dhcp  id 6441  weight 255
    os 'Android'  src dhcp  id 6441  weight 255
    hardware version 'GT-7-Pro'  src dhcp  id 6441  weight 255
    software version '16'  src dhcp  id 6441  weight 255
    host 'realme-GT-7-Pro'  src dhcp
  vd root/0  00:50:56:57:5a:9a  gen 12430624  req HU/18
    created 70852971s  gen 161557  seen 22s  default  gen 391454
  vd root/0  e4:30:22:30:b1:a3  gen 12359969  req OHUSA/3e
    created 88407667s  gen 438  seen 5s  SECURITY_ExtDev  gen 389496
    ip 10.210.48.139  src mac
  vd root/0  e4:30:22:30:b1:bf  gen 456  req OHUSA/3e
    created 88407667s  gen 455  seen 6s  SECURITY_ExtDev  gen 215
    ip 10.210.48.162  src mac
  vd root/0  e4:30:22:30:b1:c0  gen 11888648  req OHUSA/3e
    created 7784258s  gen 11888263  seen 5s  SECURITY_ExtDev  gen 375484
    ip 10.210.48.170  src mac
  vd root/0  e4:30:22:30:b1:c1  gen 495  req OHUSA/3e
    created 88407667s  gen 458  seen 5s  SECURITY_ExtDev  gen 217
    ip 10.210.48.150  src mac
  vd root/0  e4:30:22:30:b1:c2  gen 3442270  req OHUSA/3e
    created 88407667s  gen 462  seen 3s  SECURITY_ExtDev  gen 220
    ip 10.210.48.163  src mac
  vd root/0  e4:30:22:30:b1:cd  gen 6994735  req OHUSA/3e
    created 88407667s  gen 496  seen 7s  SECURITY_ExtDev  gen 274009
    ip 10.210.48.124  src mac
  vd root/0  e4:30:22:30:b1:d0  gen 289890  req OHUSA/3e
    created 59974417s  gen 289812  seen 7s  SECURITY_CAMERA  gen 146031
    ip 10.210.32.123  src mac
  vd root/0  00:50:56:58:4c:13  gen 11280588  req OHUSA/3e
    created 83886321s  gen 44615  seen 22s  ESXMGMT  gen 358455
  vd root/0  d4:76:a0:d8:62:48  gen 12389272  req OUA/34
    created 88407664s  gen 584  seen 1s  WIRELESS_APs  gen 390300
    ip 10.210.96.47  src arp
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003385'  src capwap
  vd root/0  d4:76:a0:d8:65:08  gen 10906050  req OUA/34
    created 88407658s  gen 776  seen 3s  WIRELESS_APs  gen 332
    ip 10.210.96.29  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003407'  src capwap
  vd root/0  d4:76:a0:d8:65:28  gen 12308936  req OUA/34
    created 88407658s  gen 770  seen 4s  WIRELESS_APs  gen 331
    ip 10.210.96.35  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003408'  src capwap
  vd root/0  d4:76:a0:d8:62:c8  gen 12389276  req OUA/34
    created 88407666s  gen 547  seen 1s  WIRELESS_APs  gen 390301
    ip 10.210.96.46  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003389'  src capwap
  vd root/0  00:50:56:57:72:23  gen 11277213  req HU/18
    created 70777191s  gen 162393  seen 22s  default  gen 358280
  vd root/0  d4:76:a0:d8:63:e8  gen 10761131  req OUA/34
    created 88407668s  gen 77  seen 0s  WIRELESS_APs  gen 47
    ip 10.210.96.20  src mac
    hardware vendor 'Fortinet'  src fortiguard  id 0  weight 255
    type 'Network'  src fortiguard  id 0  weight 255
    family 'AP'  src fortiguard  id 0  weight 255
    os 'FortiAP OS'  src fortiguard  id 0  weight 255
    hardware version 'FortiAP-234F'  src fortiguard  id 0  weight 255
    host 'FP234FTF21003398'  src capwap
  vd root/0  d4:76:a0:d8:63:e9  gen 1656866  req OHUSA/3e
    created 88407529s  gen 1229  seen 22s  CORP WIRELESS  gen 196267
  vd root/0  d4:76:a0:d8:65:e8  gen 10798773  req OUA/34
    created 88407666s  gen 548  seen 0s  WIRELESS_APs  gen 253
    ip 10.210.96.14  src mac
    hardware vendor 'Fortinet'  src capwap  id 2679  weight 220
    type 'Network Generic'  src capwap  id 2679  weight 220
    family 'FortiAP'  src capwap  id 2679  weight 220
    os 'FortiAP OS'  src capwap  id 2679  weight 220
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003414'  src capwap
  vd root/0  e0:dc:a0:e8:ef:7d  gen 906  req OHUSA/3e
    created 88407647s  gen 905  seen 17s  ENG_LAND  gen 373
    ip 10.210.144.61  src arp
  vd root/0  e0:dc:a0:e8:ef:7e  gen 1654936  req OHUSA/3e
    created 88407521s  gen 1458  seen 19s  ENG_LAND  gen 196008
  vd root/0  e0:dc:a0:e8:ef:82  gen 1150438  req OHUSA/3e
    created 88407636s  gen 954  seen 19s  ENG_LANC  gen 184714
    ip 10.210.140.56  src arp
  vd root/0  e0:dc:a0:e8:ef:83  gen 1655188  req OHUSA/3e
    created 88407522s  gen 1362  seen 19s  ENG_LANC  gen 196065
  vd root/0  e0:dc:a0:e8:ef:87  gen 935  req OHUSA/3e
    created 88407641s  gen 934  seen 12s  ENG_LANC  gen 386
    ip 10.210.140.66  src arp
  vd root/0  e0:dc:a0:e8:ef:88  gen 1654864  req OHUSA/3e
    created 88407498s  gen 1624  seen 22s  ENG_LANC  gen 195988
  vd root/0  e0:dc:a0:e8:ef:91  gen 927  req OHUSA/3e
    created 88407643s  gen 926  seen 18s  ENG_LAND  gen 383
    ip 10.210.144.66  src arp
  vd root/0  e0:dc:a0:e8:ef:92  gen 1654743  req OHUSA/3e
    created 88407522s  gen 1432  seen 18s  ENG_LAND  gen 195972
  vd root/0  e0:dc:a0:e8:ef:93  gen 969  req OHUSA/3e
    created 88407685s  gen 16  seen 12s  ENG_LANC  gen 16
    ip 10.210.140.61  src arp
  vd root/0  e0:dc:a0:e8:ef:94  gen 1657822  req OHUSA/3e
    created 88407520s  gen 1538  seen 22s  ENG_LANC  gen 196310
  vd root/0  e0:dc:a0:e8:ef:ec  gen 885  req OHUSA/3e
    created 88407650s  gen 884  seen 7s  ENG_LAND  gen 362
    ip 10.210.144.56  src arp
  vd root/0  e0:dc:a0:e8:ef:ed  gen 1655010  req OHUSA/3e
    created 88407520s  gen 1544  seen 22s  ENG_LAND  gen 196037
  vd root/0  00:50:56:55:c3:2c  gen 11277216  req OHUSA/3e
    created 83886140s  gen 44625  seen 22s  ESXMGMT  gen 358283
  vd root/0  00:50:56:57:7d:b5  gen 11281508  req HU/18
    created 70768424s  gen 162573  seen 22s  default  gen 358492
  vd root/0  d4:76:a0:d8:77:e8  gen 11133870  req OUA/34
    created 88407657s  gen 801  seen 0s  WIRELESS_APs  gen 119960
    ip 10.210.96.57  src mac
    hardware vendor 'Fortinet'  src capwap  id 4  weight 230
    type 'Network Generic'  src capwap  id 4  weight 230
    family 'FortiAP'  src capwap  id 4  weight 230
    os 'FortiAP OS'  src capwap  id 4  weight 230
    hardware version '234F'  src capwap  id 2679  weight 220
    host 'FP234FTF21003558'  src capwap
  vd root/0  00:50:56:5b:05:6d  gen 11277212  req HU/18
    created 70777191s  gen 162394  seen 22s  default  gen 358279
  vd root/0  00:50:56:59:50:64  gen 12429601  req HU/18
    created 70773348s  gen 162469  seen 22s  default  gen 391410
  vd root/0  00:50:56:57:95:2d  gen 11279824  req OHUSA/3e
    created 83886320s  gen 44616  seen 22s  ESXMGMT  gen 358399
  vd root/0  00:50:56:57:97:92  gen 11277392  req HU/18
    created 70868224s  gen 161275  seen 22s  default  gen 358297
  vd root/0  10:3d:1c:9b:42:1d  gen 14418907  req OUA/34
    created 3738082s  gen 13349906  seen 1845509s  Guest  gen 430957
    ip 172.176.0.15  src arp  ip6 2a02:1210:221d:ea00:7501:dea2:b464:e1b0  src mac
    os 'Windows'  src http  id 1077  weight 130
    software version '10/11'  src http  id 1453  weight 130
    host 'LAPTOP-3H4A3JB4'  src dhcp
  vd root/0  00:50:56:56:c4:37  gen 11277396  req OHUSA/3e
    created 83886140s  gen 44628  seen 22s  ESXMGMT  gen 358301
  vd root/0  00:50:56:58:81:b2  gen 11279827  req OHUSA/3e
    created 83886320s  gen 44620  seen 22s  ESXMGMT  gen 358402
"""

# 1. 將整段文字以 "vd " 為界線，切割成一個個獨立的設備區塊
blocks = raw_data.split('vd ')

print(f"{'MAC Address':<20} | {'VLAN/Interface':<15} | {'IP Address'}")
print("-" * 55)

# 2. 針對每一個設備區塊進行單獨解析
for block in blocks:
    if not block.strip():
        continue  # 跳過空白區塊

    # 提取 MAC 位址 (尋找 17 個字元的 MAC 格式)
    mac_match = re.search(r"([a-f0-9:]{17})", block)
    if not mac_match:
        continue  # 如果連 MAC 都沒有，就跳過這個區塊
    mac = mac_match.group(1)

    # 提取 VLAN/Interface (尋找 seen [數字]s 後面的字串)
    vlan_match = re.search(r"seen\s+\d+s\s+(.+?)\s+gen", block)
    vlan = vlan_match.group(1) if vlan_match else "Unknown"

    # 提取 IP 位址 (尋找 ip x.x.x.x 格式)
    ip_match = re.search(r"ip\s+(\d{1,3}(?:\.\d{1,3}){3})", block)
    ip = ip_match.group(1) if ip_match else "N/A"

    # 印出結果
    print(f"{mac:<20} | {vlan:<15} | {ip}")