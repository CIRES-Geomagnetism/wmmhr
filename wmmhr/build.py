from typing import Optional
import os
import numpy as np
import warnings


from wmm import wmm_calc
from wmmhr import uncertainty

class wmmhr_calc(wmm_calc):

    def __init__(self):


        super().__init__()
        self.nmax = 133
        self.max_sv = 15
        self.coef_file = "WMMHR.COF"
        self.err_vals = uncertainty.err_models


    def get_coefs_path(self, filename: str) -> str:
        """
        Get the path of coefficient file
        :param filename: Provide the file name of coefficient file. The coefficient file should saved in wmm/wmm/coefs
        :return: The path to the coefficient file
        """

        currdir = os.path.dirname(__file__)

        coef_file = os.path.join(currdir, "coefs", filename)



        return coef_file

    def check_coords(self, lat: np.ndarray, lon: np.ndarray, alt: np.ndarray):

        if np.any(lat > 90.0) or np.any(lat < -90.0) or np.any(lon > 360.0) or np.any(lon < -180.0):
            super().check_coords(lat, lon, alt)
        if np.any(alt < -1) or np.any(alt > 1900):
            link = "\033[94mhttps://www.ncei.noaa.gov/products/world-magnetic-model/accuracy-limitations-error-model\033[0m" #Blue color
            warnings.warn(
                f"Warning: WMMHR will not meet MilSpec at this altitude. For more information see {link}")








