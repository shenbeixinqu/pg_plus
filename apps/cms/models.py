from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# 员工表
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # password_hash = db.Column(db.String(128), nullable=False)
    pwd = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return self.account

    def check_pwd(self, pwd):
        # 返回true密码正确  返回false密码错误
        return check_password_hash(self.pwd, pwd)
    # 加上property装饰器后，会把函数变为属性，属性名即为函数
    # @property
    # def password(self):
    #     """
    #     函数的返回值作为属性值，使用property必须要有返回值
    #     :return:
    #     """
    #     raise AttributeError("属性只能设置,不能读取")
    #
    # @password.setter
    # def password(self, password):
    #     """
    #     它在设置属性的时候被调用
    #     设置属性的方式： user.password = "xxxx"
    #     :param password: 参数是设置属性的属性值，明文密码
    #     :return:
    #     """
    #     # 在视图中设置user_password属性值时，方法被调用，接收password参数，并将设置为字段值
    #     self.password = generate_password_hash(password)
    #
    # def check_password(self, passwd):
    #     """
    #     检验密码的正确性
    #     :param passwd: 登录时填写的原始密码
    #     :return: 正确 返回True 错误 返回 False
    #     """
    #     return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换成字典数据"""
        user_dict = {
            "user_id": self.id,
            "username": self.name
        }
        return user_dict


# 法律
class CMSLaw(db.Model):
    __tablename__ = 'cms_law'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    reorder = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 会员列表
class CMSMember(db.Model):
    __tablename__ = 'cms_member'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    addtime = db.Column(db.DateTime, default=datetime.now)


# 漏洞发布
class CMSLoophole(db.Model):
    __tablename__ = 'cms_loophole'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    reorder = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 安全事件
class CMSEvent(db.Model):
    __tablename__ = 'cms_event'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    reorder = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 安全服务
class CMSService(db.Model):
    __tablename__ = 'cms_service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    mold = db.Column(db.String(10))
    link = db.Column(db.String(100))
    file_dir = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.now)


# 协会简介
class CMSIntroduction(db.Model):
    __tablename__ = 'cms_introduction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 协会章程
class CMSBylaws(db.Model):
    __tablename__ = 'cms_bylaws'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 协会章程
class CMSBranch(db.Model):
    __tablename__ = 'cms_branch'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logo = db.Column(db.String(100))
    address = db.Column(db.String(100))
    href = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 理事单位
class CMSDirectorCompany(db.Model):
    __tablename__ = 'cms_director_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    desc = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 会员单位
class CMSMemberCompany(db.Model):
    __tablename__ = 'cms_member_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 支撑单位
class CMSSupportCompany(db.Model):
    __tablename__ = 'cms_support_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 会费标准
class CMSStandard(db.Model):
    __tablename__ = 'cms_standard'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


"""
协会工作
"""

# 党建活动
class CMSBuilding(db.Model):
    __tablename__ = 'cms_building'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    reorder = db.Column(db.Integer)
    if_banner = db.Column(db.Integer)
    banner_url = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)
    kind = db.Column(db.Integer)