"""
Entry point for modwsgi.
"""

import sys
from StringIO import StringIO
from financial.core.application import WsgiApplication
from financial.core.dispatch import Dispatcher


def application(environ, start_response):
    """
    modwsgi entry point.

    It should initialize a WsgiApplication, capture stdout and stderr, dispatch the request,
    write output and errors to the response, then return the response data.
    """
    sys.stdout = StringIO()
    sys.stderr = StringIO()
    
    """ Instanciate WsgiApplication object """
    app = WsgiApplication(environ)
    app.set_status('200 OK')
    app.add_header("Content-type", "text/html")
    
    
    """
    Dispatch to the proper controller
    """
    dispatcher = Dispatcher(app)
    dispatcher.pre_dispatch()
    retval = dispatcher.dispatch()
    app.write(retval)
    dispatcher.post_dispatch()
        
    data = app.get_response()
    
    app.write(sys.stdout.getvalue())
    app.write(sys.stderr.getvalue())
    
    start_response(app.status, app.header)
    return data
    


