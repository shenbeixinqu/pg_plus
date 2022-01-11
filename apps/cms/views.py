from flask import Blueprint, request, jsonify, send_from_directory, url_for
from .models import (
    CMSUser,
    CMSLaw,
    CMSMember,
    CMSLoophole,
    CMSEvent,
    CMSService,
    CMSIntroduction,
    CMSMemberCompany,
    CMSBuilding,
    CMSLeader,
    CMSNotice,
    CMSFooter,
    CMSIndustry,
    CMSBanner,
    CMSMessageCode
)
from utils.response_code import RET
from utils.return_method import success_return, error_return
from utils.datetime_format import datetimeformat, dateformat
from config import Base_dir, Base_url
from exts import db
from flask_httpauth import HTTPBasicAuth
from utils.minerequests import generate_auth_token, verify_auth_token
from werkzeug.security import generate_password_hash
from utils.random_code import generate_code
from utils.sent_message import sent_message
from bos_conf import Bd_Storage

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
    print('account', account, 'password', password, 'token', token)
    if token and account == "":
        check_value = verify_auth_token(token)
    if account == "":
        data["rc"] = 1
        data["msg"] = "手机号不能为空"
    else:
        user = CMSUser.query.filter(CMSUser.phone == account).first()
        if not user:
            data["rc"] = 1
            data["msg"] = "手机号错误"
            return success_return(msg="手机号或密验证码错误", rc=1)
        else:
            user_id = user.id
            token_data = generate_auth_token(user_id)
            token_data = bytes.decode(token_data)
            data["msg"] = "登录成功"
            data["account"] = account
            data["token"] = token_data
    return success_return(**{"data": data})


@bp.route('/message')
def message():
    account = request.args.get('account')
    code = generate_code()
    sent_message(account,code)
    message_code = CMSMessageCode(phone=account, code=code, sort=3)
    db.session.add(message_code)
    db.session.commit()
    return success_return(**{"code": code})

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
    img_dir = Base_dir + '/static/uploads/editorImgs'
    img_info_lst = []
    imgs = request.files
    img_len = len(imgs)
    if img_len == 1:
        img_info_dict = {}
        f = imgs["file"]
        f_name = f.filename
        uuid_name = picname(f_name)
        f.save(os.path.join(img_dir, uuid_name))
        basic_file_dir = img_dir + '/' + uuid_name
        basic_file_dir = basic_file_dir.replace('\\', '/')
        file_dir = Bd_Storage.open_image(basic_file_dir, uuid_name)
        # url = url_for('cms.get_image', filename=uuid_name)
        img_info_dict["name"] = f_name
        img_info_dict["url"] = file_dir
        img_info_lst.append(img_info_dict)

    elif img_len > 1:
        for index in range(img_len):
            img_info_dict = {}
            fileStr = "file" + str(index+1)
            f = imgs[fileStr]
            f_name = f.filename
            uuid_name = picname(f_name)
            f.save(os.path.join(img_dir, uuid_name))
            basic_file_dir = img_dir + '/' + uuid_name
            basic_file_dir = basic_file_dir.replace('\\', '/')
            file_dir = Bd_Storage.open_image(basic_file_dir, uuid_name)
            # url = url_for('cms.get_image', filename=uuid_name)
            img_info_dict["name"] = f_name
            img_info_dict["url"] = file_dir
            img_info_lst.append(img_info_dict)
    return jsonify(code=RET.OK, errmsg="上传成功", img_info=img_info_lst)


# 文件上传
@bp.route('/fileUpload', methods=['POST'])
def fileUpload():
    base_dir = Base_dir + '/static/uploads/files'
    # base_url = Base_url + '/static/uploads/files'
    files = request.files
    f = files["file"]
    f_name = f.filename
    uuid_name = picname(f_name)
    f.save(os.path.join(base_dir, uuid_name))
    basic_file_dir = base_dir + '/' + uuid_name
    basic_file_dir = basic_file_dir.replace('\\', '/')
    file_dir = Bd_Storage.open_image(basic_file_dir, uuid_name)
    return jsonify(code=RET.OK, file_dir=file_dir)


# 管理员列表
@bp.route('/userList')
def user_list():
    phone = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    if phone:
        querys = CMSUser.query.filter(CMSUser.phone.contains(phone)).order_by(CMSUser.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSUser.query.filter(CMSUser.phone.contains(phone)).count()
    else:
        querys = CMSUser.query.order_by(CMSUser.addtime.desc()).offset((pn - 1) * limit_num).limit(
            limit_num).all()
        total = CMSUser.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "phone": q.phone
        }
        data.append(record)
    return success_return(**{"data": data, "total":total})


# 添加管理员
@bp.route('/addUser', methods=['POST'])
def add_user():
    data = request.get_data()
    data = json.loads(data)
    print("Data", data)
    phone = data["phone"]
    if data["id"]:
        user_id = data["id"]
        user = CMSUser.query.get(user_id)
        user.phone = phone
    else:
        user = CMSUser(phone=phone)
        db.session.add(user)
    db.session.commit()
    return success_return()


# 删除管理员
@bp.route('/deleteUser', methods=['POST'])
def delete_user():
    data = {}
    get_data = request.get_data()
    get_data = json.loads(get_data)
    user_id = get_data["deleteId"]
    user = CMSUser.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return success_return(**{"data": data})



# 添加安全服务
@bp.route('/addService', methods=['POST'])
def add_service():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    mold = data["mold"]
    link = data["link"]
    file_dir = data["file_dir"]
    detail = data["detail"]
    if data['id']:
        service_id = data['id']
        service = CMSService.query.get(service_id)
        service.mold = mold
        service.link = link
        service.file_dir = file_dir
        service.detail = detail
    else:
        # if mold == '1':
        #     service = CMSService(title=title, mold=mold, link=link, detail=detail)
        # else:
        #     service = CMSService(title=title, mold=mold, file_dir=file_dir, detail=detail)
        service = CMSService(title=title, mold=mold, file_dir=file_dir, link=link, detail=detail)
        db.session.add(service)
    db.session.commit()
    return success_return()


# 安全服务列表
@bp.route('/serviceList')
def service_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    if title:
        querys = CMSService.query.filter(CMSService.title.contains(title)).order_by(CMSService.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSService.query.filter(CMSService.title.contains(title)).count()
    else:
        querys = CMSService.query.order_by(CMSService.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSService.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "mold": "链接" if q.mold == '1' else "文件",
            "mold_val": q.mold,
            "link": q.link,
            "detail": q.detail,
            "file_dir": q.file_dir,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除安全服务
@bp.route('/deleteService', methods=['POST'])
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
    reorder = data["reorder"]
    if data["id"]:
        law_id = data["id"]
        law = CMSLaw.query.get(law_id)
        law.title = title
        law.content = content
        law.reorder = reorder
    else:
        law = CMSLaw(title=title, content=content, reorder=reorder)
        db.session.add(law)
    db.session.commit()
    return success_return()


# 法律法规列表
@bp.route('/lawList')
def lawList():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    if title:
        querys = CMSLaw.query.filter(CMSLaw.title.contains(title)).order_by(CMSLaw.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSLaw.query.filter(CMSLaw.title.contains(title)).count()
    else:
        querys = CMSLaw.query.order_by(CMSLaw.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSLaw.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "reorder": q.reorder,
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
    reorder = data["reorder"]
    if data["id"]:
        loophole_id = data["id"]
        loophole = CMSLoophole.query.get(loophole_id)
        loophole.title = title
        loophole.content = content
        loophole.reorder = reorder
    else:
        loophole = CMSLoophole(title=title, content=content, reorder=reorder)
        db.session.add(loophole)
    db.session.commit()
    return success_return()


# 漏洞发布列表
@bp.route('/loopholeList')
def loophole_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn",1))
    limit_num = int(request.values.get("limit", 10))
    if title:
        querys = CMSLoophole.query.filter(CMSLoophole.title.contains(title)).order_by(CMSLoophole.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSLoophole.query.filter(CMSLoophole.title.contains(title)).count()
    else:
        querys = CMSLoophole.query.order_by(CMSLoophole.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSLoophole.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "reorder": q.reorder,
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
    reorder = data["reorder"]
    if data["id"]:
        event_id = data["id"]
        event = CMSEvent.query.get(event_id)
        event.title = title
        event.content = content
        event.reorder = reorder
    else:
        event = CMSEvent(title=title, content=content, reorder=reorder)
        db.session.add(event)
    db.session.commit()
    return success_return()


# 安全事件列表
@bp.route('/eventList')
def event_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    if title:
        querys = CMSEvent.query.filter(CMSEvent.title.contains(title)).order_by(CMSEvent.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSEvent.query.filter(CMSEvent.title.contains(title)).count()
    else:
        querys = CMSEvent.query.order_by(CMSEvent.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSEvent.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "title": q.title,
            "content": q.content,
            "reorder": q.reorder,
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
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    if title:
        querys = CMSMember.query.filter(CMSMember.name.contains(title)).offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSMember.query.filter(CMSMember.name.contains(title)).count()
    else:
        querys = CMSMember.query.offset((pn-1)*limit_num).limit(limit_num).all()
        total = CMSMember.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "company": q.company,
            "position": q.position,
            "phone": q.phone,
            "status": "正常" if q.status == 1 else "移除",
            "status_val": q.status,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 更改会员状态
@bp.route('/memberStatus')
def member_status():
    id = request.args.get('id')
    kind = int(request.args.get("kind"))
    member = CMSMember.query.filter(CMSMember.id == id).first()
    member.status = kind
    db.session.commit()
    return success_return()


"""
网站接口
"""


# 添加简介/章程/会费
@bp.route('/addIntroduction', methods=['POST'])
def add_introduction():
    data = request.get_data()
    data = json.loads(data)
    content = data["content"]
    kind = data["kind"]
    if data["id"]:
        introduction_id = data["id"]
        introduction = CMSIntroduction.query.get(introduction_id)
        introduction.content = content
    else:
        introduction = CMSIntroduction(content=content, kind=kind)
        db.session.add(introduction)
    db.session.commit()
    return success_return()


# 简介/章程/会费列表
@bp.route('/introductionList')
def introduction_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSIntroduction.query.filter(CMSIntroduction.kind == kind).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSIntroduction.query.filter(CMSIntroduction.kind == kind).count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除简介/章程/会费
@bp.route('/deleteIntroduction', methods=['POST'])
def delete_introduction():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    introduction_id = get_data["deleteId"]
    introduction = CMSIntroduction.query.get(introduction_id)
    db.session.delete(introduction)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加协会负责人
@bp.route('/addLeader', methods=['POST'])
def add_leader():
    data = request.get_data()
    data = json.loads(data)
    name = data["name"]
    photo = data["photo"]
    content = data["content"]
    duty = data["duty"]
    company = data["company"]
    if data["id"]:
        leader_id = data["id"]
        leader = CMSLeader.query.get(leader_id)
        leader.name = name
        leader.content = content
        leader.photo = photo
        leader.duty = duty
        leader.company = company
    else:
        leader = CMSLeader(name=name, content=content, photo=photo, duty=duty, company=company)
        db.session.add(leader)
    db.session.commit()
    return success_return()


# 协会负责人列表
@bp.route('/leaderList')
def leader_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSLeader.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSLeader.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "photo": q.photo,
            "content": q.content,
            "duty": q.duty,
            "company": q.company,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除协会负责人
@bp.route('/deleteLeader', methods=['POST'])
def delete_leader():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    leader_id = get_data["deleteId"]
    leader = CMSLeader.query.get(leader_id)
    db.session.delete(leader)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加会员单位/支撑单位/理事单位/分支机构
@bp.route('/addMemberCompany', methods=['POST'])
def add_member_company():
    data = request.get_data()
    data = json.loads(data)
    print('data', data)
    name = data["name"]
    content = data["content"]
    logoUrl = data["logoUrl"]
    desc = data["desc"]
    address = data["address"]
    href = data["href"]
    kind = data["kind"]
    if data["id"]:
        member_id = data["id"]
        member = CMSMemberCompany.query.get(member_id)
        member.name = name
        member.address = address
        member.href = href
        member.content = content
        member.logo = logoUrl
        member.desc = desc
    else:
        member = CMSMemberCompany(name=name, content=content, logo=logoUrl, desc=desc, address=address, href=href, kind=kind)
        db.session.add(member)
    db.session.commit()
    return success_return()


# 会员单位/支撑单位/理事单位/分支机构列表
@bp.route('/memberCompanyList')
def member_company_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSMemberCompany.query.filter(CMSMemberCompany.kind == kind).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSMemberCompany.query.filter(CMSMemberCompany.kind == kind).count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "address": q.address,
            "href": q.href,
            "logoUrl": q.logo,
            "desc": q.desc,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除会员单位/支撑单位/理事单位/分支机构
@bp.route('/deleteMemberCompany', methods=['POST'])
def delete_member_company():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    member_id = get_data["deleteId"]
    member = CMSMemberCompany.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加党建活动
@bp.route('/addBuilding', methods=['POST'])
def add_building():
    data = request.get_data()
    data = json.loads(data)
    print("DATA", data)
    name = data["name"]
    reorder = data["reorder"] if data["reorder"] else 1
    if_new = data["if_new"]
    if_banner = data["if_banner"]
    banner_url = data["banner_url"]
    content = data["content"]
    kind = data["kind"]
    mold = data["mold"]
    link = data["link"]
    desc = data["desc"]
    file_name = data["file_name"]
    file_dir = data["file_dir"]
    if data["id"]:
        building_id = data["id"]
        building = CMSBuilding.query.get(building_id)
        if kind != 4:
            banner = CMSBanner.query.filter(CMSBanner.o_id == building_id).first()
            banner.banner_url = banner_url
            banner.if_banner = if_banner
        building.name = name
        building.reorder = reorder
        building.if_new = if_new
        building.if_banner = if_banner
        building.content = content
        building.banner_url = banner_url
        building.mold = mold
        building.link = link
        building.desc = desc
        building.file_dir = file_dir
        building.file_name = file_name

        db.session.commit()
    else:
        if kind == 4:
            building = CMSBuilding(name=name, reorder=reorder, if_new=if_new, if_banner=if_banner, content=content,
                                banner_url=banner_url, kind=kind, mold=mold,  link=link, desc=desc, file_dir=file_dir, file_name=file_name)
        else:
            building = CMSBuilding(name=name, reorder=reorder, if_new=if_new,
                                 if_banner=if_banner, content=content, banner_url=banner_url, kind=kind)
        db.session.add(building)
        db.session.commit()
        if kind != 4:
            banner = CMSBanner(kind=kind, sort=1, if_banner=if_banner, banner_url=banner_url, o_id=building.id)
            db.session.add(banner)
            db.session.commit()
    return success_return()


# 党建活动列表
@bp.route('/buildingList')
def building_list():
    pn = int(request.values.get("pn", 1))
    title = request.values.get("kword")
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSBuilding.query.filter(CMSBuilding.kind == kind, CMSBuilding.name.contains(title)).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSBuilding.query.filter(CMSBuilding.kind == kind,).count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "reorder": q.reorder,
            "if_new": q.if_new,
            "if_banner": q.if_banner,
            "banner_url": q.banner_url,
            "content": q.content,
            # "mold": "链接" if q.mold == '1' else "文件",
            "mold": q.mold,
            "link": q.link,
            "desc": q.desc,
            "file_dir": q.file_dir,
            "file_name": q.file_name,
            "addtime": datetimeformat(q.addtime),
            "adddate": dateformat(q.adddate)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除党建活动
@bp.route('/deleteBuilding', methods=['POST'])
def delete_building():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    building_id = get_data["deleteId"]
    building = CMSBuilding.query.get(building_id)
    db.session.delete(building)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加行业动态
@bp.route('/addIndustry', methods=['POST'])
def add_industry():
    data = request.get_data()
    data = json.loads(data)
    name = data["name"]
    reorder = data["reorder"] if data["reorder"] else 1
    if_new = data["if_new"]
    if_banner = data["if_banner"]
    banner_url = data["banner_url"]
    content = data["content"]
    kind = data["kind"]
    if data["id"]:
        industry_id = data["id"]
        industry = CMSIndustry.query.get(industry_id)
        banner = CMSBanner.query.filter(CMSBanner.o_id == industry_id,CMSBanner.sort == 2).first()
        industry.name = name
        industry.reorder = reorder
        industry.if_new = if_new
        industry.if_banner = if_banner
        industry.content = content
        industry.banner_url = banner_url
        banner.if_banner = if_banner
        banner.banner_url = banner_url
        db.session.commit()
    else:
        industry = CMSIndustry(name=name, reorder=reorder, if_new=if_new, if_banner=if_banner,
                                   content=content, banner_url=banner_url, kind=kind)
        db.session.add(industry)
        db.session.commit()
        banner = CMSBanner(kind=kind, sort=2, if_banner=if_banner, banner_url=banner_url, o_id=industry.id)
        db.session.add(banner)
        db.session.commit()
    return success_return()


# 行业动态列表
@bp.route('/industryList')
def industry_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSIndustry.query.filter(CMSIndustry.kind == kind, CMSIndustry.name.contains(title)).order_by(CMSIndustry.reorder.asc(), CMSIndustry.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSIndustry.query.filter(CMSIndustry.kind == kind).count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "reorder": q.reorder,
            "if_new": q.if_new,
            "if_banner": q.if_banner,
            "banner_url": q.banner_url,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除行业动态
@bp.route('/deleteIndustry', methods=['POST'])
def delete_industry():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    industry_id = get_data["deleteId"]
    industry = CMSIndustry.query.get(industry_id)
    db.session.delete(industry)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加通知公告
@bp.route('/addNotice', methods=['POST'])
def add_notice():
    data = request.get_data()
    data = json.loads(data)
    name = data["name"]
    reorder = data["reorder"] if data["reorder"] else 1
    if_new = data["if_new"]
    if_banner = data["if_banner"]
    banner_url = data["banner_url"]
    content = data["content"]
    kind = data["kind"]
    if data["id"]:
        notice_id = data["id"]
        notice = CMSNotice.query.get(notice_id)
        banner = CMSBanner.query.filter(CMSBanner.o_id == notice_id, CMSBanner.sort == 3).first()
        notice.name = name
        notice.reorder = reorder
        notice.if_new = if_new
        notice.if_banner = if_banner
        notice.content = content
        notice.banner_url = banner_url
        banner.if_banner = if_banner
        banner.banner_url = banner_url
        db.session.commit()
    else:
        notice = CMSNotice(name=name, reorder=reorder, if_new=if_new,
                             if_banner=if_banner, content=content, banner_url=banner_url, kind=kind)
        db.session.add(notice)
        db.session.commit()
        banner = CMSBanner(kind=kind, sort=3, if_banner=if_banner, banner_url=banner_url, o_id=notice.id)
        db.session.add(banner)
        db.session.commit()
    return success_return()


# 通知公告列表
@bp.route('/noticeList')
def notice_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSNotice.query.filter(CMSNotice.kind == kind, CMSNotice.name.contains(title)).order_by(CMSNotice.addtime.desc()).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSNotice.query.filter(CMSNotice.kind == kind).count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "reorder": q.reorder,
            "if_new": q.if_new,
            "if_banner": q.if_banner,
            "banner_url": q.banner_url,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除通知公告
@bp.route('/deleteNotice', methods=['POST'])
def delete_notice():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    notice_id = get_data["deleteId"]
    notice = CMSNotice.query.get(notice_id)
    db.session.delete(notice)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加底部信息
@bp.route('/addFooter', methods=['POST'])
def add_footer():
    data = request.get_data()
    data = json.loads(data)
    content = data["content"]
    code = data["code"]
    if data["id"]:
        footer_id = data["id"]
        footer = CMSFooter.query.get(footer_id)
        footer.content = content
        footer.code = code
    else:
        footer = CMSFooter(content=content, code=code)
        db.session.add(footer)
    db.session.commit()
    return success_return()


# 底部信息列表
@bp.route('/footerList')
def footer_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSFooter.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSFooter.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "code": q.code,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除底部信息
@bp.route('/deleteFooter', methods=['POST'])
def delete_footer():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    footer_id = get_data["deleteId"]
    footer = CMSFooter.query.get(footer_id)
    db.session.delete(footer)
    db.session.commit()
    return success_return(**{"data": {}})