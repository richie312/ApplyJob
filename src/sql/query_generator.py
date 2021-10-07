

class Generator(object):

    """
    Generator class generates common sql insert, update, delete,
    select along with where clause.

    """

    def __init__(self, payload):
        self.payload = payload

    def delete_query(self):
        query = """delete from {table_name} where {target_column}=%s;""".format(table_name=self.table_name,
                                                                                target_column = self.payload["target_column"])

    def update_query(self,payload):
        pass

    def insert_query(self,payload):
        pass


