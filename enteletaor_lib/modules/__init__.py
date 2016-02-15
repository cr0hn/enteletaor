# -*- coding: utf-8 -*-

import abc
import logging
import argparse

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
class IModule:
    """Interface for modules"""

    name = None
    description = None

    @abc.abstractmethod
    def run(self, module_config):
        pass


# ----------------------------------------------------------------------
def find_modules():
    """
    Find modules and return a dict module instances.

    :return: dict with modules instaces as format: dict(str: IModule)
    :rtype: dict(str: IModule)

    """
    import os
    import os.path
    import inspect

    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Modules found
    results = dict()

    for root, dirs, files in os.walk(base_dir):
        # Check if folder is a package
        if "__init__.py" not in files:
            continue
        # Remove files or path that starts with "_"
        if any(True for x in root.split("/") if x.startswith("_")):
            continue

        for filename in files:
            if filename.endswith(".py") and \
                    not filename.startswith("celery") and \
                    not filename.startswith("test_"):

                if filename.startswith("_"):
                    if filename != "__init__.py":
                        continue

                # loop_file = os.path.join(root, filename)
                loop_file = os.path.join(root, filename) \
                    .replace(base_dir, '') \
                    .replace(os.path.sep, '.') \
                    .replace('.py', '')

                loop_file = loop_file[1:] if loop_file.startswith(".") else loop_file

                # Load module info
                classes = __import__(loop_file, globals=globals(), locals=locals(), level=loop_file.count("."))

                # Get Modules instances
                for m in dir(classes):
                    _loaded_module = getattr(classes, m)
                    if inspect.isclass(_loaded_module) \
                            and _loaded_module.__name__ != "IModule" \
                            and issubclass(_loaded_module, IModule):
                        try:
                            results[_loaded_module.name] = _loaded_module
                        except AttributeError:
                            log.warning("Module '%s' has not attribute 'name' and can't be loaded." %
                                        _loaded_module.__name__)

    return results
