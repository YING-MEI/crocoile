# Tim Cornwell <realtimcornwell@gmail.com>
#
# Definition of structures needed by the function interface. These are mostly
# subclasses of astropy classes.
#
import numpy as numpy

from astropy.table import Table

import os

import numpy

import astropy.units as units
from astropy.coordinates import SkyCoord, ICRS, EarthLocation
from astropy.table import Table, Column, vstack
from astropy.wcs import WCS
from astropy import units

from crocodile.simulate import *

from arl.data_models import *
from arl.image_operations import import_image_from_fits, add_wcs_to_image
from arl.parameters import crocodile_path

from util.read_oskar_vis import OskarVis

import logging
log = logging.getLogger("arl.test_support")

def filter_configuration(fc: Configuration, params={}):
    """ Filter a configuration e.g. remove certain antennas

    :param fc:
    :type Configuration:
    :param params: Dictionary containing parameters
    :returns: Configuration
    """
    log.error("filter_configuration: No filter implemented yet")
    return fc


def create_configuration_from_array(antxyz: numpy.array, name: str = None, location: EarthLocation = None,
                                    mount: str = 'alt-az', names: str = '%d', meta: dict = None, params={}):
    """ Define from parts

    :param name:
    :param antxyz: locations of antennas numpy.array[...,3]
    :type numpy.array:
    :param location: Location of array centre (reference for antenna locations)
    :type EarthLocation:
    :param mount: Mount type e.g. 'altaz'
    :type str:
    :param names: Generator for names e.g. 'SKA1_MID%d'
    :type generator:
    :type meta:
    :type dict:
    :returns: Configuration
    """
    fc = Configuration()
    assert len(antxyz) == 2, "Antenna array has wrong shape"
    fc.data = Table(data=[names, antxyz, mount], names=["names", "xyz", "mount"], meta=meta)
    fc.location = location
    return fc


def create_configuration_from_file(antfile: str, name: str = None, location: EarthLocation = None, mount: str = 'altaz',
                                   names: str = "%d", frame: str = 'local',
                                   meta: dict =
                                   None,
                                   params={}):
    """ Define from a file

    :param antfile: Antenna file name
    :type str:
    :param name: Name of array e.g. 'LOWBD2'
    :type str:
    :param location:
    :type EarthLocation:
    :param mount: mount type: 'altaz', 'xy'
    :type str:
    :param frame: 'local' | 'global'
    :type str:
    :param meta: Any meta info
    :type dict:
    :returns: Configuration
    """
    fc = Configuration()
    fc.name = name
    fc.location = location
    antxyz = numpy.genfromtxt(antfile, delimiter=",")
    assert antxyz.shape[1] == 3, ("Antenna array has wrong shape %s" % antxyz.shape)
    nants = antxyz.shape[0]
    if frame == 'local':
        latitude = location.geodetic[1].to(units.rad).value
        antxyz = xyz_at_latitude(antxyz, latitude)
    xyz = Column(antxyz, name="xyz")

    anames = [names % ant for ant in range(nants)]
    mounts = Column(numpy.repeat(mount, nants), name="mount")
    fc.data = Table(data=[anames, xyz, mounts], names=["names", "xyz", "mount"], meta=meta)
    fc.frame = frame
    return fc


def create_LOFAR_configuration(antfile: str, meta: dict = None,
                               params={}):
    """ Define from the LOFAR configuration file

    :param antfile:
    :type str:
    :param name:
    :type str:
    :param meta:
    :type dict:
    :param params: Dictionary containing parameters
    :returns: Configuration
    """
    fc = Configuration()
    antxyz = numpy.genfromtxt(antfile, skip_header=2, usecols=[1, 2, 3], delimiter=",")
    nants = antxyz.shape[0]
    assert antxyz.shape[1] == 3, "Antenna array has wrong shape %s" % antxyz.shape
    anames = numpy.genfromtxt(antfile, dtype='str', skip_header=2, usecols=[0], delimiter=",")
    mounts = Column(numpy.repeat('XY', nants), name="mount")
    fc.data = Table(data=[anames, antxyz, mounts], names=["names", "xyz", "mount"], meta=meta)
    fc.location = EarthLocation(x=[3826923.9] * units.m, y=[460915.1] * units.m, z=[5064643.2] * units.m)
    return fc


def create_named_configuration(name: str = 'LOWBD2', params={}):
    """ Standard configurations e.g. LOWBD2, MIDBD2

    :param name: name of Configuration LOWBD2, LOWBD1, LOFAR, VLAA
    :type str:
    :returns: Configuration
    """
    
    if name == 'LOWBD2':
        location = EarthLocation(lon="116.4999", lat="-26.7000", height=300.0)
        fc = create_configuration_from_file(antfile=crocodile_path("data/configurations/LOWBD2.csv"),
                                            location=location, mount='xy', names='LOWBD2_%d')
    elif name == 'LOWBD1':
        location = EarthLocation(lon="116.4999", lat="-26.7000", height=300.0)
        fc = create_configuration_from_file(antfile=crocodile_path("data/configurations/LOWBD1.csv"),
                                            location=location, mount='xy', names='LOWBD1_%d')
    elif name == 'LOFAR':
        fc = create_LOFAR_configuration(antfile=crocodile_path("data/configurations/LOFAR.csv"))
    elif name == 'VLAA':
        location = EarthLocation(lon="-107.6184", lat="34.0784", height=2124.0)
        fc = create_configuration_from_file(antfile=crocodile_path("data/configurations/VLA_A_hor_xyz.csv"),
                                            location=location,
                                            mount='altaz',
                                            names='VLA_%d')
    elif name == 'VLAA_north':
        location = EarthLocation(lon="-107.6184", lat="90.000", height=2124.0)
        fc = create_configuration_from_file(antfile=crocodile_path("data/configurations/VLA_A_hor_xyz.csv"),
                                            location=location,
                                            mount='altaz',
                                            names='VLA_%d')
    else:
        fc = Configuration()
        raise UserWarning("No such Configuration %s" % name)
    return fc

def import_visibility_from_ms(msfile: str, params={}) -> Visibility:
    """ Import a visibility set from a measurement set

    :param msfile: Name of measurement set
    :type str:
    :returns: Visibility
    """
    log.error('test_support.import_visibility_from_ms: not yet implemented')
    return Visibility()


def export_visibility_to_ms(vis: Visibility, msfile: str = None, params={}) -> Visibility:
    """ Export a visibility set to a measurement set

    :param vis: Name of visibility set
    :param Visibility:
    :param msfile: Name of output measurement set
    :type str:
    :returns: Visibility
    """
    log.error('test_support.visibility_from_ms: not yet implemented')

def import_visibility_from_oskar(oskar_file: str, params={}) -> Visibility:
    """ Import a visibility set from an OSKAR visibility file

    :param oskar_file: Name of OSKAR visibility file
    :type str:
    :returns: Visibility
    """

    # Extract data from Oskar file
    oskar_vis = OskarVis(oskar_file)
    ra,dec = oskar_vis.phase_centre()
    a1,a2 = oskar_vis.stations(flatten=True)

    # Make configuration
    location = EarthLocation(lon = oskar_vis.telescope_lon,
                             lat = oskar_vis.telescope_lat,
                             height = oskar_vis.telescope_alt)
    antxyz = numpy.transpose([oskar_vis.station_x,
                              oskar_vis.station_y,
                              oskar_vis.station_z])
    config = Configuration(
        name     = oskar_vis.telescope_path,
        location = location,
        xyz      = antxyz
    )

    # Construct visibilities
    return Visibility(
        frequency     = [oskar_vis.frequency(i) for i in range(oskar_vis.num_channels)],
        phasecentre   = SkyCoord(frame=ICRS, ra=ra, dec=dec, unit=units.deg),
        configuration = config,
        uvw           = numpy.transpose(oskar_vis.uvw(flatten=True)),
        time          = oskar_vis.times(flatten=True),
        antenna1      = a1,
        antenna2      = a2,
        vis           = oskar_vis.amplitudes(flatten=True),
        weight        = numpy.ones(a1.shape))


def create_test_image(canonical=True):
    """Create a useful test image

    This is the test image M31 widely used in ALMA and other simulations. It is actually part of an Halpha region in
    M31.

    :param canonical: Make the image into a 4 dimensional image
    :returns: Image
    """
    im = import_image_from_fits(crocodile_path("data/models/M31.MOD"))
    if canonical:
        im = replicate_image(im, npol=4)
    return im


def replicate_image(im: Image, npol = 4, nchan = 1, frequency=1.4e9):
    """ Make a new canonical shape Image, extended along third and fourth axes by replication.

    The order is [chan, pol, dec, ra]


    :param im:
    :type Image:
    :param npol: Number of polarisation axes
    :param nchan: Number of spectral channels
    :returns: Image
    """
    
    if len(im.data.shape) == 2:
        fim = Image()
        
        newwcs = WCS(naxis=4)
        
        newwcs.wcs.crpix = [im.wcs.wcs.crpix[0], im.wcs.wcs.crpix[1], 1.0, 1.0]
        newwcs.wcs.cdelt = [im.wcs.wcs.cdelt[0], im.wcs.wcs.cdelt[1], 1.0, 1.0]
        newwcs.wcs.crval = [im.wcs.wcs.crval[0], im.wcs.wcs.crval[1], 1.0, frequency]
        newwcs.wcs.ctype = [im.wcs.wcs.ctype[0], im.wcs.wcs.ctype[1], 'STOKES', 'FREQ']
        
        add_wcs_to_image(fim, newwcs)
        fshape = [nchan, npol, im.data.shape[1], im.data.shape[0]]
        fim.data = numpy.zeros(fshape)
        log.debug("replicate_image: replicating shape %s to %s" % (im.data.shape, fim.data.shape))
        for i3 in range(nchan):
            for i2 in range(npol):
                fim.data[i3, i2, :, :] = im.data[:, :]
    else:
        fim = im
    
    return fim

