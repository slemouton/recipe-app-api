from django.core.management import call_command
from unittest.mock import patch
from django.db.utils import OperationalError
from django.test import TestCase

class Commandtests(TestCase):
	def test_wait_for_db_ready(self):
		"""test waiting for db up befaore starting app"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			gi.return_value = True
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 1)

	@patch('time.sleep', return_value = True)
	def test_wait_for_db(self, ts):
		"""test waiting for db"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			gi.side_effect = [OperationalError] * 5 + [True]
			call_command('wait_for_db')
			self.assertEqual(gi.call_count,6)

