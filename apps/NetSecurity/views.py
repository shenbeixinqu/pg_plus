from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from apps.cms.models import *

import json

bp = Blueprint('NetSecurity', __name__, url_prefix='/NetSecurity')


@bp.route('/')
def index():
	buildings = CMSBuilding.query.filter(CMSBuilding.kind == 1).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	communications = CMSBuilding.query.filter(CMSBuilding.kind == 2).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	educations = CMSBuilding.query.filter(CMSBuilding.kind == 3).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	services = CMSBuilding.query.filter(CMSBuilding.kind == 4).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	hot_concerns = CMSIndustry.query.filter(CMSIndustry.kind == 1).order_by(CMSIndustry.adddate.desc(), CMSIndustry.reorder.desc()).limit(3)
	security_dynamics = CMSIndustry.query.filter(CMSIndustry.kind == 2).order_by(CMSIndustry.adddate.desc(), CMSIndustry.reorder.desc()).limit(3)
	leak_releases = CMSIndustry.query.filter(CMSIndustry.kind == 3).order_by(CMSIndustry.adddate.desc(), CMSIndustry.reorder.desc()).limit(3)
	security_events = CMSIndustry.query.filter(CMSIndustry.kind == 4).order_by(CMSIndustry.adddate.desc(), CMSIndustry.reorder.desc()).limit(3)
	notices = CMSNotice.query.filter(CMSNotice.kind == 1).order_by(CMSNotice.adddate.desc(), CMSNotice.reorder.desc()).limit(7)
	laws = CMSNotice.query.filter(CMSNotice.kind == 2).order_by(CMSNotice.addtime.desc()).limit(6)
	leaders = CMSLeader.query.order_by(CMSLeader.addtime.desc()).limit(6)
	director_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 2).order_by(CMSMemberCompany.addtime.desc()).limit(7)
	support_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 4).order_by(CMSMemberCompany.addtime.desc()).limit(7)
	member_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).order_by(CMSMemberCompany.addtime.desc()).limit(7)
	return render_template('NetSecurity/index.html', **locals())


@bp.route('/task')
def task():
	kind = request.args.get("kind")
	# data = json.loads(data)
	print("kind", kind)
	return "123454321"


@bp.route('/get_id')
def get_id():
	kind = request.args.get('kind')
	data = {
		"code": 200,
		"id": kind
	}
	return jsonify(data)


@bp.route('/association', methods=['GET', 'POST'])
def association():
	kind = request.args.get('kind')
	print("association_kind", kind)
	# querys = CMSBuilding.query.filter(CMSBuilding.kind == kind)
	buildings = CMSBuilding.query.filter(CMSBuilding.kind == 1).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	communications = CMSBuilding.query.filter(CMSBuilding.kind == 2).order_by(CMSBuilding.adddate.desc(),CMSBuilding.reorder.desc()).limit(3)
	educations = CMSBuilding.query.filter(CMSBuilding.kind == 3).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).limit(3)
	services = CMSBuilding.query.filter(CMSBuilding.kind == 4).order_by(CMSBuilding.adddate.desc(),CMSBuilding.reorder.desc()).limit(3)

	return render_template('NetSecurity/association_list.html', **locals())


@bp.route('/association_detail', methods=['GET', 'POST'])
def association_detail():
	params = request.args.get('params')
	print("params", params)
	query = CMSBuilding.query.filter(CMSBuilding.id == params).first()
	content = query.content
	print("content", content)
	return jsonify(content)
	# return render_template('NetSecurity/association_detail.html')


@bp.route('/association_search', methods=['GET', 'POST'])
def association_search():
	search_val = request.args.get('search_val')
	kind = request.args.get('kind')
	print("search_val", search_val, kind)
	querys = CMSBuilding.query.filter(CMSBuilding.kind == kind, CMSBuilding.name.contains(search_val))
	search_list = []
	for query in querys:
		search_dict = {}
		search_dict["name"] = query.name
		search_dict["content"] = query.content
		search_list.append(search_dict)
	return jsonify(data=search_list)


@bp.route('/overview', methods=['GET', 'POST'])
def overview():
	introduction = CMSIntroduction.query.filter(CMSIntroduction.kind == 1).first()
	bylaws = CMSIntroduction.query.filter(CMSIntroduction.kind == 2).first()
	standard = CMSIntroduction.query.filter(CMSIntroduction.kind == 3).first()
	leaders = CMSLeader.query.all()
	branches = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 1)
	directors = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 2)
	members = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).paginate(page=1, per_page=4).items
	pagination = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).paginate(page=1, per_page=4)
	supports = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 4)
	return render_template('NetSecurity/overview_list.html', **locals())


@bp.app_template_filter("date_format")
def date_format(value, format="%Y-%m-%d"):
	if not value:
		return ""
	try:
		return value.strftime(format)
	except Exception as e:
		return value


@bp.app_template_filter("get_day")
def get_day(value):
	if not value:
		return ""
	value = value.split('-')[-1]
	return value


@bp.app_template_filter("get_year_month")
def get_year_month(value):
	if not value:
		return ""
	value = value[0:7]
	return value


@bp.route('/hello')
def index_one():
	return "123456"