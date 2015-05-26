def url(wsgi, *args, **kwargs):
    from bruces.webapp.url import url
    baseurl = wsgi.url if wsgi is not None else ""
    return baseurl + url(*args, **kwargs)


def static(wsgi, path):
    return url(wsgi, "static", path) 


def route(wsgi, __controller, __action, **kwargs):
    from bruces.webapp import route
    return url(wsgi, route.reverse("GET", __controller, __action, kwargs=kwargs))

def post_route(wsgi, __controller, __action, **kwargs):
    from bruces.webapp import route
    return url(wsgi, route.reverse("POST", __controller, __action, kwargs=kwargs))