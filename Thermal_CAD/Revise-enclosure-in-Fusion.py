import adsk.core, adsk.fusion, math, json, os

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
 base=next(c for c in d.allComponents if c.name=='01 Rear shell - PETG')
 ref=next(c for c in d.allComponents if c.name.startswith('90 Hardware'))
 for o in list(root.occurrences):
  if o.component.name.startswith(('02 Front','03 Removable')):root.features.removeFeatures.add(o)
 for b in list(ref.bRepBodies):
  if '500mAh' in b.name:ref.features.removeFeatures.add(b)
 base.name='01 Main housing - Rev B'
 # Remove the four obstructing tray shelves, without cutting the perimeter walls.
 for x in (12,39):
  for y in (-.7,35.2):box(base,x,y,23.45,7,5.5,1.4,'Remove old tray shelf',F.CutFeatureOperation)
 # Replace through-fastening with independent blind pilot holes for direct M3 threading.
 for j,(x,y) in enumerate([(4,4),(4,36),(76,4),(76,36)]):
  cyl(base,x,y,0,1.7,21.05,'Fill obsolete through hole '+str(j+1),F.JoinFeatureOperation)
  cyl(base,x,y,12.65,1.3,8.5,'PCB M3 direct thread pilot '+str(j+1),F.CutFeatureOperation)
 # Extend behind the existing display service floor. Existing component stack stays fixed.
 outer=(-2.5,-2.5,82.5,42.5,3);inner=(-.7,-.7,80.7,40.7,1.2)
 ring(base,-11.8,11.8,outer,inner,'Rear battery compartment extension',F.JoinFeatureOperation)
 ears=[(-5,4),(-5,36),(85,4),(85,36)]
 for j,(x,y) in enumerate(ears):
  box(base,-5 if x<0 else 80.6,y-3.4,-11.8,4.4,6.8,36.8,'External screw boss bridge '+str(j+1),F.JoinFeatureOperation)
  cyl(base,x,y,-11.8,3.4,36.8,'External screw boss '+str(j+1),F.JoinFeatureOperation)
  cyl(base,x,y,16.5,1.3,8.6,'Front M3 blind pilot '+str(j+1),F.CutFeatureOperation)
  cyl(base,x,y,-11.9,1.3,8.6,'Rear M3 blind pilot '+str(j+1),F.CutFeatureOperation)
 # Recess-free rear access: battery lifts straight out after taking off the back lid.
 # A rounded end stop locates the 50 mm length; existing walls locate the 40 mm width.
 for x in (6,58.8):box(base,x,-.7,-11.8,1.2,41.4,1.8,'Battery end locator',F.JoinFeatureOperation)
 # Open wire corridor above the battery stop, to the original controller compartment.
 box(base,58.2,15,-.1,6,10,2.6,'Battery lead passage to Heltec',F.CutFeatureOperation,r=.5)
 front=comp(root,'02 Flat front lid - Rev B');rear=comp(root,'03 Rear battery lid - Rev B')
 for c,z,lipz,title in [(front,25,23,'Front'),(rear,-14.2,-11.8,'Rear')]:
  box(c,-4,-4,z,88,48,2.4,title+' flat plate',r=4.5)
  ring(c,lipz,2,(-4,-4,84,44,4.5),(-2.8,-2.8,82.8,42.8,3.3),title+' locating collar 0.30 mm per side',F.JoinFeatureOperation)
  # Side interruptions clear the external bosses; remaining collar registers all four sides.
  for x in (-8.5,82.5):
   for y in (.3,32.3):box(c,x,y,lipz-.01,6,7.4,2.02,title+' collar boss relief',F.CutFeatureOperation)
  for j,(x,y) in enumerate(ears):
   cyl(c,x,y,z,3.4,2.4,title+' screw ear '+str(j+1),F.JoinFeatureOperation)
   cyl(c,x,y,z-.1,1.7,2.6,title+' M3 clearance '+str(j+1),F.CutFeatureOperation)
 # Sensor's nominal optical face is 28.43: 1.03 mm above the flat front face.
 cyl(front,69,20,24.9,5.6,2.6,'Thermal sensor through opening 11.2 mm',F.CutFeatureOperation)
 label(front,'HKU',7,23,48,30,27.4,5,.45,'HKU engraved')
 label(front,'IoT Beyond Lab',7,15,49,22,27.4,3,.45,'IoT Beyond Lab engraved')
 label(front,'THERMAL NODE',7,8,48,12,27.4,1.6,.35,'Thermal node identifier')
 # Rear lid insulation floor is continuous. 0.2 mm loose adhesive/foam allowance.
 batt=box(ref,8,0,-11.6,50,40,8,'804050 LiPo 3.7V 2000mAh nominal envelope',r=.5).bodies.item(0)
 color(d,batt,'Battery silver',174,182,193)
 ant=box(ref,63,6,-9,15,28,8,'LoRa antenna reserved envelope - verify selected antenna',r=.5).bodies.item(0)
 color(d,ant,'Antenna violet',109,80,148)
 for c,n,rgb in [(base,'Rear warm grey',(72,79,88)),(front,'Front porcelain',(224,226,219)),(rear,'Rear lid grey',(100,109,122))]:
  for b in c.bRepBodies:color(d,b,n,*rgb)
 if base.bRepBodies.count>1:
  bs=list(base.bRepBodies);ci=base.features.combineFeatures.createInput(bs[0],oc(bs[1:]));ci.operation=F.JoinFeatureOperation;ci.isKeepToolBodies=False
  base.features.combineFeatures.add(ci).name='Unify revised housing and integral mounting bosses'
 for o in root.occurrences:
  o.isLightBulbOn=True
  for b in o.component.bRepBodies:b.isLightBulbOn=True
 for n,value in [('Battery_length_limit',50),('Battery_width_limit',40),('Battery_thickness_limit',8),('Case_height',41.6),('Sensor_face_height',27.4),('Lid_fit_clearance',.3)]:
  d.userParameters.itemByName(n).expression=str(value)+' mm'
 for c in (base,front,rear,ref):
  c.isOriginFolderLightBulbOn=False
  for s in c.sketches:s.isVisible=False
 root.isOriginFolderLightBulbOn=False
 cam=a.activeViewport.camera;cam.viewOrientation=adsk.core.ViewOrientations.IsoTopRightViewOrientation;cam.isFitView=True;a.activeViewport.camera=cam;a.activeViewport.fit();a.activeViewport.refresh()
 print('Revised',[(o.component.name,o.component.bRepBodies.count) for o in root.occurrences])
