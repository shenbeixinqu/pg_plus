# 从Python SDK导入BOS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
# 导入BOS相关模块
from baidubce.services.bos.bos_client import BosClient


class Bd_Storage(object):
    def __init__(self):
        # 设置BosClient的Host，Access Key ID和Secret Access Key
        self.bos_host = "liaoningshengxinxiwangluoanquanxiehui.bj.bcebos.com"	# 地址可以改，参考百度的python SDK文档
        self.access_key_id = "7fa9a8d02a1240888971f2b928daba7c"
        self.secret_access_key = "27d91e7a4d95452cbed0aec229c81f84"
        self.back_name = "waxh"

    def up_image(self, key_name, file):
        config = BceClientConfiguration(credentials =
                                        BceCredentials(self.access_key_id, self.secret_access_key),
                                        endpoint = self.bos_host)
        client = BosClient(config)

        key_name = key_name
        try:
            res = client.put_object_from_string(bucket = self.back_name, key = key_name, data = file)
        except Exception as e:
            return None
        else:
            result = res.__dict__
            if result['metadata']:
                url = 'https://' + self.bos_host + '/' + self.back_name + '/' + key_name
                return url

    @staticmethod
    def open_image(file_dir, file_name):
        with open(file_dir, 'rb') as f:
            bd = Bd_Storage()
            s = f.read()
            result = bd.up_image(file_name, s)
        return result
