"""Dedicated storage plugin for loading density from LAMMPS output.
"""
import dlite
from dlite.options import Options
from utils.parse_lammps import parse_lammps


class lammpslog(dlite.DLiteStorageBase):  # pylint: disable=invalid-name
    """DLite storage plugin for LAMMPS output.

    Options:
        converged_step: Step number at which the LAMMPS simulation converges.
            If not proveded, only the latest value is returned.
    """

    metaid = "http://ontotrans.eu/meta/0.1/LAMMPSOutput"

    def open(self, uri, options=None):
        """Opens `uri`."""
        # pylint: disable=attribute-defined-outside-init
        self.options = Options(options)
        self.uri = uri

    def load(self, id=None):
        """Store load density from LAMMPS output."""
        results = parse_lammps(
            self.uri, converged_step=self.options.get("converged_step")
        )
        meta = dlite.get_instance(self.metaid)
        inst = meta(dimensions={})
        inst.density = results["density"]
        return inst
