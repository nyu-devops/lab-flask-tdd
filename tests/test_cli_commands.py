from unittest import TestCase
from click.testing import CliRunner
from service.utils.cli_commands import create_db


class TestFlaskCLI(TestCase):
    """Test Flask CLI Commands"""

    def setUp(self):
        self.runner = CliRunner()

    def test_create_db(self):
        """It should call the create-db command"""
        result = self.runner.invoke(create_db)
        self.assertEqual(result.exit_code, 0)
