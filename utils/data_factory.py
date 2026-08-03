from faker import Faker
from models.base_model import UserCreateRequest,UserCreateResponse,UserLoginRequest

fake = Faker()

class UserDataFactory:

    @staticmethod
    def valid_user_payload() ->UserCreateRequest:
        """Generates a dynamic valid user payload for poST/PUt endpoints"""
        return UserCreateRequest(
            name = fake.name(),
            job= fake.job()
        )
    
    @staticmethod
    def valid_login_payload(email:str = "eve.holt@reqres.in")->UserLoginRequest:
        """
        Generates a valid login payload
        Reqres.in requires specific email, but we generate dynamic password
        """
        return UserLoginRequest(
            email=email,
            password=fake.password(length = 12,special_chars = True)
        )

    @staticmethod
    def invalid_logging_missing_password(email:str="eve.holt@reqres.in")->UserLoginRequest:
        """
        Generates a login payload missing a password for negative tests
        """
        return UserLoginRequest(
            email=email,
            password=""
        )

    @staticmethod
    def edge_case_user_payload(name_length:int=150)->UserCreateRequest:
        """
        Generates boundary payloads like extra long strings
        """
        return UserCreateRequest(
            name = fake.text(max_nb_chars=name_length),
            job= fake.job()
        )

    @staticmethod
    def invalid_user_payload():
        """
        Generates a list of tuples containing (name,payload and status code)
        Used for data-driven negative testing
        """
        return [
            ("missing_name",{"job":"Developer"},400),
            ("missing_job",{"name":"Saransh"},400),
            ("empty_string",{"name":"","jobx`":""},400),
            ("null_values",{"name":None,"job":None},400)
        ]