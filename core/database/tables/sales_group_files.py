from ..no_value import NoValue
from ...common_exceptions import ExportException

NO_VALUE = NoValue()

sales_group_files_cols = ("sales_group_id", "name", "link", "file_id", "is_archived")

class SalesGroupFiles:

    def __init__(self, db):
        self._db = db

    def insert_sales_group_files(self, sales_group_id, name, link, file_id=None):
        """
        Inserts a new sales group file row

        Params:
            sales_group_id: The ID of the sales group
            name: Name of the uploaded file
            link: Link to download the file
            file_id: File ID if the file has been uploaded to S3
        """
        self._db.execute(
            """
            INSERT INTO sales_group_files (sales_group_id, name, link, file_id)
            VALUES (%(sales_group_id)s, %(name)s, %(link)s, %(file_id)s)
            """,
            {
                "sales_group_id": sales_group_id,
                "name": name,
                "link": link,
                "file_id": file_id
            }
        )
        return self._db.last_row_id()

    def get_sales_group_files(self, id=NO_VALUE,  sales_group_id=NO_VALUE, name=NO_VALUE
                               , link=NO_VALUE, file_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Gets the sales group file rows based on the provided parameters

        Params:
            id: The ID of the sales group file row
            sales_group_id: The ID of the sales group
            name: Name of the uploaded file
            link: Link to download the file
            file_id: File ID if the file has been uploaded to S3
            is_archived: Whether the file has been marked as archived
        
        Returns:
            A list of sales group files rows or an empty list.
        """
        base_query = "SELECT * FROM sales_group_files"

        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id
        if sales_group_id is not NO_VALUE:
            query_conditions.append(" sales_group_id = %(sales_group_id)s")
            query_values["sales_group_id"] = sales_group_id
        if name is not NO_VALUE:
            query_conditions.append(" name = %(name)s")
            query_values["name"] = name
        if link is not NO_VALUE:
            query_conditions.append(" link = %(link)s")
            query_values["link"] = link
        if file_id is not NO_VALUE:
            query_conditions.append(" file_id = %(file_id)s")
            query_values["file_id"] = file_id
        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived
        
        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE " + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        sales_group_files_rows = self._db.execute_d(query, query_values)
        if len(sales_group_files_rows) > 0:
            return sales_group_files_rows
        else:
            return []

    def update_sales_group_files(self, id,  sales_group_id=NO_VALUE, name=NO_VALUE, link=NO_VALUE, 
                                 file_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Updates the sales group file row based on the provided parameters

        Params:
            id: The ID of the sales group file row
            sales_group_id: The ID of the sales group
            name: Name of the uploaded file
            link: Link to download the file
            file_id: File ID if the file has been uploaded to S3
            is_archived: Whether the file has been marked as archived
        """
        base_query = "UPDATE sales_group_files "

        query_updated_columns = []
        query_updated_values = {}
        query_updated_values["id"] = id
        if sales_group_id is not NO_VALUE:
            query_updated_columns.append(" sales_group_id = %(sales_group_id)s")
            query_updated_values["sales_group_id"] = sales_group_id
        if name is not NO_VALUE:
            query_updated_columns.append(" name = %(name)s")
            query_updated_values["name"] = name
        if link is not NO_VALUE:
            query_updated_columns.append(" link = %(link)s")
            query_updated_values["link"] = link
        if file_id is not NO_VALUE:
            query_updated_columns.append(" file_id = %(file_id)s")
            query_updated_values["file_id"] = file_id
        if is_archived is not NO_VALUE:
            query_updated_columns.append(" is_archived = %(is_archived)s")
            query_updated_values["is_archived"] = is_archived
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ",".join(query_updated_columns) + " WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)
    
    def validate_sales_group_file(self, sales_group_id=NO_VALUE, name=NO_VALUE, link=NO_VALUE):
        """
        Validates the sales group file data

        Params:
            sales_group_id: The ID of the sales group
            name: Name of the uploaded file
            link: Link to download the file
        
        Returns: 
            ExportExcpetion with related message
        """
        if sales_group_id is not NO_VALUE:
            if sales_group_id is None:
                raise ExportException("Sales Group ID cannot be blank")
        if name is not NO_VALUE:
            if name is None or len(name.strip()) == 0:
                raise ExportException("Sales Group File name cannot be blank")
            if len(name.strip()) > 100:
                raise ExportException("Sales Group File name cannot exceed 100 characters")
        if link is not NO_VALUE:
            if link is None or len(link.strip()) == 0:
                raise ExportException("Sales Group File link cannot be blank")
            if len(link.strip()) > 511:
                raise ExportException("Sales Group File link cannot exceed 512 characters")
    
    def get_sales_group_files_pending_upload(self):
        """
        Get sales group files to be uploaded

        Params:
        
        Returns: 
            ExportExcpetion with related message
        """
        unuploaded_files = self._db.execute_d(
            """
            SELECT * from sales_group_files WHERE file_id is NULL AND is_archived = 0
            """,{}
        )
        return unuploaded_files