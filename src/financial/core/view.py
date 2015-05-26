ass BaseView(object):
    """
    Base view object.

    Interacts at the lowest level with the template renderer.
    """

    def __init__(self, filename):
        """
        Initialize a base view object.
        """
        pass

    def __setitem__(self, var, value):
        """
        Pass a variable to the view.
        """
        pass

    def __getitem__(self, var, value):
        """
        Obtain a saved variable.
        """
        pass

    def __iter__(self, var, value):
        """
        Iterator for all the view's variables.
        """
        pass

    def render(self):
        """
        Render and return the view.
        """
        pass

    def display(self):
        """
        Display the rendered view.
        """
        pass


class View(BaseView):
    """
    View object.
    """

    def __init__(self, package, submodule, view_name):
        """
        Initialize the view.
        """
        pass


