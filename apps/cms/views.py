from flask import Blueprint, request, jsonify, send_from_directory, url_for
from .models import (
    CMSUser,
    CMSLaw,
    CMSMember,
    CMSLoophole,
    CMSEvent,
    CMSService,
    CMSIntroduction,
    CMSBylaws,
    CMSStandard,
    CMSMemberCompany,
    CMSSupportCompany,
    CMSDirectorCompany,
    CMSBranch,
    CMSBuilding,
    CMSLeader,
    CMSNotice,
    CMSFooter,
    CMSIndustry
)
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
    base_dir = Base_dir + '/static/uploads/files'
    base_url = Base_url + '/static/uploads/files'
    files = request.files
    f = files["file"]
    f_name = f.filename
    uuid_name = picname(f_name)
    f.save(os.path.join(base_dir, uuid_name))
    file_dir = base_url + '/' + uuid_name
    file_dir = file_dir.replace('\\', '/')
    print("file_dir", file_dir)
    return jsonify(code=RET.OK, file_dir=file_dir)


# 添加安全服务
@bp.route('/addService', methods=['POST'])
def add_service():
    data = request.get_data()
    data = json.loads(data)
    title = data["title"]
    mold = data["mold"]
    link = data["link"]
    file_dir = data["file_dir"]
    print("文件上传", file_dir)
    if mold == '1':
        service = CMSService(title=title, mold=mold, link=link)
    else:
        service = CMSService(title=title, mold=mold, file_dir=file_dir)
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
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


"""
网站接口
"""


# 添加简介
@bp.route('/addIntroduction', methods=['POST'])
def add_introduction():
    data = request.get_data()
    data = json.loads(data)
    content = data["content"]
    if data["id"]:
        introduction_id = data["id"]
        introduction = CMSIntroduction.query.get(introduction_id)
        introduction.content = content
    else:
        introduction = CMSIntroduction(content=content)
        db.session.add(introduction)
    db.session.commit()
    return success_return()


# 协会简介
@bp.route('/introductionList')
def introduction_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSIntroduction.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSIntroduction.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除简介
@bp.route('/deleteIntroduction', methods=['POST'])
def delete_introduction():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    introduction_id = get_data["deleteId"]
    introduction = CMSIntroduction.query.get(introduction_id)
    db.session.delete(introduction)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加协会章程
@bp.route('/addBylaws', methods=['POST'])
def add_bylaws():
    data = request.get_data()
    data = json.loads(data)
    content = data["content"]
    if data["id"]:
        bylaws_id = data["id"]
        bylaws = CMSBylaws.query.get(bylaws_id)
        bylaws.content = content
    else:
        bylaws = CMSBylaws(content=content)
        db.session.add(bylaws)
    db.session.commit()
    return success_return()


# 协会章程列表
@bp.route('/bylawsList')
def bylaws_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSBylaws.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSBylaws.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除协会章程
@bp.route('/deleteBylaws', methods=['POST'])
def delete_bylaws():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    bylaws_id = get_data["deleteId"]
    bylaws = CMSBylaws.query.get(bylaws_id)
    db.session.delete(bylaws)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加分支机构
@bp.route('/addBranch', methods=['POST'])
def add_branch():
    data = request.get_data()
    data = json.loads(data)
    logo = data["logo"]
    content = data["content"]
    address = data["address"]
    href = data["href"]
    if data["id"]:
        branch_id = data["id"]
        branch = CMSBranch.query.get(branch_id)
        branch.logo = logo
        branch.content = content
        branch.address = address
        branch.href = href
    else:
        branch = CMSBranch(logo=logo, content=content, address=address, href=href)
        db.session.add(branch)
    db.session.commit()
    return success_return()


# 分支机构列表
@bp.route('/branchList')
def branch_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSBranch.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSBranch.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "address": q.address,
            "logo": q.logo,
            "content": q.content,
            "href": q.href,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除分支机构
@bp.route('/deleteBranch', methods=['POST'])
def delete_branch():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    branch_id = get_data["deleteId"]
    branch = CMSBranch.query.get(branch_id)
    db.session.delete(branch)
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


# 添加理事单位
@bp.route('/addDirectorCompany', methods=['POST'])
def add_director_company():
    data = request.get_data()
    data = json.loads(data)
    print('data', data)
    name = data["name"]
    content = data["content"]
    logoUrl = data["logoUrl"]
    desc = data["desc"]
    if data["id"]:
        director_id = data["id"]
        director = CMSDirectorCompany.query.get(director_id)
        director.name = name
        director.content = content
        director.logoUrl = logoUrl
        director.desc = desc
    else:
        director = CMSDirectorCompany(name=name, content=content, logo=logoUrl, desc=desc)
        db.session.add(director)
    db.session.commit()
    return success_return()


# 会员单位列表
@bp.route('/directorCompanyList')
def director_company_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSDirectorCompany.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSDirectorCompany.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "logoUrl": q.logo,
            "desc": q.desc,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除会员单位
@bp.route('/deleteDirectorCompany', methods=['POST'])
def delete_director_company():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    director_id = get_data["deleteId"]
    director = CMSDirectorCompany.query.get(director_id)
    db.session.delete(director)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加会员单位
@bp.route('/addMemberCompany', methods=['POST'])
def add_member_company():
    data = request.get_data()
    data = json.loads(data)
    print('data', data)
    name = data["name"]
    content = data["content"]
    logoUrl = data["logoUrl"]
    if data["id"]:
        member_id = data["id"]
        member = CMSMemberCompany.query.get(member_id)
        member.name = name
        member.content = content
        member.logoUrl = logoUrl
    else:
        member = CMSMemberCompany(name=name, content=content, logo=logoUrl)
        db.session.add(member)
    db.session.commit()
    return success_return()


# 会员单位列表
@bp.route('/memberCompanyList')
def member_company_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSMemberCompany.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSMemberCompany.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "logoUrl": q.logo,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除会员单位
@bp.route('/deleteMemberCompany', methods=['POST'])
def delete_member_company():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    member_id = get_data["deleteId"]
    member = CMSMemberCompany.query.get(member_id)
    db.session.delete(member)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加支撑单位
@bp.route('/addSupportCompany', methods=['POST'])
def add_support_company():
    data = request.get_data()
    data = json.loads(data)
    name = data["name"]
    content = data["content"]
    logoUrl = data["logoUrl"]
    if data["id"]:
        support_id = data["id"]
        support = CMSSupportCompany.query.get(support_id)
        support.name = name
        support.content = content
        support.logoUrl = logoUrl
    else:
        support = CMSSupportCompany(name=name, content=content, logo=logoUrl)
        db.session.add(support)
    db.session.commit()
    return success_return()


# 支撑单位列表
@bp.route('/supportCompanyList')
def support_company_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSSupportCompany.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSSupportCompany.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "name": q.name,
            "logoUrl": q.logo,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除支撑单位
@bp.route('/deleteSupportCompany', methods=['POST'])
def delete_support_company():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    support_id = get_data["deleteId"]
    support = CMSSupportCompany.query.get(support_id)
    db.session.delete(support)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加会费标准
@bp.route('/addStandard', methods=['POST'])
def add_standard():
    data = request.get_data()
    data = json.loads(data)
    content = data["content"]
    if data["id"]:
        standard_id = data["id"]
        standard = CMSStandard.query.get(standard_id)
        standard.content = content
    else:
        standard = CMSStandard(content=content)
        db.session.add(standard)
    db.session.commit()
    return success_return()


# 会费标准列表
@bp.route('/standardList')
def standard_list():
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    querys = CMSStandard.query.offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSStandard.query.count()
    data = []
    for q in querys:
        record = {
            "id": q.id,
            "content": q.content,
            "addtime": datetimeformat(q.addtime)
        }
        data.append(record)
    return success_return(**{"data": data, "total": total})


# 删除会费标准
@bp.route('/deleteStandard', methods=['POST'])
def delete_standard():
    get_data = request.get_data()
    get_data = json.loads(get_data)
    standard_id = get_data["deleteId"]
    standard = CMSStandard.query.get(standard_id)
    db.session.delete(standard)
    db.session.commit()
    return success_return(**{"data": {}})


# 添加党建活动
@bp.route('/addBuilding', methods=['POST'])
def add_building():
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
        building_id = data["id"]
        building = CMSBuilding.query.get(building_id)
        building.name = name
        building.reorder = reorder
        building.if_new = if_new
        building.if_banner = if_banner
        building.content = content
        building.banner_url = banner_url
    else:
        branch = CMSBuilding(name=name, reorder=reorder, if_new=if_new,
                             if_banner=if_banner, content=content, banner_url=banner_url, kind=kind)
        db.session.add(branch)
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
    total = CMSBuilding.query.count()
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
        industry.name = name
        industry.reorder = reorder
        industry.if_new = if_new
        industry.if_banner = if_banner
        industry.content = content
        industry.banner_url = banner_url
    else:
        industry = CMSIndustry(name=name, reorder=reorder, if_new=if_new,
                             if_banner=if_banner, content=content, banner_url=banner_url, kind=kind)
        db.session.add(industry)
    db.session.commit()
    return success_return()


# 行业动态列表
@bp.route('/industryList')
def industry_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSIndustry.query.filter(CMSIndustry.kind == kind, CMSIndustry.name.contains(title)).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSIndustry.query.count()
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
        notice.name = name
        notice.reorder = reorder
        notice.if_new = if_new
        notice.if_banner = if_banner
        notice.content = content
        notice.banner_url = banner_url
    else:
        notice = CMSNotice(name=name, reorder=reorder, if_new=if_new,
                             if_banner=if_banner, content=content, banner_url=banner_url, kind=kind)
        db.session.add(notice)
    db.session.commit()
    return success_return()


# 通知公告列表
@bp.route('/noticeList')
def notice_list():
    title = request.values.get("kword")
    pn = int(request.values.get("pn", 1))
    limit_num = int(request.values.get("limit", 10))
    kind = int(request.values.get('kind'))
    querys = CMSNotice.query.filter(CMSNotice.kind == kind, CMSNotice.name.contains(title)).offset((pn-1)*limit_num).limit(limit_num).all()
    total = CMSNotice.query.count()
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