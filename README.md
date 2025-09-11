# InstellCa
Exoplanet Instellation Calculator
﻿User Guide

The InstellCa code for computing instellation values is written in Python, and it uses numerical integration techniques from the scientific python(SciPy) library. It reads the required input from the observational data available at the Extrasolar planet encyclopedia or the NASA exoplanet archive. As an output, it generates a curve of Instellation vs. sub-stellar longitude in addition to the curve for the standard point-size approximation of the star to enable the user to compare the difference between the two approaches.


    • The code needs multiple parameters to run. It reads these parameters from catalogue files available at either NASA Exoplanet archive or Exoplanet.eu. The user needs to download the current Exoplanet data from these databases in a csv format. For NASA archive, the data should be downloaded for all columns.
    • The InstellCa package consists of the Python code, user guide, exoplanet observational data and limb darkening data. The downloaded csv file should be saved in the exoplanet catalog sub-directory of InstellCa package.
    • The code can be run for multiple exoplanets depending on the user input.
    • The code asks the user for a choice between manual entry of parameters or to read from exoplanet.eu or NASA archive. 
    • Subsequently, the code asks the user to input the name of the exoplanet. The user should carefully mention the name exactly as mentioned in the catalog file with attention to case sensitivity.
    • The code needs three crucial parameters to run: semi-major axis, stellar radius, stellar effective temperature. If either of these is missing in the catalog the code stops and displays the warning message "Crucial parameter missing". In this case, the user should manually input the missing parameters.
    • If the planetary radius, stellar mass or metallicity is missing in the catalog data, the code specifically asks for these. If the eccentricity is missing, the code assumes a circular orbit. 
    • In case the user needs to enter a different value for one or two parameters but does not want to input all the other values, the code gives an option to change one or two values. For changing one of the values the input is as follows:
      Stellar radius:1
      planetary radius:2
      effective temperature:3
      semi-major axis:4
      
    • For changing two values the user needs to feed the following input:
       Stellar radius, planetary radius:12
      Stellar radius, effective temperature:13
      Stellar radius, semi-major axis:14
      planetary radius, effective temperature:23
      planetary radius, semi-major axis:24
      effective temperature, semi-major axis:34
      
    • For highly eccentric orbits(e>0.3) the code computes an annual mean of instellation over one complete orbit.
    • As an output, the code generates a plot of Instellation vs. latitude and saves it according to a user-defined filename. 

