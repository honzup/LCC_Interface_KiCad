# PCB build pipeline

Regenerates `../LCC_Interface.kicad_pcb` from scratch:
placement (pcbnew) -> autoroute (Freerouting 1.9.0) -> import + bottom-layer
ground pour -> DRC.

- `build_place.py` — component placement, net assignment, silkscreen labels,
  board outline. **Edit this to change the layout**, then run `./run.sh`.
- `import_ses.py` — imports the routed session and fills the CAN_GND pour.
- `run.sh` — runs the whole chain and reports DRC.

Requires the extracted KiCad 10 AppImage and `freerouting19.jar` under
`~/AppImages/`, plus `xvfb-run`. Paths are hard-coded for this machine.
