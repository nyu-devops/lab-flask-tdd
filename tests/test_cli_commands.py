"""
CLI Command Extensions for Flask
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from service.common.cli_commands import create_db


class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = CliRunner()

    @patch('service.common.cli_commands.db')
    def test_create_db(self, db_mock):
        """It should call the create-db command"""
        db_mock.return_value = MagicMock()
        result = self.runner.invoke(create_db)
        self.assertEqual(result.exit_code, 0)
