from ...exceptions import ExecutionException


def block_eid_from_animal_id(account_id, animal_id):
    """Generates a MFA EID block key.

    Params:
        account_id: BTN account ID
        animal_id: MFA AnimalID

    Returns:
        The block key as a string
    """
    if not isinstance(account_id, int):
        raise ExecutionException("Account ID should be an int")
    # Note that if someone tries to compromise the AnimalID it doesn't matter
    return "MFA:ANEID:" + str(account_id) + ":" + animal_id
