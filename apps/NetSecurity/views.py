from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from flask_login import login_user, login_required, current_user
from apps.cms.models import *

import json

bp = Blueprint('NetSecurity', __name__, url_prefix='/NetSecurity')


@bp.route('/footer', methods=['GET', 'POST'])
def footer_info():
	query = CMSFooter.query.first()
	data = {
		"code": query.code,
		"content": query.content
	}
	return jsonify(data)


@bp.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('NetSecurity/login/register.html')


@bp.route('/register_validate', methods=['POST', 'GET'])
def register_validate():
	name = request.args.get('name')
	company = request.args.get('company')
	job = request.args.get('job')
	mobile = request.args.get('mobile')
	code = request.args.get('code')
	return jsonify('123456')


@bp.route('/login')
def login():
	return render_template('NetSecurity/login/login.html')


@bp.route('/login_validate', methods=['POST', 'GET'])
def login_validate():
	get_data = request.get_data()
	print('get_Data', get_data)
	return jsonify('12345678')


@bp.route('/')
def index():
	buildings = CMSBuilding.query.filter(CMSBuilding.kind == 1).order_by(CMSBuilding.addtime.desc(), CMSBuilding.reorder.desc()).limit(3)
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
	director_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 2).order_by(CMSMemberCompany.addtime.desc()).limit(2)
	support_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 4).order_by(CMSMemberCompany.addtime.desc()).limit(7)
	member_company = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).order_by(CMSMemberCompany.addtime.desc()).limit(7)
	whole_banners = CMSBanner.query.filter(CMSBanner.if_banner == 1).all()
	half_banners = CMSBanner.query.filter(CMSBanner.if_banner == 2).all()
	return render_template('NetSecurity/index.html', **locals())


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
		return render_template('NetSecurity/common/404.html')


# 安全服务
@bp.route('/aqfw', methods=['GET', 'POST'])
@login_required
def service():
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')
	services = CMSBuilding.query.filter(CMSBuilding.kind == 4, CMSBuilding.name.contains(key)).order_by(CMSBuilding.adddate.desc(),CMSBuilding.reorder.desc()).paginate(page=page, per_page=3)
	return render_template('NetSecurity/xhgz/aqfw.html', service=services.items, pagination=services, key=key)


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
		return render_template('NetSecurity/hydt/wadt.html', querys=querys.items, pagination=querys, kind=kind, key=key)
	elif kind == 3:
		return render_template('NetSecurity/hydt/ldfb.html', querys=querys.items, pagination=querys, kind=kind, key=key)
	elif kind == 4:
		return render_template('NetSecurity/hydt/aqsj.html', querys=querys.items, pagination=querys, kind=kind, key=key)
	else:
		return render_template('NetSecurity/common/404.html')


@bp.route('/hydtxq', methods=['GET', 'POST'])
def industry_detail():
	kind = int(request.args.get('sc'))
	id = int(request.args.get('pid'))
	query = CMSIndustry.query.filter(CMSIndustry.id == id).first()
	return render_template('NetSecurity/hydt/hydt_detail.html', query=query, kind=kind)


@bp.route('/xhgzxq', methods=['GET', 'POST'])
def association_detail():
	res = request.args.get('sc')
	print('res', res, type(res))
	kind = int(request.args.get('sc'))
	id = int(request.args.get('pid'))
	query = CMSBuilding.query.filter(CMSBuilding.id == id).first()
	return render_template('NetSecurity/xhgz/xhgz_detail.html', query=query, kind=kind)


@bp.route('/tzgg', methods=['GET', 'POST'])
def notice():
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')
	querys = CMSNotice.query.filter(CMSNotice.kind == 1, CMSNotice.name.contains(key)).order_by(CMSNotice.addtime.desc(), CMSNotice.reorder.desc()).paginate(page=page, per_page=3)
	return render_template('NetSecurity/tzgg/tzgg.html', querys=querys.items, pagination=querys, key=key)


@bp.route('/tzggxq', methods=['GET', 'POST'])
def notice_detail():
	id = int(request.args.get('pid'))
	query = CMSNotice.query.filter(CMSNotice.id == id).first()
	return render_template('NetSecurity/tzgg/tzgg_detail.html', query=query)


@bp.route('/flfg', methods=['GET', 'POST'])
def law():
	page = request.args.get("page", 1, type=int)
	key = request.args.get('key', '')
	querys = CMSNotice.query.filter(CMSNotice.kind == 2, CMSNotice.name.contains(key)).order_by(CMSNotice.addtime.desc(), CMSNotice.reorder.desc()).paginate(page=page, per_page=3)
	return render_template('NetSecurity/flfg/flfg.html', querys=querys.items, pagination=querys, key=key)


@bp.route('/flfgxq', methods=['GET', 'POST'])
def law_detail():
	id = int(request.args.get('pid'))
	query = CMSNotice.query.filter(CMSNotice.id == id).first()
	return render_template('NetSecurity/flfg/flfg_detail.html', query=query)


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
		return render_template('NetSecurity/xhgk/xhfzr.html', leaders=leaders.items, pagination=leaders, kind=kind, key=key)
	elif kind == 5:
		directors = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 2).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=4)
		return render_template('NetSecurity/xhgk/lsdw.html', directors=directors.items, pagination=directors, kind=kind, key=key)
	elif kind == 6:
		supports = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 4).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/zcdw.html', supports=supports.items, pagination=supports, kind=kind, key=key)
	elif kind == 7:
		members = CMSMemberCompany.query.filter(CMSMemberCompany.kind == 3).order_by(CMSMemberCompany.addtime.desc()).paginate(page=page, per_page=8)
		return render_template('NetSecurity/xhgk/hydw.html', members=members.items, pagination=members, kind=kind, key=key)
	elif kind == 8:
		standard = CMSIntroduction.query.filter(CMSIntroduction.kind == 3).first()
		return render_template('NetSecurity/xhgk/hfbz.html', standard=standard)
	else:
		return jsonify("0-00")


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