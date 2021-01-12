# Temporary database interface
import mysql.connector
import InsertModel
class DatabaseInterface:
    def __init__(self):
        self.db_connection = None
        self.cursor = None
        try:
            self.db_connection = mysql.connector.connect(
                user='dev',
                password='ag489jag4p98hj',
                host='127.0.0.1',
                database='example_db_1'
            )
            self.cursor = self.db_connection.cursor()
            sql = '''SELECT * FROM INSERTS;'''
            self.cursor.execute(sql)
        except:
            print('Failed to Establish Connection to DB')

    def get_next_insert(self):
        if (self.cursor != None):
            try:
                row = self.cursor.fetchone()
                new_insert = InsertModel.InsertModel()
                new_insert.load_from_list(list(row))
                return new_insert
            except:
                print('Error: get next insert failed.')
                return None
        else:
            return None

    def get_all_inserts(self):
        pass

    def upload_match(self):
        pass

    def close_connection(self):
        try:
            self.db_connection.close()
        except:
            print('Test DB Connection Failed to Close!')