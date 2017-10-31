"""View routes."""
from learning_journal.views.default import (
    list_view,
    detail_view,
    create_view,
    update_view
)


def includeme(config):
    """List of views to include for the configurator object."""
    config.add_view(list_view, route_name='home')
    config.add_view(detail_view, route_name='home')
    config.add_view(create_view, route_name='home')
    config.add_view(update_view, route_name='home')
