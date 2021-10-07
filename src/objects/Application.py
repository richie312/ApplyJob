import datetime
from config.database import db_connection
from abc import abstractmethod
from flask import jsonify

class Application(object):
    def __init__(self, table_name,*bundle):
        """
        bundle: This is the payload bundle. This argument is optional. The payload contains the infor
                mation on table columns.
        """

        # Check whether the instance is initiated with initializer or just using specific class method
        try:
            self.initializer = bundle[0]
        except IndexError:
            # return empty dictionary
            self.initializer = {}
        try:
            self.company = self.initializer['Company']
            self.location = self.initializer['Location']
            self.email = self.initializer['EmailAddress']

        except KeyError:
            print("Application instance is initialized without initializer.")

        self.application_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.connection = db_connection()
        self.cursor = self.connection.cursor()

    def add_details(self):
        self.function = "add details"
        sql_query = "INSERT INTO company_email1 (Company_Name, Location, Email_Address, Application_Date)\
        VALUES (%s, %s, %s,%s)"
        val = (self.company, self.location, self.email, self.application_date)
        self.cursor.execute(sql_query, val)
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def update(self):
        self.function = "update"
        # pass sql to update table
        pass

    def delete(self,payload):
        query = """delete from company_email1 where {target_column}=%s;""".format(target_column = payload["target_column"])
        self.cursor(query,(payload["target_column"],))
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_data(self):
        query = "select * from company_email1"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # get the columns
        connection = db_connection()
        cursor = connection.cursor()
        col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s"
        cursor.execute(col_query, ("company_email1",))
        cols = cursor.fetchall()
        dict_ = {"col": cols, "data": data}
        cursor.close()
        connection.close()
        return dict_