import json, math, numpy as np, trimesh
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
tv=json.load(open('build/verify/tv.json')); pcb=json.load(open('build/verify/geom_pcb.json'))
m=trimesh.load('case/polymetis-frame.stl')
print("frame extents (mm):", m.extents.round(3), "watertight:", m.is_watertight, "volume cm3: %.1f"%(m.volume/1000))
zt=m.bounds[1][2]
top=unary_union([Polygon(t[:,:2]).buffer(0) for t in m.triangles if np.allclose(t[:,2],zt)]).buffer(0)
F2T=lambda x,y:(167.967+x, 73.894-y)
def tvpoly(poly): return Polygon([F2T(*p) for p in poly.exterior.coords]), [Polygon([F2T(*p) for p in r.coords]) for r in poly.interiors]
outer, ints = tvpoly(top)
ints.sort(key=lambda p:p.area)
holes=[p for p in ints if p.area<20]; cavity=max(ints,key=lambda p:p.area)
print("frame top face: interiors", len(ints), "small holes", len(holes), "hole dia ~%.2f"%(2*math.sqrt(holes[0].area/math.pi)))
# holes vs plate screw holes
worst=max(min(math.hypot(h.centroid.x-s[0],h.centroid.y-s[1]) for s in tv['screw_t']) for h in holes)
print("2a frame holes vs plate holes: worst offset %.3f mm"%worst)
po=Polygon(tv['plate_outline']); print("2b outline: frame %s  plate %s"%(tuple(round(v,3) for v in outer.bounds),tuple(round(v,3) for v in po.bounds)))
# cavity vs PCB outline
pcbp=Polygon(tv['pcb_outline_tv']).buffer(0)
# the cavity polygon may be merged with the USB opening; check PCB inside the full open region
opening=Polygon(outer.exterior).difference(Polygon([F2T(*p) for p in top.exterior.coords])) if False else None
solid=Polygon([F2T(*p) for p in top.exterior.coords],[ [F2T(*p) for p in r.coords] for r in top.interiors]).buffer(0)
inter=solid.intersection(pcbp)
print("2c PCB overlap with frame material: %.4f mm2"%inter.area, "| min gap PCB edge to frame wall: %.3f mm"%solid.boundary.distance(pcbp.boundary) if inter.area<1e-6 else "")
# wall thickness between screw holes and cavity
print("   min distance screw hole to PCB edge: %.2f mm"%min(h.distance(pcbp) for h in holes))
# USB opening vs USB-C receptacle
u=pcb['usb']; b=u['bbox']; ux0,uy0=F2T(0,0)  # dummy
x0=310.842-b[2]; x1=310.842-b[0]; y0=b[1]+26.269; y1=b[3]+26.269
print("2d USB1 footprint incl. solder pins (top view) x %.2f..%.2f y %.2f..%.2f, centre x %.2f"%(x0,x1,y0,y1,(x0+x1)/2))
print("   back wall: plate edge y %.2f, PCB edge y %.2f, USB1 front y %.2f"%(outer.bounds[1],pcbp.bounds[1],y0))
json.dump({"usb_tv":[x0,y0,x1,y1]},open('build/verify/frame.json','w'))
