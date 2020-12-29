from customer_lineup.utils.db_models import *
from datetime import datetime

@db_session
def add_webuser(email, name, surname, user_type):
    webuser = WebUser(email_address=email, name=name, surname=surname, user_type=user_type, registration_time=datetime.now())
    return webuser

@db_session
def get_webuser_with_id(id):
    webuser = WebUser.get(id=id)
    return webuser

@db_session
def get_webuser_with_email(email):
    webuser = WebUser.get(email_address=email)
    return webuser

@db_session
def asign_user_to_workplace(user_ref, wplace_ref):
    user_ref.managed_workplace_ref = wplace_ref
    return
