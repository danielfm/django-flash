# -*- coding: utf-8 -*-

"""Project's test suite.
"""

import sys

# Add the Django test project to system path
from django.core.management import setup_environ
import djangoflash.tests.testproj.settings as project_settings
sys.path.insert(0, setup_environ(project_settings))

# Bootstrap Django test environment
from django.test.utils import setup_test_environment
from django.db import connection
setup_test_environment()
connection.creation.create_test_db()

# Finally, add the tests to this suite
from models import *
from testproj.app.tests import *
