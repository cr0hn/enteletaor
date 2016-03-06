# -*- coding: utf-8 -*-
#
# Enteletaor - https://github.com/cr0hn/enteletaor
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import logging

log = logging.getLogger(__name__)


# --------------------------------------------------------------------------
class IModule(object):
    """Interface for modules"""

    name = None
    description = None

    def run(self, module_config):
        if hasattr(self, "__submodules__"):
            try:
                self.__submodules__[module_config.sub_action]['action'](module_config)
            except KeyError:
                self.__submodules__["default"]['action'](module_config)
        else:
            raise NotImplemented("Run method must be override")


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
                try:
                    classes = __import__("%s.%s" % (__package__, loop_file), globals=globals(), locals=locals(), level=loop_file.count("."))
                except ImportError:
                    classes = __import__(loop_file, globals=globals(), locals=locals(), level=loop_file.count("."))

                # Get Modules instances
                for m in dir(classes):
                    _loaded_module = getattr(classes, m)
                    if inspect.isclass(_loaded_module) \
                            and _loaded_module.__name__ != "IModule":

                        # Check if class inherits from IModule
                        for c in inspect.getmro(_loaded_module):
                            if c.__name__ == "IModule":
                                try:
                                    results[_loaded_module.name] = _loaded_module
                                except AttributeError:
                                    log.warning("Module '%s' has not attribute 'name' and can't be loaded." %
                                                _loaded_module.__name__)

                                # Found!
                                break

    return results
