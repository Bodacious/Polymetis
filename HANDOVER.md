# Polymetis: decisions and status

The current state of the project, for Gavin and for any Claude session picking it up. Read this before changing anything. The original brief from 12 October 2026, with its measurements of the unmodified boethia60, is in [`docs/history/handover-brief-2026-10-12.md`](docs/history/handover-brief-2026-10-12.md); where it disagrees with this page, this page wins.

## Aims

1. **Low action.** Short key travel, so fingers move nimbly across the board. Short travel matters more than a light press. The keys should feel flat and even to glide over, not like cobblestones.
2. **HHKB Professional 2 layout**, exactly, with a one-piece space bar.
3. **Function keys on a Fn layer**, such as Fn+P for play/pause, remappable later without rebuilding the firmware.

## Decisions

Don't reopen these without asking Gavin.

| Topic | Decision |
|---|---|
| Layout | HHKB Professional 2: 60 keys, Backspace on the Tab row, `\` and `` ` `` top right, Ctrl beside A, Fn right of right Shift, no right Ctrl. Not ISO. |
| Key sizes | 51 × 1u, 4 × 1.5u (Tab, Backspace, both Cmd), 2 × 1.75u (Ctrl, right Shift), 2 × 2.25u (Enter, left Shift), 1 × 6.25u space bar. |
| Bottom row | 1.25u gap, Alt 1u, Cmd 1.5u, Space 6.25u, Cmd 1.5u, Alt 1u, 2.5u gap. A real HHKB has a 6u space bar and a 1.5u left gap; low-profile keycap sets carry 6.25u, so the extra 0.25u comes out of the left gap. The space bar is centred between the index fingers (6.875u from the left), not on the case. The right-hand keys stay put, clear of the RP2040, reset pad and boot button. |
| Switches | Gateron KS-33 Low Profile 2.0, linear (Red). Gateron's drawing: 3.0 ± 0.2 mm total travel, 1.7 ± 0.4 mm to actuation, 50 ± 15 gf. Chosen for short travel. |
| Sockets | Gateron KS-2P02B01-02 hot-swap, soldered by hand (JLCPCB has no stock). |
| Stabilisers | One: Gateron low-profile plate-mounted 6.25U (KS-57B623T) under Space. None under Enter, left Shift, Ctrl or right Shift. |
| Stabiliser PCB slot | Keebio's slot size, 6.5 × 16 mm at 100 mm spacing; Gateron publishes none. Test-fit on the top plate before ordering the main PCB. |
| Plates | Top 1.2 mm FR4 (Gateron's figure for both switch and stabiliser). Bottom 1.6 mm FR4 with a USB-C notch. |
| Frame | 5.3 mm, one piece, printed by a professional service. |
| Keycaps | As low as possible without hurting ease of build or quality; cross (MX) stems for KS-33. A flat, uniform profile suits the "not cobblestones" aim. Fit on KS-33 not yet confirmed. |
| Keycap colours | Five colours, one per finger: thumb, index, middle, ring, little. Modifiers take the colour of the finger that presses them (Alt and Cmd thumb; Tab, Ctrl, Shift, Enter, Backspace, Fn little finger). [`docs/layout.html`](docs/layout.html) has the full colouring. |
| Firmware | RMK 0.5 with Vial. Two layers: base and Fn. The old layer 2 is gone. USB product name stays `boethia60` unless Gavin says otherwise. |
| Electronics | RP2040, USB-C and power circuit unchanged from the boethia60. |

## Fn layer

Hold Fn (right of right Shift) and press:

| Keys | Function |
|---|---|
| `1` … `=` | F1 … F12 |
| `\` | Insert |
| `` ` `` | Delete |
| Backspace | Delete |
| `I` `O` `P` | Previous track, next track, play/pause |
| `A` `S` `D` `F` | Volume down, volume up, mute, eject |
| `[` | Up |
| `;` `'` `/` | Left, right, down |
| `K` `L` `,` `.` | Home, Page Up, End, Page Down |
| Tab | Bootloader (for flashing new firmware) |

Defined in `firmware/keyboard.toml`. Any key can be changed live in the Vial app.

## Status

| Part | State |
|---|---|
| Main PCB | Routed. DRC: 0 unconnected pads, schematic parity clean; the only errors are two clearances inside the original USB-C footprint. Factory files in `jlcpcb/`. |
| Top plate | Done, DRC clean. Factory files in `top-plate/`. |
| Bottom plate | Done. Assumes the logo faces outwards so the USB notch lines up with the frame opening. |
| Frame | `case/polymetis-frame.stl`, watertight. |
| Firmware | Builds; `cargo make uf2` makes `boethia60.uf2`. Not flashed. |
| Ordering | Nothing ordered. |

## Next steps

1. Order the top plate on its own, plus one KS-57B623T stabiliser and a few KS-33 switches and sockets.
2. Test-fit the stabiliser and a switch. Check the stabiliser wire and housings sit inside the main board's slot outlines.
3. Order the main PCB with assembly and the bottom plate; print the frame.
4. Buy 60 switches, 60 sockets and keycaps; solder the sockets; build; flash.

## Ground rules

- Work on `main`.
- Never order anything from anywhere unless Gavin specifically asks.
- Don't guess a physical dimension. Confirm it from Gateron's datasheets (`docs/datasheets/`) or drawings, or ask Gavin.
- Leave the RP2040, USB and power circuit unchanged unless Gavin agrees.

## Stop and ask Gavin when

- a dimension can't be confirmed from a primary source
- a change would move a key or alter the layout
- anything would change the RP2040, USB or power circuit
- renaming the USB product
