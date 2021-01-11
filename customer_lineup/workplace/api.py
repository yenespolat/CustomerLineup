from flask import Blueprint, jsonify, request
import customer_lineup.workplace.db as db

workplace_api_bp = Blueprint('workplace_api_bp', __name__)


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
    latitude = workplace.address_ref.latitude
    longitude = workplace.address_ref.longitude

    managers = workplace.managers_set
    manager_list = []
    for manager in managers:
        manager_list.append(manager.to_dict())

    comments = workplace.comments_set
    comment_list = []
    for comment in comments:
        comment_list.append(comment.to_dict())

    return jsonify(result=True, name=workplace.name, id=workplace.id, wptype=workplace.type, status=workplace.status,
                   city=city, district=district, managers=manager_list, latitude=latitude, lonitude=longitude,
                   comments=comment_list)


@workplace_api_bp.route('/get_workplaces')
def get_workplaces_api():
    workplace_filter = {}
    city_id = request.args.get("city_id")
    district_id = request.args.get("district_id")
    wp_type = request.args.get("type")
    if district_id:
        workplace_filter["district_ref"] = db.get_district_with_id(district_id=district_id)
    if city_id:
        workplace_filter["city_ref"] = db.get_city_with_id(city_id=city_id)
    if wp_type:
        workplace_filter["type"] = wp_type

    workplaces = db.get_workplaces(**workplace_filter)

    return jsonify(result=True, workplaces=[wp.custom_dict() for wp in workplaces])


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


@workplace_api_bp.route('/add_city')
def api_add_city():
    args = request.args
    if 'city' in args:
        city_name = args.get('city')
    if db.get_city_with_name(city_name) is None:
        added_city = db.add_city(city_name)
    else:
        return jsonify(result=False, msg='You\'ve added this city before!')
    return jsonify(result=True, msg='City added!', added_city=added_city.to_dict())


@workplace_api_bp.route('/add_district')
def api_add_district():
    args = request.args
    if 'district' in args:
        district_name = args.get('district')
    if 'city' in args:
        city_name = args.get('city')
        city = db.get_city_with_name(city_name)
    if city is None:
        return jsonify(result=False, msg='You should add city before adding district!')
    if db.get_district_with_name(district_name) is not None:
        return jsonify(result=False, msg='You\'ve added this district before!')
    added_district = db.add_district(district_name, city)
    return jsonify(result=True, msg='District added to given city!', added_district=added_district.to_dict())


@workplace_api_bp.route('/add_address')
def api_add_address():
    args = request.args
    if 'district' in args and 'lat' in args and 'long' in args:
        district_name = args.get('district')
        latitude = args.get('lat')
        longitude = args.get('long')
    else:
        return jsonify(result=False, msg='Example usage: /add_address?district=XYZ&lat=999&long=999')

    district = db.get_district_with_name(district_name)
    if district is None:
        return jsonify(result=False, msg='District not exist!')

    added_address = db.add_address(district, latitude, longitude)
    return jsonify(result=True, msg='Address added!', added_address=added_address.to_dict())


@workplace_api_bp.route('/add_workplace')
def api_add_workplace():
    args = request.args
    if 'name' in args and 'type' in args and 'address_id' in args and 'status' in args:
        wp_name = args.get('name')
        wp_type = args.get('type')
        wp_address_id = args.get('address_id')
        wp_status = args.get('status')
    else:
        return jsonify(result=False, msg='Example usage: /add_workplace?name=ABC&type=DEF&address_id=14&status=3')

    if db.get_workplace_with_name(wp_name):
        return jsonify(result=False, msg='Name used before!')

    address = db.get_address_with_id(wp_address_id)
    added_workplace = db.add_workplace(wp_name, wp_type, address, wp_status)
    return jsonify(result=True, msg='Workplace added!', added_workplace=added_workplace.to_dict())
