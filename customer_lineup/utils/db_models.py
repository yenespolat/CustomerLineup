import os
from datetime import datetime

from pony.orm import *

db = Database()


class WebUser(db.Entity):
    id = PrimaryKey(int, auto=True)
    email_address = Required(str, unique=True)
    phone_number = Optional(str)
    name = Optional(str)
    surname = Optional(str)
    user_type = Optional(int)
    # 1: Admin
    # 2: Workplace manager
    # 3: Customer
    queue_elements_set = Set('QueueElement')
    comments_set = Set('Comment')
    managed_workplace_ref = Optional('Workplace')
    registration_time = Required(datetime)


class Workplace(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    address_ref = Required('Address')
    managers_set = Set(WebUser)
    queue_elements_set = Set('QueueElement')
    staff_warning_limit = Optional(int)  # Bekleme süresi kaçı geçerse ek personel uyarısı versin?
    created_time = Required(datetime, default=lambda: datetime.now())
    status = Required(int)
    # 1: Sistemden ayrılmış
    # 2: İşyeri şu an açık
    # 3: İş yeri şu an kapalı
    comments_set = Set('Comment')


class City(db.Entity):
    id = PrimaryKey(int, auto=True)
    city = Required(str, unique=True)
    districts_set = Set('District')


class District(db.Entity):
    id = PrimaryKey(int, auto=True)
    district = Required(str, unique=True)
    addresses_set = Set('Address')
    city_ref = Required(City)


class Address(db.Entity):
    id = PrimaryKey(int, auto=True)
    workplace_ref = Optional(Workplace)
    district_ref = Required(District)
    latitude = Required(float)
    longitude = Required(float)


class QueueElement(db.Entity):
    id = PrimaryKey(int, auto=True)
    web_users_ref = Required(WebUser)
    workplaces_ref = Required(Workplace)
    status = Required(int)
    # 1: Sıra alındı
    # 2: Sıradan çıkıldı
    # 3: İş yerine girildi
    taking_time = Required(datetime, default=lambda: datetime.now())
    status_time = Required(datetime, default=lambda: datetime.now())
    type = Required(int)
    waiting_person = Required(int)
    # 1: from application
    # 2: on workplace
    first_estimated_waiting_time = Optional(int)
    comment_ref = Optional('Comment')


class Comment(db.Entity):
    id = PrimaryKey(int, auto=True)
    web_user_ref = Required(WebUser)
    workplace_ref = Required(Workplace)
    score = Required(int)
    comment = Optional(str)
    time = Required(datetime, default=lambda: datetime.now())
    queue_element_ref = Optional(QueueElement)


DATABASE_URL = 'postgres://keundksfanucgq:0b9bf52a9ba31b333562f7ec42304631aa48a66c09badf4b96900ccae6329805@ec2-54-159-107-189.compute-1.amazonaws.com:5432/ddc7mu3s7k4o9o'  #os.getenv("DATABASE_URL")
#if os.getenv("DATABASE_URL"):
db.bind(provider="postgres", dsn=DATABASE_URL)
#else:
#    db.bind(provider="sqlite", filename='database.sqlite', create_db=True)

db.generate_mapping(create_tables=True)

if __name__ == '__main__':
    with db_session:
        # Initialize operations
        pass
