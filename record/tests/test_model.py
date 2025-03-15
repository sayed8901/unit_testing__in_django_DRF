from django.test import TestCase
from ..models import Record

# Create your tests here.

class TestModel(TestCase):
    def test_record_model(self):
        record_name = 'test_name'

        # Create and save a Record instance
        record = Record.objects.create(name = record_name)

        # perform test
        self.assertEqual(record.name, record_name)
