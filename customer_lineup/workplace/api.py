from flask import Blueprint, jsonify, request
import customer_lineup.workplace.db as db

workplace_api_bp = Blueprint('workplace_api_bp', __name__)


@workplace_api_bp.route('/example')
def example_api():
    # Example for http://127.0.0.1:5000/api/workplace/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    arg0 = request.args.get('arg0')
    return jsonify(result=True, msg="Hello world", data=arg0)

@workplace_api_bp.route('/get_workplace')
def get_workplace():
    args = request.args
    workplace = None
    if 'name' in args:
        name = args.get('name')
        workplace = db.get_workplace_with_name(name)
    elif 'id' in args:
        id = args.get('id')
        workplace = db.get_workplace_with_id(id)

    if workplace == None:
        return jsonify(result=False, msg='Workplace not found!')

    city = workplace.address_ref.district_ref.city_ref.city
    district = workplace.address_ref.district_ref.district
    return jsonify(result=True, workplace_name=workplace.name, type=workplace.type, status=workplace.status, city=city, district=district)

@workplace_api_bp.route('/get_all_addresses')
def get_all_addresses():
    addresses = db.get_all_addresses()
    a_list = []
    for a in addresses:
        address = {}
        address['address_id'] = a.id
        address['district_id'] = a.district_ref.id
        address['district_name'] = a.district_ref.district
        address['city_id'] = a.district_ref.city_ref.id
        address['city_name'] = a.district_ref.city_ref.city
        if a.workplace_ref != None:
            address['workplace_id'] = a.workplace_ref.id
            address['workplace_name'] = a.workplace_ref.name
        address['latitude'] = a.latitude
        address['longitude'] = a.longitude
        a_list.append(address)

    if len(a_list) == 0:
        return jsonify(result=False, msg='No address found!')

    return jsonify(result=True, addresses=a_list)

@workplace_api_bp.route('/get_city')
def get_city():
    args = request.args
    city = None
    if 'id' in args:
        id = args.get('id')
        city = db.get_city_with_id(id)
    elif 'city' in args:
        city_name = args.get('city')
        city = db.get_city_with_name(city_name)

    if city == None:
        return jsonify(result=False, msg='City not found!')

    return jsonify(result=True, city_id=city.id, city_name=city.city)

@workplace_api_bp.route('/get_district')
def get_district():
    args = request.args
    district = None
    if 'id' in args:
        id = args.get('id')
        district = db.get_district_with_id(id)
    elif 'district' in args:
        district_name = args.get('district')
        district = db.get_district_with_name(district_name)

    if district is None:
        return jsonify(result=False, msg='District not found!')

    return jsonify(result=True, district_id=district.id, district_name=district.district)

@workplace_api_bp.route('/get_city_districts')
def get_city_districts():
    args = request.args
    if 'city' in args:
        city_name = args.get('city')
        city = db.get_city_with_name(city_name)

    if city is None:
        return jsonify(result=False, msg='City not found!')

    districts = db.get_all_districts_with_city_ref(city)

    if districts is None:
        return jsonify(result=False, msg='Given city has no districts!')

    district_list = []
    for district in districts:
        district_list.append(district.to_dict())

    return jsonify(result=True, districts=district_list)
