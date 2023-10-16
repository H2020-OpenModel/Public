"""Test script for MMSIM dlite plugin."""


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

    # Additional namespaces
    MMSIM = Namespace("http://ontotrans.eu/meta/0.1/MesoMultiSimDemo#")

    # Create OTE client
    client = OTEClient("python")

    data_resource = client.create_dataresource(
        downloadUrl=f"file://{indir}/mmsim_input.yml",
        mediaType="application/vnd.dlite-parse",
        configuration={
            "driver": "yaml",
            "options": "mode=r",
            "label": "mmsim_input",
        },
    )

    mapping = client.create_mapping(
        mappingType="triples",
        prefixes={
            "emmo": f"{EMMO}",
            "map": f"{MAP}",
        },
        triples=[
        ],
    )

    function = client.create_function(
        functionType="application/vnd.dlite-generate",
        configuration={
            "driver": "mmsim",
            "location": f"{outdir}/water_aa.lt",
            "options": "mode=w",
            "label": "mmsim_input",
        },
    )

    pipeline = data_resource >> mapping >> function

    pipeline.get()
