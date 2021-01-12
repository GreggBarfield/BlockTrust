# Temporary database interface
import mysql.connector
import InsertModel
class DatabaseInterface:
    """ This class is meant to serve as a (temporary)
        solution to interfacing the inserts and matches table
        for the api-worker functionality.

        It creates a connection to a given database, 
        and provides simplified functionality for uploading
        matches and downloading insert records.
    
    """
    def __init__(self):
        """ Constructor for DatabaseInterface
            It sets up a database connection and prepares the
            inserts table for reading.

            Params:
                NONE
        
        """
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
        """ get_next insert
            purpose: reads rows from inserts
                     one row at a time.
        """
        if (self.cursor != None):
            try:
                row = self.cursor.fetchone()
                new_insert = InsertModel.InsertModel()
                new_insert.load_from_list(list(row))
                new_insert.shrink_data()
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