"""Testing runing of moltemplate"""
# from aiida.engine import calcfunction
from pathlib import Path

from aiida import load_profile
from aiida.orm import SinglefileData
from aiida_shell import launch_shell_job

load_profile()

# To test that aiida-shell is working, you can uncomment the two next lines
# results, node = launch_shell_job('date')
# print(results['stdout'].get_content())

def test_moltemplate(repo_dir, shell_job_case_dir) -> None:

    results, node = launch_shell_job(
        shell_job_case_dir / "multiscale_flb" / "01_step.sh",
        arguments=["{infile1}", "{infile2}", "{infile3}"],
        # arguments=['{infile}','{outdir}'],
        nodes={
            "infile1": SinglefileData(
                file=shell_job_case_dir / "multiscale_flb" / "01_input_variables.txt"
            ),
            "infile2": SinglefileData(
                file=repo_dir / "demo_pm" / "molc" / "tip4p2005_cg_01.lt"
            ),
            "infile3": SinglefileData(
                file=repo_dir / "demo_pm" / "molc" / "solvent_cg_creation.lt"
            ),
        },
        outputs=["s01_water_cg.in*", "s01_water_cg.data"],
        # NB! outputs cannot start with a number, as they need to be valid python variables
    )   

    print(node.outputs.remote_folder.get_remote_path())
    print(results.keys())


