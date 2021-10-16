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
        self.payload = payload
        self.table_name = payload["TableName"]
        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()
        self.generator = Generator(self.payload)

    def add_details(self):
        # todo dynamically create placeholder and prepare the query.
        sql_query = self.generator.insert_query()
        val = self.payload["Params"]["Data"]["RowValues"]
        self.cursor.execute(sql_query, tuple(val))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    # def update(self):
    #     self.function = "update"
    #     # pass sql to update table
    #     pass

    def delete(self):
        delete_query = self.generator.delete_query()
        self.cursor.execute("SET SQL_SAFE_UPDATES=0")
        self.connection.commit()
        self.cursor.execute(delete_query,(self.payload["Value"],))
        self.connection.commit()
        print(self.cursor.rowcount, "rows deleted.")
        self.cursor.close()
        self.connection.close()


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