import pytest
from models.base_model import(
    UserCreateResponse,
    UserLoginResponse,
    SingleUserResponse,
    ErrorResponse,
    UserUpdateResponse
)

#HAPPY PATH TEST
def test_create_user_sucess(user_service,dynamic_user_payload,validator):

    response = user_service.create_user(dynamic_user_payload)

#WITHOUT REPSONSEVALIDATOR
    # #action, execute request using service and fixture payload

    # #status code assertion
    # assert response.status_code == 201

    # #contract/schema validation using Pydantic 
    # parsed_repsonse = UserCreateResponse(**response.json())
    # assert parsed_repsonse.name == dynamic_user_payload.name
    # assert parsed_repsonse.job == dynamic_user_payload.job
    # assert parsed_repsonse.id is not None

#WITH VALIDATOR
    parsed_response = validator.validate_response(
        response =response,
        expected_code = 201,
        model_class = UserCreateResponse
    )   

    assert parsed_response.name == dynamic_user_payload.name
    assert parsed_response.job == dynamic_user_payload.job

def test_successful_login(user_service,dynamic_login_payload):
    response = user_service.login_user(dynamic_login_payload)
    assert response.status_code == 200

    parsed_response = UserLoginResponse(**response.json())
    assert parsed_response.token, "Token was empty or missing"
    assert len(parsed_response.token) > 0


def test_get_user_success(user_service):
    user_id = 2

    response = user_service.get_user(user_id)

    assert response.status_code == 200

    parsed_response = SingleUserResponse(**response.json())
    assert parsed_response.data.id == user_id
    assert "@" in parsed_response.data.email

#NEGATIVE TEST (ERROR handling)

def test_login_user_missing_password(user_service,missing_password_login_payload):
    #Action
    response = user_service.login_user(missing_password_login_payload)
    #status code assertion
    assert response.status_code == 400
    #Error payload validation
    parsed_error = ErrorResponse(**response.json())
    assert parsed_error.error == "Missing password"

def test_get_non_existent_user(user_service):
    non_existence_id = 9999
    #action
    response = user_service.get_user(non_existence_id)
    assert response.status_code == 404

def test_update_user_sucess(user_service,dynamic_user_payload,validator):
    user_id = 2 
    response = user_service.update_user(user_id,dynamic_user_payload)
#With Validator
    # assert response.status_code == 201
    # parsed_response = UserUpdateResponse(**response.json())
    # assert parsed_response.name == dynamic_user_payload.name
    # assert parsed_response.job == dynamic_user_payload.job

#Without Validator
    parsed_response = validator.validate_response(
        response=response,
        expected_code = 200,
        model_class = UserUpdateResponse
    )
    assert parsed_response.name == dynamic_user_payload.name
    assert parsed_response.job == dynamic_user_payload.job

def test_delete_user_success(user_service):
    user_id = 2 
    response = user_service.delete_user(user_id)
    assert response.status_code == 204
    assert response.text == ""

def test_login_unregistered_user(user_service,login_unregistered_user):
    response = user_service.login_user(login_unregistered_user)
    assert response.status_code == 400
    parse_error = ErrorResponse(**response.json())
    assert "user not found" in parse_error.error.lower()