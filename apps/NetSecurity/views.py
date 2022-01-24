from flask import Blueprint, request, jsonify, render_template, url_for, redirect, session
from flask_login import login_user, login_required, logout_user
from apps.cms.models import *
import config
from utils.random_code import generate_code
from utils.sent_message import sent_message
from datetime import datetime, timedelta
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
	data = request.get_json()
	name = data["name"]
	company = data["company"]
	job = data["job"]
	mobile = data["mobile"]
	m_code = data["code"]
	ifCode = CMSMessageCode.query.filter(CMSMessageCode.phone == mobile, CMSMessageCode.sort == 2).order_by(CMSMessageCode.addtime.desc()).first()
	user = CMSMember.query.filter(CMSMember.phone == mobile).first()
	result = {
		"status": 200,
		"msg": ''
	}
	if user:
		result["status"] = 201
		result["msg"] = "手机号已注册"
		return jsonify(result)
	else:
		code = ifCode.code
		time_delta = (datetime.now() - ifCode.addtime).seconds
		if code == m_code and time_delta < 120:
			c_user = CMSMember(name= name, company=company, position=job, phone=mobile)
			db.session.add(c_user)
			db.session.commit()
			return jsonify(result)
		else:
			result["status"] = '202'
			result["msg"] = "验证码错误"
			return jsonify(result)

@bp.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('NetSecurity/login/login2.html')


@bp.route('/login_validate', methods=['POST', 'GET'])
def login_validate():
	data = request.get_json()
	mobile = data["mobile"]
	m_code = data["m_code"]
	result = {
		"status": 200,
		"msg": ''
	}
	ifCode = CMSMessageCode.query.filter(CMSMessageCode.phone == mobile, CMSMessageCode.sort == 1).order_by(CMSMessageCode.addtime.desc()).first()
	user = CMSMember.query.filter(CMSMember.phone == mobile).first()
	if user:
		code = ifCode.code
		time_delta = (datetime.now() - ifCode.addtime).seconds
		if code == m_code and time_delta < 120:
			login_user(user)
			session[config.CMS_USER_ID] = user.id
			return jsonify(result)
		else:
			result["status"] = '202'
			result["msg"] = "动态码错误"
			return jsonify(result)
	else:
		result["status"] = '201'
		result["msg"] = "手机号不存在"
		return jsonify(result)


# 退出
@bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('NetSecurity.index'))


# 发送验证码
@bp.route('/message')
def message():
	phone = request.args.get("phone")
	sort = request.args.get('sort')
	code = generate_code()
	sent_message(phone, code)
	message_code = CMSMessageCode(phone=phone, code=code, sort=sort)
	db.session.add(message_code)
	db.session.commit()
	result = {
		"status": 200,
		"msg": ''
	}
	return jsonify(result)


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
	two_leaders = CMSLeader.query.order_by(CMSLeader.addtime.desc()).offset(6).limit(6)
	if_two_leader = CMSLeader.query.order_by(CMSLeader.addtime.desc()).offset(6).first()
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
	return render_template('NetSecurity/xhgz/aqfw.html', services=services.items, pagination=services)


@bp.route('/aqfwxq', methods=['GET', 'POST'])
def aqfw_detail():
	id = int(request.args.get('pid'))
	query = CMSBuilding.query.filter(CMSBuilding.id == id).first()
	return render_template('NetSecurity/xhgz/xhgz_detail.html', query=query, kind=4)


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