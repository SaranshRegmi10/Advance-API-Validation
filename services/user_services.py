from client.base_client import BaseClient
from models.base_model import (
            UserProfile,
            UserCreateRequest,
            UserCreateResponse,
            UserLoginRequest,
            UserLoginResponse,
            SingleUserResponse,
            ErrorResponse
)
import allure
class UserServices:
    def __init__(self):
        #initalized our HTTP driver engine
        self.client = BaseClient()
        #Store endpoint paths in one place
        self.USERS_ENDPOINT = "/api/users"
        self.LOGIN_ENDPOINT = "/api/login"

    #Create a USER (POST: /api/users)
    @allure.step("User API: Create new user")
    def create_user(self,payload:UserCreateRequest):
    #nodel.dump() turns your Pydantic object into a JSON -ready dictionary
        response = self.client.post(self.USERS_ENDPOINT,json=payload.model_dump())
        return response
    
    #Get a User by ID (GET /api/users/user_id)
    @allure.step("User API: Fetch user by ID {used_id}.")
    def get_user(self,user_id:int):
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        print(f"\n[Debug Get URL]:{endpoint}")
        response = self.client.get(endpoint=endpoint)
        return response

    #Login user (POST /api/users/login)
    @allure.step("User API: Login User")
    def login_user(self,payload:UserLoginRequest):
        response = self.client.post(self.LOGIN_ENDPOINT,json=payload.model_dump())
        return response

    #Update User(PUT /api/users/user_id)
    @allure.step("User API: Update user {user_id}")
    def update_user(self,user_id:int,payload:UserCreateRequest):
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        response =  self.client.put(endpoint=endpoint,json=payload.model_dump())
        return response
    @allure.step("User API: Delete user {user_id}")
    def delete_user(self,user_id:int):
        endpoint = f"{self.USERS_ENDPOINT}/{user_id}"
        response = self.client.delete(endpoint=endpoint)
        return response

    def _attach_http_details(self,title,request_body,response):
        if request_body:
            allure.attach(
                str(request_body),
                name=f"{title}-Request Payload",
                attachment_type=allure.attachment_type.JSON    
            )

