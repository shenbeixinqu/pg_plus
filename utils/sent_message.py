from utils import sms_client_conf
from baidubce.services.sms.sms_client import SmsClient

CONF = sms_client_conf
sms_client = SmsClient(CONF.config)


def sent_message(phone, code):
	invoke_id = 'sms-sign-nsKuoj84415'
	template_id = 'sms-tmpl-glPphb32011'
	# 签名id
	# invoke_id = 'sms-sign-WzJrGP38877'
	# 模板id
	# template_id = 'sms-tmpl-DmUjoF26348'
	mobile = phone
	content_var = {"code": code}
	response = sms_client.send_message(invoke_id, template_id, mobile, content_var)
