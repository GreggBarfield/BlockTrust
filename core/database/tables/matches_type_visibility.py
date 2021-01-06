from ...common_exceptions import DebugException
from ...match_types import match_types_by_name
from ..frag import frag, frag_insert_into


class MatchesTypeVisibility:

    def __init__(self, db):
        self._db = db

    def _delete_account_type_visibilities(self, account_id):
        """Deletes all the type visibilites for an account.

        Params:
            account_id: Account ID to delete
        """
        return self._db.exec_frag_d(
            frag(
                "DELETE FROM matches_type_visibility",
                frag(
                    "WHERE account=:account",
                    account=account_id
                )
            )
        )

    def set_account_type_visibilities(self, account_id, settings):
        """Sets all the type visibilities for an account.

        Params:
            account_id: Account ID to set for
            settings: A dictionary of type name and true / false
        """
        self._delete_account_type_visibilities(account_id)

        if len(settings) != 0:
            self._db.exec_frag_d(
                frag_insert_into(
                    "matches_type_visibility",
                    [
                        {
                            'account': account_id,
                            'type': match_types_by_name[setting],
                            'visibility': settings[setting] is True  # Default to false if weird
                        }
                        for setting in settings
                    ]
                )
            )

    def get_account_type_visibilities(self, account_id):
        """Gets all the type visibilities for an account.

        Params:
            account_id: Account ID to get for
        """
        return self._db.exec_frag_d(
            frag(
                "SELECT * FROM matches_type_visibility WHERE account=:account",
                account=account_id
            )
        )
