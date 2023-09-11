
# Instructions for setup and requirements

In this example, YAML files are used to specify a declarative workchain based on AiiDA shell.
Those files contain references to local files that need be copied to a remote folder for execution.
In the current version, absolute paths are used.
To make those paths system-independent (*i.e.* to allow the workflow being executed on different machines), the paths have been renamed to `/tmp/OntoTrans2ndWorkshop`.
Wherever your local repo is located, issue these commands prior to execution in order to create a softlink to your OntoTRans2ndWorkshop folder.
Note that the lammps executable in workflow_full.yml needs to be set to you lammps installation.

```bash
$ cd /tmp
$ ln -s /path/to/OntoTrans2ndWorkshop
```

The minimal requirement to run this example is:
- [ExecFlow](https://github.com/H2020-OpenModel/ExecFlow)
  (Which requires AiiDA-core, oteapi-core, oteapi-dlite, DLite-Python, Tripper, AiiDA-shell)
and a simlified lammpsparser.

This can all be installed by running `pip install .` in the current folder

Note that in order to run the example AiiDA needs to be setup, please follow the 
installation instructions by [AiiDA](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/install_system.html#intro-get-started-system-wide-install).

We recommmend using a dedicated python environment which can be created with 
`pythonX.XX -m vevn environment_name` and activated with `source path/to/environment_name/bin/activate`.	
This needs to be done _before_ installing ExecFlow (pip install .).
After installing ExecFlow, the aiida profile needs to be setup with `verdi quicksetup`, the rabbitmq-server and postgresql must be started, and finally the aiida daemon started with `verdi daemon start`.

# Step 1: Documentation of data

The first step is to document the input needed for your simulation.
Also the data made available to the system which the simulation should find needs to be documented.

Ideally this would be done by two different people or groups: the `data provider` and the `modeller`
For each type of data `partial pipelines` are constructed which document where the data is found,
how it can be parsed and understood in the DLite
interoperability framework and how the data is mapped to ontological concepts.

We start with documenting two datasets, which
have been provided in the excel workbook `../data/multidata_moltemplateinput.xlsx`.
This excelsheet consists of two sheets, but
one could imagine data comming in from different workbooks as well.


## Step 1a: Documentation of dataresource

The partial pipeline for the Physical Parameters
consists of two parts (strategies). These have to be specified separately
before definitnng the partial pipeline. The first strategy is shown below:

```yaml
  - dataresource: load_data
    downloadUrl: "file:///tmp/OntoTrans2ndWorkshop/data/multidata_moltemplateinput.xlsx"
    mediaType: application/vnd.dlite-xlsx
    configuration:
      metadata: http://openmodel.eu/meta/0.1/MoltemplateInputPhysicalProperties
      excel_config:
        worksheet: "PhysicalParameters"
        header_row: "1"
        row_from: "2"
        row_to: "2"
      label: moltemplate_input_1
```

Here `dataresource` refers to this being an oteapi strategy that is used to fetch (and parse) data.
A name, `load_data` is given to it so that it can be referred to when constructing the partial pipeline.
`downloadUrl` is the path to the file or dataresource.
`mediatype` specifies what type of file you are dealing with so that the strategy knows how to handle it.
In this case it is an xlsx-file and we use the (application/vnd.dlite-xlsx)[https://emmc-asbl.github.io/oteapi-dlite/latest/api_reference/strategies/parse_excel/] strategy to parse it.
Each strategy takes a `configuration`.
The `excel_config` specifies which worksheet to use which header and which rows to read.
The `metadata` is the DLite data model used to describe your data.

## Step 1b: Creating the data model (Note this is often eaiser to do before writing the strategy in 1a)

The data model for the the PhysicalProperties is shown below and can be found in the folder ../entities/.
```
{
    "uri": "http://openmodel.eu/meta/0.1/MoltemplateInputPhysicalProperties",
    "description": "Entity describing input variables for the simulation",
    "dimensions": [
      {
        "name": "nrows",
        "description": "Number of elements (i.e. number or rows)."
      }
    ],
    "properties": {
        "temperature": {
            "type": "float",
	    "dims": ["nrows"],
            "description": "Temperature"
        },
        "pressure": {
            "type": "float",
	    "dims": ["nrows"],
            "description": "Pressure."
        }
    }
}
```
The metdata needs a unique `uri` and as long as the path to the folder where it exists is known to DLite it will
be found (done in the script run_workflow.py).
Note that if there are more data models with the same uri it will fail.

The dimensions can also be unspecified (then just written as an empty []),
but in the case of the excelparser it requires one dimension that is the length of the
nuber of rows used from the excelsheet. The `properties` that we want to document in our dataset
are `temperature` and `pressure`.

## Step 1c: Documenting the mappings to the ontology

The second part of the partial pipeline
takes care of the mapping to the ontology.

```yaml
  - mapping: mappings
    mappingType: mappings
    prefixes:
      emmo: http://emmo.info/emmo#
      map: http://emmo.info/domain-mappings#
      prop: http://openmodel.eu/meta/0.1/MoltemplateInputPhysicalProperties#
      demonto: http://openmodel.eu/0.1/domainonto#
    triples:
      - ["prop:temperature", "map:mapsTo", "demonto:Temperature"]
      - ["prop:pressure", "map:mapsTo", "demonto:Pressure"]
```

Here the strategy is a `mapping` and we call it mappings. The `mappingType`is `mappings`.
Prefixes are used to simplify the writing of the triples since we in this
case are giving the triples below directly.
The triples are the mappings between the properties in the datamodel and the ontological concepts.

The final partial pipeline is seen i [pipeline_1.yml](pipeline_1.yml).

The same procedure is done for the SimulationParameter, and the result can be seen in [pipeline_2.yml](pipeline_2.yml).


# Step 2: Documentation of data desired for model input.

In our case we need to create a file that sets some variables.
Note that the format and content of this file is decided by the software we are going to use,
in our case bash and moltemplate. The file that we want to create is the following, but
the order of the lines is not important, and without the comments starting with # at the end of
each line.

```
grid_size=4                        # Molecules on a $grid_size*$grid_size*$grid_size cubic grid.
grid_spacing=6.4                   # Separation between grid points.
temp=298.15                        # Temperature
ts=10                              # timestep
p=1000                             # correlation length
s=5                                # sample interval
steps=50                           # Steps for equilibration.
equi=100                           # Equilibration steps
prod=50000                         # Production steps
```

## Step 2a: Creating the datamodel

The correponding datamodel is called MOLETEMPLATEinput2.json, the top of which is reported below:
This is a datamodel that describes the data that your software needs as input, but it is not the
data itself.

```
{
    "uri": "http://openmodel.eu/meta/0.1/MoltemplateInput",
    "description": "Entity describing input variables for the simulation",
    "dimensions": [],
    "properties": {
        "steps": {
            "type": "int",
            "description": "Number of steps for something."
        },
        "equi": {
            "type": "int",
            "description": "Number of steps during equilibration."
        },
        "s": {
            "type": "int",
            "description": "Sample interval."```
       },
   ...
   }
}
```

Note that it is possible to check whether the generated datamodel is valid or not with the DLite tool `dlite-validate`.
Currently data models need to be generated by hand, but tools for simplifying this process are planned.

## Step 2b: Create mappings to ontology

Create the mappings to the ontology as done above.
This can be seen in the file [pipeline_3.yml](pipeline_3.yml).
Note that the datamodels have names that differ, but that they map to the same ontological concepts.

TODO: Update mappings to the correct ontology

## Step 2c: Creating a DLite plugin that generates the desired input file from the data model.

Now, the software provider has made the datamodel that corresponds to the input that needs to be fetched from 'somewhere'.
The DLite plugin generates the required input from an instance of the datamodel.
In this specific case, an instance of [MoltemplateInput](../entities/MOLTEMPLATEInput2.json) (representing the content of `moltemplate_input.yml`) must be written into a file formatted as shown above.
An example of this is in the file [`storage_plugins/moltemplate_input.py`](storage_plugins/moltemplate_input.py).
Such storage plugins are relatively easy to write and use (once DLite is installed only a path to the storage_plugin must be added).
It is important that this folder is then available to DLite during the workflow execution.
For now this is handled with setting paths in the script that runs the workflow `run_workflow.py`.


```
"""Dedicated storage plugin for creating an input file that provides variable values for
a moltemplate input file.
"""
import dlite
from dlite.options import Options

class moltemplate_input(dlite.DLiteStorageBase):
    """DLite storage plugin for atomistic structures."""

    def open(self, uri, options=None):
        """Opens `uri`."""
        # pylint: disable=attribute-defined-outside-init
        self.options = Options(options)
        self.uri = uri

    def save(self, inst):
        """Store instance to a file that moltemplate can read."""
        with open(self.uri, "w", encoding="utf8") as handle:
            for key, value in inst.properties.items():
                try:
                    if len(value) > 1:
                        raise ValueError(
                            "Moltemplate takes one value per "
                            f"parameter, but for {key} there is "
                            "more than one"
                        )
                    # If the value provided is the only element in a list, use it

                    handle.write(f"{key}={value[0]}\n")
                except:
                    handle.write(f"{key}={value}\n")
```

The important part of the above plugin is how to handle the writing of the file.
As long as you have written down the specifications, this should be relatively easy to write for
a software engineer.


The final pipeline is shown in [pipeline.yml](pipeline.yml).


# Step 3: Run the pipeline

The three partial pipelines must be combined in order to run. This is done in the file pipeline.yml.

These partial pipeline will eventually be stored somewhere where they can be fetched and combination of
them should be done on-the-fly.

In order to run the example: `./run_workflow.py workflow_pipeline.yml`.

# Step 4: Run the full example including the simulation with lammps.

This requires the installation of (1) lammps and (2) moltemplate, which are the two computational codes that we want to run.

NB! There are currently two versions for runinng the shell_jobs. If using the `exec_wrapper` version no further installations are needed.
For the `shell_job` version the shell_job plugin must be installed with `pip install .`in the curren folder.
This was the first implementation and will be deprecated. However, there are some files that
test that their run which will not be removed until proper testing in ExecFlow has been implemented.

Once these are in place and the softlink to OntoTrans2ndWorkshop is made in /tmp/ (see top of this file), you only need to
change the path to your lammps executable.

The workflows are run as follows: `python run_workflow.py name_of_yamlfile.yml`

There are several workflows that can be run:

- `workflow_pipeline.yml`: only runs the pipeline designed to retreive data and construct required input.
- `workflow_complete.yml`: runs the full workflow using the latest implementation for running the shelljob with the declarative workchain.
This is installed when installing ExecFlow and no further installations are needed.
- `workflow_complete_mockexecutables.yml`: same as above, but without the need for
lammps and moltemplate installed.




-----------
To recapitulate, this is a list of what is required to make the software available for execflow through aiida-shell.
(Note that the full restrictions on the software to be used is not yet fully investigated.)

- A DLite DataModel that describes the data that the software needs as input
- A DLite-plugin that converts that data into the desired format.

In OpenModel the first step in making the wrappers needed for each use case is to do the documentation of data available and data needed for the simulations (steps 1-3).
