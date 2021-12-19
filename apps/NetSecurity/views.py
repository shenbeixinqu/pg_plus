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


@bp.route('/xhgz', methods=['GET', 'POST'])
def association():
	kind = int(request.args.get('sc'))
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')
	if kind == 1:
		buildings = CMSBuilding.query.filter(CMSBuilding.kind == 1, CMSBuilding.name.contains(key)).order_by(CMSBuilding.adddate.desc(),
						 CMSBuilding.reorder.desc()).paginate(page=page, per_page=3)
		return render_template('NetSecurity/xhgz/djhd.html', buildings=buildings.items, pagination=buildings, kind=kind, key=key)
	elif kind == 2:
		communications = CMSBuilding.query.filter(CMSBuilding.kind == 2, CMSBuilding.name.contains(key)).order_by(CMSBuilding.adddate.desc(),
						  CMSBuilding.reorder.desc()).paginate(page=page, per_page=3)
		return render_template('NetSecurity/xhgz/jlhd.html', communications=communications.items, pagination=communications, kind=kind, key=key)
	elif kind == 3:
		educations = CMSBuilding.query.filter(CMSBuilding.kind == 3, CMSBuilding.name.contains(key)).order_by(CMSBuilding.adddate.desc(), CMSBuilding.reorder.desc()).paginate(page=page, per_page=3)
		return render_template('NetSecurity/xhgz/jypx.html', educations=educations.items, pagination=educations, kind=kind, key=key)
	elif kind == 4:
		services = CMSBuilding.query.filter(CMSBuilding.kind == 4, CMSBuilding.name.contains(key)).order_by(CMSBuilding.adddate.desc(),CMSBuilding.reorder.desc()).paginate(page=page, per_page=3)
		return render_template('NetSecurity/xhgz/aqfw.html', services=services.items, pagination=services, kind=kind, key=key)
	else:
		return jsonify("2222")


@bp.route('/hydt', methods=['GET', 'POST'])
def industry():
	kind = int(request.args.get('sc'))
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')

	querys = CMSIndustry.query.filter(CMSIndustry.kind == kind, CMSIndustry.name.contains(key)).order_by(CMSIndustry.adddate.desc(),
											CMSIndustry.reorder.desc()).paginate(page=page, per_page=4)
	if kind == 1:
		return render_template('NetSecurity/hydt/rdgz.html', querys=querys.items, pagination=querys, kind=kind, key=key)
	elif kind == 2:
		return render_template('NetSecurity/hydt/wadt.html', querys=querys.items, pagination=querys, kind=kind)
	elif kind == 3:
		return render_template('NetSecurity/hydt/ldfb.html', querys=querys.items, pagination=querys, kind=kind)
	elif kind == 4:
		return render_template('NetSecurity/hydt/aqsj.html', querys=querys.items, pagination=querys, kind=kind)
	else:
		return jsonify('123456')


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


@bp.route('/xhgk', methods=['GET', 'POST'])
def overview():
	kind = int(request.args.get('sc'))
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')
	if kind == 1:
		introduction = CMSIntroduction.query.filter(CMSIntroduction.kind == 1).first()
		return render_template('NetSecurity/xhgk/xhjj.html', introduction=introduction)
	elif kind == 2:
		bylaws = CMSIntroduction.query.filter(CMSIntroduction.kind == 2).first()
		return render_template('NetSecurity/xhgk/xhzc.html', bylaws=bylaws)
	elif kind == 3:
		branches = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 1).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/fzjg.html', branches=branches.items, pagination=branches, kind=kind, key=key)
	elif kind == 4:
		leaders = CMSLeader.query.order_by(CMSLeader.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/xhfzr.html', leaders=leaders.items, pagination=leaders, kind=kind)
	elif kind == 5:
		directors = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 2).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=4)
		return render_template('NetSecurity/xhgk/lsdw.html', directors=directors.items, pagination=directors, kind=kind)
	elif kind == 6:
		supports = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 4).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/zcdw.html', supports=supports.items, pagination=supports, kind=kind)
	elif kind == 7:
		members = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/hydw.html', members=members.items, pagination=members, kind=kind)
	elif kind == 8:
		standard = CMSIntroduction.query.filter(CMSIntroduction.kind == 3).first()
		return render_template('NetSecurity/xhgk/hfbz.html', standard=standard)
	else:
		return jsonify("0-00")


@bp.route('/overview_page', methods=['POST', 'GET'])
def overview_page():
	page = int(request.args.get('page'))
	print("page", page)
	# members = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).offset(page).limit(4)

	members = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).paginate(page=page, per_page=4).items
	pagination = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).paginate(page=page, per_page=4)

	page_list = []
	for query in members:
		page_dict = {}
		page_dict["name"] = query.name
		page_dict["logo"] = query.logo
		page_dict["content"] = query.content
		page_list.append(page_dict)

	return jsonify(data=page_list)


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