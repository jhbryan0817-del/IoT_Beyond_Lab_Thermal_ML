# Historical Rev A builder. For current Rev B, open HKU-thermal-enclosure.f3d.
# To reproduce from scratch: build Rev A, then run Revise-enclosure-in-Fusion.py once.
import adsk.core, adsk.fusion, math, json, os

OUT = r'C:/Users/jhbryan/Documents/Codex/2026-09-23/https-github-com-jhbryan0817-del-iot-4/outputs'
F=adsk.fusion.FeatureOperations
def p(x,y,z=0): return adsk.core.Point3D.create(x/10,y/10,z/10)
def v(mm): return adsk.core.ValueInput.createByString(mm if isinstance(mm,str) else str(mm)+' mm')
def oc(items):
 c=adsk.core.ObjectCollection.create()
 for i in items: c.add(i)
 return c
def comp(root,name):
 o=root.occurrences.addNewComponent(adsk.core.Matrix3D.create());o.component.name=name
 return o.component
def sketch(c,z,name):
 i=c.constructionPlanes.createInput();i.setByOffset(c.xYConstructionPlane,v(z));pl=c.constructionPlanes.add(i)
 pl.name=name+' plane';s=c.sketches.add(pl);s.name=name;pl.isLightBulbOn=False
 return s
def rr(s,x0,y0,x1,y1,r):
 l=s.sketchCurves.sketchLines;a=s.sketchCurves.sketchArcs
 l.addByTwoPoints(p(x0+r,y0),p(x1-r,y0)); a.addByCenterStartSweep(p(x1-r,y0+r),p(x1-r,y0),math.pi/2)
 l.addByTwoPoints(p(x1,y0+r),p(x1,y1-r)); a.addByCenterStartSweep(p(x1-r,y1-r),p(x1,y1-r),math.pi/2)
 l.addByTwoPoints(p(x1-r,y1),p(x0+r,y1)); a.addByCenterStartSweep(p(x0+r,y1-r),p(x0+r,y1),math.pi/2)
 l.addByTwoPoints(p(x0,y1-r),p(x0,y0+r)); a.addByCenterStartSweep(p(x0+r,y0+r),p(x0,y0+r),math.pi/2)
def ex(c,s,h,op,name,profile=None):
 pr=profile if profile else s.profiles.item(0)
 ei=c.features.extrudeFeatures.createInput(pr,op);ei.setDistanceExtent(False,v(h))
 if op==F.CutFeatureOperation:ei.participantBodies=list(c.bRepBodies)
 e=c.features.extrudeFeatures.add(ei);e.name=name;s.isVisible=False
 if op==F.NewBodyFeatureOperation:e.bodies.item(0).name=name
 return e
def box(c,x,y,z,l,w,h,name,op=F.NewBodyFeatureOperation,r=0):
 s=sketch(c,z,name)
 if r: rr(s,x,y,x+l,y+w,r)
 else: s.sketchCurves.sketchLines.addTwoPointRectangle(p(x,y),p(x+l,y+w))
 return ex(c,s,h,op,name)
def cyl(c,x,y,z,r,h,name,op=F.NewBodyFeatureOperation):
 s=sketch(c,z,name);s.sketchCurves.sketchCircles.addByCenterRadius(p(x,y),r/10)
 return ex(c,s,h,op,name)
def ring(c,z,h,outer,inner,name,op):
 s=sketch(c,z,name);rr(s,*outer);rr(s,*inner)
 pr=min(list(s.profiles),key=lambda a:a.areaProperties().area)
 return ex(c,s,h,op,name,pr)
def xzpoly(c,coords,y,depth,name,op):
 i=c.constructionPlanes.createInput();i.setByOffset(c.xZConstructionPlane,v(y));pl=c.constructionPlanes.add(i)
 s=c.sketches.add(pl);s.name=name;pl.isLightBulbOn=False
 pts=[s.modelToSketchSpace(p(x,y,z)) for x,z in coords]
 for j in range(len(pts)):s.sketchCurves.sketchLines.addByTwoPoints(pts[j],pts[(j+1)%len(pts)])
 return ex(c,s,-depth,op,name)
def color(d,body,name,r,g,b):
 base=None
 for lib in adsk.core.Application.get().materialLibraries:
  for ap in lib.appearances:
   if ap.name=='Plastic - Matte (Black)':base=ap;break
  if base:break
 if not base:return
 a=d.appearances.itemByName(name) or d.appearances.addByCopy(base,name)
 cp=adsk.core.ColorProperty.cast(a.appearanceProperties.itemById('opaque_albedo'))
 if cp:cp.value=adsk.core.Color.create(r,g,b,255)
 body.appearance=a
def label(c,txt,x0,y0,x1,y1,z,height,depth,name):
 s=sketch(c,z,name);i=s.sketchTexts.createInput2(txt,height/10);i.fontName='Arial'
 i.setAsMultiLine(p(x0,y0),p(x1,y1),adsk.core.HorizontalAlignments.LeftHorizontalAlignment,adsk.core.VerticalAlignments.MiddleVerticalAlignment,0)
 t=s.sketchTexts.add(i);ex(c,s,-depth,F.CutFeatureOperation,name,t)

def run(_context: str):
 a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeProduct);root=d.rootComponent
 if root.occurrences.count or root.bRepBodies.count:raise RuntimeError('Expected empty Thermal_Enclosure document; no existing geometry changed.')
 d.designIntent=adsk.fusion.DesignIntentTypes.HybridDesignIntentType
 d.designType=adsk.fusion.DesignTypes.ParametricDesignType;d.unitsManager.distanceDisplayUnits=adsk.fusion.DistanceUnits.MillimeterDistanceUnits
 params=[('PCB_thickness',1.6,'Repository KiCad Rev1.1'),('Female_socket_height',8.51,'Samtec SSW drawing'),('Male_spacer_assumed',2.54,'VERIFY actual soldered male header'),('Wall',1.8,'PETG 0.4 mm nozzle prototype'),('PCB_edge_clearance',0.7,'Per side nominal'),('Lid_fit_clearance',0.35,'Per side locating lip clearance'),('Battery_length_limit',36,'Adafruit 1578 protected 500mAh envelope'),('Battery_width_limit',29,'Protected pack'),('Battery_thickness_limit',4.75,'Protected pack'),('Case_height',33.5,'Maximum at battery side'),('Sensor_face_height',29.5,'Lowered nose preserves field of view')]
 for n,num,comment in params:d.userParameters.add(n,v(num),'mm',comment)
 base=comp(root,'01 Rear shell - PETG');lid=comp(root,'02 Front shell - engraved');tray=comp(root,'03 Removable insulated battery tray');ref=comp(root,'90 Hardware references - do not print')
 outer=(-2.5,-2.5,82.5,42.5,3.0);inner=(-0.7,-0.7,80.7,40.7,1.2)
 floor=box(base,-2.5,-2.5,0,85,45,2.4,'Rear floor',r=3).bodies.item(0)
 ring(base,2.4,22.6,outer,inner,'Perimeter wall to service seam',F.JoinFeatureOperation)
 holes=[(4,4),(4,36),(76,4),(76,36)]
 for j,(x,y) in enumerate(holes):
  cyl(base,x,y,2.4,3.2,18.65,'PCB support '+str(j+1),F.JoinFeatureOperation)
  cyl(base,x,y,-.1,1.7,21.3,'M3 clearance '+str(j+1),F.CutFeatureOperation)
  s0=sketch(base,-.01,'Countersink outer');s0.sketchCurves.sketchCircles.addByCenterRadius(p(x,y),.311)
  s1=sketch(base,1.4,'Countersink inner');s1.sketchCurves.sketchCircles.addByCenterRadius(p(x,y),.17)
  ci=base.features.loftFeatures.createInput(F.CutFeatureOperation);ci.loftSections.add(s0.profiles.item(0));ci.loftSections.add(s1.profiles.item(0));ci.participantBodies=list(base.bRepBodies);base.features.loftFeatures.add(ci).name='M3 flush 90 degree countersink';s0.isVisible=False;s1.isVisible=False
 # USB opening accepts the cable overmould because the carrier recesses the Heltec.
 box(base,-3,11.6,5.0,13.5,15,9.5,'USB-C cable access corridor',F.CutFeatureOperation,r=1)
 # Local relief lets two insulated battery conductors turn around the carrier edge.
 box(base,-1.75,15,18.3,2.1,10,7.0,'Battery wire edge bypass',F.CutFeatureOperation,r=.3)
 for x in (12,39):
  for y in (-.7,35.2):box(base,x,y,23.45,7,5.5,1.4,'Tray support shelf',F.JoinFeatureOperation)
 # Cable vent slots only in the controller chamber, below the carrier.
 for x in (20,26,32,38,44):box(base,x,39.8,8,2.2,3.5,6,'Rear side ventilation',F.CutFeatureOperation,r=.6)
 # SMA pigtail bulkhead access in the vacant rear nose, not over the sensor face.
 i=base.constructionPlanes.createInput();i.setByOffset(base.xZConstructionPlane,v(43));pl=base.constructionPlanes.add(i);s=base.sketches.add(pl);pl.isLightBulbOn=False
 s.name='SMA bulkhead 6.5 mm - verify selected hardware';pt=s.modelToSketchSpace(p(68,43,12));s.sketchCurves.sketchCircles.addByCenterRadius(pt,.325);ex(base,s,-5,F.CutFeatureOperation,'SMA antenna port')
 # Clean rear service display opening and tool access: positions are conservative envelopes.
 box(base,25.8,8.6,-.1,31,21,2.6,'OLED service window',F.CutFeatureOperation,r=1.2)
 for y in (9.9,28.3):cyl(base,13.7,y,-.1,2,2.6,'RST PRG service access - verify alignment',F.CutFeatureOperation)
 # Front cap with a lowered sensor nose and a sloping transition.
 box(lid,-2.5,-2.5,25,85,45,'Case_height - 25 mm','Front cap blank',r=3)
 box(lid,-.7,-.7,24.9,81.4,41.4,2.8,'Front cavity lower level',F.CutFeatureOperation,r=1.2)
 xzpoly(lid,[(-.7,27.69),(58,27.69),(50,31.7),(-.7,31.7)],40.7,41.4,'Battery cavity with sloped roof',F.CutFeatureOperation)
 xzpoly(lid,[(50,33.5),(58,29.5),(84,29.5),(84,34),(50,34)],43,46,'Lowered thermal nose',F.CutFeatureOperation)
 ring(lid,23.3,1.7,(-.35,-.35,80.35,40.35,.85),(.85,.85,79.15,39.15,.55),'Locating lip - 0.35 per side',F.JoinFeatureOperation)
 for j,(x,y) in enumerate(holes):
  top=31.7 if x<50 else 27.7
  cyl(lid,x,y,22.65,3.2,top-22.65,'Carrier clamping column '+str(j+1),F.JoinFeatureOperation)
  cyl(lid,x,y,22.55,2.1,4.3,'M3 insert pocket 4.2 x 4.2 '+str(j+1),F.CutFeatureOperation)
  cyl(lid,x,y,26.75,1.7,1.5,'M3 screw tip clearance '+str(j+1),F.CutFeatureOperation)
 # Circular flare clears both horizontal and vertical FOV, regardless of sensor clocking.
 s0=sketch(lid,27.59,'Thermal aperture throat');s0.sketchCurves.sketchCircles.addByCenterRadius(p(69,20),.55)
 s1=sketch(lid,33.7,'Thermal aperture flare');s1.sketchCurves.sketchCircles.addByCenterRadius(p(69,20),1.19)
 li=lid.features.loftFeatures.createInput(F.CutFeatureOperation);li.loftSections.add(s0.profiles.item(0));li.loftSections.add(s1.profiles.item(0));li.participantBodies=list(lid.bRepBodies);lf=lid.features.loftFeatures.add(li);lf.name='Unobstructed 110 x 75 degree thermal flare';s0.isVisible=False;s1.isVisible=False
 # Wire pass through the lip at the battery exit.
 box(lid,-1,15,23.1,3,10,2.1,'Wire clearance in locating lip',F.CutFeatureOperation)
 for x in (11.7,38.7):
  for y in (-.5,38.8):box(lid,x,y,23.2,7.6,1.7,1.75,'Tray shelf relief in lid lip',F.CutFeatureOperation)
 for x in (10,45):
  for y in (3.8,34.8):box(lid,x,y,27.85,2,1.4,3.85,'Tray anti-lift pad - 0.2 clearance',F.JoinFeatureOperation)
 label(lid,'HKU',7,23,48,30,33.5,5,.45,'HKU engraved')
 label(lid,'IoT Beyond Lab',7,15,49,22,33.5,3.0,.45,'IoT Beyond Lab engraved')
 label(lid,'THERMAL NODE',7,8,48,12,33.5,1.6,.35,'Thermal node identifier')
 # Tray sits on shell shelves, not on solder joints or components.
 box(tray,9.2,4.1,24.85,39.6,31.8,.8,'Battery insulation floor',r=.6)
 ring(tray,25.65,2,(9.2,4.1,48.8,35.9,.6),(10,4.9,48,35.1,.3),'Loose battery retaining rim',F.JoinFeatureOperation)
 box(tray,8.9,15,25.6,2,10,2.3,'Battery lead exit',F.CutFeatureOperation)
 # Thin hook-and-loop strap slots, outside the nominal pouch footprint.
 for x in (19,38):
  for y in (4.2,35.1):box(tray,x,y,24.75,5,.6,3.2,'Optional 5 mm retention ribbon slot',F.CutFeatureOperation)
 # Hardware envelope assembly, dimensions in mm. These are references, not vendor STEP geometry.
 pcb=box(ref,0,0,21.05,80,40,'PCB_thickness','Carrier PCB Rev1.1 - exact outline').bodies.item(0);pcb.name='PCB 80 x 40 x 1.6'
 for x,y in holes:cyl(ref,x,y,20.95,1.6,1.8,'Carrier mounting hole',F.CutFeatureOperation)
 color(d,pcb,'PCB green',28,104,73)
 for y in (7.672,30.532):
  b=box(ref,11.03,y-1.205,12.54,46.23,2.41,'Female_socket_height','Samtec SSW-118 socket envelope').bodies.item(0);color(d,b,'Socket charcoal',35,38,43)
  b=box(ref,11.28,y-1.27,10,45.72,2.54,2.54,'Male header spacer - assumed 2.54').bodies.item(0);color(d,b,'Socket charcoal',35,38,43)
 module=box(ref,9.04,6.352,8.4,50.2,25.5,1.6,'Heltec V3.2 PCB envelope',r=.8).bodies.item(0);color(d,module,'Heltec dark',40,46,58)
 oled=box(ref,25.96,9.82,3.4,33.28,18.56,5,'Heltec OLED envelope').bodies.item(0);color(d,oled,'OLED blue black',17,33,50)
 usb=box(ref,8.34,14.55,5.6,8,9.1,3.2,'USB-C socket approximate envelope').bodies.item(0);color(d,usb,'Connector metal',170,174,178)
 for x in (12.55,55.73):
  for y in (7.672,30.532):
   b=cyl(ref,x,y,22.65,.45,1.1,'Socket tail keepout').bodies.item(0);color(d,b,'Connector metal',170,174,178)
 sens=cyl(ref,69,20,22.65,4.725,5.7,'MLX90640 maximum can envelope').bodies.item(0);color(d,sens,'Sensor dark metal',65,70,80)
 flange=cyl(ref,69,20,22.65,5.12,.5,'Sensor flange and tab envelope').bodies.item(0);color(d,flange,'Connector metal',170,174,178)
 eye=cyl(ref,69,20,28.35,1.35,.08,'Thermal optical window').bodies.item(0);color(d,eye,'Lens graphite',14,18,24)
 batt=box(ref,11,5.5,25.85,36,29,4.75,'Adafruit 1578 protected 500mAh envelope',r=.7).bodies.item(0);color(d,batt,'Battery silver',174,182,193)
 # Front-side components and solder tails retained as conservative envelopes.
 for x,y,l,w,h in [(68.94,11.7,4,2.8,2),(68.94,7.7,4,2.8,2),(24,13,5.5,2.5,1.4)]:
  b=box(ref,x,y,22.65,l,w,h,'Front component keepout').bodies.item(0);color(d,b,'Component beige',148,121,76)
 for target,parts,n in [(module,[oled,usb],'Heltec V3.2 component envelope'),(sens,[flange,eye],'MLX90640 can flange and aperture')]:
  ci=ref.features.combineFeatures.createInput(target,oc(parts));ci.operation=F.JoinFeatureOperation;ci.isKeepToolBodies=False
  co=ref.features.combineFeatures.add(ci);co.name=n;co.bodies.item(0).name=n
 for c,n,rgb in [(base,'Rear warm grey',(72,79,88)),(lid,'Front porcelain',(224,226,219)),(tray,'Tray graphite',(70,81,94))]:
  for b in c.bRepBodies:color(d,b,n,*rgb)
 for c in (base,lid,tray,ref):
  c.isOriginFolderLightBulbOn=False
  for s in c.sketches:s.isVisible=False
 root.isOriginFolderLightBulbOn=False
 d.attributes.add('HKU','design_status','Fit-check prototype; verify male header, connector alignment, battery actual pack and aperture before manufacture.')
 a.activeViewport.camera= a.activeViewport.camera
 cam=a.activeViewport.camera;cam.viewOrientation=adsk.core.ViewOrientations.IsoTopRightViewOrientation;cam.isFitView=True;a.activeViewport.camera=cam;a.activeViewport.fit();a.activeViewport.refresh()
 print('CREATED',[(o.name,o.component.bRepBodies.count) for o in root.occurrences])
 print('Envelope 85 x 45 x 33.5 mm, lowered sensor nose 29.5 mm. PCB back z21.05, front z22.65.')
