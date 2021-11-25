from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import jsonify

# 密钥
SECRET_KEY = 'attack_web_secret'


# 生成token
def generate_auth_token(user_id, expiration=36000):
    """
    :param user_id:内部参数
    :param expiration: 有效期(秒)
    :return:
    """
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({"user_id": user_id})


# 解析token
def verify_auth_token(token):
    data = {"rc": 0, "msg": "", "data": ""}
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        token_data = s.loads(token)
        data["data"] = token_data
        data["msg"] = "登录成功"
        print("token success", jsonify(data))
        return jsonify(data)
    # token过期
    except SignatureExpired:
        data["rc"] = 1
        data["msg"] = "token过期"
        print("token out")
        return jsonify(data)
    # token错误
    except BadSignature:
        data["rc"] = 1
        data["msg"] = "token错误"
        print("token wrong")
        return jsonify(data)
