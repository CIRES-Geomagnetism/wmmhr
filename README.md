
## WMMHR Python module
![PyPI - Version](https://img.shields.io/pypi/v/wmmhr)
![PyPI - License](https://img.shields.io/pypi/l/wmmhr)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wmmhr)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wmmhr)

This is a Python implementation of the latest World Magnetic Model High Resolution(WMMHR) by the Cooperative Institute For Research in Environmental Sciences (CIRES), University of Colorado. The software computes all the geomagnetic field components from the WMM model for a specific date and location. 
The World Magnetic Model High Resolution (WMMHR) is an advanced geomagnetic field model that provides a more detailed, accurate depiction of the geomagnetic field than the World Magnetic Model ([WMM](https://www.ncei.noaa.gov/products/world-magnetic-model)). 

**For more information about the WMMHR model, please visit [WMMHR](https://www.ncei.noaa.gov/products/world-magnetic-model-high-resolution)**

## Installation

The recommended way to install wmmhr is via [pip](https://pip.pypa.io/en/stable/)

```
pip install wmmhr 
```


## WMMHR Python API Quick Start

WARNING: Input arrays of length 50,000 datapoints require ~16GB of memory.
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

Get all of the geomagnetic elements

```python
mag_map = model.get_all()
```
It will return 

```python
{'x': array([33828.95752178, 33505.44405357]), 'y': array([2171.53955086, 1932.26765383]), 'z': array([23865.06803054, 26184.61762661]), 'h': array([33898.58331894, 33561.1149921 ]), 'f': array([41456.66922383, 42567.38939334]), 'dec': array([3.67287636, 3.3006066 ]), 'inc': array([35.14607142, 37.96160489]), 'dx': array([ 9.74138229, 14.15269211]), 'dy': array([-3.08678058, -4.24326699]), 'dz': array([39.2944816 , 33.10674659]), 'dh': array([ 9.52363521, 13.88491134]), 'df': array([30.40773033, 31.3122469 ]), 'ddec': array([-0.00626134, -0.00862321]), 'dinc': array([0.03682951, 0.02363721])}
```

### Get the uncertainty value of geomagnetic elements

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

### Description of the components

- **‘dec’ - Declination (deg)** Angle between the horizontal magnetic field vector and true north, positive east, measured in degrees.
- **‘inc’ - Inclination (deg)**: The angle made by the Earth's magnetic field with the horizontal plane, positive down, measured in degrees.
- **‘h’ - H (nT)**: Horizontal intensity of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘x’- X (nT)**: Northward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘y’ - Y (nT)**: Eastward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘z’ - Z (nT)**: Downward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **F (nT)**: Total intensity of the Earth's magnetic field, measured in nanoteslas (nT).
- **ddec/dt (deg/year)**: Rate of change of declination over time, measured in degrees per year.
- **dinc/dt (deg/year)**: Rate of inclination change over time, measured in degrees per year.
- **dh/dt (nT/year)**: Rate of change of horizontal intensity over time, measured in nanoteslas per year.
- **dx/dt (nT/year)**: Rate of change of the northward component over time, measured in nanoteslas per year.
- **dy/dt (nT/year)**: Rate of change of the eastward component over time, measured in nanoteslas per year.
- **dz/dt (nT/year)**: Rate of change of the downward component over time, measured in nanoteslas per year.
- **df/dt (nT/year)**: Rate of change of the total intensity over time, measured in nanoteslas per year.



## WMMHR Python API Reference

### Set up the time and environment for the WMMHR model

#### Set up time 

**setup_time(year**=None, **month**=None, **day**=None, **dyear** = None)

If users don't call or assign any value to setup_time(), the current time will be used to compute the model.
Either by providing year, month, day or decimal year.
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

#### Set up the coordinates

**setup_env(lat**, **lon**, **alt**, **unit**="km", **msl**=True)
```python
from wmmhr import wmmhr_calc
model = wmmhr_calc()
lat, lon, alt = 50.3, 100.4, 0
model.setup_env(lat, lon, alt, unit="m")
```

The default unit and type of altitude is km and mean sea level. 
Assign the parameter for unit and msl, if the latitude is not in km or ellipsoid height.
"m" for meter and "feet" for feet. For example,
```
from wmmhr import wmmhr_calc
model = wmmhr_calc()
model.setup_env(lat, lon, alt, unit="m", msl=True)
```

#### Get the geomagnetic elements

**get_all()**

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

or get single magnetic elements by calling

- `get_Bx()`
- `get_By()`
- `get_Bz()`
- `get_Bh()`
- `get_Bf()`
- `get_Bdec()`
- `get_Binc()`
- `get_dBx()`
- `get_dBy()`
- `get_dBz()`
- `get_dBh()`
- `get_dBf()`
- `get_dBdec()`
- `get_dBinc()`

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

