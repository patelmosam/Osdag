import numpy
from cad.items.ModelUtils import *
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
#from notch import Notch
from cad.items.plate import Plate
from cad.items.ISection import ISection

class IsectionCoverPlate(object):

    def __init__(self, D, B, T, t, s, l, t1, H):
        self.B = B
        self.T = T
        self.D = D
        self.t = t
        self.l = l
        self.s = s
        self.t1 = t1
        self.H = H

        self.Isection1 = ISection(B, T, D, t, 0, 0, 0, H, None)
        self.Isection2 = ISection(B, T, D, t, 0, 0, 0, H, None)
        self.Plate1 = Plate(t1, H, l)
        self.Plate2 = Plate(t1, H, l)
        
    def place(self, sec_origin, uDir, wDir):
        self.sec_origin = sec_origin
        self.uDir = uDir
        self.wDir = wDir
        
        origin = numpy.array([-self.s/2.,0.,0.])
        self.Isection1.place(origin, self.uDir, self.wDir)
        origin1 = numpy.array([self.s/2.,0.,0.])
        self.Isection2.place(origin1, self.uDir, self.wDir)
        origin2 = numpy.array([0.,(self.D+self.t1)/2,0.])
        self.Plate1.place(origin2, self.uDir, self.wDir)
        origin3 = numpy.array([0.,-(self.D+self.t1)/2,0.])
        self.Plate2.place(origin3, self.uDir, self.wDir)
        #self.compute_params()

    def compute_params():
        self.Isection1.compute_params()
        self.Isection2.compute_params()
        self.Plate1.compute_params()
        self.Plate2.compute_params()

    def create_model(self):
        
        prism1 = self.Isection1.create_model()
        prism2 = self.Isection2.create_model()

        prism3 = self.Plate1.create_model()
        prism4 = self.Plate2.create_model()
        
        prism = BRepAlgoAPI_Fuse(prism1, prism2).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism3).Shape()
        prism = BRepAlgoAPI_Fuse(prism, prism4).Shape()
        return prism

if __name__ == '__main__':

    from OCC.Display.SimpleGui import init_display
    display, start_display, add_menu, add_function_to_menu = init_display()

    B = 40
    T = 3
    D = 40
    t = 3
    s = 50
    l = B + s
    t2 = 3
    H = 50
    
    ISecPlate = IsectionCoverPlate(D, B, T, t, s, l, t2, H)

    origin = numpy.array([0.,0.,0.])
    uDir = numpy.array([1.,0.,0.])
    shaftDir = numpy.array([0.,0.,1.])

    ISecPlate.place(origin, uDir, shaftDir)
    prism = ISecPlate.create_model()
    display.DisplayShape(prism, update=True)
    display.DisableAntiAliasing()
    start_display()