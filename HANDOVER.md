# Polymetis handover

Written 12 October 2026 by Claude in a cloud session for Gavin Morrice, as a brief for Claude Code running on Gavin's own computer. The cloud session could read and analyse these files but could not install KiCad (its network policy blocked every KiCad source), so none of the board work below has been started. Everything in sections 3, 4 and 5 was measured from the files in this repo; anything not measured is marked as unverified.

## 1. What this repo is and what "done" means

Polymetis is Gavin's fork of [arviceblot/boethia60](https://github.com/arviceblot/boethia60) (MIT licence, keep `LICENSE`). The boethia60 is a 62-key, low-profile, HHKB-like keyboard: RP2040 on the board, wired USB-C, Kailh Choc V1/V2 hot-swap sockets, a split spacebar, RMK firmware in Rust, and a sandwich case of two FR4 plates around a 3D-printed middle frame.

Gavin wants it turned into a 60-key board in the exact HHKB Professional 2 layout with a one-piece spacebar, on Gateron KS-33 low-profile switches.

The job is done when all of this is on a branch with a pull request, and nothing has been ordered:

1. Main PCB (`boethia60/`) updated, ERC and DRC clean, factory files for JLCPCB regenerated in `jlcpcb/`.
2. Top plate (`top-plate/`) updated for the new switches and stabilisers, factory files regenerated.
3. Bottom plate (`bottom-plate/`) checked; regenerate only if something had to change.
4. Middle frame (`case/`) checked against the new stack height, STL exported, plus a two-piece version if Gavin's printer bed needs it.
5. Firmware key map (`firmware/keyboard.toml`, `firmware/vial.json`) and layout file (`boethia60.json`) updated, firmware builds.
6. README updated, and check reports and board renders saved for Gavin to look at.

## 2. Decisions already made

Do not reopen these without asking Gavin.

| Topic | Decision |
|---|---|
| Layout | HHKB Professional 2, exactly. 60 keys. Not ISO. |
| Spacebar | One piece, 6.25u. Gavin rejected split spacebars and remapping tricks. |
| Where the extra 0.25u goes | Taken from the blank area at the **left** end of the bottom row (see section 5). Chosen because the right-hand end sits over the RP2040, reset pad and boot button. Gavin was earlier told the right-hand keys would move instead, so mention this change in the PR. |
| Switches | Gateron KS-33 (Low Profile 2.0). |
| Sockets | Gateron KS-2P02B01-02 low-profile hot-swap sockets. |
| Stabilisers | Gateron low-profile plate-mounted: 2u under Enter and left Shift, 6.25u under Space. The 1.75u keys (Ctrl, right Shift) have none. |
| Firmware | Rust, RMK (the existing firmware), with Vial. |
| Everything else | Keep the RP2040 circuit, USB-C position, board outline, mounting and parts list as they are unless a change is forced. |

Key sizes for the finished board: 51 × 1u, 4 × 1.5u (Tab, Backspace, two Cmd), 2 × 1.75u (Ctrl, right Shift), 2 × 2.25u (Enter, left Shift), 1 × 6.25u.

## 3. Repo map

| Path | What it is |
|---|---|
| `boethia60/` | Main PCB, KiCad 8 project (file format 20240108). Board 287.34 × 98.42 mm, 1.6 mm thick. |
| `boethia60/fp-lib-table` | Lists a `Kailh_Choc.pretty` library that is **not** in the repo. The stabiliser footprints come from the KiCad PCM library `PCM_marbastlib-xp-choc`. |
| `jlcpcb/` | Main PCB factory files: Gerbers, drills, `boethia60_bom.csv` (16 lines, all with JLCPCB part numbers), `boethia60-top-pos.csv` and `boethia60-bottom-pos.csv`. |
| `top-plate/` | KiCad project for the 1.6 mm FR4 switch plate. Switch cutouts are drawn directly on Edge.Cuts (199 items) plus four `STAB_choc_2u_plate` footprints. |
| `bottom-plate/` | KiCad project, 1.6 mm FR4: outline plus a logo footprint, nothing per switch. |
| `case/` | `Middle.FCStd` (FreeCAD source of the printed frame), `boethia60 case.stl` (309.8 × 119.2 × 4.0 mm), and DXF/SVG outlines from a plate generator. |
| `firmware/` | RMK 0.5 firmware for the RP2040: `keyboard.toml` (matrix and key map), `vial.json` (Vial layout), Rust sources. |
| `boethia60.json` | Keyboard Layout Editor description of the layout. |

## 4. Facts about the existing board

**Orientation.** All 62 switch footprints (`K_1` to `K_62`) are on **B.Cu**, and their socket pads land on **F.Cu**. The diodes, RP2040 and every other part are on **F.Cu**. So KiCad's front is the keyboard's underside, and KiCad's normal view shows the keyboard from below, mirrored left to right. To convert:

- top-view key centre in units: `u = (285.75 − x_mm) / 19.05`
- rows sit at y = 9.525, 28.575, 47.625, 66.675 and 85.725 mm
- key pitch is 19.05 mm

**Matrix.** Each switch connects to a column net (`col0` to `col14`) and to its own diode (`D_n` pairs with `K_n`), and the diode goes to a row net (`row0` to `row4`). In `keyboard.toml` the rows are inputs and the columns are outputs. Appendix A has every switch with its matrix position, key and diode.

**Parts at the right-hand end** (top view), all on F.Cu: RP2040 `U3` at (19.844, 82.550), reset pad `J1` at (41.275, 80.518), push button `SW1` at (50.006, 69.056), USB-C `USB1` at (18.667, −6.145) on the top edge. These sit under the right-hand end of rows 3 and 4, which is why the bottom-row change goes to the left.

**Stabilisers.** Four `PCM_marbastlib-xp-choc:STAB_choc_2u` footprints on B.Cu: Enter (21.431, 47.625), left Shift (264.319, 66.675), and the two spacebar halves at (188.119, 85.725) and (121.444, 85.725).

**Copper.** 1,058 track segments and 127 vias. Four zones: `+1V1` on F.Cu, `Earth` on both layers, two `GND` on both layers.

**Design rules in the project:** minimum track 0.1524 mm, minimum via diameter 0.4 mm, minimum through hole 0.3 mm, hole clearance 0.25 mm, copper-to-edge 0.1 mm.

**Known issues from the original author's README and build post:**
- The USB connector needs a cutout in the bottom plate; he suggests a mid-mount connector.
- Choc stabilisers needed a 1.2 mm plate, and his 1.6 mm plate was too thick, so his build has no stabilisers. The plate thickness question applies to the Gateron parts too (see step 1).
- When ordering FR4 plates from JLCPCB, pay the small extra to leave the order number off.

## 5. The bottom-row change, exactly

The HHKB Pro 2 bottom row is: 1.5u blank, Alt 1u, Cmd 1.5u, Space 6u, Cmd 1.5u, Alt 1u, 2.5u blank. This board uses a 6.25u spacebar because that is what low-profile keycap sets carry. The extra 0.25u comes out of the left blank, so the target row is:

**1.25u blank, Alt 1u, Cmd 1.5u, Space 6.25u, Cmd 1.5u, Alt 1u, 2.5u blank.**

| Switch | Key now | Key after | Matrix | x now (mm) | x after (mm) | Change |
|---|---|---|---|---|---|---|
| K_56 | LGui, 1u | Left Alt, 1u | (4,2) | 247.650 | 252.413 | Move +4.7625; move D_56 the same (256.381 → 261.144) |
| K_57 | LAlt, 1.5u | Left Cmd, 1.5u | (4,3) | 223.838 | 228.600 | Move +4.7625; move D_57 the same (232.569 → 237.331) |
| K_58 | Space, 2.25u | — | (4,5) | 188.119 | — | Delete, with D_58 |
| K_59 | MO(2), 1u | Space, 6.25u | (4,6) | 157.162 | 154.781 | Move −2.381; move D_59 the same (165.894 → 163.513) |
| K_60 | Space, 2.75u | — | (4,8) | 121.444 | — | Delete, with D_60 |
| K_61 | RAlt, 1.5u | Right Cmd, 1.5u | (4,10) | 80.963 | 80.963 | No move |
| K_62 | RCtrl, 1u | Right Alt, 1u | (4,12) | 57.150 | 57.150 | No move |

All y values stay at 85.725. Check the arithmetic: Space centre at u = 6.875 spans 3.75u to 10.0u; left Cmd centre 3.0 spans 2.25u to 3.75u; left Alt centre 1.75 spans 1.25u to 2.25u; the right-hand keys already start at 10.0u.

Stabilisers after the change: 2u at Enter (21.431, 47.625) and left Shift (264.319, 66.675), 6.25u at Space (154.781, 85.725). Remove all four Choc stabiliser footprints.

The space switch keeps matrix position (4,6), so the firmware only needs a key map change, not a wiring change. The board loses two diodes, so the JLCPCB parts list drops from 62 diodes to 60.

## 6. Work plan

Work on a branch named `polymetis-gateron`. Commit after each step so Gavin can follow along.

### Step 0. Set up

- Install KiCad 9 or 10 from kicad.org. Opening the project upgrades it from KiCad 8 format; commit that upgrade on its own before changing anything, so the real changes are readable in the diff.
- Install the marbastlib library through KiCad's Plugin and Content Manager, or clone [ebastler/marbastlib](https://github.com/ebastler/marbastlib) and add it as a project library. Its main branch targets KiCad 10; the PCM offers older releases for 9 and 8. Licence: CERN-OHL-P v2 (permissive); credit it in the README.
- For scripted edits use the Python that ships with KiCad, where `import pcbnew` works. `kicad-cli` handles ERC, DRC, exports and renders.
- Optional: Freerouting (needs Java) for autorouting.
- Rust via rustup; the repo's `rust-toolchain.toml` pins the toolchain. FreeCAD for the frame.

### Step 1. Confirm the unknowns before editing

Get each of these from a primary source (Gateron's datasheets and drawings, or the marbastlib footprint checked against them). Gateron publishes 3D models at https://www.gateron.com/pages/3d. If any of these can't be confirmed, stop and ask Gavin rather than guessing.

1. **KS-33 switch:** plate cutout size, required plate thickness, and the distance from the PCB top to the plate.
2. **KS-2P02B01-02 socket:** pad positions and height. marbastlib's footprint `SW_KS33_HS_KS-2P02B01-02_HS_1u` sits in its experimental library, so check it against Gateron's drawing.
3. **Gateron low-profile plate-mounted stabilisers:** plate cutout shape, stem spacing for 2u and 6.25u (standard MX spacing is about 23.9 mm for 2u and 100 mm for 6.25u; do not assume these match), whether the PCB needs clearance holes, and the plate thickness they need. Gateron sells a 60% set of four 2u and one 6.25u.
4. **Underside clearance:** the height of the sockets and the USB-C receptacle below the PCB, which sets the frame thickness in step 7.
5. **JLCPCB:** whether its parts library stocks the KS-2P02B01-02 socket. The sockets sit on F.Cu with every other part, so if JLCPCB stocks them it could fit them in the same assembly run and Gavin would have nothing to solder. Report what you find; it's his decision.

### Step 2. Schematic

- Change the footprint of every switch symbol to the marbastlib KS-33 hot-swap footprint. marbastlib has 1u, 1.25u, 1.5u and 1.75u variants; use the variant matching each key's width, and the 1u variant for the 2.25u and 6.25u keys. Check what the variants differ in before relying on them.
- Delete `K_58`, `D_58`, `K_60` and `D_60`.
- Replace the stabiliser symbols or footprints as needed for the three Gateron stabilisers.
- Run ERC and fix everything it reports.

### Step 3. Main PCB

- Update the PCB from the schematic.
- Place every KS-33 footprint so that its socket pads land on **F.Cu**, the same side as the diodes, as the Choc socket pads do now. marbastlib draws its hot-swap footprints as seen from the socket side, so on this board that likely means placing them on F.Cu without flipping, but confirm it: the switch pin holes must line up with KS-33 pins, and KiCad's flipped board view must show the keyboard in normal reading order.
- Keep every switch at its current x and y except the bottom-row moves in section 5. Move the three diodes with their switches.
- Add the three stabiliser footprints at the coordinates in section 5. Remove the four Choc ones.
- Delete the tracks and vias that ran to the old socket pads, since the pad positions change. Leave the RP2040, USB and power routing alone.
- Reroute the switch matrix (Freerouting or by hand), refill the zones, and run DRC until it reports no errors. Review the warnings.
- Check the result against JLCPCB's manufacturing capabilities for track width, spacing and via size.

### Step 4. Main PCB factory files

- Export Gerbers and drill files with `kicad-cli` into `jlcpcb/`, replacing the old ones, and zip them the way the existing files are.
- Regenerate the BOM in the same columns as `jlcpcb/boethia60_bom.csv` (Reference, Value, Datasheet, Footprint, Qty, JLCPCB Part), now with 60 diodes.
- Regenerate the placement files. Check part rotations against JLCPCB's preview conventions.

### Step 5. Top plate

- marbastlib's switch and stabiliser footprints carry plate cuts on the User.Eco2 layer. Use them to rebuild the switch and stabiliser cutouts in `top-plate/`, keeping the outline and screw holes as they are.
- Set the plate thickness from step 1. If the Gateron parts need 1.2 mm, change the project's board thickness and say so in the README.
- Run DRC and export factory files.

### Step 6. Bottom plate

Confirm nothing in it depends on switch positions (it should be outline plus logo). Check the USB-C cutout. Only regenerate if something changed.

### Step 7. Middle frame

- Open `case/Middle.FCStd`. The board outline is unchanged, so the frame's outline and holes should still fit; confirm the holes line up with both plates.
- Work out the original stack first: how the 4.0 mm frame thickness relates to the plate, the Choc switch gap, the PCB and the underside parts. Then recalculate it for the KS-33 using the step 1 figures. Write the calculation in the README.
- Export the STL. The original is 310 mm long, too long for 220 mm and 256 mm print beds, so ask Gavin his bed size and, if needed, also export a two-piece version with a simple overlapping joint.

### Step 8. Firmware and layout file

In `firmware/keyboard.toml`, layer 0, replace the bottom row:

```toml
["__", "__", "LGui", "LAlt", "__", "Space", "MO(2)", "__", "Space", "__", "RAlt", "__", "RCtrl", "__", "__"],
```

with the HHKB Pro 2 bottom row:

```toml
["__", "__", "LAlt", "LGui", "__", "__", "Space", "__", "__", "__", "RGui", "__", "RAlt", "__", "__"],
```

The `MO(2)` key no longer exists, so layer 2 (arrows on H J K L) can't be reached. Ask Gavin whether to drop it (set `layers = 2`) or put it on another key. Leave layer 1, the HHKB-style Fn layer, as it is.

In `firmware/vial.json` and `boethia60.json`, replace the last row with:

```json
[{"x": 1.25}, "4,2", {"w": 1.5}, "4,3", {"w": 6.25}, "4,6", {"w": 1.5}, "4,10", "4,12"]
```

Keep RMK at its current version unless the build forces an upgrade. Build with `cargo build --release` from `firmware/`. Don't flash anything. Ask Gavin before renaming the USB product name from boethia60.

### Step 9. Documentation

Rewrite the README for Polymetis: what changed from the boethia60, the parts (switches, sockets, stabilisers, plates, frame), the stack-height calculation, and credits to arviceblot (boethia60) and ebastler (marbastlib).

### Step 10. Checks and handback

- Save the ERC and DRC reports under `docs/checks/`.
- Render top and bottom images of the board and plates with `kicad-cli pcb render` so Gavin can look them over.
- Open a pull request to `main` describing what changed, what was verified and against which source, and what is still unverified.
- Don't merge, don't push to `main`, and don't order anything.

## 7. Stop and ask Gavin when

- a dimension in step 1 can't be confirmed from a primary source
- the bottom-row move in section 5 collides with anything
- deciding what happens to layer 2
- renaming the USB product
- you need his printer bed size
- anything would change the RP2040, USB or power circuit

## 8. Context, not part of this job

Gavin's keycap plan: blank or mostly blank low-profile cross-stem caps in five colours. Four colours are by finger, mirrored across both hands; a fifth thumb colour goes on the spacebar; modifiers are plain. Every coloured key except the spacebar is 1u. The leading source is a Yuzu custom set for the NuPhy Air75 V3 plus two SMOLO 1.5u blanks. Fit on the KS-33 isn't confirmed. None of this affects the board.

## 9. Sources

- [boethia60 design files](https://github.com/arviceblot/boethia60)
- [marbastlib KiCad library](https://github.com/ebastler/marbastlib), library `marbastlib-xp-gateron_lp`
- [Gateron 3D models](https://www.gateron.com/pages/3d)
- [Gateron low-profile plate-mounted stabiliser](https://www.gateron.com/products/gateron-low-profile-plate-mounted-stabilizer)
- [Gateron low-profile hot-swap socket](https://www.gateron.com/products/gateron-low-profile-switch-hot-swap-pcb-socket)
- [RMK firmware](https://github.com/haobogu/rmk)

## Appendix A. Every switch on the current board

Measured from `boethia60/boethia60.kicad_pcb`, `firmware/keyboard.toml` and `boethia60.json`. Coordinates are KiCad's (viewed from the keyboard's underside). Top-view centre uses the formula in section 4.

| Switch | x (mm) | y (mm) | Matrix | Firmware key | Width | Top-view centre (u) | Diode | Diode x | Diode y | Diode rot |
|---|---|---|---|---|---|---|---|---|---|---|
| K_1 | 276.225 | 9.525 | (0,0) | Escape | 1u | 0.500 | D_1 | 282.575 | 6.350 | 0 |
| K_2 | 257.175 | 9.525 | (0,1) | Kc1 | 1u | 1.500 | D_2 | 265.906 | 7.144 | -90 |
| K_3 | 238.125 | 9.525 | (0,2) | Kc2 | 1u | 2.500 | D_3 | 246.856 | 7.144 | -90 |
| K_4 | 219.075 | 9.525 | (0,3) | Kc3 | 1u | 3.500 | D_4 | 227.806 | 7.144 | -90 |
| K_5 | 200.025 | 9.525 | (0,4) | Kc4 | 1u | 4.500 | D_5 | 208.756 | 7.144 | -90 |
| K_6 | 180.975 | 9.525 | (0,5) | Kc5 | 1u | 5.500 | D_6 | 189.706 | 6.888 | -90 |
| K_7 | 161.925 | 9.525 | (0,6) | Kc6 | 1u | 6.500 | D_7 | 170.656 | 7.144 | -90 |
| K_8 | 142.875 | 9.525 | (0,7) | Kc7 | 1u | 7.500 | D_8 | 151.606 | 7.144 | -90 |
| K_9 | 123.825 | 9.525 | (0,8) | Kc8 | 1u | 8.500 | D_9 | 132.556 | 7.144 | -90 |
| K_10 | 104.775 | 9.525 | (0,9) | Kc9 | 1u | 9.500 | D_10 | 113.506 | 7.144 | -90 |
| K_11 | 85.725 | 9.525 | (0,10) | Kc0 | 1u | 10.500 | D_11 | 94.456 | 7.144 | -90 |
| K_12 | 66.675 | 9.525 | (0,11) | Minus | 1u | 11.500 | D_12 | 75.406 | 7.144 | -90 |
| K_13 | 47.625 | 9.525 | (0,12) | Equal | 1u | 12.500 | D_13 | 56.356 | 7.144 | -90 |
| K_14 | 28.575 | 9.525 | (0,13) | Backslash | 1u | 13.500 | D_14 | 37.306 | 7.144 | -90 |
| K_15 | 9.525 | 9.525 | (0,14) | Grave | 1u | 14.500 | D_15 | 18.256 | 16.131 | 90 |
| K_16 | 271.462 | 28.575 | (1,0) | Tab | 1.5u | 0.750 | D_16 | 280.194 | 26.194 | -90 |
| K_17 | 247.650 | 28.575 | (1,2) | Q | 1u | 2.000 | D_17 | 256.381 | 26.194 | -90 |
| K_18 | 228.600 | 28.575 | (1,3) | W | 1u | 3.000 | D_18 | 237.331 | 26.194 | -90 |
| K_19 | 209.550 | 28.575 | (1,4) | E | 1u | 4.000 | D_19 | 218.281 | 26.194 | -90 |
| K_20 | 190.500 | 28.575 | (1,5) | R | 1u | 5.000 | D_20 | 199.231 | 26.194 | -90 |
| K_21 | 171.450 | 28.575 | (1,6) | T | 1u | 6.000 | D_21 | 180.181 | 26.194 | -90 |
| K_22 | 152.400 | 28.575 | (1,7) | Y | 1u | 7.000 | D_22 | 161.131 | 26.194 | -90 |
| K_23 | 133.350 | 28.575 | (1,8) | U | 1u | 8.000 | D_23 | 142.081 | 26.194 | -90 |
| K_24 | 114.300 | 28.575 | (1,9) | I | 1u | 9.000 | D_24 | 123.031 | 26.194 | -90 |
| K_25 | 95.250 | 28.575 | (1,10) | O | 1u | 10.000 | D_25 | 103.981 | 26.194 | -90 |
| K_26 | 76.200 | 28.575 | (1,11) | P | 1u | 11.000 | D_26 | 84.931 | 26.194 | -90 |
| K_27 | 57.150 | 28.575 | (1,12) | LeftBracket | 1u | 12.000 | D_27 | 65.881 | 26.194 | -90 |
| K_28 | 38.100 | 28.575 | (1,13) | RightBracket | 1u | 13.000 | D_28 | 46.831 | 26.194 | -90 |
| K_29 | 14.287 | 28.575 | (1,14) | Backspace | 1.5u | 14.250 | D_29 | 23.019 | 29.369 | -90 |
| K_30 | 269.081 | 47.625 | (2,0) | LCtrl | 1.75u | 0.875 | D_30 | 277.812 | 45.244 | -90 |
| K_31 | 242.887 | 47.625 | (2,2) | A | 1u | 2.250 | D_31 | 251.619 | 45.244 | -90 |
| K_32 | 223.838 | 47.625 | (2,3) | S | 1u | 3.250 | D_32 | 232.569 | 45.244 | -90 |
| K_33 | 204.787 | 47.625 | (2,4) | D | 1u | 4.250 | D_33 | 213.519 | 45.244 | -90 |
| K_34 | 185.738 | 47.625 | (2,5) | F | 1u | 5.250 | D_34 | 194.469 | 45.244 | -90 |
| K_35 | 166.688 | 47.625 | (2,6) | G | 1u | 6.250 | D_35 | 175.419 | 44.987 | -90 |
| K_36 | 147.637 | 47.625 | (2,7) | H | 1u | 7.250 | D_36 | 156.369 | 45.244 | -90 |
| K_37 | 128.588 | 47.625 | (2,8) | J | 1u | 8.250 | D_37 | 137.319 | 45.244 | -90 |
| K_38 | 109.537 | 47.625 | (2,9) | K | 1u | 9.250 | D_38 | 118.269 | 45.244 | -90 |
| K_39 | 90.487 | 47.625 | (2,10) | L | 1u | 10.250 | D_39 | 99.219 | 45.244 | -90 |
| K_40 | 71.438 | 47.625 | (2,11) | Semicolon | 1u | 11.250 | D_40 | 80.169 | 45.244 | -90 |
| K_41 | 52.388 | 47.625 | (2,12) | Quote | 1u | 12.250 | D_41 | 61.119 | 45.244 | -90 |
| K_42 | 21.431 | 47.625 | (2,13) | Enter | 2.25u | 13.875 | D_42 | 29.845 | 47.117 | -90 |
| K_43 | 264.319 | 66.675 | (3,1) | LShift | 2.25u | 1.125 | D_43 | 278.606 | 70.644 | 180 |
| K_44 | 233.363 | 66.675 | (3,2) | Z | 1u | 2.750 | D_44 | 242.094 | 64.294 | -90 |
| K_45 | 214.312 | 66.675 | (3,3) | X | 1u | 3.750 | D_45 | 223.044 | 64.294 | -90 |
| K_46 | 195.262 | 66.675 | (3,4) | C | 1u | 4.750 | D_46 | 203.994 | 64.294 | -90 |
| K_47 | 176.213 | 66.675 | (3,5) | V | 1u | 5.750 | D_47 | 184.944 | 64.294 | -90 |
| K_48 | 157.162 | 66.675 | (3,6) | B | 1u | 6.750 | D_48 | 165.894 | 64.294 | -90 |
| K_49 | 138.113 | 66.675 | (3,7) | N | 1u | 7.750 | D_49 | 146.844 | 64.294 | -90 |
| K_50 | 119.062 | 66.675 | (3,8) | M | 1u | 8.750 | D_50 | 127.794 | 64.294 | -90 |
| K_51 | 100.013 | 66.675 | (3,9) | Comma | 1u | 9.750 | D_51 | 108.744 | 64.294 | -90 |
| K_52 | 80.963 | 66.675 | (3,10) | Dot | 1u | 10.750 | D_52 | 89.694 | 64.294 | -90 |
| K_53 | 61.913 | 66.675 | (3,11) | Slash | 1u | 11.750 | D_53 | 70.644 | 64.294 | -90 |
| K_54 | 35.719 | 66.675 | (3,13) | RShift | 1.75u | 13.125 | D_54 | 44.450 | 64.294 | -90 |
| K_55 | 9.525 | 66.675 | (3,14) | MO(1) | 1u | 14.500 | D_55 | 18.256 | 67.469 | -90 |
| K_56 | 247.650 | 85.725 | (4,2) | LGui | 1u | 2.000 | D_56 | 256.381 | 83.344 | -90 |
| K_57 | 223.838 | 85.725 | (4,3) | LAlt | 1.5u | 3.250 | D_57 | 232.569 | 83.344 | -90 |
| K_58 | 188.119 | 85.725 | (4,5) | Space | 2.25u | 5.125 | D_58 | 202.406 | 89.694 | 180 |
| K_59 | 157.162 | 85.725 | (4,6) | MO(2) | 1u | 6.750 | D_59 | 165.894 | 83.344 | -90 |
| K_60 | 121.444 | 85.725 | (4,8) | Space | 2.75u | 8.625 | D_60 | 135.731 | 89.694 | 180 |
| K_61 | 80.963 | 85.725 | (4,10) | RAlt | 1.5u | 10.750 | D_61 | 89.662 | 86.614 | -90 |
| K_62 | 57.150 | 85.725 | (4,12) | RCtrl | 1u | 12.000 | D_62 | 65.913 | 86.106 | -90 |
