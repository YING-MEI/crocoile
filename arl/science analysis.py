# Tim Cornwell <realtimcornwell@gmail.com>
#
# Science analysis
#

import numpy

from astropy.coordinates import SkyCoord
from astropy.wcs.utils import skycoord_to_pixel, pixel_to_skycoord

from arl.data_models import *
from arl.parameters import *

def rotation_measure_synthesis(im: Image, params={}):
    """ Perform rotation measure synthesis
    
    :param im:
    :param params: Dictionary containing parameters
    :return:
    """
    # TODO: implement

    log.warn("rotation_measure_synthesis: not yet implemented")
    return im