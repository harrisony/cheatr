#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A module to automatically restart the server when a module is modified.

This module depends on IOLoop, so it will not work in WSGI applications
and Google AppEngine.
"""

import functools
import logging
import os
import sys
import types

from tornado import ioloop

try:
    import signal
except ImportError:
    signal = None

def start(io_loop=None, check_time=500):
    """Restarts the process automatically when a module is modified.

    We run on the I/O loop, and restarting is a destructive operation,
    so will terminate any pending requests.
    """
    io_loop = io_loop or ioloop.IOLoop.instance()
    modify_times = {}
    callback = functools.partial(_reload_on_update, io_loop, modify_times)
    scheduler = ioloop.PeriodicCallback(callback, check_time, io_loop=io_loop)
    scheduler.start()


_reload_attempted = False

def _reload_on_update(io_loop, modify_times):
    global _reload_attempted
    if _reload_attempted:
        # We already tried to reload and it didn't work, so don't try again.
        return
    for module in sys.modules.values():
        # Some modules play games with sys.modules (e.g. email/__init__.py
        # in the standard library), and occasionally this can cause strange
        # failures in getattr.  Just ignore anything that's not an ordinary
        # module.
        if not isinstance(module, types.ModuleType): continue
        path = getattr(module, "__file__", None)
        if not path: continue
        if path.endswith(".pyc") or path.endswith(".pyo"):
            path = path[:-1]
        try:
            stat = os.stat(path)
            modified = stat.st_mtime
            if sys.platform == 'win32':
              modified = -stat.st_ctime
        except:
            continue
        if path not in modify_times:
            modify_times[path] = modified
            continue
        if modify_times[path] != modified:
          sys.exit(3) # Have the surrounding shell restart.
