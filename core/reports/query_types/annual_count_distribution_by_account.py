from core.database.tables.connections import Connections
from core.database.tables.matches import Matches
from core.sectors import SECTORS_NAME_TO_ID
from ...database.tables.sustainability_responses import QUESTIONNAIRE_STATUS_NAMES_TO_IDS, SustainabilityResponses
from ...match_types import MATCH_TYPES_NAME_TO_ID
from datetime import datetime

TYPE_NAME = "annual_count_distribution_by_account"
INITIAL_YEAR = 2021

def execute(db, query):
    """Execute the query."""
    params = query['params']
    is_partner = params.get("is_partner", False)

    partner_accounts = []
    if is_partner:
        partner = db.accounts.get_partners(id=params['account'])[0]
        if partner["sector"] == SECTORS_NAME_TO_ID["Producer Service"]:
            connected_account_ids = Connections(db).get_connected_account_ids(partner["id"])
            for account_id in connected_account_ids:
                partner_accounts.append(db.accounts.get_accounts(id=account_id)[0])
    
    if params.get("match_type", None):
        annual_count_distribution_by_account = {}
        for report_year in range(INITIAL_YEAR, datetime.now().year + 1):
            annual_count_distribution_by_account[report_year] = Matches(db).get_count_distribution(
                MATCH_TYPES_NAME_TO_ID[params["match_type"]],
                account_id=params['account'],
                is_partner=is_partner,
                get_by_year=report_year,
                associated_accounts=partner_accounts
            )
        return {"annual_count_distribution_by_account": annual_count_distribution_by_account}
    else:
        if partner["sector"] != SECTORS_NAME_TO_ID["Producer Service"]:
            partner_accounts = db.accounts.get_accounts(
                partner_account=params['account']
            )

        annual_count_distribution_by_account = {}
        for report_year in range(INITIAL_YEAR, datetime.now().year + 1):
            count_distribution = Matches(db).get_count_distribution(
                is_partner=True,
                get_by_year=report_year,
                associated_accounts=partner_accounts
            )
            for result in count_distribution.values():
                completed_sustainability_surveys = SustainabilityResponses(db).get_sustainability_responses(
                    account_id=result['account_id'], questionnaire_status_id=QUESTIONNAIRE_STATUS_NAMES_TO_IDS["Completed"]
                )
                result["survey_completed"] = True if len(completed_sustainability_surveys) > 0 else False
            annual_count_distribution_by_account[report_year] = count_distribution
        return {
            "annual_count_distribution_by_account": annual_count_distribution_by_account
        }


def accessible(query, account_id):
    """Checks whether the query is accessible by an account.

    Params:
        query: The query dictionary
        account_id: The account ID of who is accessing the query
            or None if anonymous

    Returns:
        A boolean of whether the query is accessible
    """
    if account_id is None:
        return False
    return account_id == query['params']['account']


def create(account_id, match_type=None, is_partner=False):
    """Creates a query.

    Params:
        account_id: The account ID to get cows associated with
        match_type: The match type name to generate distribution data on
        is_partner: whether the account is a partner or not.
    Returns:
        The query dictionary
    """
    params = {'account': account_id}
    if match_type:
        params['match_type'] = match_type
    if is_partner:
        params['is_partner'] = True
    return {
        'type': TYPE_NAME,
        'params': params
    }