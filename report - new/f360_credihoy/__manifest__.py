# -*- coding: utf-8 -*-
{
    'name': "f360_credihoy",

    'summary': """
        Credihoy customization
        """,

    'description': """

    """,

    'author': "mulaWare",
    'website': "http://mulaware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'contacts',
                'website',
                'f360_kyc',
                'report_py3o',
                'pragtech_loan_advance',
                ],

    'data': [
        'report/report.xml',

         'views/web_application_view.xml',
         'views/pages.xml',
         'views/assets.xml',

    ],
    'demo': [

    ],
    'application': True,
    'installable': True,
}
