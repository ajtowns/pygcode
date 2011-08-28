#! /usr/bin/python
# Copyright 2008 by Bdale Garbee <bdale@gag.com>.  GPLv2
# Copyright 2011 by Anthony Towns <aj@erisian.com.au>. GPLv2

import math
from rocket_gcode import *

CutterOD = 0.2500           # 1/8" speed cutting bit for most cuts
RingOD = mm2inch(135)       # inside diam of BT-5.38 (5.40" outer diam)
RingID = mm2inch(57.5)      # outside diameter of LOC 54mm motor mount tube
CouplerID = mm2inch(131.5)  # was 5.202"
CouplerDepth = 0.3500

FinCount = 3            # 3 fins
FinWidth = 0.2500       # fin thickness
FinDepth = 0.1750       # depth of guide for fin

ClusterCount = 3        # cluster of 3 secondary motors
ClusterOD = mm2inch(31.25) # outside diam of LOC 29mm mmt
ClusterRotation = 115   # degrees rotation
ClusterSeparation = 2.6 # separaration factor

Zfree = 0.2500          # height in Z to clear all obstructions
Zthrough = 0.500        # depth to cut all the way through
                        # (incl tool sweet spot)

Speed = 10              # cutting speed

### AFT CR
gcode = Gcode(output=open("choctop_cr_aft.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.Zdepth = FinDepth
gcode.fin_slots(FinCount, RingID, RingOD, FinWidth)

gcode.Zdepth = Zthrough
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.ring_cluster(ClusterCount, ClusterOD, ClusterSeparation, ClusterRotation)

gcode.comment("ring outer diameter")
gcode.circle(RingOD + CutterOD)

gcode.close()

### MID CR (lower side)
gcode = Gcode(output=open("choctop_cr_mid_lo.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.Zdepth = FinDepth
gcode.fin_slots(FinCount, RingID, RingOD, FinWidth)

gcode.close()

### MID CR (upper side)
gcode = Gcode(output=open("choctop_cr_mid_up.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.Zdepth = Zthrough
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.ring_cluster(ClusterCount, ClusterOD, ClusterSeparation, ClusterRotation)

gcode.comment("ring outer diameter")
gcode.circle(RingOD + CutterOD)

gcode.close()

### FORWARD CR
gcode = Gcode(output=open("choctop_cr_fwd.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.Zdepth = Zthrough
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.comment("coupler outer diameter")
gcode.Zdepth = CouplerDepth
gcode.circle(CouplerID + CutterOD)

gcode.comment("ring outer diameter")
gcode.Zdepth = Zthrough
gcode.circle(RingOD + CutterOD)

gcode.close()

### FORWARD CR UPPER SIDE DSUB
gcode = Gcode(output=open("choctop_cr_fwd_dsub.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.comment("9 pin dsub")
gcode.Zdepth = Zthrough
gcode.dsub(-5.5/4, 0, 0)

gcode.close()

### EBAY BULKHEAD 
gcode = Gcode(output=open("choctop_bh_ebay.ngc","w"), speed=Speed, free=Zfree, cutter=CutterOD)

gcode.comment("coupler outer diameter")
gcode.Zdepth = CouplerDepth
gcode.circle(CouplerID + CutterOD)

gcode.comment("ring outer diameter")
gcode.Zdepth = Zthrough
gcode.circle(RingOD + CutterOD)

gcode.close()

