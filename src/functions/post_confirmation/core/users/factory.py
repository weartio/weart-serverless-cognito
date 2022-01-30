from . import EMAIL, GOOGLE, APPLE, ADMIN
from .abstract_user import AbstractUser
from .apple import Apple
from .cognito import Cognito
from .google import Google
from .admin import Admin

class UserFactory:

    @staticmethod
    def factory(provider_type, user_attributes, username, user_pool_id) -> AbstractUser:
        cognito_id = user_attributes['sub']
        email = user_attributes.get('email', None)
        phone_number = user_attributes.get('phone_number', None)

        if provider_type == EMAIL:
            return Cognito(username, cognito_id, user_pool_id, email, phone_number)
        elif provider_type == GOOGLE:
            first_name = user_attributes.get('given_name')
            last_name = user_attributes.get('family_name')
            return Google(username, cognito_id, user_pool_id, email, phone_number, first_name, last_name)
        elif provider_type == APPLE:
            return Apple(username, cognito_id, user_pool_id, email)
        elif provider_type == ADMIN:
            return Admin(username, cognito_id, user_pool_id, email, phone_number)
        else:
            raise Exception("Not supported registration method")
