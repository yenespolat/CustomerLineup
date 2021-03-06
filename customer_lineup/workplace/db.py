from customer_lineup.utils.db_models import *


@db_session
def add_workplace(name, type, address_ref, status, url):
    workplace = Workplace(name=name, type=type, address_ref=address_ref, status=status, image_url=url)
    return workplace


@db_session
def get_workplace_with_name(name):
    return Workplace.get(name=name)


@db_session
def get_workplace_with_id(id):
    return Workplace.get(id=id)


@db_session
def get_all_workplaces():
    return Workplace.select(lambda a: a.id > 0)

    
@db_session
def get_workplaces(**kwargs):
    return Workplace.select(**kwargs)


@db_session
def add_address(district_ref, latitude, longitude):
    address = Address(district_ref=district_ref, latitude=latitude, longitude=longitude)
    return address


@db_session
def get_address_with_id(id):
    address = Address.get(id=id)
    return address


@db_session
def get_all_addresses():
    addresses = Address.select(lambda a: a.id > 0)
    return addresses


@db_session
def get_all_addresses_with_district_ref(district_ref):
    addresses = Address.select(lambda a: a.district_ref.district == district_ref.district)
    return addresses


@db_session
def get_all_addresses_with_city_ref(city_ref):
    addresses = Address.select(lambda a: a.district_ref.city_ref.city == city_ref.city)
    return addresses


@db_session
def get_all_addresses_with_district_name(district_name):
    addresses = Address.select(lambda a: a.district_ref.district == district_name)
    return addresses


@db_session
def get_all_addresses_with_city_name(city_name):
    addresses = Address.select(lambda a: a.district_ref.city_ref.city == city_name)
    return addresses


@db_session
def add_district(district, city_ref):
    district = District(district=district, city_ref=city_ref)
    return district


@db_session
def get_district_with_name(district_name):
    district = District.get(district=district_name)
    return district


@db_session
def get_district_with_id(district_id):
    district = District.get(id=district_id)
    return district


@db_session
def get_all_districts_with_city_ref(city_ref):
    districts = District.select(lambda d: d.city_ref.city == city_ref.city)
    return districts


@db_session
def get_all_districts_with_city_name(city_name):
    districts = District.select(lambda d: d.city_ref.city == city_name)
    return districts


@db_session
def add_city(city):
    city = City(city=city)
    return city


@db_session
def get_city_with_name(city_name):
    city = City.get(city=city_name)
    return city


@db_session
def get_city_with_id(city_id):
    city = City.get(id=city_id)
    return city

@db_session
def get_all_cities():
    cities = City.select(lambda c: c.id > 0)
    return cities

@db_session
def delete_wp(id):
    workplace = get_workplace_with_id(id)
    workplace.delete()
    return True

