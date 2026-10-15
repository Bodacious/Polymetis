# Polymetis: decisions and status

The current state of the project, for Gavin and for any Claude session picking it up. Read this before changing anything.

## Aims

1. **Low action.** Short key travel, so fingers move nimbly across the board. Short travel matters more than a light press. The keys should feel flat and even to glide over, not like cobblestones.
2. **HHKB Professional 2 layout**, exactly, with a one-piece space bar.
3. **The HHKB Fn layer, replicated**, plus media keys, remappable later without rebuilding the firmware.

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
| Keycap colours | Six colours. Five by finger for letters, numbers, punctuation and the space bar: thumb (space bar), index, middle, ring, little. The sixth is dark grey, the body colour, for the 11 modifiers: Tab, Backspace, Ctrl, Enter, both Shifts, Fn, both Alts, both Cmds. [`docs/layout.html`](docs/layout.html) has the full colouring. |
| Firmware | RMK 0.5 with Vial. Two layers: base and Fn. The old layer 2 is gone. The keyboard reports itself over USB as `Polymetis`. |
| Electronics | RP2040, USB-C and power circuit are fixed; change only with Gavin's agreement. F1 is a resettable fuse, SMD0805P050TF/12 (C90129: 500 mA hold, 1 A trip, 12 V), on an 0805 footprint. An earlier parts list had a ferrite bead (C1015) there by mistake. |
| Board text | "Polymetis" on the main PCB's underside and on the bottom plate's outside face. |

## Fn layer

Hold Fn (right of right Shift) and press the key. This replicates the HHKB Professional 2 Fn layer (as in QMK's HHKB keymap), plus track controls and a bootloader key on keys the HHKB leaves unused.

| Keys | Function |
|---|---|
| Esc | Power |
| `1` … `=` | F1 … F12 |
| `\` / `` ` `` | Insert / Delete |
| Tab | Caps Lock |
| `I` `O` `P` | Print Screen, Scroll Lock, Pause |
| `[` | Up |
| Backspace | Backspace |
| `A` `S` `D` | Volume down, volume up, mute |
| `F` | Eject (the HHKB's Mac-mode key) |
| `H` `J` | Keypad `*`, keypad `/` |
| `K` `L` | Home, Page Up |
| `;` `'` | Left, right |
| Enter | Keypad Enter |
| `N` `M` | Keypad `+`, keypad `-` |
| `,` `.` | End, Page Down |
| `/` | Down |
| `Z` `X` `C` | Previous track, play/pause, next track (not on the HHKB) |
| `B` | Bootloader, for flashing (not on the HHKB) |

Defined in `firmware/keyboard.toml`. Any key can be changed live in the Vial app.

## Status

| Part | State |
|---|---|
| Main PCB | Routed. DRC: 0 unconnected pads, schematic parity clean; the only errors are two clearances inside the USB-C connector footprint. Factory files in `jlcpcb/`. |
| Top plate | Done, DRC clean. Factory files in `top-plate/`. |
| Bottom plate | Done. Assumes the "Polymetis" text faces outwards so the USB notch lines up with the frame opening. |
| Frame | `case/polymetis-frame.stl`, watertight. |
| Firmware | Builds; `cargo make uf2` makes `polymetis.uf2`. Not flashed. |
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
