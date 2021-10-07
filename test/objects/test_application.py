import os
import unittest
import requests
from src.objects.Application import Application

class TestReaders(unittest.TestCase):
    def setUp(self):
        self.env = "local"

    def test_log_dir_reader(self):
        self.file_adapter.log_dir_reader()
