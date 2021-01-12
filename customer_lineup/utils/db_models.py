import os
from datetime import datetime

from pony.orm import *

db = Database()


class WebUser(db.Entity):
    id = PrimaryKey(int, auto=True)
    email_address = Required(str, unique=True)
    password_hash = Optional(str)
    phone_number = Optional(str)
    name = Optional(str)
    surname = Optional(str)
    user_type = Optional(int)
    queue_elements_set = Set('QueueElement')
    comments_set = Set('Comment')
    managed_workplace_ref = Optional('Workplace')
    registration_time = Required(datetime)

    class USER_TYPE:
        ADMIN = 1
        WORKPLACE_MANAGER = 2
        CUSTOMER = 3


class Workplace(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    type = Required(str)
    image_url = Required(str)
    address_ref = Required('Address')
    managers_set = Set(WebUser)
    queue_elements_set = Set('QueueElement')
    staff_warning_limit = Optional(int)  # Bekleme süresi kaçı geçerse ek personel uyarısı versin?
    created_time = Required(datetime, default=lambda: datetime.now())
    status = Required(int)
    comments_set = Set('Comment')

    class STATUS:
        PASSIVE = 1
        NOW_OPEN = 2
        NOW_CLOSE = 3

    class TYPE:
        BANK = "Bank"
        MARKET = "Market"

    def custom_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "staff_warning_limit": self.staff_warning_limit,
            "created_time": self.created_time,
            "status": self.status,
            "image_url": self.image_url,
            "address": self.address_ref.custom_dict(),
        }


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

    def custom_dict(self):
        return {
            "id": self.id,
            "city": self.district_ref.city_ref.city,
            "district": self.district_ref.district,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class QueueElement(db.Entity):
    id = PrimaryKey(int, auto=True)
    web_users_ref = Required(WebUser)  # DEĞİŞMELİ web_user_ref
    workplaces_ref = Required(Workplace)  ##DEĞİŞMELİ workplace_ref
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


# DATABASE_URL = 'postgres://keundksfanucgq:0b9bf52a9ba31b333562f7ec42304631aa48a66c09badf4b96900ccae6329805@ec2-54-159-107-189.compute-1.amazonaws.com:5432/ddc7mu3s7k4o9o'  #os.getenv("DATABASE_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("DATABASE_URL"):
    db.bind(provider="postgres", dsn=DATABASE_URL)
else:
    db.bind(provider="sqlite", filename='database.sqlite', create_db=True)

try:
    db.generate_mapping(create_tables=True)
except (ProgrammingError, IntegrityError, OperationalError) as e:
    print(type(e), e)
    db.drop_all_tables(with_all_data=True)
    db.generate_mapping()

if __name__ == '__main__':
    with db_session:
        sariyer = District.get(district="Sarıyer")
        if not sariyer:
            istanbul = City.get(city="İstanbul")
            if not istanbul:
                istanbul = City(city="İstanbul")
            sariyer = District(district="Sarıyer", city_ref=istanbul)

        if Workplace.select().count() == 0:
            Workplace(
                name="Bim", type=Workplace.TYPE.MARKET, status=Workplace.STATUS.NOW_OPEN,
                address_ref=Address(district_ref=sariyer, latitude=41.0990, longitude=29.0231),
                image_url="https://www.bim.com.tr/templates/images/bim-logo-single.png"
            )
            Workplace(
                name="Şok", type=Workplace.TYPE.MARKET, status=Workplace.STATUS.NOW_OPEN,
                address_ref=Address(district_ref=sariyer, latitude=41.1990, longitude=29.1231),
                image_url="https://upload.wikimedia.org/wikipedia/tr/3/3e/%C5%9Eok_Logo.png",
            )
            Workplace(
                name="Ptt", type=Workplace.TYPE.BANK, status=Workplace.STATUS.NOW_OPEN,
                address_ref=Address(district_ref=sariyer, latitude=41.1590, longitude=29.1931),
                image_url="https://upload.wikimedia.org/wikipedia/tr/e/e0/Ptt_tr.gif",
            )
            Workplace(
                name="A101", type=Workplace.TYPE.MARKET, status=Workplace.STATUS.NOW_OPEN,
                address_ref=Address(district_ref=sariyer, latitude=41.0890, longitude=29.0331),
                image_url="https://ayb.akinoncdn.com/static_omnishop/ayb587/assets/img/logo%40a101-2x.png",
            )
