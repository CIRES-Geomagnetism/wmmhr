
## WMMHR Python module
![PyPI - Version](https://img.shields.io/pypi/v/wmmhr)
![PyPI - License](https://img.shields.io/pypi/l/wmmhr)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wmmhr)
[![PyPI Downloads](https://static.pepy.tech/badge/wmmhr/month)](https://pepy.tech/projects/wmmhr)
[![PyPI Downloads](https://static.pepy.tech/badge/wmmhr)](https://pepy.tech/projects/wmmhr)


This is a Python implementation of the latest World Magnetic Model High Resolution(WMMHR) by the Cooperative Institute For Research in Environmental Sciences (CIRES), University of Colorado. The software computes all the geomagnetic field components from the WMM model for a specific date and location. 
The World Magnetic Model High Resolution (WMMHR) is an advanced geomagnetic field model that provides a more detailed, accurate depiction of the geomagnetic field than the World Magnetic Model ([WMM](https://www.ncei.noaa.gov/products/world-magnetic-model)). 

WMMHR2025 includes core field and secular variation coefficients for degrees n = 1 to 15. This model also covers the crustal field (from n=16 through n=133).  As a result, it has more coefficients (18,210 non-zero coefficients instead of 336) and more digits (4 instead of 1) in each coefficient.

**For more information about the WMMHR model, please visit [WMMHR](https://www.ncei.noaa.gov/products/world-magnetic-model-high-resolution)** website.

## Table of contents
- [Installation](#installation)
- [Outputs](#Output)
- [WMMHR Python API Quick Start](#WMMHR-Python-API-Quick-Start)
- <details> <summary><a href="#WMMHR-Python-API-Reference">WMMHR Python API Reference</a></summary>
  <ul>
  <li><a href="#1-change-the-resolutionmax-degree-of-the-model">wmm_calc(nmax=12)</a></li>
  <li><a href="#2-set-up-time">wmm_calc.setup_time</a></li>
  <li><a href="#3-set-up-the-coordinates">wmm_calc.setup_env</a></li>
  <li><a href="#5-get-uncertainty-value">wmm_calc.get_uncertainty</a></li>
  
  <li><details><summary><a href="#4-get-the-geomagnetic-elements">Get magnetic elements </a></summary>
      <nav>
     <ul>
     <li><a href="#get_all">wmm_calc.get_all() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Bx() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_By() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Bz() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Bh() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Bf() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Bdec() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_Binc() </a></li>
    
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBx() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBy() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBz() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBh() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBf() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBdec() </a></li>
     <li><a href="#get-single-magnetic-elements-by-calling-">wmmhr_calc.get_dBinc() </a></li>
    </ul>
  </ul>
  </nav>
  </details></li>
  </details>
- [Contacts and contributing to WMMHR](#contacts-and-contributing-to-wmmhr)

## Installation

The recommended way to install wmmhr is via [pip](https://pip.pypa.io/en/stable/)

```
pip install wmmhr 
```
## Outputs

It will output the magnetic components and uncertainty values. To get the detail of the outputs, please see **[Description of the WMM magnetic components](https://github.com/CIRES-Geomagnetism/wmm/blob/check_nmax/description.md)**


## WMMHR Python API Quick Start

**WARNING:** Input arrays of length 50,000 datapoints require ~16GB of memory.
Users may input scalars, vectors, and combinations thereof. However, all input vectors must have the same length. 

```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
lat = [23.35, 24.5]
lon = [40, 45]
alt = [21, 21]

year = [2025, 2026]
month = [12, 1]
day = [6, 15]

# set up time
model.setup_time(year, month, day)
# set up the coordinates
model.setup_env(lat, lon, alt)
```

Get all the geomagnetic elements

```python
mag_map = model.get_all()
```
It will return 

```python
{'x': array([33828.95752178, 33505.44405357]), 'y': array([2171.53955086, 1932.26765383]), 'z': array([23865.06803054, 26184.61762661]), 'h': array([33898.58331894, 33561.1149921 ]), 'f': array([41456.66922383, 42567.38939334]), 'dec': array([3.67287636, 3.3006066 ]), 'inc': array([35.14607142, 37.96160489]), 'dx': array([ 9.74138229, 14.15269211]), 'dy': array([-3.08678058, -4.24326699]), 'dz': array([39.2944816 , 33.10674659]), 'dh': array([ 9.52363521, 13.88491134]), 'df': array([30.40773033, 31.3122469 ]), 'ddec': array([-0.00626134, -0.00862321]), 'dinc': array([0.03682951, 0.02363721])}
```

## WMMHR Python API Reference

### 1. Change the resolution(max degree) of the model

**wmmhr_calc(nmax=133)**

The default maximum degree for WMMHR is 133. Users allow to assign the max degree from 1 to 133 to WMMHR Python API.
```python
from wmm import wmm_calc
model = wmm_calc(nmax=100)
```

### 2. Set up time 

**setup_time(year**=None, **month**=None, **day**=None, **dyear** = None)


User can set up the time either by providing year, month, day or decimal year.
If users don't call or assign any value to `setup_time()`, the current time will be used to compute the model.

For example, 
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
model.setup_time(2024, 12, 30)
```
or 
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
model.setup_time(dyear=2025.1)
```

User allow to assign the date from "2024-11-13" to "2030-01-01"

### 3. Set up the coordinates

**setup_env(lat**, **lon**, **alt**, **unit**="km", **msl**=True)
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
lat, lon, alt = 50.3, 100.4, 0
model.setup_env(lat, lon, alt, unit="m")
```

The default unit and type of altitude is kilometer(km) and mean sea level. 
Assign the parameter for unit and msl, if the latitude is not in km or ellipsoid height.
`m` for meter and `feet` for feet. 

For example,
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
model.setup_env(lat, lon, alt, unit="m", msl=True)
```

### 4. Get the geomagnetic elements

##### wmmhr_calc.get_all()

After setting up the time and coordinates for the WMMHR model, you can get all the geomagnetic elements by

```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
lat, lon, alt = 50.3, 100.4, 0
year, month, day = 2025, 3, 30
model.setup_env(lat, lon, alt, unit="m", msl=True)
model.setup_time(year, month, day)
mag_map = model.get_all()
```

which will return all magnetic elements in dict type.

##### Get single magnetic elements by calling 
<details>
<summary>Click to see the available functions to get single elements</summary>
<p> <b>wmmhr_calc.get_Bx()</b>
  <li>Northward component of the Earth's magnetic field, measured in nanoteslas (nT). </li>
</p>

<p> <b>wmmhr_calc.get_By()</b>
  <li>Eastward component of the Earth's magnetic field, measured in nanoteslas (nT). </li>
</p>
<p><b>wmmhr_calc.get_Bz()</b>
<li>Downward component of the Earth's magnetic field, measured in nanoteslas (nT). </li>
</p>
<p><b>wmmhr_calc.get_Bh()</b>
<li>Horizontal intensity of the Earth's magnetic field, measured in nanoteslas (nT).</li>
</p>
<p><b>wmmhr_calc.get_Bf()</b>
<li>Total intensity of the Earth's magnetic field, measured in nanoteslas (nT).</li>
</p>
<p><b>wmmhr_calc.get_Bdec()</b>
<li>Rate of change of declination over time, measured in degrees per year.</li>
</p>
<p><b>wmmhr_calc.get_Binc()</b>
<li>Rate of inclination change over time, measured in degrees per year.</li>
</p>
<p><b>wmmhr_calc.get_dBx()</b>
<li>Rate of change of the northward component over time, measured in nanoteslas per year.</li>
</p>
<p><b>wmmhr_calc.get_dBy()</b>
<li>Rate of change of the eastward component over time, measured in nanoteslas per year.</li>
</p>
<p><b>wmmhr_calc.get_dBz()</b>
<li>Rate of change of the downward component over time, measured in nanoteslas per year.</li>
</p>
<p><b>wmmhr_calc.get_dBh()</b>
<li>Rate of change of horizontal intensity over time, measured in nanoteslas per year.</li>
</p>
<p><b>wmmhr_calc.get_dBf()</b>
<li>Rate of change of the total intensity over time, measured in nanoteslas per year.</li>
</p>
<p><b>wmmhr_calc.get_dBdec()</b>
<li>Rate of change of declination over time, measured in degrees per year.</li>
</p>
<p><b>wmmhr_calc.get_dBinc()</b>
<li>Rate of inclination change over time, measured in degrees per year.</li>
</p>
</details>


for example,
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
from wmmhr import wmmhr_calc
model = wmmhr_calc()
lat, lon, alt = 50.3, 100.4, 0
year, month, day = 2025, 3, 30
model.setup_env(lat, lon, alt, unit="m", msl=True)
model.setup_time(year, month, day)
Bh = model.get_Bh()
```
### 5. Get uncertainty value

**wmmhr_calc.get_uncertainty()**

The WMMHR Python API includes an error model that providing uncertainty estimates for every geomagnetic element (X, Y, Z, H, F, I and D) and every location at Earth's surface. 
<details>
<summary>Click here to see the description of the outputs for <b>wmmhr_calc.get_uncertainty()</b></summary>
<li><b>x_uncertainty: </b> WMMHR 1-sigma uncertainty in the northward component of the Earth's magnetic field, measured in nanoteslas (nT)</li>
<li><b>y_uncertainty: </b>WMMHR 1-sigma uncertainty in the eastward component of the Earth's magnetic field, measured in nanoteslas (nT)</li>
<li><b>z_uncertainty: </b>WMMHR 1-sigma uncertainty in the downward component of the Earth's magnetic field, measured in nanoteslas (nT)</li>
<li><b>h_uncertainty: </b>WMMHR 1-sigma uncertainty in the horizontal intensity of the Earth's magnetic field, measured in nanoteslas (nT)</li>
<li><b>f_uncertainty: </b>WMMHR 1-sigma uncertainty in the total intensity of the Earth's magnetic field, measured in nanoteslas (nT)</li>
<li><b>dec_uncertainty: </b>WMMHR 1-sigma uncertainty in the declination, measured in degrees.</li>
<li><b>inc_uncertainty: </b>WMMHR 1-sigma uncertainty in the inclination, measured in degrees.</li>
</details>

For more information about the error model, please visit [World Magnetic Model Accuracy, Limitations, and Error Model](https://www.ncei.noaa.gov/products/world-magnetic-model/accuracy-limitations-error-model)

```python
from wmmhr import wmmhr_calc

model = wmmhr_calc()

lat = [23.35, 24.5]
lon = [40, 45]
alt = [21, 21]

year = [2025, 2026]
month = [12, 1]
day = [6, 15]

# set up time
model.setup_time(year, month, day)
# set up the coordinates
model.setup_env(lat, lon, alt)
# get the uncertainty value
print(model.get_uncertainty())
```

```python
{'x_uncertainty': 135, 'y_uncertainty': 85, 'z_uncertainty': 134, 'h_uncertainty': 130, 'f_uncertainty': 134, 'declination_uncertainty': array([7.37493947e-06, 7.44909697e-06]), 'inclination_uncertainty': 0.19}
```

### Contacts and contributing to WMMHR:
If you have any questions, please email `geomag.models@noaa.gov`, submit issue or pull request at [https://github.com/CIRES-Geomagnetism/wmmhr](https://github.com/CIRES-Geomagnetism/wmmhr).
