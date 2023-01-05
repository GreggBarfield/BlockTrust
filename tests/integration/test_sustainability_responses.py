

def test_if_response_column_exists(db_connection):
    responses = db_connection.execute_d("SELECT * FROM sustainability_responses LIMIT 1")
    if len(responses) > 0:
        assert "response" in responses[0]
