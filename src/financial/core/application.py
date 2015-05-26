"""
Application classes.
"""
import string

class WsgiApplication(object):
    """
    WSGI application class.
    """

    def __init__(self, environ):
        """
        Initialization function.
        """
        
        self.status = None
        self.header = []
        self.response = []
        self.environ = environ
        
        #for key, value in environ.items():
        #    self.write(str(key) + ": " + str(value))
        #    self.write("\r\n")
           

    def __iter__(self):
        """
        Alias of `get_response`.
        """
        pass    
    
    def set_status(self, http_status_code):
        """
        Set the HTTP status code for the response.
        """
        self.status = http_status_code
    
    def add_raw_header(self, header):
        """
        Add a raw header to the response.
        """
        pass 

    def add_header(self, name, value):
        """
        Add a header to the response.
        """
        self.header.append((name, value))

    def get_response(self):
        """
        Get the actual response data blocks. 
        """
        return self.response

    def write(self, data):
        """
        Write data to the response.
        """
        self.response.append(data)
        
        
    def get_package(self):
        """
        Fetch the package name
        """
        path_elements = self.environ["PATH_INFO"].split('/')
        try:
            return path_elements[1]
        except IndexError:
            return "Package index value does not exist"
            
        
    def get_controller(self):
        """
        Fetch the controller name
        """
        path_elements = self.environ["PATH_INFO"].split('/')
        try:
            return path_elements[2]
        except IndexError:
            return "Controller index value does not exist"
    
    def get_method(self):
        """
        Fetch the method name
        """
        path_elements = self.environ["PATH_INFO"].split('/')
        try:
            return path_elements[3]
        except IndexError:
            return "default"

