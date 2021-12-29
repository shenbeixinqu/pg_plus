# 导入日志模块
import logging

from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

host = "smsv3.bj.baidubce.com"
access_key_id = "c9650a0c8c6d41fd86fb00952b1ee8a2"
secret_access_key = "12f00b5e229d4a8abe75390da389b8bc"

#设置日志文件的句柄和日志级别
logger = logging.getLogger('baidubce.services.sms.smsclient')
fh = logging.FileHandler("sms_sample.log")
fh.setLevel(logging.DEBUG)

#设置日志文件输出的顺序、结构和内容
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

#创建BceClientConfiguration
config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                endpoint=host)
