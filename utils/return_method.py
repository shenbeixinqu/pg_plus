from flask import jsonify


# 返回错误信息
def error_return(msg, status=0):
    result = {
        "rc": 0,
        "msg": msg,
        "data": {
            "status": status
        }
    }
    return jsonify(result)


# 返回成功信息
def success_return(msg="操作成功", **kwargs):
    result = {
        "rc": 0,
        "msg": msg,
        "data": {
            "status": 200
        }
    }
    for key in kwargs:
        result["data"][key] = kwargs[key]
    return jsonify(result)