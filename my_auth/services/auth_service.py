from django.db.utils import IntegrityError

from my_auth.models import CustomUser


def create_user(first_name: str, phone_number: str, password: str):
    try:
        user = CustomUser.objects.create_user(
            phone_number=phone_number, first_name=first_name, password=password
        )
        return user, None
    except IntegrityError:
        return None, "Phone number already exist"
