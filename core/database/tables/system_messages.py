from .. import database
from ..no_value import NoValue
from ...sectors import sectors_by_id

from .accounts import Accounts

NO_VALUE = NoValue()

message_type = {
    "global_message": 0,
    "sector_specific_message": 1,
    "partner_specific_message": 2
}


class SystemMessages:

    def __init__(self, db: 'database.Database'):
        self._db = db

    def get_system_messages_for_account(self, account_id):
        """
        Gets the system messages for an account

        Params:
            account_id: Account Id of user for which messages need to be retrieved

        Returns:
            An array of messages
        """
        account_row = Accounts(self._db).get_by_id(account_id=account_id)
        messages = []
        if account_row is not None:
            global_messages = self.get_system_messages(message_type=message_type["global_message"])
            sector_specific_messages = self.get_system_messages(
                message_type=message_type["sector_specific_message"],
                sector=account_row.sector_id())
            partner_specific_messages = self.get_system_messages(
                message_type=message_type["partner_specific_messages"],
                partner_account_id=account_row.partner_account_id())
            messages = global_messages+sector_specific_messages+partner_specific_messages
        return messages

    def insert_system_message(self, message_subject, message, message_type, sector, partner_account_id):
        """
        Inserts a new system message

        Params:
            message_subject: The subject for the message
            message: Message text
            message_type: Type of message which is being inserted. (Refer message_type dictionary)
            sector: Sector ID if the message is sector specific
            partner_account_id: Partner account ID if the message is partner specific
        """
        self._db.execute(
            """
            INSERT INTO system_messages
            VALUES
            (%(message_subject)s, %(message)s, %(message_type)s, %(sector)s, %(partner_account_id)s)
            """,
            {
                "message_subject": message_subject,
                "message": message,
                "message_type": message_type,
                "sector": sector,
                "partner_account_id": partner_account_id,
            }
        )

    def get_system_messages(self, message_subject=NO_VALUE, message=NO_VALUE, message_type=NO_VALUE, sector=NO_VALUE,
                            partner_account_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Gets the system messages based on the provided parameters

        Params:
            message_subject: The subject for the message
            message: Message text
            message_type: Type of message which is being inserted. (Refer message_type dictionary)
            sector: Sector ID if the message is sector specific
            partner_account_id: Partner account ID if the message is partner specific
            is_archived: Message archive status. (0-Not archived, 1-Archived)

        Returns:
            An array of system messages or an empty array
        """
        base_query = "SELECT * FROM system_messages"

        query_conditions = []
        query_values = {}

        if message_subject is not NO_VALUE:
            query_conditions.append(" message_subject = %(message_subject)s")
            query_values["message_subject"] = message_subject

        if message is not NO_VALUE:
            query_conditions.append(" message = %(message)s")
            query_values["message"] = message

        if message_type is not NO_VALUE:
            query_conditions.append(" message_type = %(message_type)s")
            query_values["message_type"] = message_type

        if sector is not NO_VALUE:
            query_conditions.append(" sector = %(sector)s")
            query_values["sector"] = sector

        if partner_account_id is not NO_VALUE:
            query_conditions.append(" partner_account_id = %(partner_account_id)s")
            query_values["partner_account_id"] = partner_account_id

        if is_archived is not NO_VALUE:
            query_conditions.append(" is_archived = %(is_archived)s")
            query_values["is_archived"] = is_archived

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        system_message_rows = self._db.execute_d(query, query_values)
        if len(system_message_rows) > 0:
            return system_message_rows
        else:
            return []

    def update_system_messaage(self, id, message_subject=NO_VALUE, message=NO_VALUE, message_type=NO_VALUE,
                               sector=NO_VALUE, partner_account_id=NO_VALUE, is_archived=NO_VALUE):
        """
        Updates the message based on the id specified

        Params:
            id: The ID of the system message to be updated
            message: Message text
            message_type: Type of message which is being inserted. (Refer message_type dictionary)
            sector: Sector ID if the message is sector specific
            partner_account_id: Partner account ID if the message is partner specific
            is_archived: Message archive status. (0-Not archived, 1-Archived)
        """
        base_query = "UPDATE system_messages "

        query_updated_columns = []
        query_updated_values = {}
        query_updated_values["id"] = id
        if message_subject is not NO_VALUE:
            query_updated_columns.append(" message_subject = %(message_subject)s")
            query_updated_values["message_subject"] = message_subject
        if message is not NO_VALUE:
            query_updated_columns.append(" message = %(message)s")
            query_updated_values["message"] = message
        if message_type is not NO_VALUE:
            query_updated_columns.append(" message_type = %(message_type)s")
            query_updated_values["message_type"] = message_type
        if sector is not NO_VALUE:
            query_updated_columns.append(" sector = %(sector)s")
            query_updated_values["sector"] = sector
        if partner_account_id is not NO_VALUE:
            query_updated_columns.append(" partner_account_id = %(partner_account_id)s")
            query_updated_values["partner_account_id"] = partner_account_id
        if is_archived is not NO_VALUE:
            query_updated_columns.append(" is_archived = %(is_archived)s")
            query_updated_values["is_archived"] = is_archived
        if len(query_updated_columns) >= 1:
            combined_query_updated_values = " SET " + ",".join(query_updated_columns) + "WHERE id=%(id)s"
            query = base_query + combined_query_updated_values
            self._db.execute(query, query_updated_values)
