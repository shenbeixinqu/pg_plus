from flask import Blueprint, request, jsonify, render_template
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
	querys = CMSBuilding.query.filter(CMSBuilding.kind == kind)
	# buildings = CMSBuilding.query.filter(CMSBuilding.kind == kind)
	# communications = CMSBuilding.query.filter(CMSBuilding.kind == kind).order_by(CMSBuilding.adddate.desc(),
	# 																		  CMSBuilding.reorder.desc()).limit(3)
	# educations = CMSBuilding.query.filter(CMSBuilding.kind == kind).order_by(CMSBuilding.adddate.desc(),
	# 																	  CMSBuilding.reorder.desc()).limit(3)
	# services = CMSBuilding.query.filter(CMSBuilding.kind == 4).order_by(CMSBuilding.adddate.desc(),
	# 																	CMSBuilding.reorder.desc()).limit(3)
	return render_template('NetSecurity/association_list.html', querys=querys, kind=kind)


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