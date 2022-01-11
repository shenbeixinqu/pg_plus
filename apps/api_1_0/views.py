from flask import Blueprint, render_template, request, jsonify, session
from apps.cms.models import *
from utils.random_code import generate_code
from utils.sent_message import sent_message

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		data = request.get_json()
		name = data["name"]
		company = data["company"]
		job = data["job"]
		phone = data["phone"]
		code = data["code"]
		result = {
			"status": 200,
			"msg": ''
		}
		ifCode = CMSMessageCode.query.filter(CMSMessageCode.phone == phone, CMSMessageCode.sort == 7).order_by(
			CMSMessageCode.addtime.desc()).first()
		user = CMSMember.query.filter(CMSMember.phone == phone).first()
		if user:
			result["status"] = '201'
			result["msg"] = "手机号已存在"
			return jsonify(result)
		else:
			r_code = ifCode.code
			time_delta = (datetime.now() - ifCode.addtime).seconds
			if code == r_code and time_delta < 120:
				member = CMSMember(name=name, company=company, position=job, phone=phone)
				db.session.add(member)
				db.session.commit()
				return jsonify(result)
			else:
				result["status"] = '203'
				result["msg"] = "验证码已过期"
				return jsonify(result)
	else:
		return render_template('Safety/mobile_register.html')


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


@bp.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		data = request.get_json()
		phone = data["phone"]
		m_code = data["code"]
		result = {
			"status": 200,
			"msg": ''
		}
		ifCode = CMSMessageCode.query.filter(CMSMessageCode.phone == phone, CMSMessageCode.sort == 6).order_by(CMSMessageCode.addtime.desc()).first()
		user = CMSMember.query.filter(CMSMember.phone == phone).first()
		if user:
			code = ifCode.code
			time_delta = (datetime.now() - ifCode.addtime).seconds
			if code == m_code and time_delta < 120:
				session['user'] = user.name
				return jsonify(result)
			else:
				result["status"] = '202'
				result["msg"] = "动态码错误"
				return jsonify(result)
		else:
			result["status"] = '201'
			result["msg"] = "手机号不存在"
			return jsonify(result)
	else:
		return render_template('Safety/mobile_login.html')


# 党建活动
@bp.route('/buildingList')
def building_list():
	context = {
		'buildings': CMSBuilding.query.filter(CMSBuilding.kind == 1).order_by(CMSBuilding.addtime.desc(), CMSBuilding.reorder.asc())
	}
	return render_template('Safety/djhd_list.html', **context)


# 党建活动详情
@bp.route('/buildingDetail/<building_id>')
def building_detail(building_id):
	building = CMSBuilding.query.filter(CMSBuilding.id == int(building_id)).first()
	if not building:
		print("没有")
	return render_template('Safety/djhd_detail.html', building=building)


# 网安动态
@bp.route('/netList')
def net_list():
	context = {
		'nets': CMSIndustry.query.filter(CMSIndustry.kind == 2).order_by(CMSIndustry.addtime.desc(), CMSIndustry.reorder.asc())
	}
	return render_template('Safety/wadt_list.html', **context)


# 网安动态详情
@bp.route('/netDetail/<net_id>')
def net_detail(net_id):
	net = CMSIndustry.query.filter(CMSIndustry.id == int(net_id)).first()
	if not net:
		print("没有")
	return render_template('Safety/wadt_detail.html', net=net)


# 通知公告列表
@bp.route('/adviseList')
def advise_list():
	context = {
		'advises': CMSNotice.query.filter(CMSNotice.kind == 1).order_by(CMSNotice.addtime.desc(), CMSNotice.reorder.asc())
	}
	return render_template('Safety/tzgg_list.html', **context)


# 通知公告详情
@bp.route('/adviseDetail/<advise_id>')
def advise_detail(advise_id):
	advise = CMSNotice.query.filter(CMSNotice.id == int(advise_id)).first()
	if not advise:
		print("没有")
	return render_template('Safety/tzgg_detail.html', advise=advise)


# 法律法规列表
@bp.route('/lawList')
def law_list():
	context = {
		'laws': CMSNotice.query.filter(CMSNotice.kind == 2).order_by(CMSNotice.addtime.desc())
	}
	return render_template('Safety/law_list.html', **context)


# 法律法规详情
@bp.route('/lawDetail/<law_id>')
def law_detail(law_id):
	law = CMSNotice.query.filter(CMSNotice.id == int(law_id)).first()
	if not law:
		print("没有")
	return render_template('Safety/law_detail.html', law=law)


# 漏洞发布列表
@bp.route('/loopholeList')
def loophole_list():
	context = {
		"loopholes": CMSIndustry.query.filter(CMSIndustry.kind == 3).order_by(CMSIndustry.reorder.asc(), CMSIndustry.addtime.desc())
	}
	return render_template('Safety/loophole_list.html', **context)


# 漏洞发布详情
@bp.route('/loopholeDetail/<loophole_id>')
def loophole_detail(loophole_id):
	loophole = CMSIndustry.query.filter(CMSIndustry.id == int(loophole_id)).first()
	if not loophole:
		print("没有loophole")
	return render_template('Safety/loophole_detail.html', loophole=loophole)


# 安全事件列表
@bp.route('/eventList')
def event_list():
	context = {
		"events": CMSIndustry.query.filter(CMSIndustry.kind == 4).order_by(CMSIndustry.reorder.asc(), CMSIndustry.addtime.desc())
	}
	return render_template('Safety/event_list.html', **context)


# 安全事件详情
@bp.route('/eventDetail/<event_id>')
def event_detail(event_id):
	event = CMSIndustry.query.filter(CMSIndustry.id == int(event_id)).first()
	if not event:
		print("没有event")
	return render_template('Safety/event_detail.html', event=event)


# 安全服务列表
@bp.route('/serviceList')
def service_list():
	user = session.get('user')
	if not user:
		return render_template('Safety/mobile_login.html')
	else:
		context = {
			"services": CMSBuilding.query.filter(CMSBuilding.kind == 4).order_by(CMSBuilding.addtime.desc(), CMSBuilding.reorder.asc())
		}
		return render_template('Safety/service_list.html', **context)


# 安全服务详情
@bp.route('/serviceDetail/<service_id>')
def service_detail(service_id):
	service = CMSBuilding.query.filter(CMSBuilding.id == int(service_id)).first()
	if not service:
		print('没有service')
	return render_template('Safety/service_detail.html', service=service)


@bp.app_template_filter("date_format")
def date_format(value, format="%Y-%m-%d"):
	if not value:
		return ""
	try:
		return value.strftime(format)
	except Exception as e:
		return value