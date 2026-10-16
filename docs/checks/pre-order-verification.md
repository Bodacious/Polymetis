# Pre-order verification

Run `sh tools/verify/run.sh` from the repo root to repeat these checks. All coordinates below are in millimetres, top view of the keyboard (the top plate's coordinates).

| # | Check | Result |
|---|---|---|
| 1 | Top plate vs main PCB | 59 of 60 switches each centred in a 14.00 mm cut-out (worst offset under 0.01 mm). The space switch, the stabiliser stems (±50.00 mm) and the merged space-bar cut-out share one centre; the stabiliser housing openings (x 103.06–109.06 and 203.06–209.06) sit over the PCB slots (x 102.81–109.31 and 202.81–209.31). |
| 1 | Plates vs each other | 8 screw holes (2.20 mm) coincide within 0.025 mm; outlines within 0.024 mm. PCB centred left–right in the plate outline (11.21 mm each side). |
| 2 | Frame | STL is 309.75 × 119.25 × 5.30 mm, watertight. 8 holes coincide with the plate holes within 0.002 mm; outline matches the plates. PCB sits in the cavity with 0.30 mm clearance all round and does not touch frame material. |
| 3 | USB-C | Frame opening and bottom-plate notch both span x 283.98–299.96, about 3 mm clear of the receptacle on each side. The notch runs 13.7 mm in from the back edge, to y 27.98; the receptacle body (7.35 mm long, HRO TYPE-C-31-M-12 drawing) ends at y 27.22. This only lines up with the bottom plate's "Polymetis" text facing outwards; fitted the other way the notch would be at the wrong end. |
| 4 | Firmware | All 5 row and 15 column pins in `keyboard.toml` match the RP2040 GPIOs wired to `row0`–`row4` and `col0`–`col14`. Each of the 60 switches, traced through its column net and diode to a row net, has a unique matrix position whose keymap entry matches its physical HHKB Pro 2 position. No keymap entries without a switch. |

## Finding: the USB-C plug sits low

The receptacle hangs under the PCB, so its opening is centred 6.08 mm below the top of the top plate (plate 1.20 + gap 1.30 + PCB 1.60 + 1.98 to the centre of the 0.70–3.26 mm shell, per the HRO drawing). The case is 8.10 mm deep. Any cable plug thicker than 4.04 mm therefore sticks out below the bottom plate by half its thickness minus 2.02 mm. Measure your cable's plug and fit rubber feet at least that tall, or the plug will lift the back of the keyboard.
