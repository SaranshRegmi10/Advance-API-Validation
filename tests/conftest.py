import pytest
from config.env_config import Config 
from services.user_services import UserServices
from models.base_model import UserCreateRequest,UserLoginRequest
from utils.data_factory import UserDataFactory
from utils.response_validator import ResponseValidator

#--Env loader function
def pytest_addoption(parser):
    """Adds custom --env command-line flag to Pytest."""
    parser.addoption(
        "--env", 
        action="store", 
        default="dev", 
        help="Target environment: dev, staging, or prod"
    )
@pytest.fixture(scope="session", autouse=True)
def setup_environment(request):
    """Automatically runs before all tests to load the specified --env config."""
    selected_env = request.config.getoption("--env")
    Config.load_environment(selected_env)


#--API chaining
@pytest.fixture
def created_user_id():
    """Setup: Create a user and return its ID, Teardown:Delete the user"""

    user_service = UserServices()

    payload = UserDataFactory.valid_user_payload()

    response = user_service.create_user(payload)

    ResponseValidator.assert_status_code(response,201)

#we use this to get the id in actual testing
    # user_id = response.json().get("id")
    # print(f"\n[SETUP] Created test user with ID:{user_id}")

    user_id = 2 # see in Reqres, it only holds static real data for IDs 1 to 12, so we used to other wise it would mockID and return 404
    yield user_id

    print(f"\n[TEARDOWN] Deleting test user with ID: {user_id}")
    delete_response = user_service.delete_user(user_id)

    ResponseValidator.assert_status_code(delete_response,204)
    print(f"[TEARDOWN] User{user_id} successfully deleted")



@pytest.fixture(scope = "session")
def user_service():
    """
    Provides a shares intense a UserService across all tests.
    scope = "session" mean it gets created ONCE when the test run starts
    """
    return UserServices()

@pytest.fixture
def dynamic_user_payload():
    """Provides a fresh,randomly generated UserCreateRequest for each test"""
    return UserDataFactory.valid_user_payload()

@pytest.fixture
def dynamic_login_payload():
    """Provides a valid  login payload with dynamic password"""
    return UserDataFactory.valid_login_payload()

@pytest.fixture
def dynamic_missing_password_payload():
    """Provides login payload with an empty password"""
    return UserDataFactory.invalid_logging_missing_password()

@pytest.fixture
def validator():
    """Provides the ResponseValidator class instance for tests"""
    return ResponseValidator

@pytest.fixture
def missing_password_login_payload():
    """
    Generates an invalid loin payload missing a password to trigger 400 Bad Request
    """
    return UserLoginRequest(
        email = "eve.holt@reqres.in",
        password= ""
    )

@pytest.fixture
def login_unregistered_user():
    """
    Genreates an invalid username payload to trigger 400 Bad request
    """
    return UserLoginRequest(
        email="unregisteredemial_999@test.com",
        password="somepassword123"
    )