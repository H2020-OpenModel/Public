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
