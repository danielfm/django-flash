# -*- coding: utf-8 -*-

"""
    Django-flash
    ~~~~~~~~~~~~

    Rails-like *flash* messages support for Django.

    :copyright: 2008-2009, Destaquenet Technology Solutions.
    :license: BSD.
"""

__version__ = '1.7.1'

__author__  = 'Daniel Fernandes Martins'
__email__   = 'daniel@destaquenet.com'


def run_tests(verbosity=1):
    """Runs the tests. This function is useful when you want to check if an
    already installed version of Django-Flash (e.g. one that don't have a
    ``setup.py`` file) works as expected. Example::
    
        $ python -c "import djangoflash; djangoflash.run_tests();"
    """
    from djangoflash.tests import suite
    import unittest
    runner = unittest.TextTestRunner(verbosity=verbosity)
    unittest.main(module=suite, testRunner=runner)
