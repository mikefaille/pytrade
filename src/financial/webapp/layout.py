import os
from bruces.webapp.view import LayoutView
from bruces.webapp.view import SilentViewContext


class BaseLayoutView(LayoutView):
    """
    Base layout view.
    """

    class OuterView(LayoutView.OuterView):
        """
        Outer view class for layouts.
        """

        # Base directory for layout files
        basedir = os.path.realpath(os.path.dirname(__file__))
        
        # Sub-directory for layout files
        viewdir = "layout/"

    # Base directory for view files
    basedir = os.path.realpath(os.path.dirname(__file__)) + "/impl"

    # Context class
    context_cls = SilentViewContext 


class DefaultLayoutView(BaseLayoutView):
    """
    Default view object for displaying layouts.
    """

    class OuterView(BaseLayoutView.OuterView):
        """
        Outer view class for the layout.
        """
        
        # Filename
        filename = "default.html"


class LandingLayoutView(BaseLayoutView):
    """
    Default view object for displaying layouts.
    """

    class OuterView(BaseLayoutView.OuterView):
        """
        Outer view class for the layout.
        """

        # Filename
        filename = "landing.html"

