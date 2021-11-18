from flask import Blueprint, request, jsonify
from .models import CMSUser
from utils.response_code import RET
from exts import db

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
# 注释