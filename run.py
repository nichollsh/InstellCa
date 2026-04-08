#!/usr/bin/env python3
"""
Simplified InstellCa run script with hardcoded parameters
No user input required - edit the parameters in the code below
"""

import math
import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np

Rearth = 6.371e6  # m
Rjup = 11.2 * Rearth  # m
Rsun = 6.955e8  # m
AU = 1.496e11  # m

# ============================================================================
# CUSTOM PLANET/STAR PARAMETERS - EDIT THESE VALUES
# ============================================================================

rp1 = 1.0                       # Planet radius in Earth radii
rs1 = 1.0                        # Stellar radius in solar radii
fa1 = 5778                       # Effective temperature of star in Kelvin
al1 = 0.01                        # Semi-major axis in AU
ecc = 0.1                        # Orbital eccentricity (0-1)
M1  = 0.78                         # Stellar mass in solar masses

# Limb darkening parameter (para=1 uses u=0.6)
para = 1
u = 0.6

# ============================================================================
# CALCULATION AND PLOTTING
# ============================================================================

print(f"Calculating irradiance...")
print(f"Parameters: Rp={rp1} Re, Rs={rs1} Rsun, Teff={fa1} K, a={al1} AU, e={ecc}")

# Setup figure
fig = plt.figure(figsize=(12, 10), constrained_layout=False)

newa = []
obli = 0

# Handle eccentricity
number = 1
true1 = np.linspace(0, 270, number)

average = []
inverse = []

for j in range(0, number):
    # Orbital and physical parameters
    true = true1[j] * np.pi / 180
    ob1 = float(obli)
    ob = ob1 * np.pi / 180
    
    M = M1 * 2 * 10**(30)
    rs = rs1 * Rsun
    rp = rp1 * Rearth
    al2 = al1 * AU
    al = al2 * (1 - ecc**2) / (1 + ecc * abs(math.cos(true)))
    d = al - rs - rp
    ch = math.acos(rp / (d + rp))
    s3 = (math.asin(abs(rs - rp) / al))
    s1 = (np.pi / 2 + s3)
    s1 = math.floor(s1 * 180 / np.pi)
    s1 = s1 * np.pi / 180
    s = np.pi / 2
    symp = math.acos((rs + rp) / al)
    la1 = np.linspace(-s1, s1, 500)
    la2 = np.linspace((-s1 + ob) * 180 / np.pi, (s1 - ob) * 180 / np.pi, 500)
    surfgrav = 100 * 6.67 * 10**(-11) * M / rs**(2)
    logg = math.log10(surfgrav)
    oldfor = []
    final = []
    
    # Limb Darkening
    if para == 1 and u == 0.6:
        fa = fa1 * 1.0573
    elif para == 1 and u == 0:
        fa = fa1
    else:
        fa = fa1
        
    P = 5.67 * 10**(-8) * fa**(4) * 4 * np.pi * rs**2
    
    for k in range(len(la1)):
        la = la1[k]
        beta = al + rp * math.cos(np.pi - la)
        y1 = math.acos((rs**2 - rp**2 * (math.sin(la))**2) / (beta * rs - rp * math.sin(la) * (math.sqrt(rp**2 * (math.sin(la))**2 - rs**2 + beta**2)))) * 180 / np.pi
        y4 = math.acos((rs**2 - rp**2 * (math.sin(la))**2) / (beta * rs + rp * math.sin(la) * (math.sqrt(rp**2 * (math.sin(la))**2 - rs**2 + beta**2)))) * 180 / np.pi
        y5 = math.acos(rs / math.sqrt(al**2 + rp**2 - 2 * al * rp * math.cos(la))) * 180 / np.pi
        y6 = math.acos((rs + rp * abs(math.sin(la))) / al)
        y = (y1) * np.pi / 180
        y2 = (y4) * np.pi / 180
        y3 = (y5) * np.pi / 180
        y7 = math.acos(rs / al)
        y = y7
        ad1 = 180 * math.atan(rs * math.sin(y) / (d + rs - (rs * math.cos(y)))) / np.pi
        ad = math.floor(ad1) * np.pi / 180
        vis = math.acos(rs / (math.sqrt(al**2 + rp**2 - 2 * al * rp * math.cos(la))))
        P1 = 5.67 * 10**(-8) * fa1**(4) * 4 * np.pi * (rs)**2
        
        y2 = y6
        
        # General integral function
        def function(x, th, la):
            a = -rs * math.sin(th) * math.cos(th) * math.sin(np.pi - la) + al * math.cos(np.pi - la) * math.cos(th) + rp * math.cos(th)
            b = rs * math.cos(np.pi - la) * (math.cos(th))**2
            c = rs**2 + al**2 + rp**2 - 2 * rs * rp * math.sin(th) * math.sin(la) + 2 * al * rp * math.cos(np.pi - la)
            e = -2 * (al + rp * math.cos(np.pi - la)) * rs * math.cos(th)
            mu = abs(-rs + (al + rp * math.cos(np.pi - la)) * math.cos(th) * math.cos(x) + rp * math.sin(th) * math.sin(la)) / (c + e * math.cos(x))**(1 / 2)
            if para == 1:
                lf = 1 - u * (1 - mu)
            else:
                lf = 1
            return abs(a - b * math.cos(x)) * lf * mu / (c + e * math.cos(x))**(3 / 2)
        
        def integration(th, la):
            return quad(function, -y3, y3, args=(th, la))[0]
        
        # Geometric Limits
        if la > 0 and abs(la) < symp:
            ll = -math.acos((rs * (al - rp * math.cos(la)) + rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
            ul = math.acos((rs * (al - rp * math.cos(la)) - rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
        
        if la < 0 and abs(la) < symp:
            ll = -math.acos((rs * (al - rp * math.cos(la)) + rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
            ul = math.acos((rs * (al - rp * math.cos(la)) - rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
        
        if abs(la) >= symp and la > 0:
            ll = -la + math.acos((al * math.cos(la) - rp) / rs)
            ul = math.acos((rs * (al - rp * math.cos(la)) - rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
        
        if abs(la) >= symp and la < 0:
            ul = -la - math.acos((al * math.cos(la) - rp) / rs)
            ll = -math.acos((rs * (al - rp * math.cos(la)) + rp * math.sin(la) * np.sqrt(al**2 + rp**2 - rs**2 - 2 * al * rp * math.cos(la))) / (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
        
        if la == 0:
            ll = math.acos(rs / (al - rp))
            ul = math.acos(rs / (al - rp))
        
        # Second integral
        value = quad(lambda th: integration(th, la), ll, ul)[0]
        la5 = math.atan(al * math.tan(la) * math.cos(la) / (al * math.cos(la) - rp))
        if la5 < 0:
            newp = la
            newa.append(newp)
        
        value2 = value * P / (4 * np.pi * np.pi)
        final.append(value2 / 1000)
        
        old = P1 * math.cos(la5) / (4 * np.pi * (al**2 + rp**2 - 2 * al * rp * math.cos(la)))
        if la > 0 and la5 < 0:
            old = 0
        if la < 0 and la5 > 0:
            old = 0
        oldfor.append(old / 1000)
    
    inverse.append(oldfor)
    average.append(final)
    aver = np.asarray(average)
    inve = np.asarray(inverse)
    inve1 = np.mean(inve, axis=0)
    aver1 = np.mean(aver, axis=0)

# Plot results
maxlatitude = s1 * 57.3
if newa:
    minlatitude = newa[0] * 57.3
tickarray2 = np.array([-150, -130, -110, -90, -70, -50, -30, -10, 10, 30, 50, 70, 90, 110, 130, 150])

plt.plot(la2, aver1, 'b-', label="Geometric Model")
plt.plot(la2, inve1, 'r--', label="Inverse-square law")
plt.xticks(tickarray2, fontsize=14)
plt.yticks(fontsize=14)
plt.axvline(x=maxlatitude, color='gray', linestyle='--', label='Terminator limit')
plt.axvline(x=-maxlatitude, color='gray', linestyle='--')
plt.axvline(x=symp * 57.3, color='gray', linestyle='dashdot', label='Critical point of symmetry')
plt.axvline(x=-symp * 57.3, color='gray', linestyle='dashdot')
plt.title(f"a= {al1:.4f} AU, Rs={rs1:.2f} Rsun, Teff={fa1:.0f} K, Rp={rp1:.2f} Re", fontsize=16)
plt.xlabel("Latitude (degrees)", fontsize=16)
plt.ylabel("Irradiance (kW/m^2)", fontsize=16)
plt.legend(fontsize=14)
plt.xlim(-130, 130)

# Save plot
imagename = f"nogit_irradiance_plot.pdf"
plt.savefig(imagename, dpi=300, bbox_inches='tight')
print(f"Plot saved as: {imagename}")
print(f"The Terminator extends to {round(s1 * 57.3, 3)} degrees from the equator")
