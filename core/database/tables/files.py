from ... import config
from ...utilities.aws import aws
from ..no_value import NoValue

DEFAULT_FILES_S3_ROUTE = "files/"
PRODUCT_FILES_S3_ROUTE = "products/"
MARKETPLACE_FILES_S3_ROUTE = "marketplace/"

NO_VALUE = NoValue()

class FilesException(Exception):
    """Files generic exception."""

    def __init__(self, reason):
        """Constructor for FilesException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)

class Files:

    def __init__(self, db):
        self._db = db
        self.file_cols = ("id", "name", 'account_id', "user_id", "retail_page_account_id")

    def get_url(self, file_id, expires_in=3600):
        """Gets a signed URL to a file by the ID.

        Params:
            id: The file's ID
            expires_in: The number of seconds before the link is no longer available
                (default 1 hour (3600))
        """
        return aws.get_s3_client().generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": config.AWS_S3_BUCKET,
                "Key": "files/" + str(int(file_id))
            },
            ExpiresIn=expires_in,
        )

    def is_owner(self, user_id, account_id, file_id):
        """Determines whether the user or account is the owner of the file.

        Params:
            user_id: The user ID to check if is the owner, or None to skip.
            account_id: The account ID to check if is the owner, or None to skip.
            file_id: The file ID to check on

        Returns:
            True if user or account is the owner
        """
        rows = self._db.execute_d(
            """SELECT * FROM files
                WHERE id=%(file_id)s
            """,
            {
                "file_id": file_id
            }
        )

        if len(rows) != 1:
            return False
        
        if user_id is not None:
            if user_id == rows[0]["user_id"]:
                return True
        
        if account_id is not None:
            if account_id == rows[0]["account_id"]:
                return True
        
        return False

    def insert_file_and_get_post_configuration(self, file_name, user_id, account_id, employee_id, question_id=None,
                                               limit=10000000, expires_in=480, file_s3_route=DEFAULT_FILES_S3_ROUTE):
        """Gets the POST configuration to upload a file.
        Creates the record in the files table.

        Params:
            file_name: The file name (user's file name)
            user_id: The user ID to associate with the image
                This should be provided if the user owns the image. Don't include account_id
                    if this is included.
            account_id: The account ID to associate with the image, if any
                This should be provided if an account owns the image. Don't include user_id
                    if this is included.
            limit: The file size limit in B
                (default 10MB)
            expires_in: The number of seconds available to upload the image
                (default 8 minutes)
        
        Returns:
            The file ID and the POST config (dictionary)
        """
        self._db.execute(
            """INSERT INTO files
                (name, user_id, account_id, employee_id, question_id)
                VALUES
                    (%(name)s, %(user_id)s, %(account_id)s, %(employee_id)s, %(question_id)s)
            """,
            {
                "name": file_name,
                "account_id": account_id,
                "employee_id": employee_id,
                "user_id": user_id,
                "question_id": question_id
            }
        )

        file_id = self._db.last_row_id()
        return file_id, aws.get_s3_client().generate_presigned_post(
            Bucket=config.AWS_S3_BUCKET,
            Key=file_s3_route + str(file_id),
            Fields={
                
            },
            Conditions=[
                ["content-length-range", 0, limit]
            ],
            ExpiresIn=expires_in
        )
    
    def get_file_row(self, file_id):
        """Gets a file row by ID.

        Params:
            file_id: The file row's ID
        
        Returns:
            The file row as a dictionary
        """
        file_rows = self._db.execute_d(
            """SELECT * FROM files
                WHERE id=%(id)s
            """,
            {
                "id": file_id
            }
        )
        if len(file_rows) != 1:
            raise FilesException("File not found")
        return file_rows[0]
    
    def get_auths(self, ids):
        """Gets file auths.

        Params:
            ids: a list of file IDs

        Returns:
            A dictionary mapped by file ID with values of auth dictionaries
        """
        if ids is None:
            return None
        # Optimize this later
        auths = {}
        for file_id in ids:
            file_row = self.get_file_row(file_id)
            auths[file_id] = {
                "get": self.get_url(file_id),
                "name": file_row["name"]
            }
        return auths

    def get_files(self, id=NO_VALUE, name=NO_VALUE, account_id=NO_VALUE, user_id=NO_VALUE, employee_id=NO_VALUE,
                  retail_page_account_id=NO_VALUE, sustainability_response_id=NO_VALUE, question_id=NO_VALUE,
                  get_url=False, select_columns=[]):
        """
        Gets the file rows based on attributes provided

        Params:
            id: Fild ID
            name: Name of the file during upload
            account_id: Account ID of uploading account
            user_id: User ID of uploading user
            retail_page_account_id: Account ID of Retail image uploaded
            sustainability_response_id: ID of sustainability response 
            question_id: Sustainability question ID for which file is uploaded

        Returns:
            File rows based on attributes provided
        """
        if len(select_columns) > 0:
            incorrect_columns = [col for col in select_columns if col not in self.file_cols]
            if len(incorrect_columns) > 0:
                raise Exception("Selected column(s) " + ",".join(incorrect_columns) + " don't exist in files table")
            base_query = "SELECT "
            base_query += ",".join(select_columns) + " FROM files"
        else:
            base_query = "SELECT * FROM files"

        query_conditions = []
        query_values = {}

        if id is not NO_VALUE:
            query_conditions.append("id = %(id)s")
            query_values["id"] = id
        if name is not NO_VALUE:
            query_conditions.append("name = %(name)s")
            query_values["name"] = name
        if account_id is not NO_VALUE:
            query_conditions.append("account_id = %(account_id)s")
            query_values["account_id"] = account_id
        if employee_id is not NO_VALUE:
            query_conditions.append("employee_id = %(employee_id)s")
            query_values["employee_id"] = employee_id
        if user_id is not NO_VALUE:
            query_conditions.append("user_id = %(user_id)s")
            query_values["user_id"] = user_id
        if retail_page_account_id is not NO_VALUE:
            query_conditions.append("retail_page_account_id = %(retail_page_account_id)s")
            query_values["retail_page_account_id"] = retail_page_account_id
        if sustainability_response_id is not NO_VALUE:
            query_conditions.append("sustainability_response_id = %(sustainability_response_id)s")
            query_values["sustainability_response_id"] = sustainability_response_id
        if question_id is not NO_VALUE:
            query_conditions.append("question_id = %(question_id)s")
            query_values["question_id"] = question_id

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition
        file_rows = self._db.execute_d(query, query_values)
        if len(file_rows) > 0:
            if get_url is True:
                for file in file_rows:
                    file_url = self.get_url(file["id"])
                    file["file_url"] = file_url
                return file_rows
            else:
                return file_rows
        else:
            return []

    def update_file(self, file_id, retail_page_account_id=NO_VALUE, sustainability_response_id=NO_VALUE, question_id=NO_VALUE):
        """
        Updates file data for provided ID

        Params: 
            id: File ID
            retail_page_account_id: Account ID of Retail image uploaded
            sustainability_response_id: ID of sustainability response 
            question_id: Sustainability question ID for which file is uploaded
        """
        base_query = "UPDATE files "

        query_conditions = []
        query_values = {}
        query_values["id"] = file_id
        if retail_page_account_id is not NO_VALUE:
            query_conditions.append(" retail_page_account_id = %(retail_page_account_id)s")
            query_values["retail_page_account_id"] = retail_page_account_id
        if sustainability_response_id is not NO_VALUE:
            query_conditions.append(" sustainability_response_id = %(sustainability_response_id)s")
            query_values["sustainability_response_id"] = sustainability_response_id
        if question_id is not NO_VALUE:
            query_conditions.append(" question_id = %(question_id)s")
            query_values["question_id"] = question_id
        if len(query_conditions) >= 1:
            combined_query_condition = " SET " + ", ".join(query_conditions) + " WHERE id=%(id)s"
            query = base_query + combined_query_condition
            self._db.execute(query, query_values)
        else:
            raise Exception("Must give values for fields to update on Files table")

    def update_multiple_files(self, file_ids, retail_page_account_id=NO_VALUE, sustainability_response_id=NO_VALUE):
        """
        Updates file data for provided ID

        Params:
            ids: List of file ids
            retail_page_account_id: Account ID of Retail image uploaded or None

        Returns:
            Number of rows affected
        """

        if all(isinstance(id, int) for id in file_ids):
            where_clause = "WHERE id IN (" + ",".join(str(id) for id in file_ids) + ")"
        else:
            raise Exception("Not all the File ids provided are integers")
        base_query = "UPDATE files SET"
        query_conditions = []
        query_values = {}
        if retail_page_account_id is not NO_VALUE:
            query_conditions.append(" retail_page_account_id = %(retail_page_account_id)s ")
            query_values["retail_page_account_id"] = retail_page_account_id
        if sustainability_response_id is not NO_VALUE:
            query_conditions.append(" sustainability_response_id = %(sustainability_response_id)s ")
            query_values["sustainability_response_id"] = sustainability_response_id
        if len(query_conditions) >= 1:
            query = base_query + ",".join(query_conditions) + where_clause
            self._db.execute(query, query_values)
        return self._db.row_count()