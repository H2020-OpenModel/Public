"""Dedicated storage plugin for creating meso-multi-sim input files to LAMMPS.
"""
import dlite
from dlite.options import Options


class mmsim(dlite.DLiteStorageBase):  # pylint: disable=invalid-name
    """DLite storage plugin for atomistic structures."""

    metaid = "http://ontotrans.eu/meta/0.1/MesoMultiSimDemo"

    def open(self, uri, options=None):
        """Opens `uri`."""
        # pylint: disable=attribute-defined-outside-init
        self.options = Options(options)
        self.uri = uri

    def save(self, inst):
        """Store MesoMultiSimDemo instance to current storage."""
        with open(self.uri, "w", encoding="utf8") as handle:
            handle.write(MOLTEMPLATE.format(**inst.properties))


# pylint: disable=anomalous-backslash-in-string
MOLTEMPLATE = """\
# Compute density of water.
#
# Compile with:
# moltemplate.sh -atomstyle full -overlay-all -pdb ../multiscale/02_water_bm.pdb water_aa.lt

# METADATA: the input variables that control the simulation.
write_once("In Init"){{

 # Input variables.
 variable ts     equal {timestep}     # timestep
 variable tf     equal {final_temperature}  # equilibrium temperature
 variable p      equal {final_pressure}      # equilibrium pressure
 variable cl     equal {correlation_length}     # correlation length for averaging
 variable s      equal {sample_interval}       # sample interval for averaging
 variable prod   equal {calc_steps}   # Production steps

 # PBC
 boundary p p p
}}

# Import the force field.
import ../molc/water_tip3p_01.lt
import ../molc/aa_atb.lt
ff = new atb_long

# Create the molecules. The number MUST match number
# of molecules in the input PDB structure.
sol = new TIP3[{nmolecules}]

# Create the initial velocity. This command in this point
# is required when a simulation is restarted from a static
# structure, i.e. without velocities.
write_once("In Run"){{
 variable r format r1 %.0f
 velocity all create \\$\\{{ti\\}} \\$r dist gaussian

 # Apply the SHAKE algorithm to hydrogen atoms.
 fix SHK all shake .0001 10 0 m 1.0079 a 1
}}

# Define the task to execute.
# It depends on files aa_tasks.lt and random_init.lt
import ../molc/aa_tasks.lt
task = default               # It includes the density and other standard thermodynamic output
run = new aa_npt
"""
