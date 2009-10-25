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
from codec import *

# Now, the integration tests, which depends on SQLite
has_sqlite = True

try:
    import sqlite3
except ImportError:
    try:
        import pysqlite2
        has_sqlite = True
    except ImportError:
        pass

# Runs the integration tests if at least one module was found
if has_sqlite:
    # Bootstraps integration environment
    import django.test.utils as test_utils
    from django.db import connection
    test_utils.setup_test_environment()
    connection.creation.create_test_db()

    # Imports integration tests
    from testproj.app.tests import *
else:
    print >> sys.stderr, 'Integration: module "sqlite3" (or "pysqlite2") is required... SKIPPED'
