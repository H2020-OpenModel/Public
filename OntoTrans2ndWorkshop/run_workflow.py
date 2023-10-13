#!/usr/bin/env python
"""Script to run AiiDA declarative chain"""
import os
import sys
from pathlib import Path

import aiida
import dlite
from aiida import engine, orm
from execflow.workchains.declarative_chain import DeclarativeChain

aiida.load_profile()

# Paths
thisdir = Path(__file__).resolve().parent
entitydir = thisdir / "entities"
plugindir = thisdir / "storage_plugins"

print(entitydir)
# Add utils to sys path
#sys.path.append(str(mmsdir))

# Add our storage plugin to the DLite plugin search path
dlite.python_storage_plugin_path.append(plugindir)
dlite.storage_path.append(entitydir)

if __name__ == "__main__":
    workflow = sys.argv[1]  # pylint: disable=invalid-name
    all_spec = {
        "workchain_specification": orm.SinglefileData(os.path.abspath(workflow))
    }

    engine.run(DeclarativeChain, **all_spec)
