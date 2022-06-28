from ... import config
from ...utilities.aws import aws

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

    def get_post(self, file_name, user_id, account_id, limit=10000000, expires_in=120):
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
                (default 2 minutes)
        
        Returns:
            The file ID and the POST config (dictionary)
        """
        self._db.execute(
            """INSERT INTO files
                (name, user_id, account_id)
                VALUES
                    (%(name)s, %(user_id)s, %(account_id)s)
            """,
            {
                "name": file_name,
                "account_id": account_id,
                "user_id": user_id
            }
        )

        file_id = self._db.last_row_id()
        return file_id, aws.get_s3_client().generate_presigned_post(
            Bucket=config.AWS_S3_BUCKET,
            Key="files/" + str(file_id),
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

    def get_image_url(self, image_folder_name, image_name, expires_in=3600):
        """Gets a signed URL to a file by the ID.

        Params:
            image_folder_name: Name of Image folder
            image_name: Name of Image file
            expires_in: The number of seconds before the link is no longer available
                (default 1 hour (3600))

        Returns:
            Presigned URL of required image
        """
        return aws.get_s3_client().generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": config.AWS_S3_BUCKET,
                "Key": "files/images/" + image_folder_name + "/" + str(image_name)
            },
            ExpiresIn=expires_in,
        )