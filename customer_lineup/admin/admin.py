from flask import Flask, Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
import requests
import customer_lineup.auth.db as db_auth
import customer_lineup.workplace.db as db_wp

admin_page_bp = Blueprint('admin_page_bp', __name__, template_folder='templates', static_folder='static', static_url_path='assets')

@admin_page_bp.route('/adminpage', methods=['POST', 'GET'])
@login_required
def adminpage():
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			return render_template("adminpage.html")
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


@admin_page_bp.route('/manage_userspage', methods=['POST', 'GET'])
@login_required
def manage_userspage():
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			users = db_auth.get_all_users()
			print(users)
			return render_template("manage_userspage.html",  users=users)
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


@admin_page_bp.route('/update_userpage/<int:user_id>', methods=['POST', 'GET'])
@login_required
def update_userpage(user_id):
	user_to_update = db_auth.get_webuser_with_id(user_id)
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			if request.method == "POST":
				new_user_type = request.form['user_type']
				db_auth.edit_webuser_with_id(user_id, new_user_type)
				return redirect(url_for('admin_page_bp.manage_userspage'))
			else:
				return render_template("update_userpage.html", user_to_update=user_to_update)
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

@admin_page_bp.route('/assign_manager_to_wp/<int:wp_id>', methods=['POST', 'GET'])
@login_required
def assign_manager_to_wp(wp_id):
	workplace = db_wp.get_workplace_with_id(wp_id)
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			users = db_auth.get_all_users()
			if request.method == "POST":
				new_manager_id = request.form['user_id_to_assign']
				new_manager = db_auth.get_webuser_with_id(new_manager_id)
				db_auth.asign_user_to_workplace(new_manager, workplace)
				workplaces = db_wp.get_workplaces() 
				return render_template("manage_workplacespage.html", workplaces=workplaces)
			else:	
				return render_template("assign_managerpage.html", workplace=workplace, users=users)
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


@admin_page_bp.route('/manage_workplacespage', methods=['POST', 'GET'])
@login_required
def manage_workplacespage():
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			workplaces = db_wp.get_all_workplaces()
			for wp in workplaces:
				print(wp)
			return render_template("manage_workplacespage.html", workplaces=workplaces)
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


@admin_page_bp.route('/add_workplacepage', methods=['POST', 'GET'])
@login_required
def add_workplacepage():
	if current_user.is_authenticated:
		if current_user.user_type == 1:
			if request.method == "POST":
				wp_name = request.form['name']
				wp_type = request.form['type']
				wp_status = request.form['status']
				wp_city = request.form['city']
				wp_district = request.form['district']
				wp_long = request.form['long']
				wp_lat = request.form['lat']

				cities = db_wp.get_all_cities()
				
				temp_city = None
				temp_district = None
				for city in cities:
					if city.city == wp_city:
						temp_city = wp_city

				districts = db_wp.get_all_districts_with_city_name(temp_city)
				for district in districts:
					if district.district == wp_district:
						temp_district = wp_district
				if not temp_city:
					district_city = db_wp.add_city(wp_city)
				else:
					district_city = db_wp.get_city_with_name(wp_city)
				if not temp_district:
					address_district = db_wp.add_district(wp_district, district_city)
				else:
					address_district = db_wp.get_district_with_name(wp_district)

				wp_address_id = db_wp.add_address(address_district, wp_lat, wp_long)
				db_wp.add_workplace(wp_name, wp_type, wp_address_id, wp_status)
				return redirect(url_for('admin_page_bp.manage_workplacespage'))
			else:
				return render_template("add_workplacepage.html" )
		else:
			return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))


