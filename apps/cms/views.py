from flask import Blueprint, request, jsonify, send_from_directory, url_for
from .models import CMSUser, CMSLaw
from utils.response_code import RET
from utils.return_method import success_return, error_return
from utils.datetime_format import datetimeformat
from config import Base_dir, Base_url
from exts import db

import os
import uuid
import json

bp = Blueprint('cms', __name__, url_prefix='/cms')


@bp.route('/hello')
def index():
    return "123456"


# 注册
@bp.route('/register', methods=["POST"])
def register():
    # 获取请求的json数据，返回字典
    req_dict = request.get_json()
    name = req_dict.get("name")
    password = req_dict.get("password")
    password2 = req_dict.get("password2")
    # 判断是否注册过，未注册则保存到数据库中
    user = CMSUser.query.filter(name=name).first()
    if user:
        return jsonify(errcode=RET.DATAEXIST, errmsg="用户名已存在")
    else:
        user = CMSUser(name=name, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(errcode=RET.OK, errmsg="注册成功")


# 登录
@bp.route('/login', methods=["POST"])
def login():
    data = {}
    data["code"] = RET.OK
    data["errmsg"] = '登录成功'
    return jsonify({"data": data})


# 生成图片名
def picname(name):
    info = os.path.splitext(name)
    name = str(uuid.uuid4()) + info[-1]
    return name


@bp.route('/uploads/<path:filename>')
def get_image(filename):
    up_dir = Base_dir + '/static/uploads/'
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
            print("fileStr", fileStr)
            f = imgs[fileStr]
            f_name = f.filename
            print("f_name", f_name)
            uuid_name = picname(f_name)
            f.save(os.path.join(img_dir, uuid_name))
            url = url_for('cms.get_image', filename=uuid_name)
            img_info_dict["name"] = f_name
            img_info_dict["url"] = Base_url + url
            img_info_lst.append(img_info_dict)
            print('img_info_lst', img_info_lst)
    print('img_info_lst_all', img_info_lst)
    return jsonify(code=RET.OK, errmsg="上传成功", img_info=img_info_lst)


# 添加法律法规
@bp.route('/addLaw', methods=["POST"])
def add_law():
    data = request.get_data()
    data = json.loads(data)
    print("title", data, type(data))
    title = data["title"]
    content = data["detail"]
    if data["id"]:
        print("id", data["id"], type(data["id"]))
        law_id = data["id"]
        law = CMSLaw.query.get(law_id)
        print("law_id", law.id)
        law.title = title
        law.content = content
    else:
        print("打印内容", title, content)
        law = CMSLaw(title=title, content=content)
        db.session.add(law)
    db.session.commit()
    return jsonify(status=RET.OK, msg="成功")


# 法律法规列表
@bp.route('/lawList')
def lawList():
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
    print("title", get_data, type(get_data))
    law_id = get_data["deleteId"]
    print("deleteid", law_id)
    law = CMSLaw.query.get(law_id)
    db.session.delete(law)
    db.session.commit()
    return success_return(**{"data": data})
