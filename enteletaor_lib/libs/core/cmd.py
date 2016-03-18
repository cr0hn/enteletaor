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

import six
import logging
import argparse as _argparse

from .structs import AppSettings
from ...modules import IModule
from ...config import __banner__
from ...data import GlobalExecutionParameters

log = logging.getLogger()


# --------------------------------------------------------------------------
# Setup when startup program
# --------------------------------------------------------------------------
def setup_cmd():
    """
    Try to install activate-global-python-argcomplete to enable auto-completion
    for bash command line
    """
    pass


# --------------------------------------------------------------------------
# Extended argparser
# --------------------------------------------------------------------------
class STBArgumentParser(_argparse.ArgumentParser):

    def parse_args_and_run_hooks(self, args=None, namespace=None):
        parsed_args = super(self.__class__, self).parse_args(args, namespace)

        # Run hooks
        self.run_hooks(parsed_args)

        return parsed_args

    def run_hooks(self, parsed_args):
        """
        :param parsed_args: Argument Parser object already parsed
        :type parsed_args: `argparser.Namespace`
        """
        # Run config hooks
        for hook in AppSettings.hooks["config"]:
            if not hook.__name__.startswith("test_"):
                hook(parsed_args)


# --------------------------------------------------------------------------
# Actions to build command line argparser
# ----------------------------------------------------------------------
def build_arg_parser(config=None, modules=None, parser=None):
    """
    Build the argparse object extracting information from the modules.

    :param modules: dict of Module instances
    :type modules: dict(str:model.IModule)
    
    :param config: instance or subinstance of CommonData object
    :type config: `libs.CommonData`
    
    :param parser: start point of parser to build it 
    :type parser: `ArgumentParser`

    """
    if modules is not None:
        if not isinstance(modules, dict):
            raise TypeError("Expected list, got '%s' instead" % type(modules))
        else:
            for x in six.itervalues(modules):
                if not issubclass(x, IModule):
                    raise TypeError("Expected IModule, got '%s' instead" % type(x))
    else:
        modules = AppSettings.modules

    if config is None:
        config = GlobalExecutionParameters()

    # --------------------------------------------------------------------------
    # Build command line
    # --------------------------------------------------------------------------
    if parser is None:
        parser = STBArgumentParser(description='%s' % __banner__,
                                   epilog=_build_examples(modules),
                                   formatter_class=_argparse.RawTextHelpFormatter)
    _extract_parameters(config, parser)

    # --------------------------------------------------------------------------
    # Add sub parsers for each module
    # --------------------------------------------------------------------------
    main_subparser = parser.add_subparsers(help='available commands:', dest='module_name')
    main_subparser.required = True

    for mod_name, mod_class in six.iteritems(modules):
        # Add subparser to module
        mod_parser = main_subparser.add_parser(mod_class.name,
                                               help=mod_class.description)

        sub_modules_enabled = False

        # If module has raw argsubparser, add it
        if hasattr(mod_class, "__submodules__"):

            if len([x for x in mod_class.__submodules__ if x != "default"]) > 0:

                # New sub-module added
                sub_modules_enabled = True

                sub_module_actions = mod_parser.add_subparsers(help="%s commands:" % mod_name, dest="module_%s" % mod_name)
                sub_module_actions.required = True

                for x, y in six.iteritems(mod_class.__submodules__):

                    # Skip default action info
                    if x == "default":
                        continue

                    sub_help = y.get('help', "")
                    sub_action = y.get('cmd_args', None)

                    sub_sub_parser = sub_module_actions.add_parser(x, help=sub_help)

                    # Add module parameters
                    if hasattr(mod_class, "__model__"):
                        _extract_parameters(mod_class.__model__(), sub_sub_parser, mod_name)

                    if sub_action is not None:
                        # Add sub parser
                        sub_action(sub_sub_parser)

        if sub_modules_enabled is False:
            # Add module parameters
            if hasattr(mod_class, "__model__"):
                _extract_parameters(mod_class.__model__(), mod_parser, mod_name)

    return parser


# ----------------------------------------------------------------------
def _extract_parameters(config, parser, prefix=None):
    """
    Extract parameters from config and set into existent parser object
    :param config: instance or subinstance of CommonData object
    :type config: `libs.CommonData`

    :param parser: argparser instancer
    :type parser: Namedspace

    :param prefix: prefix name for parameter. Used for differentiate submodules params.
    :type prefix: str

    """
    # Shared options
    used_opts = set()
    for x, v in six.iteritems(config.vars):
        # cmd options
        params = ["--%s%s" % (
            # Add sub-module prefix?
            "%s-" % prefix if prefix is not None and AppSettings.parallel_running is True else "",
                  x.replace("_", "-"))
        ]

        if x[0] not in used_opts:
            used_opts.add(x[0])

            # If parameter is form sub-module don't add it
            if AppSettings.parallel_running is False or prefix is None:
                params.append("-%s" % x[0])

        # Type configs
        action, type_ = _resolve_action(v)

        # Properties
        named_params = dict(
            dest=x,
            help=str(v.label),
            default=v.default,
            action=action,
            required=v.required
        )

        if type_ is not None:
            named_params["type"] = type_

        # Field has choices?
        if hasattr(v, "choices"):
            named_params["choices"] = dict(v.choices).keys()

        parser.add_argument(*params, **named_params)


# ----------------------------------------------------------------------
def _build_examples(modules):
    """
    Create usage examples

    :return: string with examples
    :rtype: str

    """
    examples = "".join(["\n  - %s.py %s ..." % (AppSettings.tool_name, x) for x in list(modules.keys())])

    return '''

Examples:%(examples)s
    ''' % dict(tool_name=str(AppSettings.tool_name),
               examples=examples)


# ----------------------------------------------------------------------
def _resolve_action(field):
    """
    Resolve argparser action and type by Field type

    :param field: BaseType object
    :type field: model.BaseType

    :return: a tuple with string with argparser type and type, as format: (str, type)
    :rtype: (str, type)
    """
    type_maps = {
        'FloatField': ("store", float),
        'StringField': ("store", str),
        'SelectField': ("store", str),
        'IntegerField': ("store", int),
        'BoolField': ("store_true", None),
        'IncrementalIntegerField': ("count", None)
    }

    in_type = field.__class__.__name__

    results = type_maps[in_type]

    return results

