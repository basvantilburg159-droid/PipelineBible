"""
PipelineBible v1.1 – Professional Pipeline & Piping Standards Tool
Extended to NPS 56, ASME & DIN Standards, B16.47 Series A/B

Version 1.1 additions:
- Enhanced data validation
- Pipe lookup helper functions
- Flange lookup helper functions  
- Export utilities for CSV/JSON
- Error handling improvements
"""

import math, traceback, datetime, csv, json

# Optional dependencies for GUI
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Optional dependencies for GUI and plotting
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.backends.backend_pdf import PdfPages
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ==================================================
#  COLORS – Dark + Gold
# ==================================================
class C:
    BG="#1a1a1a";BG2="#222222";BG3="#2a2a2a";BG4="#303030"
    HD="#1e1e1e";FG="#e0d8c8";FG2="#a09880";FG3="#706858"
    AC="#f0a500";AC2="#ffb820";AC3="#d48800";GRN="#55aa44"
    RED="#cc4444";BLU="#4488cc";PUR="#9966cc";SEL="#3a3018"
    BD="#444030";INP="#2a2a22"

# ==================================================
#  CSV DATA (embedded)
# ==================================================
CSV_PIPE_OD = """nps_inch,dn,od_mm
0.125,6,10.3
0.25,8,13.7
0.375,10,17.1
0.5,15,21.3
0.75,20,26.7
1.0,25,33.4
1.25,32,42.2
1.5,40,48.3
2.0,50,60.3
2.5,65,73.0
3.0,80,88.9
3.5,90,101.6
4.0,100,114.3
5.0,125,141.3
6.0,150,168.3
8.0,200,219.1
10.0,250,273.0
12.0,300,323.9
14.0,350,355.6
16.0,400,406.4
18.0,450,457.0
20.0,500,508.0
22.0,550,559.0
24.0,600,610.0
26.0,650,660.0
28.0,700,711.0
30.0,750,762.0
32.0,800,813.0
34.0,850,864.0
36.0,900,914.0
38.0,950,965.0
40.0,1000,1016.0
42.0,1050,1067.0
44.0,1100,1118.0
46.0,1150,1168.0
48.0,1200,1219.0
50.0,1250,1270.0
52.0,1300,1321.0
54.0,1350,1372.0
56.0,1400,1422.0
"""

CSV_SCHEDULES = """schedule,description
5,Extra thin
10,Thin wall
20,Light
30,Medium light
40,Standard
60,Medium heavy
80,Extra strong
100,Heavy
120,Extra heavy
140,Very heavy
160,Double extra heavy
STD,Standard weight
XS,Extra strong
XXS,Double extra strong
"""

CSV_B16_47_FLANGES = """series,class,nps_inch,flange_od_mm,bolt_circle_mm,bolt_holes,bolt_size_mm,thickness_mm
A,150,26,762,685.8,20,38,69.9
A,150,28,813,736.6,20,38,73.2
A,150,30,864,787.4,20,38,76.2
A,150,32,914,838.2,24,38,79.5
A,150,34,965,889.0,24,38,82.6
A,150,36,1020,939.8,24,38,85.9
A,150,38,1070,990.6,28,38,89.0
A,150,40,1120,1041.4,28,38,92.0
A,150,42,1170,1092.2,28,45,101.6
A,150,44,1220,1143.0,28,45,104.0
A,150,46,1270,1193.8,28,45,108.0
A,150,48,1321,1244.6,32,45,114.3
A,150,50,1372,1295.4,32,45,118.0
A,150,52,1422,1346.2,32,45,121.0
A,150,54,1473,1397.0,36,45,127.0
A,150,56,1524,1447.8,36,45,133.0
B,150,26,660,609.6,20,35,57.0
B,150,28,711,660.4,20,35,60.0
B,150,30,762,711.2,20,35,63.0
B,150,32,813,762.0,20,35,67.0
B,150,34,864,812.8,24,35,70.0
B,150,36,914,863.6,24,35,73.0
B,150,38,965,914.4,24,35,76.0
B,150,40,1016,965.2,24,35,79.0
B,150,42,1067,1016.0,28,41,83.0
B,150,44,1118,1066.8,28,41,86.0
B,150,46,1168,1117.6,28,41,89.0
B,150,48,1219,1168.4,28,41,92.0
B,150,50,1270,1219.2,32,41,95.0
B,150,52,1321,1270.0,32,41,98.0
B,150,54,1372,1320.8,32,41,102.0
B,150,56,1422,1371.6,36,41,105.0
"""

def _read_csv_str(s):
    r = csv.DictReader(s.strip().splitlines())
    return list(r)

PIPE_OD = {r["nps_inch"].strip(): float(r["od_mm"]) for r in _read_csv_str(CSV_PIPE_OD)}
SCHEDULES = [r["schedule"] for r in _read_csv_str(CSV_SCHEDULES)]

# ==================================================
#  DATA – ASME B36.10M (base data)
# ==================================================
ASME_PIPES=[
    ("1/2",21.3,[("5S",1.65),("10S",2.11),("40/STD",2.77),("80/XS",3.73),("160",4.75),("XXS",7.47)]),
    ("3/4",26.7,[("5S",1.65),("10S",2.11),("40/STD",2.87),("80/XS",3.91),("160",5.56),("XXS",7.82)]),
    ("1",33.4,[("5S",1.65),("10S",2.77),("40/STD",3.38),("80/XS",4.55),("160",6.35),("XXS",9.09)]),
    ("1-1/4",42.2,[("5S",1.65),("10S",2.77),("40/STD",3.56),("80/XS",4.85),("160",6.35),("XXS",9.70)]),
    ("1-1/2",48.3,[("5S",1.65),("10S",2.77),("40/STD",3.68),("80/XS",5.08),("160",7.14),("XXS",10.15)]),
    ("2",60.3,[("5S",1.65),("10S",2.77),("40/STD",3.91),("80/XS",5.54),("160",8.74),("XXS",11.07)]),
    ("2-1/2",73.0,[("5S",2.11),("10S",3.05),("40/STD",5.16),("80/XS",7.01),("160",9.53),("XXS",14.02)]),
    ("3",88.9,[("5S",2.11),("10S",3.05),("40/STD",5.49),("80/XS",7.62),("160",11.13),("XXS",15.24)]),
    ("4",114.3,[("5S",2.11),("10S",3.05),("20",4.78),("40/STD",6.02),("60",7.14),("80/XS",8.56),("100",11.13),("120",13.49),("160",17.12)]),
    ("5",141.3,[("5S",2.77),("10S",3.40),("40/STD",6.55),("80/XS",9.53),("120",15.88),("160",19.05)]),
    ("6",168.3,[("5S",2.77),("10S",3.40),("40/STD",7.11),("80/XS",10.97),("120",18.26),("160",21.95)]),
    ("8",219.1,[("5S",2.77),("10S",3.76),("20",6.35),("30",7.04),("40/STD",8.18),("60",10.31),("80/XS",12.70),("100",15.09),("120",18.26),("160",23.01)]),
    ("10",273.1,[("5S",3.40),("10S",4.19),("20",6.35),("30",7.80),("40/STD",9.27),("60",12.70),("80/XS",15.09),("100",18.26),("120",21.44),("160",28.58)]),
    ("12",323.9,[("5S",3.96),("10S",4.57),("20",6.35),("30",8.38),("STD",9.53),("40",10.31),("XS",12.70),("60",14.27),("80",17.48),("100",21.44),("120",25.40),("160",33.32)]),
    ("14",355.6,[("10S",4.78),("20",7.92),("30",9.53),("STD",9.53),("40",11.13),("XS",12.70),("60",15.09),("80",19.05)]),
    ("16",406.4,[("10S",4.78),("20",7.92),("30",9.53),("STD",9.53),("40",12.70),("XS",12.70),("60",16.66),("80",21.44)]),
    ("18",457.2,[("10S",4.78),("20",7.92),("STD",9.53),("30",11.13),("XS",12.70),("40",14.27),("60",19.05),("80",23.83)]),
    ("20",508.0,[("10S",5.54),("20",9.53),("STD",9.53),("30",12.70),("XS",12.70),("40",15.09),("60",20.62),("80",26.19)]),
    ("24",609.6,[("10S",6.35),("20",9.53),("STD",9.53),("30",14.27),("XS",12.70),("40",17.48),("60",24.61),("80",30.96)]),
]

# Add NPS 26–56 from CSV (OD only, schedules known but WT missing)
def extend_asme_pipes(base):
    existing = {p[0]: p for p in base}
    out = list(base)
    for nps, od in PIPE_OD.items():
        if nps in existing:
            continue
        schs = [(sch, None) for sch in SCHEDULES]
        out.append((nps, od, schs))
    def nk_float(n):
        try: return float(n.replace("-","."))
        except: return 0
    out.sort(key=lambda x: nk_float(x[0]))
    return out

ASME_PIPES = extend_asme_pipes(ASME_PIPES)

# DIN EN 10220 / ISO 4200 Pipes
DIN_PIPES=[
    ("DN15",21.3,[("1.5",1.5),("2.0",2.0),("2.6",2.6),("3.2",3.2),("4.0",4.0)]),
    ("DN20",26.9,[("1.5",1.5),("2.0",2.0),("2.3",2.3),("2.6",2.6),("3.2",3.2)]),
    ("DN25",33.7,[("2.0",2.0),("2.6",2.6),("3.2",3.2),("4.0",4.0),("4.5",4.5)]),
    ("DN32",42.4,[("2.0",2.0),("2.6",2.6),("3.2",3.2),("4.0",4.0),("5.0",5.0)]),
    ("DN40",48.3,[("2.0",2.0),("2.6",2.6),("3.2",3.2),("4.0",4.0),("5.0",5.0)]),
    ("DN50",60.3,[("2.0",2.0),("2.3",2.3),("2.9",2.9),("3.2",3.2),("4.0",4.0),("5.6",5.6)]),
    ("DN65",76.1,[("2.0",2.0),("2.3",2.3),("2.9",2.9),("3.2",3.2),("3.6",3.6),("5.6",5.6)]),
    ("DN80",88.9,[("2.3",2.3),("2.6",2.6),("3.2",3.2),("4.0",4.0),("5.0",5.0),("7.1",7.1)]),
    ("DN100",114.3,[("2.6",2.6),("2.9",2.9),("3.2",3.2),("3.6",3.6),("5.0",5.0),("6.3",6.3),("8.8",8.8)]),
    ("DN125",139.7,[("3.2",3.2),("4.0",4.0),("5.0",5.0),("6.3",6.3)]),
    ("DN150",168.3,[("3.2",3.2),("3.6",3.6),("4.0",4.0),("4.5",4.5),("5.6",5.6),("7.1",7.1),("11.0",11.0)]),
    ("DN200",219.1,[("3.2",3.2),("4.0",4.0),("4.5",4.5),("5.0",5.0),("5.9",5.9),("6.3",6.3),("8.0",8.0),("12.5",12.5)]),
    ("DN250",273.1,[("4.0",4.0),("5.0",5.0),("5.6",5.6),("6.3",6.3),("7.1",7.1),("8.8",8.8),("12.5",12.5)]),
    ("DN300",323.9,[("4.0",4.0),("4.5",4.5),("5.0",5.0),("5.6",5.6),("6.3",6.3),("7.1",7.1),("8.0",8.0),("10.0",10.0),("14.2",14.2)]),
    ("DN350",355.6,[("4.5",4.5),("5.0",5.0),("5.6",5.6),("6.3",6.3),("8.0",8.0),("10.0",10.0)]),
    ("DN400",406.4,[("4.5",4.5),("5.0",5.0),("5.6",5.6),("6.3",6.3),("8.0",8.0),("10.0",10.0),("12.5",12.5)]),
    ("DN500",508.0,[("5.0",5.0),("5.6",5.6),("6.3",6.3),("8.0",8.0),("10.0",10.0),("12.5",12.5)]),
    ("DN600",610.0,[("5.6",5.6),("6.3",6.3),("7.1",7.1),("8.0",8.0),("10.0",10.0),("12.5",12.5)]),
]

BENDS=[("1D",1.0,"Short Radius"),("1.5D",1.5,"Long Radius"),("2D",2.0,"2D"),
       ("3D",3.0,"3D Pipeline"),("5D",5.0,"5D Pipeline"),("10D",10.0,"10D Special")]

# ── ASME B16.5 Flanges: NPS,Class,FlangeOD,ThkWN,BC,Nbolts,BoltDia,RF_OD,Bore ──
FTYPE_CODES=["WN","SO","BL","SW","TH","LJ"]
FTYPE_THK={"WN":1.0,"SO":1.0,"BL":1.15,"SW":1.0,"TH":1.0,"LJ":1.0}
ASME_FL=[
    ("1/2",150,89,11.2,60.3,4,"1/2",35.1,15.7),("3/4",150,99,12.7,69.9,4,"1/2",42.9,20.9),
    ("1",150,108,14.2,79.4,4,"1/2",50.8,26.6),("1-1/4",150,117,15.7,89.0,4,"1/2",63.5,35.1),
    ("1-1/2",150,127,17.5,98.4,4,"1/2",73.0,40.9),("2",150,152,19.0,120.7,4,"5/8",92.1,52.5),
    ("2-1/2",150,178,22.4,139.7,4,"5/8",104.8,62.7),("3",150,190,23.9,152.4,4,"5/8",127.0,78.0),
    ("4",150,229,23.9,190.5,8,"5/8",157.2,102.4),("5",150,254,23.9,215.9,8,"3/4",185.7,128.2),
    ("6",150,279,25.4,241.3,8,"3/4",215.9,154.1),("8",150,343,28.4,298.5,8,"3/4",269.9,202.7),
    ("10",150,406,30.2,362.0,12,"7/8",323.8,254.5),("12",150,483,31.8,431.8,12,"7/8",381.0,304.8),
    ("14",150,533,35.1,476.3,12,"1",412.8,336.6),("16",150,597,36.6,539.8,16,"1",469.9,387.4),
    ("18",150,635,39.6,577.9,16,"1-1/8",533.4,438.2),("20",150,699,42.9,635.0,20,"1-1/8",584.2,489.0),
    ("24",150,813,47.8,749.3,20,"1-1/4",692.2,590.6),
    ("1/2",300,95,14.2,66.7,4,"1/2",35.1,15.7),("1",300,124,17.5,88.9,4,"5/8",50.8,26.6),
    ("1-1/2",300,156,20.6,114.3,4,"3/4",73.0,40.9),("2",300,165,22.4,127.0,8,"5/8",92.1,52.5),
    ("3",300,210,28.4,168.3,8,"3/4",127.0,78.0),("4",300,254,31.8,200.0,8,"3/4",157.2,102.4),
    ("6",300,318,36.6,269.9,12,"3/4",215.9,154.1),("8",300,381,41.1,330.2,12,"7/8",269.9,202.7),
    ("10",300,445,47.8,387.4,16,"1",323.8,254.5),("12",300,521,50.8,450.9,16,"1-1/8",381.0,304.8),
    ("14",300,584,53.8,514.4,20,"1-1/8",412.8,336.6),("16",300,648,57.2,571.5,20,"1-1/4",469.9,387.4),
    ("20",300,775,63.5,685.8,24,"1-1/4",584.2,489.0),("24",300,914,69.9,812.8,24,"1-1/2",692.2,590.6),
    ("2",600,165,25.4,127.0,8,"5/8",92.1,52.5),("3",600,210,31.8,168.3,8,"3/4",127.0,78.0),
    ("4",600,273,38.1,215.9,8,"7/8",157.2,102.4),("6",600,356,47.8,292.1,12,"1",215.9,154.1),
    ("8",600,419,55.6,349.3,12,"1-1/8",269.9,202.7),("10",600,508,63.5,431.8,16,"1-1/4",323.8,254.5),
    ("12",600,559,66.5,489.0,20,"1-1/4",381.0,304.8),
    ("2",900,165,28.4,127.0,8,"3/4",92.1,52.5),("3",900,241,38.1,190.5,8,"7/8",127.0,78.0),
    ("4",900,292,44.5,235.0,8,"1-1/8",157.2,102.4),("6",900,381,55.6,317.5,12,"1-1/8",215.9,154.1),
    ("8",900,470,63.5,393.7,12,"1-3/8",269.9,202.7),("10",900,546,69.9,469.9,16,"1-3/8",323.8,254.5),
    ("12",900,610,79.2,533.4,20,"1-3/8",381.0,304.8),
    ("2",1500,190,38.1,146.1,8,"7/8",92.1,52.5),("3",1500,241,47.8,190.5,8,"1-1/8",127.0,78.0),
    ("4",1500,292,53.8,235.0,8,"1-1/4",157.2,102.4),("6",1500,381,66.5,317.5,12,"1-1/4",215.9,154.1),
    ("8",1500,470,76.2,393.7,12,"1-1/2",269.9,202.7),
]

# Add B16.47 Series A/B (from CSV)
FLANGE_SERIES = {}
def add_b16_47():
    rows = _read_csv_str(CSV_B16_47_FLANGES)
    for r in rows:
        series = r["series"]
        cl = int(r["class"])
        nps = r["nps_inch"]
        fod = float(r["flange_od_mm"])
        bcd = float(r["bolt_circle_mm"])
        nb = int(r["bolt_holes"])
        bolt_mm = float(r["bolt_size_mm"])
        thk = float(r["thickness_mm"])
        # Map bolt size mm -> closest ASME bolt string
        bolt_map = {35:"1-3/8",38:"1-1/2",41:"1-5/8",45:"1-3/4"}
        bolt_str = bolt_map.get(int(round(bolt_mm)), "1-1/2")
        # Bore and RF_OD are not in CSV -> use pipe OD as nominal bore, RF=OD (placeholder)
        od = PIPE_OD.get(nps, fod*0.5)
        rfi = od
        rfo = od
        ASME_FL.append((nps,cl,fod,thk,bcd,nb,bolt_str,rfo,rfi))
        FLANGE_SERIES[(nps,cl,fod,bcd,nb,bolt_str)] = series
add_b16_47()

# ── DIN EN 1092-1 Flanges
DIN_FL=[
    ("DN15",10,80,12,55,4,"M12",40,18),("DN20",10,90,14,65,4,"M12",51,25),
    ("DN25",10,100,14,75,4,"M12",58,30),("DN32",10,120,14,90,4,"M16",72,40),
    ("DN40",10,130,14,100,4,"M16",82,46),("DN50",10,140,14,110,4,"M16",92,56),
    ("DN65",10,160,14,130,4,"M16",112,72),("DN80",10,190,16,150,8,"M16",132,84),
    ("DN100",10,210,16,170,8,"M16",152,106),("DN125",10,240,18,200,8,"M16",182,132),
    ("DN150",10,265,18,225,8,"M16",202,154),("DN200",10,320,20,280,8,"M20",252,206),
    ("DN250",10,375,22,335,12,"M20",306,260),("DN300",10,440,22,395,12,"M20",362,312),
    ("DN350",10,490,22,445,12,"M20",408,348),("DN400",10,540,22,495,16,"M20",458,398),
    ("DN500",10,645,24,600,20,"M20",556,498),("DN600",10,755,24,705,20,"M24",660,598),
    ("DN15",16,80,12,55,4,"M12",40,18),("DN20",16,90,14,65,4,"M12",51,25),
    ("DN25",16,100,14,75,4,"M12",58,30),("DN32",16,120,14,90,4,"M16",72,40),
    ("DN40",16,130,14,100,4,"M16",82,46),("DN50",16,140,16,110,4,"M16",92,56),
    ("DN65",16,160,16,130,4,"M16",112,72),("DN80",16,190,18,150,8,"M16",132,84),
    ("DN100",16,220,18,180,8,"M16",158,106),("DN125",16,250,20,210,8,"M16",188,132),
    ("DN150",16,285,20,240,8,"M20",212,154),("DN200",16,340,22,295,12,"M20",268,206),
    ("DN250",16,405,24,355,12,"M24",320,260),("DN300",16,460,24,410,12,"M24",378,312),
    ("DN350",16,520,26,470,16,"M24",428,348),("DN400",16,580,28,525,16,"M27",482,398),
    ("DN500",16,715,30,650,20,"M30",590,498),("DN600",16,840,32,770,20,"M33",700,598),
    ("DN15",25,80,14,55,4,"M12",40,18),("DN20",25,90,16,65,4,"M12",51,25),
    ("DN25",25,100,16,75,4,"M12",58,30),("DN32",25,120,18,90,4,"M16",72,40),
    ("DN40",25,130,18,100,4,"M16",82,46),("DN50",25,150,20,110,4,"M16",92,56),
    ("DN65",25,170,22,130,8,"M16",112,72),("DN80",25,200,24,160,8,"M20",138,84),
    ("DN100",25,235,26,190,8,"M24",162,106),("DN125",25,270,28,220,8,"M24",188,132),
    ("DN150",25,300,30,250,8,"M24",218,154),("DN200",25,360,34,310,12,"M24",278,206),
    ("DN250",25,425,38,370,12,"M27",332,260),("DN300",25,485,42,430,16,"M27",382,312),
    ("DN400",25,600,48,535,16,"M33",482,398),("DN500",25,730,55,660,20,"M33",590,498),
    ("DN15",40,80,14,55,4,"M12",40,18),("DN20",40,90,16,65,4,"M12",51,25),
    ("DN25",40,100,18,75,4,"M16",58,30),("DN32",40,120,20,90,4,"M16",72,40),
    ("DN40",40,130,20,100,4,"M16",82,46),("DN50",40,150,22,110,4,"M20",92,56),
    ("DN65",40,170,24,130,8,"M20",112,72),("DN80",40,200,26,160,8,"M20",138,84),
    ("DN100",40,235,30,190,8,"M24",162,106),("DN150",40,300,34,250,8,"M27",218,154),
    ("DN200",40,375,40,320,12,"M30",285,206),("DN300",40,510,48,450,16,"M30",396,312),
]

STUD_ASME={"1/2":(12.7,22,12,1.75),"5/8":(15.9,25,15,1.75),"3/4":(19.1,30,18,2.5),
    "7/8":(22.2,35,21,2.5),"1":(25.4,41,25,3.0),"1-1/8":(28.6,46,28,3.0),
    "1-1/4":(31.8,50,31,3.5),"1-3/8":(34.9,55,34,3.5),"1-1/2":(38.1,60,37,4.0),
    "1-5/8":(41.3,65,40,4.0),"1-3/4":(44.5,70,43,4.5),
    "2":(50.8,80,50,5.0)}
STUD_DIN={"M12":(12,19,10,1.75),"M16":(16,24,13,2.0),"M20":(20,30,16,2.5),
    "M24":(24,36,19,3.0),"M27":(27,41,22,3.0),"M30":(30,46,24,3.5),
    "M33":(33,50,26,3.5),"M36":(36,55,29,4.0)}

GASKETS=[("Spiral Wound",4.5,[150,300,600,900]),("SW+Inner",4.5,[600,900,1500]),
    ("RTJ",0,[600,900,1500]),("Flat 3mm",3.0,[150,300]),
    ("PTFE 1.5",1.5,[150,300]),("Kammprofile",3.2,[150,300,600,900,1500])]
DIN_GASKETS=[("Spiral Wound",4.5,[10,16,25,40]),("IBC",2.0,[10,16,25,40]),
    ("Flat 3mm",3.0,[10,16]),("PTFE 1.5",1.5,[10,16]),
    ("Kammprofile",3.2,[10,16,25,40]),("Graphite 3",3.0,[10,16,25,40])]

DEF_NPS="6";DEF_SCH="STD"

def nk(n):
    s=n.replace("DN","")
    try:
        if "-" in s:p=s.split("-");return float(p[0])+_f(p[1])
        return _f(s) if "/" in s else float(s)
    except:return 999
def _f(s):
    try:p=s.split("/");return float(p[0])/float(p[1])
    except:return 0

def fmt_t(std,nps):return 'ASME {}"'.format(nps) if std=="ASME" else nps

def cdm(od,wt):
    if wt is None or wt<=0:
        return dict(od=od,oi=od/25.4,wt=wt,wi=None,id=None,ii=None,ir=None,ri=None,kg=None)
    i=od-2*wt;a=(math.pi/4)*((od/1e3)**2-(i/1e3)**2)
    return dict(od=od,oi=od/25.4,wt=wt,wi=wt/25.4,id=round(i,2),ii=round(i/25.4,3),
                ir=round(i/2,2),ri=round(i/2/25.4,3),kg=round(a*7850,2))

def cbn(od,wt,m,a):
    if wt is None or wt<=0:
        return dict(R=0,ac=0,ae=0,ai=0,T=0,Ri=0,Ro=0)
    R=m*od;Ro=R+od/2;Ri=R-od/2
    ac=(a/360)*2*math.pi*R;ae=(a/360)*2*math.pi*Ro;ai=(a/360)*2*math.pi*Ri
    T=R*math.tan(math.radians(a/2))
    return dict(R=round(R,1),ac=round(ac,1),ae=round(ae,1),ai=round(ai,1),
                T=round(T,1),Ri=round(Ri,1),Ro=round(Ro,1))

def get_stud(bd,std="ASME"):
    if std=="DIN":return STUD_DIN.get(bd,(12,19,10,1.75))
    return STUD_ASME.get(bd,(12,22,12,1.75))
def stud_prot(bd,std="ASME"):return round(1.5*get_stud(bd,std)[3],1)
def bolt_len(th,bd,gt,wr=False,ft="WN",std="ASME"):
    sb=get_stud(bd,std);p=stud_prot(bd,std);t=th*FTYPE_THK.get(ft,1.0)
    L=2*t+gt+2*sb[2]+2*p+(6 if wr else 0);return math.ceil(L/5)*5

def mm2in(v):return round(v/25.4,3)
def fmm(v,inch):return "{:.3f}\"".format(v/25.4) if inch else "{:.1f} mm".format(v)
def fmm2(v,inch):return "{:.3f}\"".format(v/25.4) if inch else "{:.2f} mm".format(v)

def _fmt(v, fmt="{:.2f}", na="N/A"):
    return na if v is None else fmt.format(v)

# ==================================================
#  DRAWING FUNCTIONS
# ==================================================
def _bx(ec):return dict(boxstyle="round,pad=0.12",fc=C.BG2,ec=ec,alpha=.92,lw=.6)
def _bxw(ec):return dict(boxstyle="round,pad=0.12",fc="white",ec=ec,alpha=.92,lw=.6)

def _u(v,inch):
    if v is None: return "N/A"
    if inch:return '{:.3f}"'.format(v/25.4)
    return "{:.1f} mm".format(v)
def _u2(v,inch):
    if v is None: return "N/A"
    if inch:return '{:.3f}"'.format(v/25.4)
    return "{:.2f} mm".format(v)

# ==================================================
#  V1.1 NEW FEATURES - HELPER FUNCTIONS
# ==================================================

class PipeLookup:
    """Helper class for pipe data lookup and validation"""
    
    @staticmethod
    def find_pipe(nps_or_dn, standard="ASME"):
        """
        Find pipe by NPS (ASME) or DN (DIN) designation
        Returns: (nps, od, schedules_list) or None
        """
        pipes = ASME_PIPES if standard == "ASME" else DIN_PIPES
        for p in pipes:
            if p[0] == nps_or_dn:
                return p
        return None
    
    @staticmethod
    def get_pipe_dimension(nps_or_dn, schedule, standard="ASME"):
        """
        Get specific pipe dimensions for a given size and schedule
        Returns: dict with od, wt, id, etc. or None
        """
        pipe = PipeLookup.find_pipe(nps_or_dn, standard)
        if not pipe:
            return None
        
        nps, od, schedules = pipe
        for sch_name, wt in schedules:
            # Match exact or partial schedule names (e.g., "STD" matches "40/STD")
            if sch_name == schedule or schedule in sch_name or sch_name.startswith(schedule):
                return cdm(od, wt)
        return None
    
    @staticmethod
    def list_schedules(nps_or_dn, standard="ASME"):
        """List all available schedules for a given pipe size"""
        pipe = PipeLookup.find_pipe(nps_or_dn, standard)
        if not pipe:
            return []
        return [sch[0] for sch in pipe[2]]
    
    @staticmethod
    def validate_nps(nps_or_dn, standard="ASME"):
        """Check if a pipe size exists in the database"""
        return PipeLookup.find_pipe(nps_or_dn, standard) is not None


class FlangeLookup:
    """Helper class for flange data lookup and validation"""
    
    @staticmethod
    def find_flange(nps_or_dn, pressure_class, standard="ASME"):
        """
        Find flange by size and pressure class
        Returns: list of matching flanges (may be multiple B16.47 series)
        """
        flanges = ASME_FL if standard == "ASME" else DIN_FL
        matches = []
        for f in flanges:
            if f[0] == nps_or_dn and f[1] == pressure_class:
                matches.append(f)
        return matches if matches else None
    
    @staticmethod
    def get_flange_data(nps_or_dn, pressure_class, standard="ASME"):
        """
        Get flange dimensions
        Returns: dict with flange_od, thickness, bolt_circle, etc.
        """
        matches = FlangeLookup.find_flange(nps_or_dn, pressure_class, standard)
        if not matches:
            return None
        
        # Return first match (or could return all)
        f = matches[0]
        if standard == "ASME":
            return {
                'nps': f[0],
                'class': f[1],
                'flange_od': f[2],
                'thickness': f[3],
                'bolt_circle': f[4],
                'bolt_holes': f[5],
                'bolt_size': f[6],
                'rf_od': f[7],
                'bore': f[8],
                'series': FLANGE_SERIES.get((f[0],f[1],f[2],f[4],f[5],f[6]), 'B16.5')
            }
        else:  # DIN
            return {
                'dn': f[0],
                'pn': f[1],
                'flange_od': f[2],
                'thickness': f[3],
                'bolt_circle': f[4],
                'bolt_holes': f[5],
                'bolt_size': f[6],
                'rf_od': f[7],
                'bore': f[8]
            }
    
    @staticmethod
    def list_classes(nps_or_dn, standard="ASME"):
        """List all available pressure classes for a given flange size"""
        flanges = ASME_FL if standard == "ASME" else DIN_FL
        classes = set()
        for f in flanges:
            if f[0] == nps_or_dn:
                classes.add(f[1])
        return sorted(list(classes))
    
    @staticmethod
    def validate_flange(nps_or_dn, pressure_class, standard="ASME"):
        """Check if a flange exists in the database"""
        return FlangeLookup.find_flange(nps_or_dn, pressure_class, standard) is not None


class DataExport:
    """Export utilities for pipe and flange data"""
    
    @staticmethod
    def export_pipes_csv(filename, standard="ASME"):
        """Export all pipe data to CSV file"""
        import csv
        pipes = ASME_PIPES if standard == "ASME" else DIN_PIPES
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Size', 'OD_mm', 'Schedule', 'WT_mm', 'ID_mm', 'Weight_kg_m'])
            
            for nps, od, schedules in pipes:
                for sch_name, wt in schedules:
                    dims = cdm(od, wt)
                    writer.writerow([
                        nps, od, sch_name, 
                        wt if wt else 'N/A',
                        dims.get('id', 'N/A'),
                        dims.get('kg', 'N/A')
                    ])
        return filename
    
    @staticmethod
    def export_flanges_csv(filename, standard="ASME"):
        """Export all flange data to CSV file"""
        import csv
        flanges = ASME_FL if standard == "ASME" else DIN_FL
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            if standard == "ASME":
                writer.writerow(['NPS', 'Class', 'Flange_OD_mm', 'Thickness_mm', 
                               'Bolt_Circle_mm', 'Bolt_Holes', 'Bolt_Size', 'RF_OD_mm', 'Bore_mm'])
            else:
                writer.writerow(['DN', 'PN', 'Flange_OD_mm', 'Thickness_mm', 
                               'Bolt_Circle_mm', 'Bolt_Holes', 'Bolt_Size', 'RF_OD_mm', 'Bore_mm'])
            
            for f in flanges:
                writer.writerow(f)
        return filename
    
    @staticmethod
    def export_to_json(filename, standard="ASME"):
        """Export all data to JSON format"""
        import json
        
        pipes = ASME_PIPES if standard == "ASME" else DIN_PIPES
        flanges = ASME_FL if standard == "ASME" else DIN_FL
        
        data = {
            'standard': standard,
            'version': '1.1',
            'pipes': [
                {
                    'size': p[0],
                    'od_mm': p[1],
                    'schedules': [{'schedule': s[0], 'wt_mm': s[1]} for s in p[2]]
                }
                for p in pipes
            ],
            'flanges': [
                {
                    'size': f[0],
                    'class': f[1],
                    'flange_od_mm': f[2],
                    'thickness_mm': f[3],
                    'bolt_circle_mm': f[4],
                    'bolt_holes': f[5],
                    'bolt_size': f[6],
                    'rf_od_mm': f[7],
                    'bore_mm': f[8]
                }
                for f in flanges
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename


class PrettyPrint:
    """Formatted console output for pipe and flange data"""
    
    @staticmethod
    def print_pipe(nps_or_dn, schedule, standard="ASME"):
        """Print formatted pipe information"""
        dims = PipeLookup.get_pipe_dimension(nps_or_dn, schedule, standard)
        if not dims:
            print(f"❌ Pipe {nps_or_dn} {schedule} not found in {standard} database")
            return
        
        print("\n" + "="*60)
        print(f"  {standard} Pipe: {nps_or_dn} Schedule {schedule}")
        print("="*60)
        print(f"  Outside Diameter : {dims['od']:.2f} mm  ({dims['oi']:.3f}\")")
        if dims['wt']:
            print(f"  Wall Thickness   : {dims['wt']:.2f} mm  ({dims['wi']:.3f}\")")
            print(f"  Inside Diameter  : {dims['id']:.2f} mm  ({dims['ii']:.3f}\")")
            print(f"  Inside Radius    : {dims['ir']:.2f} mm  ({dims['ri']:.3f}\")")
            print(f"  Weight per meter : {dims['kg']:.2f} kg/m (carbon steel)")
        else:
            print(f"  Wall Thickness   : Not specified in database")
        print("="*60 + "\n")
    
    @staticmethod
    def print_flange(nps_or_dn, pressure_class, standard="ASME"):
        """Print formatted flange information"""
        data = FlangeLookup.get_flange_data(nps_or_dn, pressure_class, standard)
        if not data:
            print(f"❌ Flange {nps_or_dn} Class/PN {pressure_class} not found in {standard} database")
            return
        
        print("\n" + "="*60)
        if standard == "ASME":
            print(f"  ASME Flange: {data['nps']}\" Class {data['class']}")
            print(f"  Series: {data['series']}")
        else:
            print(f"  DIN Flange: {data['dn']} PN {data['pn']}")
        print("="*60)
        print(f"  Flange OD        : {data['flange_od']:.1f} mm")
        print(f"  Thickness        : {data['thickness']:.1f} mm")
        print(f"  Bolt Circle      : {data['bolt_circle']:.1f} mm")
        print(f"  Bolt Holes       : {data['bolt_holes']}")
        print(f"  Bolt Size        : {data['bolt_size']}")
        print(f"  Raised Face OD   : {data['rf_od']:.1f} mm")
        print(f"  Bore             : {data['bore']:.1f} mm")
        print("="*60 + "\n")
    
    @staticmethod
    def list_all_pipes(standard="ASME", max_display=20):
        """List all available pipe sizes"""
        pipes = ASME_PIPES if standard == "ASME" else DIN_PIPES
        print(f"\n{standard} Pipe Sizes Available: {len(pipes)} sizes")
        print("-" * 40)
        
        for i, (nps, od, schedules) in enumerate(pipes):
            if i >= max_display:
                print(f"... and {len(pipes) - max_display} more sizes")
                break
            sch_list = ", ".join([s[0] for s in schedules[:5]])
            if len(schedules) > 5:
                sch_list += f" ... (+{len(schedules)-5} more)"
            print(f"  {nps:8s}  OD: {od:7.1f} mm  Schedules: {sch_list}")
        print()

# ==================================================
#  MAIN ENTRY POINT
# ==================================================
# NOTE: This is a data library module. Full GUI implementation pending.
# To use: import this module and access ASME_PIPES, DIN_PIPES, ASME_FL, DIN_FL, etc.

def main():
    """
    PipelineBible v1.1
    
    This module provides comprehensive piping and pipeline standard data:
    - ASME B36.10M pipes (NPS 1/2" to 56")
    - DIN EN 10220 pipes (DN15 to DN600)
    - ASME B16.5 flanges (Class 150-1500)
    - ASME B16.47 Series A/B flanges (NPS 26"-56")
    - DIN EN 1092-1 flanges (PN 10-40)
    - Bend calculations (1D to 10D)
    - Gasket and bolt specifications
    
    V1.1 New Features:
    - PipeLookup class for easy pipe data access
    - FlangeLookup class for flange data access
    - DataExport utilities (CSV, JSON)
    - PrettyPrint console formatters
    - Enhanced validation functions
    """
    print("=" * 60)
    print("PipelineBible v1.1")
    print("Professional Pipeline & Piping Standards Tool")
    print("=" * 60)
    print()
    print("Available Standards:")
    print(f"  - ASME Pipes: {len(ASME_PIPES)} sizes")
    print(f"  - DIN Pipes: {len(DIN_PIPES)} sizes")
    print(f"  - ASME Flanges: {len(ASME_FL)} entries")
    print(f"  - DIN Flanges: {len(DIN_FL)} entries")
    print(f"  - Bend Types: {len(BENDS)}")
    print()
    print("New in v1.1:")
    print("  ✓ PipeLookup helper class")
    print("  ✓ FlangeLookup helper class")
    print("  ✓ DataExport (CSV/JSON)")
    print("  ✓ PrettyPrint formatters")
    print()
    print("Example Usage:")
    print("-" * 60)
    
    # Demo: Lookup a pipe
    print("\n>>> PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')")
    dims = PipeLookup.get_pipe_dimension('6', 'STD', 'ASME')
    if dims:
        print(f"    OD: {dims['od']} mm, WT: {dims['wt']} mm, ID: {dims['id']} mm")
    
    # Demo: Lookup a flange
    print("\n>>> FlangeLookup.get_flange_data('6', 150, 'ASME')")
    flange = FlangeLookup.get_flange_data('6', 150, 'ASME')
    if flange:
        print(f"    Flange OD: {flange['flange_od']} mm, Bolt Circle: {flange['bolt_circle']} mm")
    
    # Demo: List available schedules
    print("\n>>> PipeLookup.list_schedules('6', 'ASME')")
    schedules = PipeLookup.list_schedules('6', 'ASME')
    print(f"    {schedules}")
    
    print()
    print("=" * 60)
    print("For full documentation, see README.md")
    print("For GUI application, launch with GUI framework enabled.")
    print("=" * 60)

if __name__=="__main__":
    main()
