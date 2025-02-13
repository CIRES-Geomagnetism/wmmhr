import unittest
import warnings

import numpy as np
import os
import datetime as dt
from wmmhr import wmmhr_calc

from geomaglib import util, sh_loader




class Test_wmmhr(unittest.TestCase):

    def setUp(self):

        self.year = np.array([2025, 2026]).astype(int)
        self.month = np.array([12, 1]).astype(int)
        self.day = np.array([6, 15]).astype(int)

        self.dyears = np.array([2025.5, 2026.6])

        self.top_dir = os.path.dirname(os.path.dirname(__file__))
        self.wmm_file = os.path.join(self.top_dir, "wmm", "coefs", "WMMHR.cof")
        self.wmmhr_testval = os.path.join(self.top_dir, "tests", "WMMHR2025_TEST_VALUE_TABLE_FOR_REPORT.txt")
        self.get_wmmhr_testval()

    def get_wmmhr_testval(self):

        self.dyears, self.alts, self.lats, self.lons = [], [], [], []
        self.Bh, self.Bf, self.Bx, self.By, self.Bz, self.Bdec, self.Binc, self.Bgv = [], [], [], [], [], [], [], []
        self.dBh, self.dBf, self.dBx, self.dBy, self.dBz, self.dBdec, self.dBinc = [], [], [], [], [], [], []

        with open(self.wmmhr_testval, "r") as fp:
            for line in fp:
                vals = line.split()

                if vals[0] == "#":
                    continue
                else:
                    for i in range(len(vals)):
                        vals[i] = float(vals[i])
                    dyear, alt, lat, lon = vals[0], vals[1], vals[2], vals[3]
                    x, y, z, h, f, inc, dec, gv = vals[4], vals[5], vals[6], vals[7], vals[8], vals[9], vals[10], vals[11]
                    dx, dy, dz, dh, df, dinc, ddec = vals[12], vals[13], vals[14], vals[15], vals[16], vals[17], vals[18]

                self.dyears.append(dyear)
                self.alts.append(alt)
                self.lats.append(lat)
                self.lons.append(lon)

                self.Bdec.append(dec)
                self.Binc.append(inc)
                self.Bx.append(x)
                self.By.append(y)
                self.Bz.append(z)
                self.Bh.append(h)
                self.Bf.append(f)
                self.Bgv.append(gv)

                self.dBdec.append(ddec)
                self.dBinc.append(dinc)
                self.dBx.append(dx)
                self.dBy.append(dy)
                self.dBz.append(dz)
                self.dBh.append(dh)
                self.dBf.append(df)

    def test_get_coefs_path(self):

        model = wmmhr_calc()
        path = model.get_coefs_path("WMMHR.cof")

        self.assertTrue(os.path.exists(path))

    def test_setup_dtime_arr(self):

        model = wmmhr_calc()


        model.setup_env(self.lats, self.lons, self.alts)
        model.setup_time(dyear=self.dyears)

        for i in range(len(self.dyears)):
            self.assertAlmostEqual(self.dyears[i], model.dyear[i], places=1)



    def test_setup_strdate(self):

        model = wmmhr_calc()
        years = np.array([2025, 2026])
        months = np.array([10, 11]).astype(int)
        days = np.array([1, 2]).astype(int)

        model.setup_env(self.lats, self.lons, self.alts)
        model.setup_time(years, months, days)

        dyears = [2025.7479452054795, 2026.835616438356]

        for i in range(len(years)):
            self.assertAlmostEqual(dyears[i], model.dyear[i], places=6)


    def test_setup_empty_time(self):

        model = wmmhr_calc()
        # model.setup_time()

        model.setup_time()

        model.setup_env(self.lats, self.lons, self.alts)

        model.get_all()
        curr_time = dt.datetime.now()
        year = curr_time.year
        month = curr_time.month
        day = curr_time.day

        dyear = util.calc_dec_year(year, month, day)

        self.assertEqual(dyear, model.dyear)

    def test_broadcast(self):

        model = wmmhr_calc()
        years = np.array([2025.5, 2026]).astype(int)
        months = np.array([10, 11]).astype(int)
        days = np.array([1, 2]).astype(int)
        N = 20

        # the shape of lats and lons is 1
        lats = np.array([1])
        lons = np.array([100])
        alts = np.linspace(0, 100, N)

        model.setup_env(lats, lons, alts)
        model.setup_time(years, months, days)

        self.assertEqual(len(model.lat), N)
        self.assertEqual(len(model.lon), N)

        # the shape of lats is 1
        lons = np.linspace(0, 180, N)
        alts = np.linspace(0, 100, N)
        model.dyear = [2025.5]

        model.setup_env(lats, lons, alts)
        model.setup_time(years, months, days)

        self.assertEqual(len(model.lat), N)
        self.assertEqual(len(model.lon), N)

    def test_setup_geod_to_geoc_lat(self):

        alt_true = util.alt_to_ellipsoid_height(self.alts, self.lats, self.lons)
        r, theta = util.geod_to_geoc_lat(self.lats, alt_true)



        wmm_model = wmmhr_calc()
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False)
        wmm_model.setup_time(dyear=self.dyears)

        for i in range(len(self.lats)):
            self.assertAlmostEqual(wmm_model.lat[i], self.lats[i], places=6)
            self.assertAlmostEqual(wmm_model.theta[i], theta[i], places=6)

    def test_to_km(self):

        wmm_model = wmmhr_calc()
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False, unit="m")
        wmm_model.setup_time(2025, 1, 1)

        for i in range(len(self.alts)):
            self.assertAlmostEqual(self.alts[i] * 1000, wmm_model.alt[i], places=6)

    def test_forward_base(self):



        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=self.dyears)
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False)


        Bx, By, Bz = wmm_model.forward_base()

        for i in range(len(self.Bx)):
            self.assertAlmostEqual(Bx[i], self.Bx[i], delta=0.05)
            self.assertAlmostEqual(By[i], self.By[i], delta=0.05)
            self.assertAlmostEqual(Bz[i], self.Bz[i], delta=0.05)

    def test_setup_sv(self):


        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=self.dyears)
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False)

        dBx, dBy, dBz = wmm_model.forward_sv()

        tol = 0.05
        for i in range(len(self.Bx)):
            self.assertAlmostEqual(dBx[i], self.dBx[i], delta=tol)
            self.assertAlmostEqual(dBy[i], self.dBy[i], delta=tol)
            self.assertAlmostEqual(dBz[i], self.dBz[i], delta=tol)

    def test_get_dBh(self):


        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=self.dyears)
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False)

        dh = wmm_model.get_dBh()
        self.assertTrue(isinstance(dh[0], float))


        for i in range(len(self.dBh)):
            self.assertAlmostEqual(dh[i], self.dBh[i], delta=0.05)

    def test_inherit_GeomagElements(self):


        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=self.dyears)
        wmm_model.setup_env(self.lats, self.lons, self.alts, msl=False)

        map = wmm_model.get_all()



        for i in range(len(self.dBdec)):
            self.assertAlmostEqual(map["ddec"][i] / 60, self.dBdec[i], delta=0.05)
            self.assertAlmostEqual(map["dinc"][i] / 60, self.dBinc[i], delta=0.05)

    def test_reset_env(self):
        lat = np.array([-18])
        lon = np.array([138])
        alt = np.array([77])

        dec_year = np.array([2029.5])

        wmm_model = wmmhr_calc()
        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat, lon, alt, msl=False)

        lat1 = np.array([-19])
        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat1, lon, alt, msl=False)
        lat2 = wmm_model.lat[0]

        self.assertAlmostEqual(lat2, -19)

    def test_load_wmmcoeff(self):


        wmm_model = wmmhr_calc()
        coef = wmm_model.load_coeffs()




        self.assertEqual(2025, coef["epoch"])
        self.assertAlmostEqual(coef["min_year"][0], 2024.866, delta=1e-3)

    def test_correct_time(self):

        user_time = np.array([2024.5, 2030.0])

        wmm_model = wmmhr_calc()
        get_err = 0

        for i in range(2):
            try:
                wmm_model.setup_time(dyear=user_time)
            except ValueError as e:
                self.assertEqual(str(e), "Invalid year. Please provide date from [2024]-[11]-[13] to [2030]-[01]-[01] 00:00")
                get_err += 1

        self.assertEqual(get_err, 2)




    def test_check_latitude(self):

        user_time = np.array([2025.1])
        lon, alt = 190, 700
        lat = [-90.9, 90.1]

        wmm_model = wmmhr_calc()
        get_err = 0

        for i in range(2):
            try:
                wmm_model.setup_time(dyear=user_time)
                wmm_model.setup_env(lat[i], lon, alt, msl=False)
            except ValueError as e:
                self.assertEqual(str(e), "latitude should between -90 to 90")
                get_err += 1

        self.assertEqual(get_err, 2)

    def test_check_longtitude(self):

        user_time = np.array([2025.1])

        lat = np.array([-18])
        lon = np.array([-180.1, 360.1])
        alt = np.array([100])

        wmm_model = wmmhr_calc()
        get_err = 0

        for i in range(2):
            try:
                wmm_model.setup_time(dyear=user_time)
                wmm_model.setup_env(lat, lon, alt, msl=False)
            except ValueError as e:
                self.assertEqual(str(e), "lontitude should between -180 to 360")
                get_err += 1

        self.assertEqual(get_err, 2)

    @unittest.expectedFailure
    def test_not_setup_env(self):

        model = wmmhr_calc()
        user_time = np.array([2025.1])
        model.setup_time(dyear=user_time)
        x = model.get_Bx()

    def test_wmm_altitude_warning(self):

        user_time = np.array([2025.1])

        lat = np.array([-18])
        lon = np.array([138])
        alt = np.array([3000, -2])
        link = "\033[94mhttps://www.ncei.noaa.gov/products/world-magnetic-model/accuracy-limitations-error-model\033[0m" #Blue color

        wmm_model = wmmhr_calc()
        with self.assertWarns(UserWarning) as w:
            wmm_model.setup_env(lat, lon, alt[0])
        self.assertEqual(str(w.warning), f"Warning: WMMHR will not meet MilSpec at this altitude. For more information see {link}" )

        wmm_model = wmmhr_calc()
        with self.assertWarns(UserWarning) as w:
            wmm_model.setup_env(lat, lon, alt[1])
        self.assertEqual(str(w.warning),
                         f"Warning: WMMHR will not meet MilSpec at this altitude. For more information see {link}")


    def test_get_uncertainty(self):

        user_time = np.array([2025.1])

        lat = np.array([-18, 20, 20])
        lon = np.array([138, 139, 140])
        alt = np.array([100, 150, 200])

        model = wmmhr_calc()
        model.setup_time(dyear=user_time)
        model.setup_env(lat, lon, alt)

        print(model.get_uncertainty())



if __name__ == '__main__':
    unittest.main()
