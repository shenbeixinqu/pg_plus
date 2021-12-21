from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin


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
class CMSMember(db.Model, UserMixin):
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


# 协会简介/章程/会费标桩
class CMSIntroduction(db.Model):
    """
    kind: 种类, 1:协会简介,2:协会章程,3:会费标准
    """
    __tablename__ = 'cms_introduction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)
    kind = db.Column(db.Integer)


# 协会负责人
class CMSLeader(db.Model):
    __tablename__ = 'cms_leader'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    duty = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    company = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.now)


# 分支机构/理事单位/会员单位/支撑单位
class CMSMemberCompany(db.Model):
    """
    kind:种类, 1:分支机构,2:理事单位,3:会员单位,4:支撑单位
    """
    __tablename__ = 'cms_member_company'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    href = db.Column(db.String(100))
    logo = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    desc = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)
    kind = db.Column(db.Integer)


"""
协会工作
"""

# 协会工作
class CMSBuilding(db.Model):
    """
    reorder: 排序
    if_new: 是否有new图标
    if_banner: 是否轮播
    banner_url: 轮播图片地址
    content: 图文信息
    kind: 种类    1: 党建信息,2:交流活动,3: 教育培训, 4:安全服务
    """
    __tablename__ = 'cms_building'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    reorder = db.Column(db.Integer)
    if_new = db.Column(db.Boolean)
    if_banner = db.Column(db.Integer)
    banner_url = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    # kind =4 (安全事件字段)
    mold = db.Column(db.String(10))
    link = db.Column(db.String(100))
    file_dir = db.Column(db.String(100))
    file_name = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, default=datetime.now)
    adddate = db.Column(db.Date, default=datetime.now())
    kind = db.Column(db.Integer)


# 行业动态
class CMSIndustry(db.Model):
    """
    reorder: 排序
    if_new: 是否有new图标
    if_banner: 是否轮播
    banner_url: 轮播图片地址
    content: 图文信息
    kind: 种类    1: 热点关注, 2:网安动态, 3: 漏洞发布, 4:安全事件
    """
    __tablename__ = 'cms_industry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    reorder = db.Column(db.Integer)
    if_new = db.Column(db.Boolean)
    if_banner = db.Column(db.Integer)
    banner_url = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)
    adddate = db.Column(db.Date, default=datetime.now())
    kind = db.Column(db.Integer)


# 通知公告
class CMSNotice(db.Model):
    """
    kind: 种类, 1:通知公告,2:法律法规
    """
    __tablename__ = 'cms_notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    reorder = db.Column(db.Integer)
    if_new = db.Column(db.Boolean)
    if_banner = db.Column(db.Integer)
    banner_url = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)
    adddate = db.Column(db.Date, default=datetime.now)
    kind = db.Column(db.Integer)


# 底部信息
class CMSFooter(db.Model):
    __tablename__ = 'cms_footer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100))
    content = db.Column(db.TEXT)
    addtime = db.Column(db.DateTime, default=datetime.now)


# 轮播图
class CMSBanner(db.Model):
    """
        kind: sort的子类
        sort: 出自哪个表 1：协会工作 2：行业动态 3：通知公告
        o_id: sort表中的主键id
    """
    __tablename__ = 'cms_banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    o_id = db.Column(db.Integer)
    kind = db.Column(db.Integer)
    sort = db.Column(db.Integer)
    if_banner = db.Column(db.Integer)
    banner_url = db.Column(db.String(100))