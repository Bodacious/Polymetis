#!/bin/sh
# Factory files, check reports and renders. Run inside the KiCad 9 container from the repo root:
#   docker run --rm -v "$PWD":/w -w /w kicad/kicad:9.0 sh tools/export.sh
set -e
B=boethia60/boethia60.kicad_pcb
mkdir -p docs/checks docs/renders

# Main PCB: Gerbers and drill files for JLCPCB (same layer set and names as before)
rm -f jlcpcb/*.gbr jlcpcb/*.drl jlcpcb/*.gbrjob jlcpcb/*-pos.csv jlcpcb/*.zip
kicad-cli pcb export gerbers --output jlcpcb/ --layers F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts \
  --subtract-soldermask --no-protel-ext $B
kicad-cli pcb export drill --output jlcpcb/ --format excellon --excellon-separate-th --generate-map --map-format gerberx2 \
  --drill-origin absolute --excellon-units mm $B
kicad-cli pcb export pos --output jlcpcb/boethia60-top-pos.csv --side front --format csv --units mm $B
# JLCPCB column names; hot-swap sockets are hand-soldered, so they are left out like the old CPL left out the switches
python3 -c "p='jlcpcb/boethia60-top-pos.csv';L=open(p).read().splitlines();open(p,'w').write('\\n'.join(['Designator,Val,Package,Mid X,Mid Y,Rotation,Layer']+[l for l in L[1:] if not l.startswith('\"K_')])+'\\n')"
(cd jlcpcb && zip -q boethia60-jlcpcb.zip *.gbr *.drl *.gbrjob)

for P in top-plate bottom-plate; do
  rm -f $P/jlcpcb/* $P/jlcpcb.zip
  kicad-cli pcb export gerbers --output $P/jlcpcb/ --layers F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts \
    --subtract-soldermask --no-protel-ext $P/$P.kicad_pcb
  kicad-cli pcb export drill --output $P/jlcpcb/ --format excellon --excellon-separate-th --generate-map --map-format gerberx2 \
    --drill-origin absolute --excellon-units mm $P/$P.kicad_pcb
  (cd $P/jlcpcb && zip -q ../jlcpcb.zip *)
done

# Checks
kicad-cli sch erc --severity-all --format report -o docs/checks/boethia60-erc.rpt boethia60/boethia60.kicad_sch
kicad-cli pcb drc --severity-all --schematic-parity -o docs/checks/boethia60-drc.rpt $B
kicad-cli pcb drc --severity-all -o docs/checks/top-plate-drc.rpt top-plate/top-plate.kicad_pcb
kicad-cli pcb drc --severity-all -o docs/checks/bottom-plate-drc.rpt bottom-plate/bottom-plate.kicad_pcb

# Renders. KiCad's front of the main PCB is the keyboard underside (components); the bottom plate's front is its outside face.
kicad-cli pcb render --side bottom --width 2400 --height 1100 --quality high -o docs/renders/pcb-switch-side.png $B
kicad-cli pcb render --side top --width 2400 --height 1100 --quality high -o docs/renders/pcb-component-side.png $B
kicad-cli pcb render --side top --width 2400 --height 1100 --quality high -o docs/renders/top-plate.png top-plate/top-plate.kicad_pcb
kicad-cli pcb render --side bottom --width 2400 --height 1100 --quality high -o docs/renders/bottom-plate-inside.png bottom-plate/bottom-plate.kicad_pcb
kicad-cli pcb render --side top --width 2400 --height 1100 --quality high -o docs/renders/bottom-plate-outside.png bottom-plate/bottom-plate.kicad_pcb
echo done
