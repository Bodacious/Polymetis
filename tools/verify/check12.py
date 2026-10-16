import json, math
L=lambda n: json.load(open(f'build/verify/geom_{n}.json'))
pcb,top,bot=L('pcb'),L('top-plate'),L('bottom-plate')
P2T=lambda x,y:(310.842-x, y+26.269)          # main PCB (underside view) -> top view
B2T=lambda x,y:(339.117-x, y-3.106)           # bottom plate (outside view) -> top view
def bbox(pts): xs=[p[0] for p in pts]; ys=[p[1] for p in pts]; return min(xs),min(ys),max(xs),max(ys)
def centroid(pts): b=bbox(pts); return ((b[0]+b[2])/2,(b[1]+b[3])/2)
def circ(pts):
    b=bbox(pts); return abs((b[2]-b[0])-(b[3]-b[1]))<0.05 and (b[2]-b[0])<4
th=top['outline'][0]['holes']
screw_t=[centroid(h) for h in th if circ(h)]
squares=[(centroid(h),bbox(h)) for h in th if not circ(h) and abs((bbox(h)[2]-bbox(h)[0])-14)<0.05 and abs((bbox(h)[3]-bbox(h)[1])-14)<0.05]
others=[bbox(h) for h in th if not circ(h) and not (abs((bbox(h)[2]-bbox(h)[0])-14)<0.05 and abs((bbox(h)[3]-bbox(h)[1])-14)<0.05)]
print(f"top plate: {len(screw_t)} screw holes, {len(squares)} 14.00 mm switch cut-outs, {len(others)} other cut-outs")
# 1a. every switch has a square cut-out centred on it
errs=[]; used=set()
for s in pcb['switches']:
    X,Y=P2T(s['x'],s['y'])
    j,(c,b)=min(enumerate(squares),key=lambda e:math.hypot(e[1][0][0]-X,e[1][0][1]-Y))
    d=math.hypot(c[0]-X,c[1]-Y)
    if d<0.5: used.add(j); errs.append((d,s['ref']))
    else: errs.append((d,s['ref']+' (no square; nearest %.2f mm)'%d))
bad=[e for e in errs if e[0]>0.01]
print("1a switch vs cut-out centre: worst %.4f mm (%s); squares used %d/%d; >0.01 mm: %s"%(max(errs)[0],max(errs)[1],len(used),len(squares),[e[1] for e in bad]))
# 1b. space bar: merged cut-out spans switch + both stabiliser housings, over the PCB slots
pslots=[bbox(h) for h in pcb['outline'][0]['holes']]
for b in pslots:
    x0,y0=P2T(b[2],b[1]); x1,y1=P2T(b[0],b[3]); print("   PCB slot (top view) x %.2f..%.2f y %.2f..%.2f  centre x %.3f"%(x0,x1,y0,y1,(x0+x1)/2))
for b in others: print("   plate space-bar cut-out x %.2f..%.2f y %.2f..%.2f"%(b[0],b[2],b[1],b[3]))
sp=[s for s in pcb['switches'] if s['ref']=='K_59'][0]; X,Y=P2T(sp['x'],sp['y']); print("   space switch centre (top view) %.3f, %.3f"%(X,Y))
st=pcb['st1']; print("   ST1 centre (top view) %.3f, %.3f"%P2T(st['x'],st['y']))
# 1c/2. screw holes: top plate vs bottom plate (mapped)
bh=bot['outline'][0]['holes']; screw_b=[B2T(*centroid(h)) for h in bh]
worst=max(min(math.hypot(a[0]-b[0],a[1]-b[1]) for b in screw_b) for a in screw_t)
print("   top-plate hole dia %.2f; bottom-plate hole dia %.2f"%((bbox(th[[i for i,h in enumerate(th) if circ(h)][0]])[2]-bbox(th[[i for i,h in enumerate(th) if circ(h)][0]])[0]), bbox(bh[0])[2]-bbox(bh[0])[0]))
print("1c screw holes top vs bottom plate: worst offset %.3f mm"%worst)
ot=bbox(top['outline'][0]['outer']); ob=bbox([B2T(*p) for p in bot['outline'][0]['outer']])
print("1d outlines: top %s  bottom(mapped) %s  diff %s"%(tuple(round(v,3) for v in ot),tuple(round(v,3) for v in ob),tuple(round(a-b,3) for a,b in zip(ot,ob))))
op=bbox([P2T(*p) for p in pcb['outline'][0]['outer']]); print("   PCB outline (top view) %s; margin to plate edge L %.2f T %.2f R %.2f B %.2f"%(tuple(round(v,3) for v in op),op[0]-ot[0],op[1]-ot[1],ot[2]-op[2],ot[3]-op[3]))
json.dump({"screw_t":screw_t,"pcb_outline_tv":[P2T(*p) for p in pcb['outline'][0]['outer']],"plate_outline":top['outline'][0]['outer']},open('build/verify/tv.json','w'))
