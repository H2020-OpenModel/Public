"""Test running of shell job with aiida"""
# from aiida.engine import calcfunction

from aiida import load_profile
from aiida.orm import SinglefileData
from aiida_shell import launch_shell_job

load_profile()

# Find the path after having run the moltemplate with
# verdi node attributes PK (PK number of remote folder from previous run)

def test_lammps(shell_job_case_dir) -> None:
    '''
    Test lammps can be run from shell_job. Note that this requires lammps to be installed
    and a softlink to the executable callsed lmp_23Jun22 is in the /tmp folder.
    '''
    testfilepath = shell_job_case_dir / "tests" / "test_shell_job" / "testfiles"
    results, node = launch_shell_job(
        "/tmp/lmp_23Jun22",
        arguments=["-in", "{in1}"],
        # arguments=['{infile}','{outdir}'],
        nodes={
            "in1": SinglefileData(file=testfilepath / "s01_water_cg.in"),
            "in2": SinglefileData(file=testfilepath / "s01_water_cg.data"),
            "in3": SinglefileData(file=testfilepath / "s01_water_cg.in.settings"),
            "in4": SinglefileData(file=testfilepath / "s01_water_cg.in.run"),
            "in5": SinglefileData(file=testfilepath / "s01_water_cg.in.init"),
        },
        filenames={
            "in1": "s01_water_cg.in",
            "in2": "s01_water_cg.data",
            "in3": "s01_water_cg.in.settings",
            "in4": "s01_water_cg.in.run",
            "in5": "s01_water_cg.in.init",
        },
        outputs=["log.lammps", "s01_water_cg.log", "s01_water_cg.dump"],
    )

# print(node.outputs.remote_folder.get_remote_path())
# print(results.keys())

# print(results["energy_txt"].get_content())

# print(results["forces_json"].get_content())
