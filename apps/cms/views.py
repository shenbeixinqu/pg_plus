from flask import Blueprint, request, jsonify, send_from_directory, url_for
from .models import CMSUser, CMSLaw, CMSMember, CMSLoophole, CMSEvent, CMSService
from utils.response_code import RET
from utils.return_method import success_return, error_return
from utils.datetime_format import datetimeformat
from config import Base_dir, Base_url
from exts import db
from flask_httpauth import HTTPBasicAuth
from utils.minerequests import generate_auth_token, verify_auth_token
from werkzeug.security import generate_password_hash

import os
import uuid
import json

bp = Blueprint('cms', __name__, url_prefix='/cms')
auth = HTTPBasicAuth()


@bp.route('/hello')
def index():
    return "123456"


# 注册
@bp.route('/register', methods=["POST"])
def register():
    # 获取请求的json数据，返回字典
    data = {"rc": 0, "data": "", "msg": ""}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    name = get_data["account"]
    password = get_data["password"]
    print("name", name, "password", password)
    # 判断是否注册过，未注册则保存到数据库中
    user = CMSUser.query.filter(CMSUser.name == name).first()
    if user:
        return success_return(msg="用户名已存在", rc=1)
    else:
        account = CMSUser(name=name, pwd=generate_password_hash(password))
        db.session.add(account)
        db.session.commit()
        return success_return(msg="注册成功", rc=0)


# 登录
@bp.route('/login', methods=["POST"])
def login():
    data = {"rc": 0, "data": "", "msg": ""}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    account = get_data["account"]
    password = get_data["password"]
    token = get_data["token"]
    if token and account == "":
        check_value = verify_auth_token(token)
    if account == "" or password == "":
        data["rc"] = 1
        data["msg"] = "账号和密码不能为空"
    else:
        user = CMSUser.query.filter(CMSUser.name == account).first()
        if not user or not user.check_pwd(password):
            print("账号密码错误")
            data["rc"] = 1
            data["msg"] = "账号或密码错误"
            return success_return(msg="账号或密码错误", rc=1)
        else:
            user_id = user.id
            token_data = generate_auth_token(user_id)
            token_data = bytes.decode(token_data)
            data["msg"] = "登录成功"
            data["account"] = account
            data["token"] = token_data
    # return jsonify({"data": data})
    return success_return(**{"data": data})


# 退出
@bp.route('/logout', methods=["POST"])
def log_out():
    data = {"rc": 0, "data": "", "msg": ""}
    token_data = request.args.get("token")
    return success_return(**{"data": data})


# 生成图片名
def picname(name):
    info = os.path.splitext(name)
    name = str(uuid.uuid4()) + info[-1]
    return name


@bp.route('/uploads/<path:filename>')
def get_image(filename):
    up_dir = Base_dir + '/static/uploads/'
    return send_from_directory(up_dir, filename)


@bp.route('/fileuploads/<path:filename>')
def get_file(filename):
    up_dir = Base_dir + '/static/uploads/files'
    return send_from_directory(up_dir, filename)



# 图片上传
@bp.route('/imgUpload', methods=["POST"])
def imgUpload():
    img_dir = Base_dir + '/static/uploads/'
    img_info_lst = []
    imgs = request.files
    img_len = len(imgs)
    if img_len == 1:
        img_info_dict = {}
        f = imgs["file"]
        f_name = f.filename
        uuid_name = picname(f_name)
        f.save(os.path.join(img_dir, uuid_name))
        url = url_for('cms.get_image', filename=uuid_name)
        img_info_dict["name"] = f_name
        img_info_dict["url"] = Base_url + url
        img_info_lst.append(img_info_dict)

    elif img_len > 1:
        for index in range(img_len):
            img_info_dict = {}
            fileStr = "file" + str(index+1)
            f = imgs[fileStr]
            f_name = f.filename
            uuid_name = picname(f_name)
            f.save(os.path.join(img_dir, uuid_name))
            url = url_for('cms.get_image', filename=uuid_name)
            img_info_dict["name"] = f_name
            img_info_dict["url"] = Base_url + url
            img_info_lst.append(img_info_dict)
    return jsonify(code=RET.OK, errmsg="上传成功", img_info=img_info_lst)


# 文件上传
@bp.route('/fileUpload', methods=['POST'])
def fileUpload():
    file_dir = Base_dir + '/static/uploads/files'
    files = request.files
    f = files["file"]
    f_name = f.filename
    uuid_name = picname(f_name)
    f.save(os.path.join(file_dir, uuid_name))
    url = url_for('cms.get_file', filename=uuid_name)
    file_dir = Base_url + url
    file_dir = file_dir.replace('\\', '/')
    return jsonify(code=RET.OK, file_dir=file_dir)


# 添加安全服务
@bp.route('addService', methods=['POST'])
def add_service():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    mold = data["mold"]
    link = data["link"]
    file_dir = data["file_dir"]
    if mold == '1':
        service = CMSService(title=title, mold=mold, link=link)
    else:
        service = CMSService(title=title, mold=mold, file_dir=file_dir)
    db.session.add(service)
    db.session.commit()
    print("serviceData", data)
    return success_return()


# 安全服务列表
@bp.route('serviceList')
def service_list():
    title = request.values.get("kword")
    if title:
        querys = CMSService.query.filter(CMSService.title.contains(title)).all()
        total = CMSService.query.filter(CMSService.title.contains(title)).count()
    else:
        querys = CMSService.query.all()
        total = CMSService.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "mold": "链接" if q.mold == '1' else "文件",
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除安全服务
@bp.route('deleteService', methods=['POST'])
def delete_service():
    data = {}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    service_id = get_data["deleteId"]
    service = CMSService.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    return success_return(**{"data": data})


# 添加法律法规
@bp.route('/addLaw', methods=["POST"])
def add_law():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    content = data["detail"]
    if data["id"]:
        law_id = data["id"]
        law = CMSLaw.query.get(law_id)
        law.title = title
        law.content = content
    else:
        law = CMSLaw(title=title, content=content)
        db.session.add(law)
    db.session.commit()
    return success_return()


# 法律法规列表
@bp.route('/lawList')
def lawList():
    title = request.values.get("kword")
    if title:
        querys = CMSLaw.query.filter(CMSLaw.title.contains(title)).all()
        total = CMSLaw.query.filter(CMSLaw.title.contains(title)).count()
    else:
        querys = CMSLaw.query.all()
        total = CMSLaw.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除法律法规
@bp.route('/deleteLaw', methods=['POST'])
def delete_law():
    data = {}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    law_id = get_data["deleteId"]
    law = CMSLaw.query.get(law_id)
    db.session.delete(law)
    db.session.commit()
    return success_return(**{"data": data})


# 添加漏洞发布
@bp.route('/addLoophole', methods=["POST"])
def add_loophole():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    content = data["detail"]
    if data["id"]:
        loophole_id = data["id"]
        loophole = CMSLoophole.query.get(loophole_id)
        loophole.title = title
        loophole.content = content
    else:
        loophole = CMSLoophole(title=title, content=content)
        db.session.add(loophole)
    db.session.commit()
    return success_return()


# 漏洞发布列表
@bp.route('/loopholeList')
def loophole_list():
    title = request.values.get("kword")
    if title:
        querys = CMSLoophole.query.filter(CMSLoophole.title.contains(title)).all()
        total = CMSLoophole.query.filter(CMSLoophole.title.contains(title)).count()
    else:
        querys = CMSLoophole.query.all()
        total = CMSLoophole.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除漏洞删除
@bp.route('/deleteLoophole', methods=["POST"])
def delete_loophole():
    data = {}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    loophole_id = get_data["deleteId"]
    loophole = CMSLoophole.query.get(loophole_id)
    db.session.delete(loophole)
    db.session.commit()
    return success_return(**{"data": data})


# 添加安全事件
@bp.route('/addEvent', methods=["POST"])
def add_event():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    content = data["detail"]
    if data["id"]:
        event_id = data["id"]
        event = CMSEvent.query.get(event_id)
        event.title = title
        event.content = content
    else:
        event = CMSEvent(title=title, content=content)
        db.session.add(event)
    db.session.commit()
    return success_return()


# 安全事件列表
@bp.route('/eventList')
def event_list():
    title = request.values.get("kword")
    if title:
        querys = CMSEvent.query.filter(CMSEvent.title.contains(title)).all()
        total = CMSEvent.query.filter(CMSEvent.title.contains(title)).count()
    else:
        querys = CMSEvent.query.all()
        total = CMSEvent.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 安全事件删除
@bp.route('/deleteEvent', methods=["POST"])
def delete_event():
    data = {}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    event_id = get_data["deleteId"]
    event = CMSEvent.query.get(event_id)
    db.session.delete(event)
    db.session.commit()
    return success_return(**{"data": data})


# 会员列表
@bp.route('/memberList')
def member_list():
    title = request.values.get("kword")
    if title:
        querys = CMSMember.query.filter(CMSMember.name.contains(title)).all()
        total = CMSMember.query.filter(CMSMember.name.contains(title)).count()
    else:
        querys = CMSMember.query.all()
        total = CMSMember.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "company": q.company,
            "position": q.position,
            "phone": q.phone,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})
