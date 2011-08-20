#! /usr/bin/python
# Copyright 2008 by Bdale Garbee <bdale@gag.com>.  GPLv2
# Copyright 2011 by Anthony Towns <aj@erisian.com.au>. GPLv2

import math
from rocket_gcode import *

CutterOD = 0.1250       # 1/8" speed cutting bit for most cuts
RingOD = 5.380          # inside diam of BT-5.38 (5.40" outer diam)
RingID = 2.140          # outside diameter of LOC 54mm motor mount tube
CouplerID = 5.202
CouplerDepth = 0.3500

FinCount = 3            # 3 fins
FinWidth = 0.1870       # fin thickness
FinDepth = 0.3500       # this ring is just under 3/4" thick

ClusterCount = 3        # cluster of 3 secondary motors
ClusterOD = 1.220       # outside diam of LOC 29mm mmt
ClusterRotation = 115   # degrees rotation
ClusterSeparation = 2.6 # separaration factor

Zfree = 0.1000          # height in Z to clear all obstructions
Zdepth = 1.000          # depth of plunge (stock plus into tool sweet spot)
Speed = 16              # cutting speed

### AFT CR
gcode = Gcode(output=open("choctop_cr_aft.g","w"), speed=Speed, free=Zfree)

gcode.Zdepth = FinDepth
gcode.fin_slots(FinCount, RingID, RingOD, FinWidth)

gcode.Zdepth = Zdepth
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.ring_cluster(ClusterCount, ClusterOD, ClusterSeparation, ClusterRotation)

gcode.comment("ring outer diameter")
gcode.circle(RingOD + CutterOD)

gcode.close()

### MID CR
gcode = Gcode(output=open("choctop_cr_mid.g","w"), speed=Speed, free=Zfree)

gcode.Zdepth = FinDepth
gcode.fin_slots(FinCount, RingID, RingOD, FinWidth)

gcode.Zdepth = Zdepth
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.ring_cluster(ClusterCount, ClusterOD, ClusterSeparation, ClusterRotation)

gcode.comment("ring outer diameter")
gcode.circle(RingOD + CutterOD)

gcode.close()

### FORWARD CR
gcode = Gcode(output=open("choctop_cr_fwd.g","w"), speed=Speed, free=Zfree)

gcode.Zdepth = Zdepth
gcode.comment("MMT hole")
gcode.circle(RingID - CutterOD)

gcode.comment("coupler outer diameter")
gcode.Zdepth = CouplerDepth
gcode.circle(CouplerID + CutterOD)

gcode.comment("ring outer diameter")
gcode.Zdepth = Zdepth
gcode.circle(RingOD + CutterOD)

gcode.close()

### EBAY BULKHEAD 
gcode = Gcode(output=open("choctop_bh_ebay.g","w"), speed=Speed, free=Zfree)

gcode.Zdepth = Zdepth

gcode.comment("coupler outer diameter")
gcode.Zdepth = CouplerDepth
gcode.circle(CouplerID + CutterOD)

gcode.comment("ring outer diameter")
gcode.Zdepth = Zdepth
gcode.circle(RingOD + CutterOD)

gcode.close()

