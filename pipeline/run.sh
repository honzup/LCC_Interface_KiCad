#!/bin/bash
# Regenerate the LCC/CAN Interface PCB: place -> autoroute -> import -> pour -> DRC.
# Edit pipeline/build_place.py (placement/labels) then run this.
set -e
# KiCad 10.0.6 installed system-wide (apt); pcbnew bindings import from system python3.
FR=/home/john/AppImages/freerouting19.jar        # Freerouting 1.9.0 (Java 21)
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(dirname "$HERE")"
PY() { python3 "$@"; }
cd "$PROJ"
PY "$HERE/build_place.py"                          # place parts + nets, export .dsn
rm -f LCC_Interface.ses
xvfb-run -a java -jar "$FR" -de LCC_Interface.dsn -do LCC_Interface.ses -mp 60
PY "$HERE/import_ses.py"                            # import routes + add ground pour
kicad-cli pcb drc --format json -o /tmp/lcc_drc.json LCC_Interface.kicad_pcb || true
python3 -c "import json;d=json.load(open('/tmp/lcc_drc.json'));print('DRC violations',len(d['violations']),'| unconnected',len(d['unconnected_items']))"
rm -f LCC_Interface.dsn LCC_Interface.ses /tmp/lcc_drc.json LCC_Interface-drc.rpt; rm -rf logs
echo "regenerated LCC_Interface.kicad_pcb"
