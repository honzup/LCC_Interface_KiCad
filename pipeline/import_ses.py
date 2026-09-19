import pcbnew
from pcbnew import FromMM
B="/home/john/LCC_Interface_KiCad_RevA/LCC_Interface.kicad_pcb"
S="/home/john/LCC_Interface_KiCad_RevA/LCC_Interface.ses"
board=pcbnew.LoadBoard(B)
print("import ok:", pcbnew.ImportSpecctraSES(board, S))

# --- bottom-layer ground pour on /CAN_GND ---
gnd = board.FindNet("/CAN_GND")
z = pcbnew.ZONE(board)
z.SetLayer(pcbnew.B_Cu)
z.SetNetCode(gnd.GetNetCode())
z.SetAssignedPriority(0)
z.SetLocalClearance(FromMM(0.3))
z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
poly = z.Outline(); poly.NewOutline()
for x,y in [(0.5,0.5),(59.5,0.5),(59.5,49.5),(0.5,49.5)]:
    poly.Append(FromMM(x), FromMM(y))
board.Add(z)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())

pcbnew.SaveBoard(B, board)
print("tracks now:", len(list(board.GetTracks())), "| zones:", board.GetAreaCount())
