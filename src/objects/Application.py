import datetime
from config.database import db_connection
from abc import abstractmethod
from flask import jsonify
from src.sql.query_generator import Generator

class Application(object):
    def __init__(self, payload):
        """
        It instantiate the class with payload.
        """
        self.table_name = payload["TableName"]
        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()
        self.generator = Generator(payload)

    # def add_details(self):
    #     self.function = "add details"
    #     # todo dynamically create placeholder and prepare the query.
    #     sql_query = "INSERT INTO {table} (Company_Name, Location, Email_Address, Application_Date)\
    #     VALUES (%s, %s, %s,%s)".format(table=self.table_name)
    #     val = (self.company, self.location, self.email, self.application_date)
    #     self.cursor.execute(sql_query, val)
    #     self.connection.commit()
    #     self.cursor.close()
    #     self.connection.close()

    # def update(self):
    #     self.function = "update"
    #     # pass sql to update table
    #     pass

    # def delete(self):
    #     delete_query = self.generator.delete_query(self.initializer)
    #     self.cursor(delete_query,(self.initializer["Value"],))
    #     self.connection.commit()
    #     self.cursor.close()
    #     self.connection.close()


    def get_data(self):
        query = self.generator.select_query()
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # get the columns
        self.connection = db_connection()
        self.cursor = self.connection.cursor()
        col_query = self.generator.col_query()
        self.cursor.execute(col_query, (self.table_name,))
        cols = self.cursor.fetchall()
        dict_ = {"col": cols, "data": data}
        self.cursor.close()
        self.connection.close()
        return dict_