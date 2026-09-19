#!/usr/bin/env python3
import pcbnew
from pcbnew import VECTOR2I, FromMM

FPDIR = "/home/john/AppImages/kicad-10.0.4-extracted/usr/share/kicad/footprints"
OUT   = "/home/john/LCC_Interface_KiCad_RevA/LCC_Interface.kicad_pcb"
DSN   = "/home/john/LCC_Interface_KiCad_RevA/LCC_Interface.dsn"
BW, BH = 60, 50   # board size mm

board = pcbnew.NewBoard(OUT)
def V(x, y): return VECTOR2I(FromMM(x), FromMM(y))

NETS = ["CAN_H","CAN_L","CAN_TX","CAN_RX","+3V3","MODE5","MODE8",
        "TERM_MID","ALT_L","ALT_H","PWR_NEG","PWR_POS","CAN_GND"]
net = {}
for n in NETS:
    ni = pcbnew.NETINFO_ITEM(board, "/"+n); board.Add(ni); net[n] = ni

# ref: (lib, fp, x, y, rot, schematic-symbol-uuid or None)
COMPS = [
 ("J1","Connector_RJ","RJ45_Amphenol_RJHSE5380", 16, 13, 0,  "0e642468-49c7-4cf3-98d9-0331951453b6"),
 ("J2","Connector_RJ","RJ45_Amphenol_RJHSE5380", 37, 13, 0,  "d87adfcd-62eb-4d56-b351-95ea2de0780c"),
 ("D1","Package_TO_SOT_SMD","SOT-23",             30, 24, 0,  "a3a3a3a3-0000-0000-0000-000000000005"),
 ("U1","Package_SO","SOIC-8_3.9x4.9mm_P1.27mm",   21, 29, 0,  "18eb6a53-2da7-48ca-ab9a-8724a9be2451"),
 ("R2","Resistor_SMD","R_0805_2012Metric_Pad1.20x1.40mm_HandSolder", 35, 27, 0, "a3a3a3a3-0000-0000-0000-000000000003"),
 ("R3","Resistor_SMD","R_0805_2012Metric_Pad1.20x1.40mm_HandSolder", 35, 31, 0, "a3a3a3a3-0000-0000-0000-000000000004"),
 ("C1","Capacitor_SMD","C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 12, 35, 90, "91db2713-ef26-4823-9793-0e3c9a10895c"),
 ("C2","Capacitor_SMD","C_0805_2012Metric_Pad1.18x1.45mm_HandSolder", 15, 35, 90, "a3a3a3a3-0000-0000-0000-000000000002"),
 ("J3","Connector_PinHeader_2.54mm","PinHeader_1x04_P2.54mm_Vertical", 7, 33, 0, "2aaa87a8-e08a-4612-9c74-96b562ebb24e"),
 ("R1","Resistor_SMD","R_0805_2012Metric_Pad1.20x1.40mm_HandSolder", 40, 36, 0, "eaf89d95-e1f0-4d42-99e6-ccbbf52402f7"),
 ("JP1","Connector_PinHeader_2.54mm","PinHeader_1x02_P2.54mm_Vertical", 45, 36, 0, "e0ec58aa-6e34-4308-a816-6b80acf0a906"),
 ("TP1","TestPoint","TestPoint_THTPad_D1.5mm_Drill0.7mm", 49, 25, 0, None),
 ("TP2","TestPoint","TestPoint_THTPad_D1.5mm_Drill0.7mm", 52, 25, 0, None),
 ("TP3","TestPoint","TestPoint_THTPad_D1.5mm_Drill0.7mm", 55, 25, 0, None),
 ("H1","MountingHole","MountingHole_3.2mm_M3", 4,  4,  0, None),
 ("H2","MountingHole","MountingHole_3.2mm_M3", 56, 4,  0, None),
 ("H3","MountingHole","MountingHole_3.2mm_M3", 4,  46, 0, None),
 ("H4","MountingHole","MountingHole_3.2mm_M3", 56, 46, 0, None),
]
VALUE = {"U1":"TCAN332DR","J1":"LCC RJ45","J2":"LCC RJ45","J3":"MCU INTERFACE",
 "C1":"100nF","C2":"4.7uF","R1":"120R","R2":"10k DNP","R3":"10k DNP",
 "D1":"PESD1CAN","JP1":"TERM ENABLE","TP1":"TP","TP2":"TP","TP3":"TP",
 "H1":"","H2":"","H3":"","H4":""}
fps = {}
for ref, lib, fp, x, y, rot, uuid in COMPS:
    f = pcbnew.FootprintLoad(f"{FPDIR}/{lib}.pretty", fp)
    if f is None: raise SystemExit(f"load fail {lib}:{fp}")
    f.SetReference(ref); f.SetPosition(V(x, y))
    f.SetFPID(pcbnew.LIB_ID(lib, fp))
    if rot: f.SetOrientationDegrees(rot)
    if uuid: f.SetPath(pcbnew.KIID_PATH("/"+uuid))
    if ref in VALUE: f.SetValue(VALUE[ref])
    board.Add(f); fps[ref] = f
for r in ("R2","R3"):
    try: fps[r].SetDNP(True)
    except Exception: pass
for r in ("H1","H2","H3","H4"): fps[r].Reference().SetVisible(False)
fps["C2"].Reference().SetPosition(V(15,32.5))

def silk(txt, x, y, angle=0, size=0.8):
    t = pcbnew.PCB_TEXT(board); t.SetText(txt); t.SetLayer(pcbnew.F_SilkS)
    t.SetPosition(V(x, y))
    t.SetTextSize(pcbnew.VECTOR2I(FromMM(size), FromMM(size)))
    t.SetTextThickness(FromMM(size*0.15))
    if angle: t.SetTextAngle(pcbnew.EDA_ANGLE(angle, pcbnew.DEGREES_T))
    board.Add(t)
# test-point net names (vertical, below each TP at y=25)
silk("CAN_H",   49, 29.5, 90, 0.8)
silk("CAN_L",   52, 29.5, 90, 0.8)
silk("CAN_GND", 55, 30.0, 90, 0.8)
# MCU header pin functions (left of J3, pin1 top -> GND,3V3,TX,RX)
silk("GND", 4.0, 33.0,  0, 0.9)
silk("3V3", 4.0, 35.54, 0, 0.9)
silk("TX",  4.3, 38.08, 0, 0.9)
silk("RX",  4.3, 40.62, 0, 0.9)
# board name (bottom centre)
silk("LCC / CAN INTERFACE   Rev B", 30, 46, 0, 1.3)
# J3: put "MCU INTERFACE" (value) above the header on silk, move J3 refdes below
_j3 = fps["J3"]
_v = _j3.Value()
_v.SetLayer(pcbnew.F_SilkS); _v.SetVisible(True); _v.SetPosition(V(7, 31))
_v.SetTextSize(pcbnew.VECTOR2I(FromMM(0.85), FromMM(0.85))); _v.SetTextThickness(FromMM(0.13))
_j3.Reference().SetPosition(V(10, 42))

PADNET = {
 "U1": {"1":"CAN_TX","2":"CAN_GND","3":"+3V3","4":"CAN_RX","5":"MODE5","6":"CAN_L","7":"CAN_H","8":"MODE8"},
 "J1": {"1":"CAN_H","2":"CAN_L","3":"CAN_GND","4":"ALT_L","5":"ALT_H","6":"CAN_GND","7":"PWR_NEG","8":"PWR_POS","SH":"CAN_GND"},
 "J2": {"1":"CAN_H","2":"CAN_L","3":"CAN_GND","4":"ALT_L","5":"ALT_H","6":"CAN_GND","7":"PWR_NEG","8":"PWR_POS","SH":"CAN_GND"},
 "J3": {"1":"CAN_GND","2":"+3V3","3":"CAN_TX","4":"CAN_RX"},
 "C1": {"1":"+3V3","2":"CAN_GND"}, "C2": {"1":"+3V3","2":"CAN_GND"},
 "R1": {"1":"CAN_H","2":"TERM_MID"}, "R2": {"1":"MODE5","2":"CAN_GND"}, "R3": {"1":"MODE8","2":"CAN_GND"},
 "D1": {"1":"CAN_H","2":"CAN_L","3":"CAN_GND"}, "JP1":{"1":"TERM_MID","2":"CAN_L"},
 "TP1":{"1":"CAN_H"},"TP2":{"1":"CAN_L"},"TP3":{"1":"CAN_GND"},
}
for ref, f in fps.items():
    m = PADNET.get(ref, {})
    for pad in f.Pads():
        if pad.GetNumber() in m: pad.SetNet(net[m[pad.GetNumber()]])

rect = pcbnew.PCB_SHAPE(board); rect.SetShape(pcbnew.SHAPE_T_RECT)
rect.SetStart(V(0,0)); rect.SetEnd(V(BW,BH))
rect.SetLayer(pcbnew.Edge_Cuts); rect.SetWidth(FromMM(0.15)); board.Add(rect)

try:
    nc = board.GetAllNetClasses()["Default"]
    nc.SetClearance(FromMM(0.2)); nc.SetTrackWidth(FromMM(0.25))
    nc.SetViaDiameter(FromMM(0.6)); nc.SetViaDrill(FromMM(0.3))
except Exception as e: print("netclass warn:", e)

pcbnew.SaveBoard(OUT, board)
print("SAVED board + DSN:", pcbnew.ExportSpecctraDSN(board, DSN), f"({BW}x{BH})")
