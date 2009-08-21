# -*- coding: utf-8 -*-

"""Project's test suite.
"""

import sys

# Adds the Django test project to system path
from django.core.management import setup_environ
import djangoflash.tests.testproj.settings as project_settings
sys.path.insert(0, setup_environ(project_settings))

# Imports unit tests
from context_processors import *
from decorators import *
from models import *
from storage import *

try:
    # Required dependency
    import sqlite3

    # Bootstraps integration environment
    import django.test.utils as test_utils
    from django.db import connection
    test_utils.setup_test_environment()
    connection.creation.create_test_db()

    # Imports integration tests
    from testproj.app.tests import *
except ImportError:
    print >> sys.stderr, 'Integration: module "sqlite3" is required... SKIPPED'
