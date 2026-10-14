# Gateron datasheets

Downloaded from gateron.com on 14 October 2026. These are the primary sources for every Gateron dimension used in Polymetis.

| File | Part | Drawing |
|---|---|---|
| `Gateron-KS-33H10B050NN-Y24-KS-33-Red-Low-Profile-2.0.pdf` | KS-33 Low Profile 2.0 switch (Red) | page 6, drawing version 2, 2023-01-03 |
| `Gateron-KS-2P02B01-02-Low-Profile-Hot-swap-Socket-2.0.pdf` | KS-2P02B01-02 hot-swap socket | page 8, drawing version 7, 2023-12-07 |
| `Gateron-KS-57B210T-Low-Profile-Plate-Mounted-Stabilizer-2U.pdf` | KS-57B210T stabiliser, 2U | pages 2–3, drawing version 3, 2023-02-06 |
| `Gateron-KS-57B623T-Low-Profile-Plate-Mounted-Stabilizer-6.25U.pdf` | KS-57B623T stabiliser, 6.25U | pages 2–3, drawing version 3, 2023-02-06 |

## What they confirm

**KS-33 switch**
- Plate cutout 14.00 ± 0.05 mm square (housing below the flange).
- Plate thickness 1.20 ± 0.05 mm (clip step).
- Flange underside to housing bottom 2.50 ± 0.05 mm, so plate top to PCB top is 2.50 mm and the gap under a 1.2 mm plate is 1.30 mm.
- PCB layout (drawn from the underside): Ø3.00 holes at 4.40 / 4.70 and 2.60 / 5.75 from the switch centre, Ø5.25 centre hole, LED window 5.00 × 3.20 mm. This matches marbastlib's `SW_KS33_HS_KS-2P02B01-02_*` footprints exactly.

**KS-2P02B01-02 socket**
- Holes Ø3 at 4.4 / 4.7 and 2.6 / 5.75, 7.00 mm apart, centre hole Ø5.1.
- Body 1.87 ± 0.05 mm tall below the PCB (3.00 mm including the bosses that sit in the PCB holes).
- Terminal tabs 1.74 mm wide, 15.1 mm overall. They land inside marbastlib's 2.65 × 2.55 mm pads with about 0.5 mm margin on each side.

**Low-profile plate-mounted stabilisers**
- Stem spacing 24.00 ± 0.15 mm (2U) and 100.00 ± 0.15 mm (6.25U).
- Plate thickness 1.20 ± 0.1 mm.
- Flange 6.00 × 17.00 mm; housing below the plate 5.85 × 12.40 mm; 4.45 mm from plate top to housing bottom, so it reaches 3.25 mm below the plate and 1.95 mm into a 1.6 mm PCB. The PCB needs a slot under each housing.
- Recommended plate cutout dimensioned only at 6.00, 12.50 and a 1.70 notch; the rest of its shape is drawn but not dimensioned.
- No PCB slot dimensions are given.
