import os
import unittest
import requests, json
from src.objects.Application import Application
from src.src_context import data_dir, root_dir


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.env = "local"
        self.url = "http://127.0.0.1:5001"
        self.payload = {"TableName": "company_email1","Column": "Company","Value": "Test"}
        self.schema_file = os.path.join(data_dir, "schema.json")
        self.schema_data = json.load(open(self.schema_file))
        self.table_list = list(self.schema_data.keys())
        self.payload_multiple_tables = [{"TableName": "company_email1"}, {"TableName": "mission_half_marathon"}]

    def test_get_data(self):
        expected_list_table_col_names = [self.schema_data[self.table_list[i]] for i in range(len(self.table_list))]
        for table_index in range(len(expected_list_table_col_names)):
            data = Application(self.payload_multiple_tables[table_index]).get_data()
            incoming_colnames = [data["col"][i][0] for i in range(len(data["col"]))]
            self.assertEqual(expected_list_table_col_names[table_index],incoming_colnames,"Test case for Schema match passed.")
        print("Testcases passed for all tables' schema match.")

    # REST API TestCases
    def test_get_data_api(self):
        get_data_url = self.url + r'/get_data'
        web_data = requests.get(get_data_url, params=self.payload)
        print("Ignoring the testcase as the server is not reachable.")
        self.assertEqual(200, web_data.status_code, "TestCase for web data api passed.")
        print("Test Case for Rest API functionality of {get_data_url} passed.".format(
            get_data_url = get_data_url
        ))

    # def test_delete_api(self):
    #     delete_url = self.url + r'/delete'
    #     requests.post(delete_url,self.payload)
