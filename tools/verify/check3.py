import json, numpy as np, trimesh
from shapely.geometry import Polygon, Point, box, LineString
from shapely.ops import unary_union
fr=json.load(open('build/verify/frame.json')); bot=json.load(open('build/verify/geom_bottom-plate.json'))
x0,y0,x1,y1=fr['usb_tv']
m=trimesh.load('case/polymetis-frame.stl'); zt=m.bounds[1][2]
top=unary_union([Polygon(t[:,:2]).buffer(0) for t in m.triangles if np.allclose(t[:,2],zt)]).buffer(0)
F2T=lambda x,y:(167.967+x, 73.894-y)
solid=Polygon([F2T(*p) for p in top.exterior.coords],[[F2T(*p) for p in r.coords] for r in top.interiors]).buffer(0)
def open_runs(poly,y,xa=10,xb=326):
    xs=np.arange(xa,xb,0.02); runs=[]
    for x in xs:
        if not poly.contains(Point(x,y)):
            if runs and x-runs[-1][1]<0.03: runs[-1][1]=x
            else: runs.append([x,x])
    return [(round(a,2),round(b,2)) for a,b in runs]
print("USB1 receptacle footprint, top view: x %.2f..%.2f, back face y %.2f"%(x0,x1,y0))
print("frame gaps (ends are the rounded corners) along the back wall (y=15.0):", open_runs(solid,15.0))
print("frame gaps (ends are the rounded corners) at y=18.0:", open_runs(solid,18.0))
B2T=lambda x,y:(339.117-x, y-3.106)
bp=Polygon([B2T(*p) for p in bot['outline'][0]['outer']]).buffer(0)
print("bottom plate (text outwards) gaps at y=15.0:", open_runs(bp,15.0), " at y=27.5:", open_runs(bp,27.5))
# notch depth at receptacle centre x
xc=(x0+x1)/2; ys=np.arange(13,40,0.02); depth=[y for y in ys if not bp.contains(Point(xc,y))]
print("   notch at x=%.2f runs from plate edge to y=%.2f (receptacle opening y %.2f; body ends at %.2f per the HRO drawing, 7.35 mm long; solder pins reach %.2f)"%(xc,max(depth),y0,y0+7.35,y1))
# the other orientation (text facing in) for comparison
B2Tn=lambda x,y:(x-3.175, y-3.106)
bpn=Polygon([B2Tn(*p) for p in bot['outline'][0]['outer']]).buffer(0)
print("   if fitted text-inwards, notch would be at:", open_runs(bpn,15.0))
