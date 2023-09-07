from aiida.engine import calcfunction
from typing import TYPE_CHECKING
#if TYPE_CHECKING:  # pragma: no cover
from aiida import orm
from typing import Dict

@calcfunction
def parse_density(log: "orm.SinglefileData") -> "Dict[str, orm.Float]":
    """`Parser` implementation for the `PwCalculation` calculation job class."""

    filename_stdout = log
    stdout = log.get_content()

    data_lines = stdout.split('\n')
    istep, idensity = -1, -1
    for line in data_lines:
        if "Loop time of" in line:
            istep, idensity = -1, -1
        if "Step" in line:
            nconv = 0
            sum_density = 0.0
            header = line.split()
            istep = header.index("Step")
            idensity = header.index("Density")
            continue
        if istep == -1:
            continue
        else:
            vals = line.split()
            step = int(vals[istep])
            nconv += 1
            sum_density += float(vals[idensity])

    return {"density": orm.Float(sum_density / nconv)}
