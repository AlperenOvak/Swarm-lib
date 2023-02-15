#!/usr/bin/env python3
import numpy as np
import time
from artificial_potential_field import ArtificialPotentialField

apf = ArtificialPotentialField()
#apf.form_3d(1, 3)



apf.form_3d(2.0, 4,1.0)
time.sleep(1)
apf.go([0,0,0])
apf.rotate(120)