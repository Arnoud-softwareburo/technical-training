{
    "name": "Real Estate",  # The name that will appear in the App list
    "version": "17.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_menu.xml'
    ],
    "installable": True,
    'license': 'LGPL-3',
    'description': """
        This is the description of my real estate application.
    """
}
