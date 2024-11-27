from typing import Optional
import os

from wmm import wmm_calc

class wmmhr_calc(wmm_calc):

    def __init__(self):


        super().__init__()
        self.nmax = 133
        self.coef_file = "WMMHR.cof"

    def get_coefs_path(self, filename: str) -> str:
        """
        Get the path of coefficient file
        :param filename: Provide the file name of coefficient file. The coefficient file should saved in wmm/wmm/coefs
        :return: The path to the coefficient file
        """

        currdir = os.path.dirname(__file__)

        coef_file = os.path.join(currdir, "coefs", filename)



        return coef_file

    def check_coords(self, lat: float, lon: float, alt: float):

        if lat > 90.0 or lat < -90.0:
            raise ValueError("latitude should between -90 to 90")

        if lon > 360.0 or lon < -180.0:
            raise ValueError("lontitude should between -180 to 180")



