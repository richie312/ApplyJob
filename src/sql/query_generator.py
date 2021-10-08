

class Generator(object):

    """
    Generator class generates common sql insert, update, delete,
    select along with where clause.
    It expects the payloads which further supplies the reqd information
    to the specific methods.

    """

    def __init__(self, payload):
        self.payload = payload

    def delete_query(self):
        query = """delete from {table_name} where {target_column}=%s;""".format(
            table_name=self.table_name,target_column = self.payload["target_column"])

    def select_query(self):
        query = "select * from {table_name}".format(table_name = self.payload["TableName"])
        return query

    def insert_query(self):
        pass

    def col_query(self):
        col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s".format(
            TABLE_NAME = self.payload["TableName"])
        return col_query