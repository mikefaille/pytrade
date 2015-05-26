import os
import sys


# Set the base directory for source
src_dir = os.path.realpath(os.path.dirname(__file__) + "/..")
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Set the base directory for libraries
lib_dir = os.path.realpath(src_dir + "/../lib")
if lib_dir + "/bruces/src" not in sys.path:
    sys.path.append(lib_dir + "/bruces/src")

# Import the WSGI handler
from bruces import application

# Configure web application
from bruces import webapp
webapp.base = "financial.webapp.impl"
webapp.path = ""

# Routes
from bruces import WsgiRoute
from bruces import WsgiDispatcher
WsgiDispatcher.set_routes([
    WsgiRoute(r"^" + webapp.path + "/(?P<controller>[^/]+)/(?P<action>[^/]+)/(?P<__arglist>.+)$",
              package="webapp", action="dispatch",
              mapargs=["controller", "action"]),
    WsgiRoute(r"^" + webapp.path + "/(?P<controller>[^/]+)/(?P<action>[^/]+)$",
              package="webapp", action="dispatch",
              mapargs=["controller", "action"]),
    WsgiRoute(r"^" + webapp.path + "/(?P<controller>[^/]+)$",
              package="webapp", action="dispatch",
              kwargs={"action": "default"},
              mapargs=["controller", "action"]),
    WsgiRoute(r"^" + webapp.path + "$",
              package="webapp", action="dispatch", 
              kwargs={"controller": "home", "action": "default"},
              mapargs=["controller", "action"]),
])

# Session
from bruces import WsgiSession
WsgiSession.path = "/tmp/session"
WsgiSession.name = "session"

