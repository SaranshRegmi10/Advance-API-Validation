from utils.response_validator import ResponseValidator
from services.user_services import UserServices
from utils.data_factory import UserDataFactory

def test_get_chained(created_user_id):
    """
    Pytest automatically runs setup in 'created_user_id' fixture
    'created_user_id' variable holds the exact ID yeilded by the fixture
    We use that ID in our Get Request
    """
    user_services = UserServices()

    response = user_services.get_user(created_user_id)

    ResponseValidator.validate_response(
        response=response,
        expected_code=200,
        max_allowed_ms=1.5
    )
    print(f"/n[TEST] Successfully fetched user with ID: {created_user_id}")

def test_updated_chained_user(created_user_id):
    """
    Validates updating an existing user using the chained fixture ID.
    """
    user_service = UserServices()

    updated_payload = UserDataFactory.valid_user_payload()

    response = user_service.update_user(created_user_id,updated_payload)

    ResponseValidator.validate_response(
        response=response,
        expected_code=200,
        max_allowed_ms=1.5
    )

    response_data = response.json()
    assert response_data['name'] == updated_payload.name
    assert response_data['job'] == updated_payload.job

    print(f"\n[TEST] Successfully updated user ID:{created_user_id}")

