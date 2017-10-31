from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.views')
    config.include('home', '/')
    config.include('detail', '/journal/{id:\d+}')
    config.include('create', '/journal/new-entry')
    config.include('update', '/journal/{id:\d+}/edit-entry')
    config.scan()
    return config.make_wsgi_app()
