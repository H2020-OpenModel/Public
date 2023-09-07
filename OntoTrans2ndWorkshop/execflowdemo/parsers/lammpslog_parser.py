#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""`Parser` implementation for the `PwCalculation` calculation job class."""

from aiida import orm
import numpy

import aiida.parsers import Parser

class LammpsLogParser(Parser):
    """`Parser` implementation for the `PwCalculation` calculation job class."""

    def parse(self, **kwargs):
        filename_stdout = self.node.base.attributes.get('output_filename')
        try:
            stdout = self.retrieved.base.repository.get_object_content(filename_stdout)
        except IOError:
            self.exit_code_stdout = self.exit_codes.ERROR_OUTPUT_STDOUT_READ
            return parsed_data, logs

        nconv = 0
        sum_density = 0.0

        data_lines = stdout.split('\n')
        istep, idensity = -1, -1
        for line in data_lines:
            if "Step" in line:
                header = line.split()
                istep = header.index("Step")
                idensity = header.index("Density")
            if "Loop time of" in line:
                break
            if istep == -1:
                continue
            else:
                vals = line.split()
                step = int(tokens[istep])
                nconv += 1
                sum_density += float(tokens[idensity])
        self.out("density", sum_density / nconv)
