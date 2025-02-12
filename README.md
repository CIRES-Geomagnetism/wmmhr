## Create the environment for developing WMMHR Python module

This is a Python implementation of the latest World Magnetic Model High Resolution(WMMHR) by the Cooperative Institute For Research in Environmental Sciences (CIRES), University of Colorado. The software computes all the geomagnetic field components from the WMM model for a specific date and location. 
For more information about the WMMHR model, please visit [WMM](https://www.ncei.noaa.gov/products/world-magnetic-model)


## WMMHR Python API Quick Start

Set up the time and latitude and longtitude and altitude for the WMMHR model

```python
from wmmhr import wmmhr_calc

model = wmmhr_calc()
lat, lon, alt = 23.35, 40, 21.0

model.setup_time(2025, 1, 1)

model.setup_env(lat, lon, alt)
```

Get all of the geomagnetic elements

```python
mag_map = model.get_all()
```
It will return 

```python
{'x': 33819.7801070038, 'y': 2174.3912147114625, 'z': 23828.47071514917, 'h': 33889.60760529257, 'f': 41428.26957843431, 'dec': 3.6786815949671756, 'inc': 35.11183058537514, 
  'dx': 9.741359695584915, 'dy': -3.0866861263666308, 'dz': 39.29435224005461, 'dh': 9.523243332028592, 'df': 30.391404567147962, 'ddec': -0.3758682095492924, 'dinc': 2.2128026143134507}
```

### Get the uncertainty value of geomagnetic elements

```python
import wmmhr
print(wmmhr.uncertainty)
```

```python
{'X': 134, 'Y': 85, 'Z': 133, 'F': 133, 'H': 130, 'I': 0.19, 'D_OFFSET': 0.25, 'D_COEF': 5199}
```

### Description of the components

- **‘Dec’ - Declination (deg)** Angle between the horizontal magnetic field vector and true north, positive east, measured in degrees.
- **‘Inc’ - Inclination (deg)**: The angle made by the Earth's magnetic field with the horizontal plane, positive down, measured in degrees.
- **‘h’ - H (nT)**: Horizontal intensity of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘x’- X (nT)**: Northward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘y’ - Y (nT)**: Eastward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **‘z’ - Z (nT)**: Downward component of the Earth's magnetic field, measured in nanoteslas (nT).
- **F (nT)**: Total intensity of the Earth's magnetic field, measured in nanoteslas (nT).
- **dD/dt (deg/year)**: Rate of change of declination over time, measured in degrees per year.
- **dI/dt (deg/year)**: Rate of inclination change over time, measured in degrees per year.
- **dH/dt (nT/year)**: Rate of change of horizontal intensity over time, measured in nanoteslas per year.
- **dX/dt (nT/year)**: Rate of change of the northward component over time, measured in nanoteslas per year.
- **dY/dt (nT/year)**: Rate of change of the eastward component over time, measured in nanoteslas per year.
- **dZ/dt (nT/year)**: Rate of change of the downward component over time, measured in nanoteslas per year.
- **dF/dt (nT/year)**: Rate of change of the total intensity over time, measured in nanoteslas per year.



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
model = wmmhr_calc()
model.setup_time(dyear=2025.1)
```

User allow to assign the date from "2024-12-17" to "2030-01-01"

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
model.setup_env(lat, lon, alt, unit="m", msl=True)
```

#### Get the geomagnetic elements

After setting up the time and coordinates for the WMMHR model, you can get all the geomagnetic elements by

```
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
Bh = model.get_Bh()
```

