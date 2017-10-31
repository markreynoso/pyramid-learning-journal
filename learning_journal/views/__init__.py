from .default import list_view


def includeme(config):
    """List of views to include for the configurator object."""
    config.add_view(list_view, route_name='home')
