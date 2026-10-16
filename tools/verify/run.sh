#!/bin/sh
# Pre-order geometry and firmware checks. Run from the repo root.
# Needs Docker (KiCad 9 image) and Python 3.11+ with trimesh, shapely and numpy.
set -e
mkdir -p build/verify
docker run --rm -u "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD":/w -w /w kicad/kicad:9.0 python3 tools/verify/dump_geometry.py
echo "== 1. top plate vs main PCB, plates vs each other"; python3 tools/verify/check12.py
echo "== 2. frame";                                       python3 tools/verify/check2.py
echo "== 3. USB opening and bottom-plate notch";          python3 tools/verify/check3.py
echo "== 4. firmware pins and key matrix";                python3 tools/verify/check4.py
