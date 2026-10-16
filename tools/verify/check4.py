import json, re, tomllib
g=json.load(open('build/verify/geom_pcb.json'))
kb=tomllib.load(open('firmware/keyboard.toml','rb'))
net2gpio={}
for p in g['u3']:
    m=re.fullmatch(r'GPIO(\d+)(_ADC\d)?',p['fn'] or '')
    if m and p['net']: net2gpio[p['net']]=int(m.group(1))
rows=[f'row{i}' for i in range(5)]; cols=[f'col{i}' for i in range(15)]
ok=True
for name,nets,pins in (('rows (input_pins)',rows,kb['matrix']['input_pins']),('cols (output_pins)',cols,kb['matrix']['output_pins'])):
    for n,pin in zip(nets,pins):
        want=int(pin.split('_')[1]); got=net2gpio.get(n)
        if got!=want: ok=False; print('  MISMATCH',n,'board GPIO',got,'firmware',pin)
    print(f'{name}: {len(nets)} nets checked')
print('pin map matches board' if ok else 'pin map has mismatches')
# matrix position of every switch from the copper: col net on the switch, row net via its diode
layout=[  # expected keys in top-view order with widths (HHKB Pro 2, this board)
 [("Escape",1),("Kc1",1),("Kc2",1),("Kc3",1),("Kc4",1),("Kc5",1),("Kc6",1),("Kc7",1),("Kc8",1),("Kc9",1),("Kc0",1),("Minus",1),("Equal",1),("Backslash",1),("Grave",1)],
 [("Tab",1.5),("Q",1),("W",1),("E",1),("R",1),("T",1),("Y",1),("U",1),("I",1),("O",1),("P",1),("LeftBracket",1),("RightBracket",1),("Backspace",1.5)],
 [("LCtrl",1.75),("A",1),("S",1),("D",1),("F",1),("G",1),("H",1),("J",1),("K",1),("L",1),("Semicolon",1),("Quote",1),("Enter",2.25)],
 [("LShift",2.25),("Z",1),("X",1),("C",1),("V",1),("B",1),("N",1),("M",1),("Comma",1),("Dot",1),("Slash",1),("RShift",1.75),("MO(1)",1)],
 [(None,1.25),("LAlt",1),("LGui",1.5),("Space",6.25),("RGui",1.5),("RAlt",1)]]
expect={}
for r,row in enumerate(layout):
    x=0
    for k,w in row:
        if k: expect[(r,round(x+w/2,3))]=k
        x+=w
km=kb['layout']['keymap'][0]
problems=[]; seen=set()
for s in g['switches']:
    pads=s['pads']; col=[n for n in pads.values() if n.startswith('col')]; other=[n for n in pads.values() if not n.startswith('col')]
    d='D_'+s['ref'][2:]; dn=g['diodes'].get(d,{})
    row=[n for n in dn.values() if n.startswith('row')]
    linked = other and other[0] in dn.values()
    if len(set(col))!=1 or len(set(row))!=1 or not linked:
        problems.append((s['ref'],'wiring',col,row,other)); continue
    r,c=int(row[0][3:]),int(col[0][3:])
    if (r,c) in seen: problems.append((s['ref'],'duplicate position',r,c))
    seen.add((r,c))
    u=round((285.75-s['x'])/19.05,3); vr=round((s['y']-9.525)/19.05)
    want=expect.get((vr,u)); got=km[r][c]
    if vr!=r: problems.append((s['ref'],'physical row %d but matrix row %d'%(vr,r)))
    if want!=got: problems.append((s['ref'],'at row %d u %.3f expects %s; keymap[%d][%d] = %s'%(vr,u,want,r,c,got)))
print('switches checked:',len(g['switches']),'| unique matrix positions:',len(seen))
used={(r,c) for r in range(5) for c in range(15) if km[r][c]!='__'}
print('keymap entries without a switch:',sorted(used-seen),'| switches on "__" entries:',sorted(seen-used))
print('problems:',problems if problems else 'none')
