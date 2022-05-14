import numpy as np
import pandas as pd
import math

def angle_two_vectors(seg0,seg1):
    #normalise
    seg0norm = (seg0)/np.linalg.norm(seg0)
    seg1norm = (seg1)/np.linalg.norm(seg1)
    #dot product 
    cos = np.dot(seg0norm,seg1norm)
    #cos to norm
    angle = math.acos(cos)/math.pi
    #return angle
    return angle