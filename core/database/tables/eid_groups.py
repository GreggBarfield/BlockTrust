from core.database.tables.accounts import NO_VALUE
from ..frag import frag, frag_insert_into
from .. import database


class EIDGroupsException(Exception):
    """EIDGroups generic exception."""

    def __init__(self, reason):
        """Constructor for EIDGroupsException.

        Params:
            reason: the reason for the exception
        """
        super().__init__(reason)


class EIDGroups:

    def __init__(self, db):
        self._db = db

    def get_eids(self, group_id):
        """Gets all EIDs for a group.

        Could return the same eid twice.

        Params:
            group_id: The group ID

        Returns:
            A list of EIDs
        """
        return [
            row["eid"]
            for row in
            self._db.exec_frag_d(
                frag(
                    "SELECT eid FROM eid_group_eids WHERE eid_group=:eid_group",
                    eid_group=group_id
                )
            )
        ]

    def insert_eids(self, group_id, eids):
        """Inserts eids.

        Params:
            group_id: EID Group ID to insert into
            eids: A list of EIDs to insert
        """
        if len(eids) > 0:
            self._db.exec_frag_d(
                frag_insert_into(
                    "eid_group_eids",
                    [
                        {
                            "eid_group": group_id,
                            "eid": eid
                        }
                        for eid in eids
                    ]
                )
            )

    def new_group(self, owner, eids=[]):
        """Creates a new group.

        Params:
            owner: An account ID to associate with the group
            eids: A list of EIDs to insert

        Returns:
            The group ID
        """
        self._db.exec_frag(
            frag_insert_into(
                "eid_groups",
                [
                    {
                        "owner": owner
                    }
                ]
            )
        )
        group_id = self._db.last_row_id()
        self.insert_eids(group_id, eids)
        return group_id

    def set_group(self, group_id, eids):
        """Sets the EIDs in a group.

        Params:
            group_id: The group to set
            eids: A list of EIDs to set
        """
        self.empty_group(group_id)
        self.insert_eids(group_id, eids)

    def empty_group(self, group_id):
        """Deletes a group.

        Params:
            group_id: The group ID
        """
        self._db.exec_frag(
            frag(
                "DELETE FROM eid_group_eids WHERE eid_group=:group_id",
                group_id=group_id
            )
        )

    def delete_group(self, group_id):
        """Deletes a group.

        Params:
            group_id: The group ID
        """
        self.empty_group(group_id)
        self._db.exec_frag(
            frag(
                "DELETE FROM eid_groups WHERE id=:group_id",
                group_id=group_id
            )
        )

    def get_eid_groups(self, id=NO_VALUE, owner=NO_VALUE):
        """
        Gets the eid_groups tuples based on given conditions
        Params:
            id: EID group ID
            owner: Account ID of the account which owns the sales group

        Returns:
            A list of eid group(s) record if found else []
        """
        # base query
        base_query = "SELECT * FROM eid_groups "
        query_conditions = []
        query_values = {}
        if id is not NO_VALUE:
            query_conditions.append(" id = %(id)s")
            query_values["id"] = id

        if owner is not NO_VALUE:
            query_conditions.append(" owner = %(owner)s")
            query_values["owner"] = owner

        if len(query_conditions) >= 1:
            combined_query_condition = " WHERE" + " AND ".join(query_conditions)
        else:
            combined_query_condition = ""

        query = base_query + combined_query_condition

        eid_groups_rows = self._db.execute_d(query, query_values)
        if len(eid_groups_rows) > 0:
            return eid_groups_rows
        else:
            return []
