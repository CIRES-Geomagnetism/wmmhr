import unittest
import wmmhr
from wmmhr import wmmhr_calc

from geomaglib import util
import os



class MyTestCase(unittest.TestCase):

    def setUp(self):

        self.lat = -18
        self.lon = 138
        self.alt = 77
        self.dec_year = 2025.5

        self.top_dir = os.path.dirname(os.path.dirname(__file__))
        self.wmm_file = os.path.join(self.top_dir, "wmm", "coefs", "WMMHR.cof")
    def test_get_coefs_path(self):

        model = wmmhr_calc()
        path = model.get_coefs_path("WMMHR.cof")

        print(path)

    def test_setup_time(self):



        model = wmmhr_calc()
        lat, lon, alt = 23.35, 40, 21.0

        model.setup_time(2025, 1, 1)

        model.setup_env(lat, lon, alt)

        model.get_all()

        print(model.get_all())
    def test_setup_env(self):

        lat = -18
        lon = 138
        alt = 77
        dec_year = 2025.5

        alt_true = util.alt_to_ellipsoid_height(alt, lat, lon)
        r, theta = util.geod_to_geoc_lat(lat, alt_true)


        wmmhr_model = wmmhr_calc()
        wmmhr_model.setup_env(lat, lon, alt)
        wmmhr_model.setup_time(dyear=dec_year)



        self.assertAlmostEqual(wmmhr_model.lat, lat, places=6)

        self.assertAlmostEqual(wmmhr_model.theta, theta, places=6)

    def test_wmm_altitude_warning(self):

        lat = -18
        lon = 138
        alt = -20
        dec_year = 2025.5

        wmmhr_model = wmmhr_calc()
        wmmhr_model.setup_env(lat, lon, alt)

        # Should not return wmm warning

    def test_forward_base(self):

        lat = -18
        lon = 138
        alt = 77

        dec_year = 2029.5

        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat, lon, alt, msl=False)



        Bx, By, Bz = wmm_model.forward_base()

        self.assertAlmostEqual(Bx, 31768.834236, delta=1e-6)
        self.assertAlmostEqual(By, 2448.858959, delta=1e-6)
        self.assertAlmostEqual(Bz, -34799.807102, delta=1e-6)

    def test_get_dBh(self):

        lat = -18
        lon = 138
        alt = 77

        dec_year = 2029.5

        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat, lon, alt, msl=False)


        self.assertTrue(isinstance(wmm_model.get_dBh(), float))



    def test_inherit_GeomagElements(self):
        lat = -21
        lon = 32
        alt = 66



        dec_year = 2029.5

        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat, lon, alt, msl=False)


        map = wmm_model.get_all()

        print(map)

        self.assertAlmostEqual(round(map["ddec"]/60, 1), -0.1, places=6)
        self.assertAlmostEqual(round(map["dinc"] / 60, 1), 0.1, places=6)

    def test_reset_env(self):
        lat = -18
        lon = 138
        alt = 77

        dec_year = 2029.5

        wmm_model = wmmhr_calc()
        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat, lon, alt, msl=False)



        lat1 = -19
        wmm_model.setup_time(dyear=dec_year)
        wmm_model.setup_env(lat1, lon, alt, msl=False)
        lat2 = wmm_model.lat

        self.assertAlmostEqual(lat2, -19)

    def test_get_minyear(self):
        lat = -18
        lon = 138
        alt = 77

        dec_year = 2029.5

        #coef = load.load_wmm_coef(self.wmm_file, skip_two_columns=True)
        model = wmmhr_calc()
        model.setup_time(dyear=dec_year)
        model.setup_env(lat, lon, alt, msl=False)

        self.assertAlmostEqual(model.coef_dict["min_year"], 2024.96, delta=1e-6)


    def test_correct_time(self):



        user_time = 2030.0



        model = wmmhr_calc()

        try:
            model.setup_time(dyear=user_time)
        except ValueError as e:
            print(e)




    def test_check_altitude(self):
        user_time = 2020.0
        user_time = 2026.1

        lat, lon, alt = 30.0, 20, 700

        wmm_model = wmmhr_calc()

        wmm_model.setup_time(dyear=user_time)
        wmm_model.setup_env(lat, lon, alt, msl=False)


    def test_check_latitude(self):
        user_time = 2020.0
        user_time = 2024.1

        lat, lon, alt = 90.1, 20, 700

        wmm_model = wmmhr_calc()

        try:
            wmm_model.setup_time(dyear=user_time)
            wmm_model.setup_env(lat, lon, alt, msl=False)
        except ValueError as e:
            print(e)




    def test_check_longtitude(self):

        user_time = 2020.0
        user_time = 2024.1

        lat, lon, alt = 90.0, 361, 700

        wmm_model = wmmhr_calc()

        try:
            wmm_model.setup_time(dyear=user_time)
            wmm_model.setup_env(lat, lon, alt, msl=False)
        except ValueError as e:
            print(e)







    def test_not_setup_env(self):

        model = wmmhr_calc()
        model.setup_time(dyear=2025.5)
        x = model.get_Bx()

        print(x)

    def test_coef_load(self):

        model = wmmhr_calc()
        model.setup_time(dyear=2025.5)
        for lat in range(-90, 91):
            for lon in range(-180, 180):

                model.setup_env(lat, lon, 0)
                model.get_all()













if __name__ == '__main__':
    unittest.main()
