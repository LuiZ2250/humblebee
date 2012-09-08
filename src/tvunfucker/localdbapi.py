import sqlite3


"""
Connection pool make sense with sqlite/
Create a test database with all the test tv
"""
class Database(object):

    def __init__(self, dbfile):
        self.db_file = dbfile


    def get_connection(self):
        """
        Returns a connection to the sqlite database.
        """
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = self.dict_factory
        return conn

    def _get_row(self, query, oneormany):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(query)
        #TODO: error handling, conn doesn't close if error        
        if oneormany == 'one':
            result = cur.fetchone()
        elif oneormany == 'many':
            result = cur.fetchall()
        else:
            raise ValueError(
                'last argument must be either "one" or "many"'
                )
        conn.close()
        return result

    def get_row(self, query):
        #TODO: make it take params too
        return self._get_row(query, 'one')

    def get_rows(self, query):
        return self._get_row(query, 'many')

    

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d            