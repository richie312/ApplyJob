import datetime
from config.database import db_connection
from abc import abstractmethod
from flask import jsonify
from src.sql.query_generator import Generator

class Application(object):
    def __init__(self, table_name,*payload):
        """
        bundle: This is the payload bundle. This argument is optional. The payload contains the infor
                mation on table columns.
        """

        # Check whether the instance is initiated with initializer or just using specific class method
        try:
            self.initializer = payload[0]
        except IndexError:
            # return empty dictionary
            self.initializer = {}
            print("Application instance is initialized without initializer.")

        self.table_name = table_name
        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()
        self.generator = Generator(payload)

    def add_details(self):
        self.function = "add details"
        # todo dynamically create placeholder and prepare the query.
        sql_query = "INSERT INTO {table} (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)".format(table=self.table_name)
        val = (self.company, self.location, self.email, self.application_date)
        self.cursor.execute(sql_query, val)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update(self):
        self.function = "update"
        # pass sql to update table
        pass

    def delete(self):
        delete_query = self.generator.delete_query(self.initializer)
        self.cursor(delete_query,(self.initializer["target_column"],))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_data(self):
        query = "select * from {table_name}".foramt(table=self.table_name)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # get the columns
        connection = db_connection()
        cursor = connection.cursor()
        col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
        cursor.execute(col_query, (self.table_name,))
        cols = cursor.fetchall()
        dict_ = {"col": cols, "data": data}
        cursor.close()
        connection.close()
        return dict_