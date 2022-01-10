from flask import Blueprint, render_template, request, jsonify, session
from apps.cms.models import *
from utils.random_code import generate_code
from utils.sent_message import sent_message

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == "POST":
		name = request.values.get("name")
		company = request.values.get("company")
		position = request.values.get("job")
		phone = request.values.get("tel")
		member = CMSMember(name=name, company=company, position=position, phone=phone)
		db.session.add(member)
		db.session.commit()
		return render_template('Safety/success.html')
	return render_template('Safety/register.html')


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


@bp.route('/login', methods=['POST'])
def login():
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


# 法律法规列表
@bp.route('/lawList')
def law_list():
	context = {
		'laws': CMSLaw.query.order_by(CMSLaw.reorder.asc(), CMSLaw.addtime.desc())
	}
	return render_template('Safety/law_list.html', **context)


# 法律法规详情
@bp.route('/lawDetail/<law_id>')
def law_detail(law_id):
	law = CMSLaw.query.filter(CMSLaw.id == int(law_id)).first()
	if not law:
		print("没有")
	return render_template('Safety/law_detail.html', law=law)


# 漏洞发布列表
@bp.route('/loopholeList')
def loophole_list():
	context = {
		"loopholes": CMSLoophole.query.order_by(CMSLoophole.reorder.asc(), CMSLoophole.addtime.desc())
	}
	return render_template('Safety/loophole_list.html', **context)


# 漏洞发布详情
@bp.route('/loopholeDetail/<loophole_id>')
def loophole_detail(loophole_id):
	loophole = CMSLoophole.query.filter(CMSLoophole.id == int(loophole_id)).first()
	if not loophole:
		print("没有loophole")
	return render_template('Safety/loophole_detail.html', loophole=loophole)


# 安全事件列表
@bp.route('/eventList')
def event_list():
	context = {
		"events": CMSEvent.query.order_by(CMSEvent.reorder.asc(), CMSEvent.addtime.desc())
	}
	return render_template('Safety/event_list.html', **context)


# 安全事件详情
@bp.route('/eventDetail/<event_id>')
def event_detail(event_id):
	event = CMSEvent.query.filter(CMSEvent.id == int(event_id)).first()
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
			"services": CMSService.query.order_by(CMSService.addtime.desc())
		}
		return render_template('Safety/service_list.html', **context)


# 安全服务详情
@bp.route('/serviceDetail/<service_id>')
def service_detail(service_id):
	service = CMSService.query.filter(CMSService.id == int(service_id)).first()
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