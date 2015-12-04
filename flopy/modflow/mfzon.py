"""
mfzon module.  Contains the ModflowZone class. Note that the user can access
the ModflowZone class as `flopy.modflow.ModflowZone`.

Additional information for this MODFLOW package can be found at the `Online
MODFLOW Guide
<http://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/zone.htm>`_.

"""
import sys
import collections
import numpy as np
from flopy.mbase import Package
from flopy.utils import Util2d


class ModflowZon(Package):
    """
    MODFLOW Zone Package Class.

    Parameters
    ----------
    model : model object
        The model object (of type :class:`flopy.modflow.mf.Modflow`) to which
        this package will be added.
    zone_dict : dict
        Dictionary with zone data for the model. zone_dict is typically
        instantiated using load method.
    extension : string
        Filename extension (default is 'drn')
    unitnumber : int
        File unit number (default is 21).


    Attributes
    ----------

    Methods
    -------

    See Also
    --------

    Notes
    -----
    Parameters are supported in Flopy only when reading in existing models.
    Parameter values are converted to native values in Flopy and the
    connection to "parameters" is thus nonexistent.

    Examples
    --------

    >>> import flopy
    >>> m = flopy.modflow.Modflow()
    >>> zonedict = flopy.modflow.ModflowZon(m, zone_dict=zone_dict)

    """

    def __init__(self, model, zone_dict=None,
                 extension='zon', unitnumber=1001):
        """
        Package constructor.

        """
        Package.__init__(self, model, extension, 'ZONE',
                         unitnumber)  # Call ancestor's init to set self.parent, extension, name and unit number
        self.heading = '# ZONE for MODFLOW, generated by Flopy.'
        self.url = 'zon.htm'

        self.nzn = 0
        if zone_dict is not None:
            self.nzn = len(zone_dict)
            self.zone_dict = zone_dict
        self.parent.add_package(self)


    def write_file(self):
        """
        Write the package file.

        Returns
        -------
        None

        Notes
        -----
        Not implemented because parameters are only supported on load

        """
        pass


    @staticmethod
    def load(f, model, nrow=None, ncol=None, ext_unit_dict=None):
        """
        Load an existing package.

        Parameters
        ----------
        f : filename or file handle
            File to load.
        model : model object
            The model object (of type :class:`flopy.modflow.mf.Modflow`) to
            which this package will be added.
        nrow : int
            number of rows. If not specified it will be retrieved from
            the model object. (default is None).
        ncol : int
            number of columns. If not specified it will be retrieved from
            the model object. (default is None).
        ext_unit_dict : dictionary, optional
            If the arrays in the file are specified using EXTERNAL,
            or older style array control records, then `f` should be a file
            handle.  In this case ext_unit_dict is required, which can be
            constructed using the function
            :class:`flopy.utils.mfreadnam.parsenamefile`.

        Returns
        -------
        zone : ModflowZone dict

        Examples
        --------

        >>> import flopy
        >>> m = flopy.modflow.Modflow()
        >>> zon = flopy.modflow.ModflowZon.load('test.zon', m)

        """

        if model.verbose:
            sys.stdout.write('loading zone package file...\n')

        if not hasattr(f, 'read'):
            filename = f
            f = open(filename, 'r')
        # dataset 0 -- header
        while True:
            line = f.readline()
            if line[0] != '#':
                break
        #dataset 1
        t = line.strip().split()
        nzn = int(t[0])

        #get nlay,nrow,ncol if not passed
        if nrow is None and ncol is None:
            nrow, ncol, nlay, nper = model.get_nrow_ncol_nlay_nper()

        #read zone data
        zone_dict = collections.OrderedDict()
        for n in range(nzn):
            line = f.readline()
            t = line.strip().split()
            if len(t[0]) > 10:
                zonnam = t[0][0:10].lower()
            else:
                zonnam = t[0].lower()
            if model.verbose:
                sys.stdout.write('   reading data for "{:<10s}" zone\n'.format(zonnam))
            # load data
            t = Util2d.load(f, model, (nrow, ncol), np.int, zonnam,
                             ext_unit_dict)
            # add unit number to list of external files in ext_unit_dict to remove.
            if t.locat is not None:
                model.add_pop_key_list(t.locat)
            zone_dict[zonnam] = t
        zon = ModflowZon(model, zone_dict=zone_dict)
        return zon
