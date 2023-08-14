import aiida

aiida.load_profile()
import os
import sys
from pathlib import Path

import dlite
from aiida import engine, orm
from execflow.workchains.declarative_chain import DeclarativeChain

# Paths
thisdir = Path(__file__).resolve().parent
casedir = thisdir
mmsdir = casedir.parent
entitydir = mmsdir / "entities"
plugindir = mmsdir / "storage_plugins"

# Add utils to sys path
sys.path.append(str(mmsdir))

# Add our storage plugin to the DLite plugin search path
dlite.python_storage_plugin_path.append(plugindir)
dlite.storage_path.append(entitydir)

if __name__ == "__main__":
    workflow = sys.argv[1]
    all = {"workchain_specification": orm.SinglefileData(os.path.abspath(workflow))}

    engine.run(DeclarativeChain, **all)


