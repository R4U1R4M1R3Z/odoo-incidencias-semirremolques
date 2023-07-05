# -*- coding:utf-8 -*-

{
    'name': 'Modulo de incidencias',
    'version': '1.0',
    'depends': [
        'contacts',
        'mail',
        'hr',
    ],
    'author': 'Raúl Ramírez',
    'category': 'Sale',
    'summary': 'Modulo de incidencias',
    'description': '''
    Modulo de incidencias
    ''',
    'data': [
        'views/incidencias.xml',
        'data/secuencia.xml',
        'report/report_incidencia.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

    ],
    'icon': 'static/description/icon.png', 

}
