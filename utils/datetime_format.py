# 日期时间格式化
def datetimeformat(value, format="%Y-%m-%d %H:%M:%S"):
    if not value:return ""
    try:
        return value.strftime(format)
    except:
        return value


def dateformat(value, format="%Y-%m-%d"):
    if not value:return ""
    try:
        return value.strftime(format)
    except:
        return value