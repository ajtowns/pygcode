#! /usr/bin/python
# Copyright 2008 by Bdale Garbee <bdale@gag.com>.  GPLv2
# Copyright 2011 by Anthony Towns <aj@erisian.com.au>. GPLv2

# This is a Python library to emit g-code for a MaxNC-10 milling machine 
# with upgraded "trim router" spindle to cut motor mount centering rings
# or bulkheads for a model rocket.
#
# Z reference plane is top surface of stock, X/Y origin is center of ring

import math
import sys

def mm2inch(mm):
    return mm/25.4

def polar2xy(radius, degrees = None, radians = None):
    if degrees is not None:
        radians = degrees / 180.0 * math.pi
    x = radius * math.cos(radians)
    y = radius * math.sin(radians)
    return x,y

class Gcode(object):
    def __init__(self, output = sys.stdout, 
                 free = 0.1, depth = 1.0, cutter = 0.125, 
                 speed = 8):
        self.Zfree = free
        self.Zdepth = depth
        self.Speed = speed
        self.CutterOD = cutter
        self.output = output

        self.write("%")
        self.origin()

    def comment(self, comment):
        self.output.write("\n(%s)\n" % (comment))

    def close(self):
        self.write("%")
        self.output.close()

    def write(self, gcode):
        self.output.write(gcode + "\n")

    def plunge(self):
        self.write("(plunge)")
        self.write("G01 Z %.2f F%d" % (-self.Zdepth, self.Speed))
        
    def retract(self, depth=None, speed=None):
        self.write("(retract)")
        self.write("G01 Z %.2f F%d" % (self.Zfree, self.Speed))

    def origin(self):
        self.retract()
        self.write("(origin)")
        self.write("G00 X0 Y0")

    def circle(self, diameter, x=0, y=0):
        radius = diameter/2.0
        self.write("G00 X %6.4f Y %6.4f" % (x, y + radius))
        self.plunge()
        self.write("G02 X %6.4f Y %6.4f I %6.4f J %6.4f F%d" % (
            x, y - radius, 0, -radius, self.Speed))
        self.write("G02 X %6.4f Y %6.4f I %6.4f J %6.4f F%d" % (
            x, y + radius, 0, +radius, self.Speed))
        self.retract()

    def slot(self, startX, startY, endX, endY, width):
        deltaX = endX - startX
        deltaY = endY - startY
        length = (deltaX**2 + deltaY**2)**0.5
        offX = -deltaY / length  # unit vector, 90 degrees to slot
        offY = deltaX / length 

        width += 0.0

        if width < self.CutterOD:
            self.comment("***desired slot width smaller than cutter***")
            runs = 1
            step = 0
        elif width == self.CutterOD:
            runs = 1
            step = 0
        else:
            runs = int(math.ceil((width)/self.CutterOD))
            startX += offX * (width-self.CutterOD)/2
            startY += offY * (width-self.CutterOD)/2
            endX += offX * (width-self.CutterOD)/2
            endY += offY * (width-self.CutterOD)/2
            step = (width-self.CutterOD)/(runs-1)

        self.write("G00 X%6.4f Y%6.4f" % (startX, startY))

        self.plunge()
        for n in range(runs-1):
            self.write("G01 X%6.4f Y%6.4f F%d" % (endX, endY, self.Speed))
            startX, endX = endX - offX * step, startX - offX * step
            startY, endY = endY - offY * step, startY - offY * step
            self.write("G01 X%6.4f Y%6.4f F%d" % (startX, startY, self.Speed))

        self.write("G01 X%6.4f Y%6.4f F%d" % (endX, endY, self.Speed))
        self.retract() 

    def fin_slots(self, FinCount, innerD, outerD, width, rotate = 0):
        for fin in range(FinCount):
            self.comment("fin slot %d" % (fin))

            FinDegrees = 90 + rotate + 360.0 / FinCount * fin
            while FinDegrees > 360: FinDegrees -= 360
            # angle from origin (on y-axis)

            FinSlotInX, FinSlotInY = polar2xy((innerD-self.CutterOD)/2.0, 
                                              degrees=FinDegrees)
            FinSlotOutX, FinSlotOutY = polar2xy((outerD+self.CutterOD)/2.0, 
                                              degrees=FinDegrees)
    
            self.slot(FinSlotInX, FinSlotInY, FinSlotOutX, FinSlotOutY, width)

    def ring_cluster(self, count, diam, sep = 1.0, rotation = 0):
        base_dist = diam/2.0 / math.sin(math.pi/count)

        for cluster in range(count):
            self.comment("cluster MMT hole %d" % (cluster))

            degrees = rotation + cluster*360.0/count
            while degrees > 360: degrees -= 360

            ClusX, ClusY = polar2xy(base_dist * sep, degrees=degrees)
            self.circle(diam - self.CutterOD, x=ClusX, y=ClusY)

