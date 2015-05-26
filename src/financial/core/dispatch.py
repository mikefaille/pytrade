class Dispatcher(object):
    
    def __init__(self, app):
        """
        Initialize the dispatcher.
        """
        self.app = app
    
    def pre_dispatch(self):
        """
        Hook executed before dispatch.
        """
        pass 

    def post_dispatch(self):
        """
        Hook executed after dispatch.
        """
        pass

    def dispatch(self):
        """
        Dispatch the request.
        Create the controller class and fetch the method
        """
        import importlib

        package_name = self.app.get_package()
        controller_name = self.app.get_controller()
        controller_package = importlib.import_module("financial." + package_name + "." + controller_name + ".controller")
        
        cls = getattr(controller_package, controller_name.title() + "Controller")
        controller = cls()
        method = getattr(controller, self.app.get_method())
        
        return method()

