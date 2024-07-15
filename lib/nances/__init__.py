# -*- coding: utf-8 -*-
"""pyRevit root level config for all pyrevit sub-modules.

Examples:
    >>> from pyrevit import DB, UI
    >>> from pyrevit import PyRevitException, PyRevitIOError

    >>> # pyrevit module has global instance of the
    >>> # _HostAppPostableCommand and _ExecutorParams classes already created
    >>> # import and use them like below
    >>> from pyrevit import HOST_APP
    >>> from pyrevit import EXEC_PARAMS
"""
#pylint: disable=W0703,C0302,C0103,C0413,raise-missing-from
import sys
import os
import os.path as op
from collections import namedtuple
import traceback
import re

import clr  #pylint: disable=E0401


PYREVIT_ADDON_NAME = 'pyRevit'
PYREVIT_CLI_NAME = 'pyrevit.exe'

# extract version from version file
VERSION_STRING = '0.0.'
with open(op.join(op.dirname(__file__), 'version'), 'r') as version_file:
    VERSION_STRING = version_file.read()
VERSION_MAJOR, VERSION_MINOR, BUILD_METADATA = \
    re.findall(r'(\d+).(\d+)(.+)', VERSION_STRING)[0]
VERSION_MAJOR = int(VERSION_MAJOR)
VERSION_MINOR = int(VERSION_MINOR)

# -----------------------------------------------------------------------------
# config environment paths
# -----------------------------------------------------------------------------
# main pyrevit repo folder
try:
    # 3 steps back for <home>/Lib/pyrevit
    HOME_DIR = op.dirname(op.dirname(op.dirname(__file__)))
except NameError:
    raise Exception('Critical Error. Can not find home directory.')

# BIN directory
BIN_DIR = op.join(HOME_DIR, 'bin')

# main pyrevit lib folders
MAIN_LIB_DIR = op.join(HOME_DIR, 'pyrevitlib')
MISC_LIB_DIR = op.join(HOME_DIR, 'site-packages')

# path to pyrevit module
MODULE_DIR = op.join(MAIN_LIB_DIR, 'pyrevit')

# loader directory
LOADER_DIR = op.join(MODULE_DIR, 'loader')

# runtime directory
RUNTIME_DIR = op.join(MODULE_DIR, 'runtime')

# addin directory
ADDIN_DIR = op.join(LOADER_DIR, 'addin')

# if loader module is available means pyRevit is being executed by Revit.
import pyrevit.engine as eng
if eng.EngineVersion != 000:
    ENGINES_DIR = op.join(BIN_DIR, 'engines', eng.EngineVersion)
# otherwise it might be under test, or documentation processing.
# so let's keep the symbols but set to None (fake the symbols)
else:
    ENGINES_DIR = None

# add the framework dll path to the search paths
sys.path.append(BIN_DIR)
sys.path.append(ADDIN_DIR)
sys.path.append(ENGINES_DIR)


PYREVIT_CLI_PATH = op.join(BIN_DIR, PYREVIT_CLI_NAME)


# now we can start importing stuff
from pyrevit.compat import safe_strtype
from pyrevit.framework import Process
from pyrevit.framework import Windows
from pyrevit.framework import Forms
from pyrevit import api
from pyrevit.api import DB, UI, ApplicationServices, AdWindows

# -----------------------------------------------------------------------------
# Base Exceptions
# -----------------------------------------------------------------------------
TRACEBACK_TITLE = 'Traceback:'


# General Exceptions
class PyRevitException(Exception):
    """Common base class for all pyRevit exceptions.

    Parameters args and message are derived from Exception class.
    """

    @property
    def msg(self):
        """Return exception message."""
        if self.args:
            return self.args[0] #pylint: disable=E1136
        else:
            return ''

    def __repr__(self):
        return str(self)

    def __str__(self):
        """Process stack trace and prepare report for output window."""
        sys.exc_type, sys.exc_value, sys.exc_traceback = sys.exc_info()
        try:
            tb_report = traceback.format_tb(sys.exc_traceback)[0]
            if self.msg:
                return '{}\n\n{}\n{}'.format(self.msg,
                                             TRACEBACK_TITLE,
                                             tb_report)
            else:
                return '{}\n{}'.format(TRACEBACK_TITLE, tb_report)
        except Exception:
            return Exception.__str__(self)


class PyRevitIOError(PyRevitException):
    """Common base class for all pyRevit io-related exceptions."""


class PyRevitCPythonNotSupported(PyRevitException):
    """Common base class for all pyRevit io-related exceptions."""
    def __init__(self, feature_name):
        super(PyRevitCPythonNotSupported, self).__init__()
        self.feature_name = feature_name

    def __str__(self):
        return self.msg

    @property
    def msg(self):
        """Return exception message."""
        return '\"{}\" is not currently supported under CPython' \
                .format(self.feature_name)


# -----------------------------------------------------------------------------
# Wrapper for __revit__ builtin parameter set in scope by C# Script Executor
# -----------------------------------------------------------------------------
# namedtuple for passing information about a PostableCommand
_HostAppPostableCommand = namedtuple('_HostAppPostableCommand',
                                     ['name', 'key', 'id', 'rvtobj'])
"""Private namedtuple for passing information about a PostableCommand

Attributes:
    name (str): Postable command name
    key (str): Postable command key string
    id (int): Postable command id
    rvtobj (``RevitCommandId``): Postable command Id Object
"""


class _HostApplication(object):
    """Private Wrapper for Current Instance of Revit.

    Provides version info and comparison functionality, alongside providing
    info on the active screen, active document and ui-document, available
    postable commands, and other functionality.

    Args:
        host_uiapp (``UIApplication``): Instance of running host.

    Example:
        >>> hostapp = _HostApplication()
        >>> hostapp.is_newer_than(2017)
    """

    def __init__(self):
        self._postable_cmds = []

    @property
    def uiapp(self):
        """Return UIApplication provided to the running command."""
        if isinstance(__revit__, UI.UIApplication):  #pylint: disable=undefined-variable
            return __revit__  #pylint: disable=undefined-variable

    @property
    def app(self):
        """Return Application provided to the running command."""
        if self.uiapp:
            return self.uiapp.Application
        elif isinstance(__revit__, ApplicationServices.Application):  #pylint: disable=undefined-variable
            return __revit__  #pylint: disable=undefined-variable

    @property
    def addin_id(self):
        """Return active addin id."""
        return self.app.ActiveAddInId

    @property
    def has_api_context(self):
        """Determine if host application is in API context"""
        return self.app.ActiveAddInId is not None

    @property
    def uidoc(self):
        """Return active UIDocument."""
        return getattr(self.uiapp, 'ActiveUIDocument', None)

    @property
    def doc(self):
        """Return active Document."""
        return getattr(self.uidoc, 'Document', None)

    @property
    def active_view(self):
        """Return view that is active (UIDocument.ActiveView)."""
        return getattr(self.uidoc, 'ActiveView', None)

    @active_view.setter
    def active_view(self, value):
        """Set the active view in user interface."""
        setattr(self.uidoc, 'ActiveView', value)

    @property
    def docs(self):
        """Return :obj:`list` of open :obj:`Document` objects."""
        return getattr(self.app, 'Documents', None)

    @property
    def available_servers(self):
        """Return :obj:`list` of available Revit server names."""
        return list(self.app.GetRevitServerNetworkHosts())

    @property
    def version(self):
        """str: Return version number (e.g. '2018')."""
        return self.app.VersionNumber

    @property
    def subversion(self):
        """str: Return subversion number (e.g. '2018.3')."""
        if hasattr(self.app, 'SubVersionNumber'):
            return self.app.SubVersionNumber
        else:
            return '{}.0'.format(self.version)

    @property
    def version_name(self):
        """str: Return version name (e.g. 'Autodesk Revit 2018')."""
        return self.app.VersionName

    @property
    def build(self):
        """str: Return build number (e.g. '20170927_1515(x64)')."""
        if int(self.version) >= 2021:
            # uses labs module that is imported later in this code
            return labs.extract_build_from_exe(self.proc_path)
        else:
            return self.app.VersionBuild

    @property
    def serial_no(self):
        """str: Return serial number number (e.g. '569-09704828')."""
        return api.get_product_serial_number()

    @property
    def pretty_name(self):
        """str: Pretty name of the host
        (e.g. 'Autodesk Revit 2019.2 build: 20190808_0900(x64)')
        """
        host_name = self.version_name
        if self.is_newer_than(2017):
            host_name = host_name.replace(self.version, self.subversion)
        return "%s build: %s" % (host_name, self.build)

    @property
    def is_demo(self):
        """bool: Determine if product is using demo license."""
        return api.is_product_demo()

    @property
    def language(self):
        """str: Return language type (e.g. 'LanguageType.English_USA')."""
        return self.app.Language

    @property
    def username(self):
        """str: Return the username from Revit API (Application.Username)."""
        uname = self.app.Username
        uname = uname.split('@')[0]  # if username is email
        # removing dots since username will be used in file naming
        uname = uname.replace('.', '')
        return uname

    @property
    def proc(self):
        """System.Diagnostics.Process: Return current process object."""
        return Process.GetCurrentProcess()

    @property
    def proc_id(self):
        """int: Return current process id."""
        return Process.GetCurrentProcess().Id

    @property
    def proc_name(self):
        """str: Return current process name."""
        return Process.GetCurrentProcess().ProcessName

    @property
    def proc_path(self):
        """str: Return file path for the current process main module."""
        return Process.GetCurrentProcess().MainModule.FileName

    @property
    def proc_window(self):
        """``intptr``: Return handle to screen hosting current process."""
        if self.is_newer_than(2019, or_equal=True):
            return self.uiapp.MainWindowHandle
        else:
            return AdWindows.ComponentManager.ApplicationWindow

    @property
    def proc_screen(self):
        """``intptr``: Return handle to screen hosting current process."""
        return Forms.Screen.FromHandle(self.proc_window)

    @property
    def proc_screen_workarea(self):
        """``System.Drawing.Rectangle``: Return screen working area."""
        screen = HOST_APP.proc_screen
        if screen:
            return screen.WorkingArea

    @property
    def proc_screen_scalefactor(self):
        """float: Return scaling for screen hosting current process."""
        screen = HOST_APP.proc_screen
        if screen:
            actual_wdith = Windows.SystemParameters.PrimaryScreenWidth
            scaled_width = screen.PrimaryScreen.WorkingArea.Width
            return abs(scaled_width / actual_wdith)

    def is_newer_than(self, version, or_equal=False):
        """bool: Return True if host app is newer than provided version.

        Args:
            version (str or int): version to check against.
        """
        if or_equal:
            return int(self.version) >= int(version)
        else:
            return int(self.version) > int(version)

    def is_older_than(self, version):
        """bool: Return True if host app is older than provided version.

        Args:
            version (str or int): version to check against.
        """
        return int(self.version) < int(version)

    def is_exactly(self, version):
        """bool: Return True if host app is equal to provided version.

        Args:
            version (str or int): version to check against.
        """
        return int(self.version) == int(version)

    def get_postable_commands(self):
        """Return list of postable commands.

        Returns:
            :obj:`list` of :obj:`_HostAppPostableCommand`
        """
        # if list of postable commands is _not_ already created
        # make the list and store in instance parameter
        if not self._postable_cmds:
            for pc in UI.PostableCommand.GetValues(UI.PostableCommand):
                try:
                    rcid = UI.RevitCommandId.LookupPostableCommandId(pc)
                    self._postable_cmds.append(
                        # wrap postable command info in custom namedtuple
                        _HostAppPostableCommand(name=safe_strtype(pc),
                                                key=rcid.Name,
                                                id=rcid.Id,
                                                rvtobj=rcid)
                        )
                except Exception:
                    # if any error occured when querying postable command
                    # or its info, pass silently
                    pass

        return self._postable_cmds

    def post_command(self, command_id):
        """Request Revit to run a command

        Args:
            command_id (str): command identifier e.g. ID_REVIT_SAVE_AS_TEMPLATE
        """
        command_id = UI.RevitCommandId.LookupCommandId(command_id)
        self.uiapp.PostCommand(command_id)



try:
    # Create an intance of host application wrapper
    # making sure __revit__ is available
    HOST_APP = _HostApplication()
except Exception:
    raise Exception('Critical Error: Host software is not supported. '
                    '(__revit__ handle is not available)')


# -----------------------------------------------------------------------------
# Wrapper to access builtin parameters set in scope by C# Script Executor
# -----------------------------------------------------------------------------
class _ExecutorParams(object):
    """Private Wrapper that provides runtime environment info."""

    @property   # read-only
    def exec_id(self):
        """Return execution unique id"""
        try:
            return __execid__
        except NameError:
            pass

    @property   # read-only
    def exec_timestamp(self):
        """Return execution timestamp"""
        try:
            return __timestamp__
        except NameError:
            pass

    @property   # read-only
    def engine_id(self):
        """Return engine id"""
        try:
            return __cachedengineid__
        except NameError:
            pass

    @property   # read-only
    def engine_ver(self):
        """str: Return PyRevitLoader.ScriptExecutor hardcoded version."""
        if eng.ScriptExecutor:
            return eng.ScriptExecutor.EngineVersion

    @property  # read-only
    def cached_engine(self):
        """bool: Check whether pyrevit is running on a cached engine."""
        try:
            return __cachedengine__
        except NameError:
            return False

    @property  # read-only
    def first_load(self):
        """bool: Check whether pyrevit is not running in pyrevit command."""
        # if no output window is set by the executor, it means that pyRevit
        # is loading at Revit startup (not reloading)
        return True if self.window_handle is None else False

    @property   # read-only
    def script_runtime(self):
        """``PyRevitLabs.PyRevit.Runtime.ScriptRuntime``: Return command."""
        try:
            return __scriptruntime__
        except NameError:
            return None

    @property   # read-only
    def output_stream(self):
        """Return ScriptIO"""
        if self.script_runtime:
            return self.script_runtime.OutputStream

    @property   # read-only
    def script_data(self):
        """Return ScriptRuntime.ScriptData"""
        if self.script_runtime:
            return self.script_runtime.ScriptData

    @property   # read-only
    def script_runtime_cfgs(self):
        """Return ScriptRuntime.ScriptRuntimeConfigs"""
        if self.script_runtime:
            return self.script_runtime.ScriptRuntimeConfigs

    @property   # read-only
    def engine_cfgs(self):
        """Return ScriptRuntime.ScriptRuntimeConfigs"""
        if self.script_runtime:
            return self.script_runtime.EngineConfigs

    @property
    def command_mode(self):
        """bool: Check if pyrevit is running in pyrevit command context."""
        return self.script_runtime is not None

    @property
    def event_sender(self):
        """``Object``: Return event sender object."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.EventSender

    @property
    def event_args(self):
        """``DB.RevitAPIEventArgs``: Return event arguments object."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.EventArgs

    @property
    def event_doc(self):
        """``DB.Document``: Return document set in event args if available."""
        if self.event_args:
            if hasattr(self.event_args, 'Document'):
                return getattr(self.event_args, 'Document')
            elif hasattr(self.event_args, 'ActiveDocument'):
                return getattr(self.event_args, 'ActiveDocument')
            elif hasattr(self.event_args, 'CurrentDocument'):
                return getattr(self.event_args, 'CurrentDocument')
            elif hasattr(self.event_args, 'GetDocument'):
                return self.event_args.GetDocument()

    @property   # read-only
    def needs_refreshed_engine(self):
        """bool: Check if command needs a newly refreshed IronPython engine."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.RefreshEngine
        else:
            return False

    @property   # read-only
    def debug_mode(self):
        """bool: Check if command is in debug mode."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.DebugMode
        else:
            return False

    @property   # read-only
    def config_mode(self):
        """bool: Check if command is in config mode."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.ConfigMode
        else:
            return False

    @property   # read-only
    def executed_from_ui(self):
        """bool: Check if command was executed from ui."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.ExecutedFromUI
        else:
            return False

    @property   # read-only
    def needs_clean_engine(self):
        """bool: Check if command needs a clean IronPython engine."""
        if self.engine_cfgs:
            return self.engine_cfgs.CleanEngine
        else:
            return False

    @property   # read-only
    def needs_fullframe_engine(self):
        """bool: Check if command needs a full-frame IronPython engine."""
        if self.engine_cfgs:
            return self.engine_cfgs.FullFrameEngine
        else:
            return False

    @property   # read-only
    def needs_persistent_engine(self):
        """bool: Check if command needs a persistent IronPython engine."""
        if self.engine_cfgs:
            return self.engine_cfgs.PersistentEngine
        else:
            return False

    @property   # read
    def window_handle(self):
        """``PyRevitLabs.PyRevit.Runtime.ScriptConsole``:
                Return output window. handle
        """
        if self.script_runtime:
            return self.script_runtime.OutputWindow

    @property
    def command_data(self):
        """``ExternalCommandData``: Return current command data."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.CommandData

    @property
    def command_elements(self):
        """``DB.ElementSet``: Return elements passed to by Revit."""
        if self.script_runtime_cfgs:
            return self.script_runtime_cfgs.SelectedElements

    @property   # read-only
    def command_path(self):
        """str: Return current command path."""
        if '__commandpath__' in __builtins__ \
                and __builtins__['__commandpath__']:
            return __builtins__['__commandpath__']
        elif self.script_runtime:
            return op.dirname(self.script_runtime.ScriptData.ScriptPath)

    @property   # read-only
    def command_config_path(self):
        """str: Return current command config script path."""
        if '__configcommandpath__' in __builtins__ \
                and __builtins__['__configcommandpath__']:
            return __builtins__['__configcommandpath__']
        elif self.script_runtime:
            return op.dirname(self.script_runtime.ScriptData.ConfigScriptPath)

    @property   # read-only
    def command_name(self):
        """str: Return current command name."""
        if '__commandname__' in __builtins__ \
                and __builtins__['__commandname__']:
            return __builtins__['__commandname__']
        elif self.script_runtime:
            return self.script_runtime.ScriptData.CommandName

    @property   # read-only
    def command_bundle(self):
        """str: Return current command bundle name."""
        if '__commandbundle__' in __builtins__ \
                and __builtins__['__commandbundle__']:
            return __builtins__['__commandbundle__']
        elif self.script_runtime:
            return self.script_runtime.ScriptData.CommandBundle

    @property   # read-only
    def command_extension(self):
        """str: Return current command extension name."""
        if '__commandextension__' in __builtins__ \
                and __builtins__['__commandextension__']:
            return __builtins__['__commandextension__']
        elif self.script_runtime:
            return self.script_runtime.ScriptData.CommandExtension

    @property   # read-only
    def command_uniqueid(self):
        """str: Return current command unique id."""
        if '__commanduniqueid__' in __builtins__ \
                and __builtins__['__commanduniqueid__']:
            return __builtins__['__commanduniqueid__']
        elif self.script_runtime:
            return self.script_runtime.ScriptData.CommandUniqueId

    @property   # read-only
    def command_controlid(self):
        """str: Return current command control id."""
        if '__commandcontrolid__' in __builtins__ \
                and __builtins__['__commandcontrolid__']:
            return __builtins__['__commandcontrolid__']
        elif self.script_runtime:
            return self.script_runtime.ScriptData.CommandControlId

    @property   # read-only
    def command_uibutton(self):
        """str: Return current command ui button."""
        if '__uibutton__' in __builtins__ \
                and __builtins__['__uibutton__']:
            return __builtins__['__uibutton__']

    @property
    def doc_mode(self):
        """bool: Check if pyrevit is running by doc generator."""
        try:
            return __sphinx__
        except NameError:
            return False

    @property
    def result_dict(self):
        """``Dictionary<String, String>``: Return results dict for logging."""
        if self.script_runtime:
            return self.script_runtime.GetResultsDictionary()


# create an instance of _ExecutorParams wrapping current runtime.
EXEC_PARAMS = _ExecutorParams()


# -----------------------------------------------------------------------------
# type to safely get document instance from app or event args
# -----------------------------------------------------------------------------

class _DocsGetter(object):
    """Instance to safely get document from HOST_APP instance or EXEC_PARAMS"""

    @property
    def doc(self):
        """Active document"""
        return HOST_APP.doc or EXEC_PARAMS.event_doc

    @property
    def docs(self):
        """List of active documents"""
        return HOST_APP.docs


DOCS = _DocsGetter()

# -----------------------------------------------------------------------------
# config user environment paths
# -----------------------------------------------------------------------------
# user env paths
if EXEC_PARAMS.doc_mode:
    ALLUSER_PROGRAMDATA = USER_ROAMING_DIR = USER_SYS_TEMP = USER_DESKTOP = \
    EXTENSIONS_DEFAULT_DIR = THIRDPARTY_EXTENSIONS_DEFAULT_DIR = ' '
else:
    ALLUSER_PROGRAMDATA = os.getenv('programdata')
    USER_ROAMING_DIR = os.getenv('appdata')
    USER_SYS_TEMP = os.getenv('temp')
    USER_DESKTOP = op.expandvars('%userprofile%\\desktop')

    # verify directory per issue #369
    if not USER_DESKTOP or not op.exists(USER_DESKTOP):
        USER_DESKTOP = USER_SYS_TEMP

    # default extensions directory
    EXTENSIONS_DEFAULT_DIR = op.join(HOME_DIR, 'extensions')
    THIRDPARTY_EXTENSIONS_DEFAULT_DIR = \
        op.join(USER_ROAMING_DIR, PYREVIT_ADDON_NAME, 'Extensions')

# create paths for pyrevit files
if EXEC_PARAMS.doc_mode:
    PYREVIT_ALLUSER_APP_DIR = PYREVIT_APP_DIR = PYREVIT_VERSION_APP_DIR = ' '
else:
    # pyrevit file directory
    PYREVIT_ALLUSER_APP_DIR = op.join(ALLUSER_PROGRAMDATA, PYREVIT_ADDON_NAME)
    PYREVIT_APP_DIR = op.join(USER_ROAMING_DIR, PYREVIT_ADDON_NAME)
    PYREVIT_VERSION_APP_DIR = op.join(PYREVIT_APP_DIR, HOST_APP.version)

    # add runtime paths to sys.paths
    # this will allow importing any dynamically compiled DLLs that
    # would be placed under this paths.
    for pyrvt_app_dir in [PYREVIT_APP_DIR,
                          PYREVIT_VERSION_APP_DIR,
                          THIRDPARTY_EXTENSIONS_DEFAULT_DIR]:
        if not op.isdir(pyrvt_app_dir):
            try:
                os.mkdir(pyrvt_app_dir)
                sys.path.append(pyrvt_app_dir)
            except Exception as err:
                raise PyRevitException('Can not access pyRevit '
                                       'folder at: {} | {}'
                                       .format(pyrvt_app_dir, err))
        else:
            sys.path.append(pyrvt_app_dir)


# -----------------------------------------------------------------------------
# standard prefixes for naming pyrevit files (config, appdata and temp files)
# -----------------------------------------------------------------------------
if EXEC_PARAMS.doc_mode:
    PYREVIT_FILE_PREFIX_UNIVERSAL = PYREVIT_FILE_PREFIX = \
        PYREVIT_FILE_PREFIX_STAMPED = None
    PYREVIT_FILE_PREFIX_UNIVERSAL_USER = PYREVIT_FILE_PREFIX_USER = \
        PYREVIT_FILE_PREFIX_STAMPED_USER = None
else:
    # e.g. pyRevit_
    PYREVIT_FILE_PREFIX_UNIVERSAL = '{}_'.format(PYREVIT_ADDON_NAME)
    PYREVIT_FILE_PREFIX_UNIVERSAL_REGEX = \
        r'^' + PYREVIT_ADDON_NAME + r'_(?P<fname>.+)'

    # e.g. pyRevit_2018_
    PYREVIT_FILE_PREFIX = '{}_{}_'.format(PYREVIT_ADDON_NAME,
                                          HOST_APP.version)
    PYREVIT_FILE_PREFIX_REGEX = \
        r'^' + PYREVIT_ADDON_NAME + r'_(?P<version>\d{4})_(?P<fname>.+)'

    # e.g. pyRevit_2018_14422_
    PYREVIT_FILE_PREFIX_STAMPED = '{}_{}_{}_'.format(PYREVIT_ADDON_NAME,
                                                     HOST_APP.version,
                                                     HOST_APP.proc_id)
    PYREVIT_FILE_PREFIX_STAMPED_REGEX = \
        r'^' + PYREVIT_ADDON_NAME \
        + r'_(?P<version>\d{4})_(?P<pid>\d+)_(?P<fname>.+)'

    # e.g. pyRevit_eirannejad_
    PYREVIT_FILE_PREFIX_UNIVERSAL_USER = '{}_{}_'.format(PYREVIT_ADDON_NAME,
                                                         HOST_APP.username)
    PYREVIT_FILE_PREFIX_UNIVERSAL_USER_REGEX = \
        r'^' + PYREVIT_ADDON_NAME + r'_(?P<user>.+)_(?P<fname>.+)'

    # e.g. pyRevit_2018_eirannejad_
    PYREVIT_FILE_PREFIX_USER = '{}_{}_{}_'.format(PYREVIT_ADDON_NAME,
                                                  HOST_APP.version,
                                                  HOST_APP.username)
    PYREVIT_FILE_PREFIX_USER_REGEX = \
        r'^' + PYREVIT_ADDON_NAME \
        + r'_(?P<version>\d{4})_(?P<user>.+)_(?P<fname>.+)'

    # e.g. pyRevit_2018_eirannejad_14422_
    PYREVIT_FILE_PREFIX_STAMPED_USER = '{}_{}_{}_{}_'.format(PYREVIT_ADDON_NAME,
                                                             HOST_APP.version,
                                                             HOST_APP.username,
                                                             HOST_APP.proc_id)
    PYREVIT_FILE_PREFIX_STAMPED_USER_REGEX = \
        r'^' + PYREVIT_ADDON_NAME \
        + r'_(?P<version>\d{4})_(?P<user>.+)_(?P<pid>\d+)_(?P<fname>.+)'

# -----------------------------------------------------------------------------
# config labs modules
# -----------------------------------------------------------------------------
from pyrevit import labs



"""ARC"""
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
from rpw.ui.forms import Alert
import pickle
import os.path as op
import os
import sys
import pyrevit
from pyrevit import coreutils
from pyrevit import revit
import platform
from Autodesk.Revit.DB import (FilteredElementCollector,Element, View, ElementId, FamilyInstance, FillPatternElement, Color, OverrideGraphicSettings,FilteredElementCollector, BuiltInCategory)
from nances import forms

PYREVIT_ADDON_NAME = 'pyRevit'
PYREVIT_FILE_PREFIX = '{}_'.format(PYREVIT_ADDON_NAME)
USER_ROAMING_DIR = os.getenv('appdata')
PYREVIT_APP_DIR = op.join(USER_ROAMING_DIR, PYREVIT_ADDON_NAME)
PYREVIT_VERSION_APP_DIR = op.join(PYREVIT_APP_DIR)

#Get UIDocument
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
# Def nay cho current element
def get_selected_elements(tem_uidoc, tem_doc, noti = True):
    selection = tem_uidoc.Selection
    selection_ids = selection.GetElementIds()
    elements = []
    for element_id in selection_ids:
        elements.append(tem_doc.GetElement(element_id))

    if len(elements) == 0:
        if noti:
            from Autodesk.Revit.UI import TaskDialog
            # module_path = Autodesk.__file__
            # print module_path
            dialog = TaskDialog("ARC")
            from pyrevit.coreutils import applocales
            current_applocale = applocales.get_current_applocale()
            if str(current_applocale) == "日本語 / Japanese (ja)":
                message = "このツールを使用する前に要素をご選択ください。"
            else:
                message = "Please select element before use this tool."
            dialog.MainContent = message
            dialog.TitleAutoPrefix = False
            dialog.Show()
        return False
    else: 
        return elements
    
def get_elements(iuidoc,idoc, string_warning_bar, noti = False):
    selected_element = get_selected_elements(iuidoc,idoc, noti)
    if selected_element == False:
        list_ele = []
        with forms.WarningBar(title=string_warning_bar):
            try:
                pick = iuidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element)
                for tung_ref in pick:
                    list_ele.append(idoc.GetElement(tung_ref.ElementId))
            except:
                sys.exit()
            selected_element = list_ele
    return selected_element

def get_element(iuidoc,idoc, string_warning_bar, noti = False):
    selected_element = get_selected_elements(iuidoc,idoc, noti)
    if selected_element == False:
        list_ele = []
        with forms.WarningBar(title=string_warning_bar):
            try:
                pick = iuidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element)
                list_ele.append(idoc.GetElement(pick.ElementId))
            except:
                sys.exit()
            selected_element = list_ele
    return selected_element


# Code nay de lay thong tin chip cua may tinh
def information():
    info = platform.processor()
    newma = "/M%A*D/".join(info)
    return (newma)

# Def join geometry
def joingeometry(idoc,List1, List2):
    if checklicense():
        CountSwitchJoin = []
        Join = []
        for i in List1:
            Bdb = i.get_BoundingBox(None)
            Outlineofbb = (Outline(Bdb.Min, Bdb.Max))
            for intersected in Autodesk.Revit.DB.FilteredElementCollector(idoc).WherePasses(Autodesk.Revit.DB.BoundingBoxIntersectsFilter(Outlineofbb)):
            # Check xem list filter
                for a in List2:
                    if a.Id == intersected.Id:
                # Code join geometry
                        try:
                            result = Autodesk.Revit.DB.JoinGeometryUtils.JoinGeometry(idoc,i,intersected)
                            checkcutting = Autodesk.Revit.DB.JoinGeometryUtils.IsCuttingElementInJoin(idoc,i,intersected)
                            Join.Add("OK")
                            if str(checkcutting) == "False":
                                switchjoin = Autodesk.Revit.DB.JoinGeometryUtils.SwitchJoinOrder(idoc,i,intersected)
                        except:
                            try:
                                checkcutting = Autodesk.Revit.DB.JoinGeometryUtils.IsCuttingElementInJoin(idoc,i,intersected)
                                if str(checkcutting) == "False":
                                    switchjoin = Autodesk.Revit.DB.JoinGeometryUtils.SwitchJoinOrder(idoc,i,intersected)
                                    CountSwitchJoin.append("OK")
                            except:
                                pass
        LenJoin = str(len (Join))
        LenSwitchjoin = str(len (CountSwitchJoin))
        Mes = "Joined: " + LenJoin + " and Switch join: " + LenSwitchjoin
        Alert(Mes,title="Mes",header= "Report number Join and Switch joined")
    return 



# So sanh license
def machinecode(input):
    info = platform.processor()
    a_string = bytes.fromhex(input)
    a_string = a_string.decode("ascii")
    if a_string == info:
        check = "OK"
    else:
        check = "Not OK"
    return check



'''cai nay check key'''

def _get_app_file(file_id, file_ext,
                filename_only=False, stamped=False, universal=False):
    appdata_folder = PYREVIT_VERSION_APP_DIR
    file_prefix = PYREVIT_FILE_PREFIX
    if stamped:
        file_prefix = pyrevit.PYREVIT_FILE_PREFIX_STAMPED
    elif universal:
        appdata_folder = PYREVIT_APP_DIR
        file_prefix = pyrevit.PYREVIT_FILE_PREFIX_UNIVERSAL

    full_filename = '{}{}.{}'.format(file_prefix, file_id, file_ext)
    if filename_only:
        return full_filename
    else:
        return op.join(
            appdata_folder,
            coreutils.cleanup_filename(full_filename)
            )

def get_data_file(file_id, file_ext, name_only=False):
    return _get_app_file(file_id, file_ext, filename_only=name_only)

def get_document_data_file(file_id, file_ext, add_cmd_name=False):
    proj_info = revit.query.get_project_info()
    # print (proj_info)
    if add_cmd_name:
        script_file_id = '{}_{}'.format(EXEC_PARAMS.command_name,
                                        file_id)
                                        #    proj_info.filename
                                        #    or proj_info.name)
    else:
        script_file_id = '{}'.format(file_id)
                                        # proj_info.filename
                                        # or proj_info.name)
    # print (get_data_file(script_file_id, file_ext))
    return get_data_file(script_file_id, file_ext)


'''Check lisence'''
info = platform.processor()
def checklicense():
    check =''
    datafile = get_document_data_file("pyrevit", "dll")
    try:
        f = open(datafile, 'r')
        current_selection = pickle.load(f)
        f.close()
        newstring= current_selection[:-2]
        a_string = bytes.fromhex(newstring)
        a_string = a_string.decode("ascii")
        if a_string == info:
            check = 'OK'
        else:
            check = "Not OK"
            sys.exit()
    except Exception:
        pass
    return check


'''check lisence, giong cai check lisence nhung no khong co dong sys.exit()'''
def checklicense_for_info():
    check =''
    datafile = get_document_data_file("pyrevit", "dll")
    try:
        f = open(datafile, 'r')
        current_selection = pickle.load(f)
        f.close()
        newstring= current_selection[:-2]
        a_string = bytes.fromhex(newstring)
        a_string = a_string.decode("ascii")
        if a_string == info:
            check = 'OK'
        else:
            check = "Not OK"
    except Exception:
        pass
    return check
def AutodeskData():
    datafile = get_document_data_file("pyrevit", "dll")
    if datafile:
        try:
            f = open(datafile, 'r')
            current_selection = pickle.load(f)
            f.close()
            newstring= current_selection[:-2]
            a_string = bytes.fromhex(newstring)
            a_string = a_string.decode("ascii")
            if a_string == info:
                check = "OK"
            return check
        except Exception:
            thong_bao_loi_license()
            pass
            return False
    else:
        thong_bao_loi_license()
    return False

def thong_bao_loi_license():
    tin_nhan = "Hãy mở khóa Add-in.\nSử dụng command [Get info] và gửi mã tới skype của Sơn\nhoặc email:nguyenthanhson1712@gmail.com\n\n\nこちらのツールを使用するには、\nアドインをロック解除する必要があります。\nコマンド [Get info] を使用してコードを取得し、その後\nSonのSkypeまたは以下のメールアドレスに送信してください：nguyenthanhson1712@gmail.com"
    MessageBox.Show(tin_nhan, "ARC", MessageBoxButtons.OK, MessageBoxIcon.Information)

def machine_code():
    info = platform.processor()
    newma = "/M%A*D/".join(info)
    return newma

def all_elements_of_category(idoc, category):
	return FilteredElementCollector(idoc).OfCategory(category).WhereElementIsNotElementType().ToElements()

def override_graphics_in_view(idoc, view, list_element_id, color):
    name_pattern = "<Solid fill>"
    patterns = FilteredElementCollector(idoc).OfClass(FillPatternElement)
    for pattern in patterns:
        if pattern.Name == name_pattern:
            solidPatternId = pattern.Id
    override = OverrideGraphicSettings()
    for i in list_element_id:
        override.SetSurfaceForegroundPatternColor(color)
        override.SetSurfaceForegroundPatternId(solidPatternId)
        override.SetCutForegroundPatternColor(color)
        override.SetCutForegroundPatternId(solidPatternId)
        view.SetElementOverrides(i, override)
    return
def Active_view(idoc):
    AcView= idoc.ActiveView
    return AcView

def get_parameter_by_name(element, name, is_UTF8 = False):
    import base64
    if is_UTF8 == True:
        base64_encoded = base64.b64decode(name).decode('utf-8')
        list_param = element.GetParameters(base64_encoded)
        param = list_param[0]
    else:
        list_param = element.GetParameters(name)
        param = list_param[0]    
    return param    

def get_builtin_parameter_by_name(element, built_in_parameter):
    # vi du: is_structure = module.get_builtin_parameter_by_name(element, BuiltInParameter.FLOOR_PARAM_IS_STRUCTURAL)
    param = element.get_Parameter(built_in_parameter)
    return param    

def get_parameter_value_by_name(element, name, is_UTF8 = False):
    import base64
    if is_UTF8 == True:
        base64_encoded = base64.b64decode(name).decode('utf-8')
        list_param = element.GetParameters(base64_encoded)
        param = list_param[0]
    else:
        list_param = element.GetParameters(name)
        param = list_param[0]    
    return param.AsValueString()   

def set_parameter_value_by_name(element, name, value, is_UTF8 = False):
    import base64
    if is_UTF8 == True:
        base64_encoded = base64.b64decode(name).decode('utf-8')
        list_param = element.GetParameters(base64_encoded)
        param = list_param[0]
    else:
        list_param = element.GetParameters(name)
        param = list_param[0]
    set_param = param.Set(value)            
    return set_param

def get_type(idoc, element):
    type_id = element.GetTypeId()
    get_type = idoc.GetElement(type_id)
    return get_type

def get_type_name (idoc, element):
    type_id = element.GetTypeId()
    get_type = idoc.GetElement(type_id)
    def_type_name = Autodesk.Revit.DB.Element.Name.GetValue(get_type)
    return def_type_name

def all_type_of_class_and_OST (idoc, ofClass, BuiltInCategory_OST):
    #Class nao xuat hien trong Revit API thi moi get type duoc
    # vi du: list_type = all_type_of_class_and_OST(doc, FloorType, BuiltInCategory.OST_Floors)
    # vi du ve framing: list_type = all_type_of_class_and_OST(FamilySymbol, BuiltInCategory.OST_StructuralFraming)
    all_OST_type = FilteredElementCollector(idoc).OfClass(ofClass).OfCategory(BuiltInCategory_OST)
    return all_OST_type

def get_all_elements_of_OST(idoc, BuiltInCategory_OST):
    collector = FilteredElementCollector(idoc).OfCategory(BuiltInCategory_OST).WhereElementIsNotElementType().ToElements()
    return collector

def get_all_elements_of_OST_in_current_view(idoc, BuiltInCategory_OST):
    collector = FilteredElementCollector(idoc, idoc.ActiveView.Id).OfCategory(BuiltInCategory_OST).WhereElementIsNotElementType().ToElements()
    return collector


def active_symbol(family_symbol):
    try:
        if family_symbol.IsActive == False:
            family_symbol.Activate()
    except:
        pass
    return 

def flatten_list(input_list):
    flat_list = [item for sublist in input_list for item in sublist]
    return flat_list

def create_plane_from_point_and_normal(point, normal):
    plane = Autodesk.Revit.DB.Plane(normal, point)
    return plane

def are_planes_parallel(normal1, normal2):
    tolerance=0.0000001
    cross_product = normal1.CrossProduct(normal2)
    return cross_product.GetLength() < tolerance

def distance_between_planes(normal1, point_on_plane1, normal2):
    vector_between_planes = point_on_plane1 - (point_on_plane1.DotProduct(normal2) - normal2.DotProduct(normal1)) / normal1.DotProduct(normal2) * normal1
    distance = vector_between_planes.GetLength()
    return distance

def get_center_line_of_wall(wall):
    wall_location = wall.Location
    wall_location_curve = wall_location.Curve
    return wall_location_curve

def create_plane_follow_line (line):
    start_point = line.GetEndPoint(0)
    end_point = line.GetEndPoint(1)
    mid_point = line.Evaluate(0.5, True)
    offset_mid_point = XYZ(start_point.X, start_point.Y, mid_point.Z +10000)
    point1 = start_point
    point2 = end_point
    point3 =offset_mid_point
    vector1 = point2 - point1
    vector2 = point3 - point1
    normal_vector = vector1.CrossProduct(vector2).Normalize()
    plane = Plane.CreateByNormalAndOrigin(normal_vector, mid_point)
    return plane

def get_geometry_ver_2(element):
    option = Options()
    option.ComputeReferences = True
    geo_ref =  element.get_Geometry(option)
    return geo_ref

def get_geometry(element, view):
    geo_opt = Options()
    geo_opt.ComputeReferences = True
    geo_opt.IncludeNonVisibleObjects = True
    geo_opt.View = view
    geo_ref =  element.get_Geometry(geo_opt)
    return geo_ref

def get_face(geometry):
    list_faces =[]
    for geometry_object in geometry:
        if hasattr(geometry_object, "Faces"):
            for face in geometry_object.Faces:
                if str(type(face)) == "<type 'PlanarFace'>":
                    list_faces.append(face)
    return list_faces


def distance_from_point_to_plane(point, plane):
    distance = plane.Normal.DotProduct(point - plane.Origin)
    return distance


def distance_between_parallel_planes(plane1, plane2):
    point_on_plane = XYZ(0, 0, 0)
    distance1 = abs(distance_from_point_to_plane(point_on_plane, plane1))
    distance2 = abs(distance_from_point_to_plane(point_on_plane, plane2))
    distance = (distance1 - distance2)
    return distance

def get_rotate_90_location_wall (wall):
    from Autodesk.Revit.DB import Line, BuiltInParameter
    wall_location = wall.Location
    wall_location_curve = wall_location.Curve
    start = wall_location_curve.GetEndPoint(0)
    end = wall_location_curve.GetEndPoint(1)
    flat_start = XYZ(start.X,start.Y, start.Z)
    flat_end =  XYZ(end.X,end.Y, start.Z)
    flat_line =  Line.CreateBound(flat_start,flat_end)
    mid_point = flat_line.Evaluate(0.5, True)
    Z_point = XYZ(mid_point.X, mid_point.Y, mid_point.Z + 10)
    Z_axis = Line.CreateBound(mid_point, Z_point)
    curve_of_location_curve = Line.CreateBound(flat_start,flat_end)
    detail_curve_of_location_curve = doc.Create.NewDetailCurve(Currentview,curve_of_location_curve)
    locate_detail_curve_of_location_curve = detail_curve_of_location_curve.Location
    rotate_locate_detail_curve_of_location_curve = locate_detail_curve_of_location_curve.Rotate(Z_axis, 2 * math.pi / 4)
    direction_of_wall = flat_line.Direction
    Scale = Currentview.Scale
    Snap_dim = 4.5 * 0.0032808 #1mm bang 0.0032808feet
    Vector_for_scale = Snap_dim * Scale *direction_of_wall
    move_detail_curve = locate_detail_curve_of_location_curve.Move(Vector_for_scale)
    return detail_curve_of_location_curve

def get_wall_reference_by_magic(uid,index):
    format = "{0}:{1}:{2}"
    nine = -9999
    refString = str.Format(format,uid,nine,index)
    return refString


def get_wall_reference_by_type(uid,index):
    from Autodesk.Revit.DB import Reference
    format = "{0}:{1}:{2}"
    type = 'SURFACE'
    refString = str.Format(format,uid,index,type)
    return refString

def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point


def get_all_grid():
    collector = FilteredElementCollector(doc).OfClass(Grid)
    grids = collector.ToElements()
    return grids
def get_all_geometry_of_grids(grid, DatumExtentType = DatumExtentType.ViewSpecific):
    all_geometry = []
    DatumExtentType = DatumExtentType.ViewSpecific
    try:
        geometry_element = grid.GetCurvesInView(DatumExtentType,Currentview)
        all_geometry.append(geometry_element)
    except:
        pass
    return all_geometry

def check_hide_isolate(view, element):
    view_mode = TemporaryViewMode.TemporaryHideIsolate
    boolean = view.IsElementVisibleInTemporaryViewMode(view_mode, element.Id)
    return boolean
def check_hidden(element, view):
    boolean = element.IsHidden(view)
    not_boolean = not(boolean)
    return not_boolean

def create_beam(curve,beam_type,level):
    beam = doc.Create.NewFamilyInstance(curve, beam_type, level, Autodesk.Revit.DB.Structure.StructuralType.Beam)
    param_start_offset = get_parameter_by_name(beam, "Start Level Offset", False)
    param_end_offset = param_start_offset = get_parameter_by_name(beam, "End Level Offset", False)
    param_start_offset.Set(0)
    param_end_offset.Set(0)
    return beam

def active_symbol(element):
    try:
        if element.IsActive == False:
            element.Activate()
    except:
        pass
    return 

def curve_from_dwg(dwg, Layer_name, view):
# Nhap layer cua line trong dwg
# Khai bao option cua "get_Geometry"
    geo_opt = Autodesk.Revit.DB.Options()
    geo_opt.ComputeReferences = True
    geo_opt.IncludeNonVisibleObjects = True
    geo_opt.View = view
    list_curve=[]
# get_Geometry cua tat ca line trong file dwg
    geometry = dwg.get_Geometry(geo_opt)
    for geo_inst in geometry:
        geo_elem = geo_inst.GetInstanceGeometry()
        for polyline in geo_elem:
            element = doc.GetElement(polyline.GraphicsStyleId)
            if not element:
                continue

# Kiem tra layer cua line trong file dwg thong qua "GraphicsStyleCategory.Name"
# Dung de ve cac doi tuong "polyline"
            is_target_layer = element.GraphicsStyleCategory.Name == Layer_name
            is_polyline = polyline.GetType().Name == "PolyLine"
            if is_polyline and is_target_layer:

                begin = None
                for pts in polyline.GetCoordinates():
                    if not begin:
                        begin = pts
                        continue
                    end = pts
                    line = Autodesk.Revit.DB.Line.CreateBound(begin, end)
                    list_curve.append(line)
                    # det_line = doc.Create.NewDetailCurve(acview, line)
                    begin = pts

# Dung de ve cac doi tuong "line"
            is_line = polyline.GetType().Name == "Line"
            if is_line and is_target_layer:
                    straight_line = polyline
                    list_curve.append(straight_line)
                    # det_line = doc.Create.NewDetailCurve(acview, straight_line)
# Dung de ve cac doi tuong "arc"
            is_arc = polyline.GetType().Name == "Arc"
            if is_arc and is_target_layer:
                arc = polyline
                list_curve.append(arc)
                # det_line = doc.Create.NewDetailCurve(acview, arc) #Neu khong ve detail line thi thoi khong dung
    return list_curve


#  Dung de cut geometry
def cut_geometry(idoc, List1, List2):
    Cut = []
    import Autodesk
    for i in List1:
        Bdb = i.get_BoundingBox(None)
        Outlineofbb = (Autodesk.Revit.DB.Outline(Bdb.Min, Bdb.Max))
        for intersected in Autodesk.Revit.DB.FilteredElementCollector(doc).WherePasses(Autodesk.Revit.DB.BoundingBoxIntersectsFilter(Outlineofbb)):
        # Check xem list filter
            for a in List2:
                if a.Id == intersected.Id:
                    try:
                        Autodesk.Revit.DB.SolidSolidCutUtils.AddCutBetweenSolids(idoc,i, a)
                        Cut.Add("OK")
                    except:
                        try:
                            Autodesk.Revit.DB.InstanceVoidCutUtils.AddInstanceVoidCut(idoc,i, a)
                            Cut.Add("OK")
                        except:
                            pass
    len_cut = str(len (Cut))
    Mes = "Cut: " + len_cut
    Alert(Mes,title="Mes",header= "Report number Join and Switch joined")
    return Cut

def cut_geometry_all(idoc, List1, List2):
    import Autodesk
    for i in List1:
            for a in List2:
                try:
                    Autodesk.Revit.DB.SolidSolidCutUtils.AddCutBetweenSolids(idoc,i, a)
                except:
                    try:
                        Autodesk.Revit.DB.InstanceVoidCutUtils.AddInstanceVoidCut(idoc,i, a)
                    except:
                        pass
    return

def get_current_selection(iuidoc,elements):
    select = iuidoc.Selection
    listid = []
    for i in elements:
        i_id = i.Id
        listid.append(i_id)
    Icollection = List[ElementId](listid)
    select.SetElementIds(Icollection)
    return 

def encode_to_base64(input_string):
    import base64
    input_bytes = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(input_bytes)  
    return base64_bytes



def angle_between_planes(plane1, plane2):
    import math
    normal1 = plane1.Normal
    normal2 = plane2.Normal
    dot_product = normal1.DotProduct(normal2)
    magnitude1 = normal1.GetLength()
    magnitude2 = normal2.GetLength()
    
    if magnitude1 == 0 or magnitude2 == 0:
        return None    
    cos_angle = dot_product / (magnitude1 * magnitude2)
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def degrees_to_radians(degrees):
    import math
    radians = degrees * (math.pi / 180)
    return radians

"Form"
import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import MessageBox, MessageBoxButtons, MessageBoxIcon
def message_box(message):
    MessageBox.Show(message, "ARC", MessageBoxButtons.OK, MessageBoxIcon.Information)

# math
import Autodesk
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from System.Collections.Generic import *

def get_nearest_point(points, reference_point):

    min_distance = float('inf')
    nearest_point = None
    
    for point in points:
        distance = point.DistanceTo(reference_point)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    return nearest_point


def distance_2_point(point , reference_point):
    distance = point.DistanceTo(reference_point)
    return distance

def xac_dinh_kich_co_chu (view,value, one_unit_width = 1.85): #don vi phai la mm
    round_format_value = round(value,2)
    formatted_value = str(round_format_value).rstrip('0').rstrip('.') #don vi mm
    len_formatted_value = len(formatted_value) #co bao nhieu ky tu, vi du 200 in ra la 3 
    width_text = float(len_formatted_value * one_unit_width * (view.Scale)) #don vi mm trong moi truong view (khong phai ban ve)
    return width_text


def move_point_along_vector(point, vector, distance):
    new_point = point + vector.Normalize() * distance
    return new_point



def add_prefix_to_dimension(dimension):
    try:
        dimension.Prefix = "W="
    except:
        pass    

def orientation_mat_bang(A, B, vector):
    C = move_point_along_vector(B, vector, 1)
    # Chuyển đổi tọa độ thành tuple
    # Vector AB
    vector_AB = (B.X - A.X, B.Y - A.Y)
    # Vector BC
    vector_BC = (C.X - B.X, C.Y - B.Y)
    # Tính cross product
    cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
    # Xác định hướng dựa trên dấu của cross product
    if cross_product > 0:
        ket_qua = "Bên trái"
    elif cross_product < 0:
        ket_qua = "Bên phải"
    else:
        ket_qua= "Thẳng hàng"        
    return ket_qua

def orientation_mat_cat(A, B, vector):
    C = move_point_along_vector(B, vector, 1)
    # Chuyển đổi tọa độ thành tuple
    # Vector AB
    vector_AB = (B.Z - A.Z, B.Y - A.Y)
    # Vector BC
    vector_BC = (C.Z - B.Z, C.Y - B.Y)
    # Tính cross product
    cross_product = vector_AB[0] * vector_BC[1] - vector_AB[1] * vector_BC[0]
    # Xác định hướng dựa trên dấu của cross product
    if cross_product > 0:
        ket_qua = "Bên trái"
    elif cross_product < 0:
        ket_qua = "Bên phải"
    else:
        ket_qua= "Thẳng hàng"        
    return ket_qua


def distance_mat_bang(point1, point2):
    return ((point2.X - point1.X)**2 + (point2.Y - point1.Y)**2)**0.5

def distance_mat_cat(point1, point2):
    return ((point2.Z - point1.Z)**2 + (point2.Y - point1.Y)**2)**0.5


def distance_from_point_to_element_mat_bang(point1, obj):
    return distance_mat_bang(point1, obj.Origin)

def distance_from_point_to_element_mat_cat(point1, obj):
    return distance_mat_cat(point1, obj.Origin)

def sort_points_by_distance(A, points_list):
    # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
    sorted_points = sorted(points_list, key=lambda point: distance_mat_bang(A, point), reverse=True)
    return sorted_points


def sort_seg_by_distance_mat_bang(A, seg_list):
    # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
    sorted_points = sorted(seg_list, key=lambda obj: distance_from_point_to_element_mat_bang(A, obj), reverse=True)
    return sorted_points

def sort_seg_by_distance_mat_cat(A, seg_list):
    # Sắp xếp các điểm trong list dựa trên khoảng cách từ xa đến gần điểm A
    sorted_points = sorted(seg_list, key=lambda obj: distance_from_point_to_element_mat_cat(A, obj), reverse=True)
    return sorted_points


def move_segment_xa_nhat (list_sorted, vector_cua_dim, kich_co_chu, khoang_cach_dim_toi_text, huong_phai = True):

    seg_xa_nhat= list_sorted[0]

    value_segment = seg_xa_nhat.Value
    
    vi_tri = seg_xa_nhat.Origin

    cong_thuc = ((kich_co_chu/304.8)/2) + ((value_segment)/2) + khoang_cach_dim_toi_text
    if huong_phai:
        move = move_point_along_vector(vi_tri, vector_cua_dim, cong_thuc) #move theo don vi feet
    else:
        move = move_point_along_vector(vi_tri, -vector_cua_dim, cong_thuc) #move theo don vi feet
    
    seg_xa_nhat.TextPosition = move

    return 

def chuan_hoa_vector_mat_bang(vector): #vector tu trai qua phai, tu duoi len tren
    point_start = DB.XYZ(0,0,0)
    point_end = move_point_along_vector(point_start, vector, 1)

    if abs(vector.X) < abs(vector.Y):
        if point_start.Y < point_end.Y:
            return vector          
        else:
            return - vector
    elif point_start.X < point_end.X:
        return vector 
    else: 
        return - vector
    
def chuan_hoa_vector_mat_cat(vector): #vector tu trai qua phai, tu duoi len tren
    point_start = DB.XYZ(0,0,0)
    point_end = move_point_along_vector(point_start, vector, 1)

    if abs(vector.Z) < abs(vector.Y):
        if point_start.Y < point_end.Y:
            return vector          
        else:
            return - vector
    elif point_start.Z < point_end.Z:
        return vector 
    else: 
        return - vector
    
def pick_point_with_nearest_snap(iuidoc):       
    snap_settings = UI.Selection.ObjectSnapTypes.None
    prompt = "Click"
    try:
        click_point = iuidoc.Selection.PickPoint(snap_settings, prompt)
    except:
        # print(traceback.format_exc())
        pass
    return click_point

def set_work_plane_for_view(view):
    current_work_plane = view.SketchPlane
    if current_work_plane is None:
        sketch_plane = view.SketchPlane
        try:
            sketch_plane = Autodesk.Revit.DB.SketchPlane.Create(view.Document, Autodesk.Revit.DB.Plane.CreateByNormalAndOrigin(view.ViewDirection, view.Origin))
            view.SketchPlane = sketch_plane
        except:
            pass
    return True




class DimensionSelectionFilter(Autodesk.Revit.UI.Selection.ISelectionFilter):
    def AllowElement(self, element):
        # Chỉ cho phép chọn đối tượng Dimension
        return isinstance(element, Autodesk.Revit.DB.Dimension)

    def AllowReference(self, reference, point):
        # Không sử dụng AllowReference trong trường hợp này
        return False

# Hàm chọn một Dimension từ danh sách sử dụng ISelectionFilter
def pick_dimension_element(iuidoc,idoc):
    selected_dimension = iuidoc.Selection.PickObject(Autodesk.Revit.UI.Selection.ObjectType.Element, DimensionSelectionFilter(), "Pick 1 Dimension")
    return idoc.GetElement(selected_dimension.ElementId) if selected_dimension else None

def pick_dimension_elements(iuidoc,idoc):
    list_dimension = []
    selected_dimension = iuidoc.Selection.PickObjects(Autodesk.Revit.UI.Selection.ObjectType.Element, DimensionSelectionFilter(), "Pick Dimensions")
    for tung_dimension in selected_dimension:
        list_dimension.append(idoc.GetElement(tung_dimension.ElementId) if tung_dimension else None)
    return list_dimension

