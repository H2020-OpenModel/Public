"""Test script for meso multi sim demo DLite plugins case."""

def test_mmsim_dlite_plugin(repo_dir, use_case_dir, shell_job_case_dir) -> None:
    import dlite
    from tripper import EMMO, MAP, Namespace
    from otelib import OTEClient

    # Paths
    outdir = shell_job_case_dir / "output"

    indir = use_case_dir / "input"
    entitydir = use_case_dir / "entities"
    plugindir = shell_job_case_dir / "storage_plugins"


    # Add our storage plugin to the DLite plugin search path
    dlite.python_storage_plugin_path.append(plugindir)
    dlite.storage_path.append(entitydir)

 
    # Add our storage plugin to the DLite plugin search path
    dlite.python_storage_plugin_path.append(plugindir)
    dlite.storage_path.append(entitydir)
    # Create output directory
    outdir.mkdir(exist_ok=True, parents=True)

    # Load Moltemplate input entity
    datamodel = dlite.get_instance("http://openmodel.eu/meta/0.1/MoltemplateInput")
    # Create an instance
    instance = dlite.Instance.from_location(
        "yaml", indir / "moltemplate_input.yml", "mode=r"
    )

    # Save Moltemplate input using the dlite plugin that you have created.
    instance.save("moltemplate_input", outdir / "moltemplate_input.lt")
