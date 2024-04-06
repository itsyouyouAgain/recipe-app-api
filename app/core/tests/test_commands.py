"""
Test custom Django management commands.
"""
# mock the behavior of the database because we need to be able to simulate
# when database is return response or not
from unittest.mock import patch

# errors we might get when we try and connect to db
from psycopg2 import OperationalError as Psycopg2Error

# allow us to simulate or call command by the name
from django.core.management import call_command

# depending on what stage of the start up process
from django.db.utils import OperationalError

from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # the more you add on top, the more it adds to the end
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        """This is how mocking work, db was not ready"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
