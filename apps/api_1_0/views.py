from flask import Blueprint, render_template, request, jsonify
from apps.cms.models import *

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


# 法律法规列表
@bp.route('/lawList')
def law_list():
	context = {
		'laws': CMSLaw.query.all()
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
		"loopholes": CMSLoophole.query.all()
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
		"events": CMSEvent.query.all()
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
	context = {
		"services": CMSService.query.all()
	}
	return render_template('Safety/service_list.html', **context)


@bp.app_template_filter("date_format")
def date_format(value, format="%Y-%m-%d"):
	if not value:
		return ""
	try:
		return value.strftime(format)
	except Exception as e:
		return value