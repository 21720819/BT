# import hashlib
# import hmac
# import base64

# def make_signature(timestamp):
#     access_key = 'SdCSP6m7s7H4bba0QO3E'
#     secret_key = 'j2ZH44VF7CoGQNhANEdbJygDSbqJzAUDfcqBCTUg' 

#     secret_key = bytes(secret_key, 'UTF-8')

#     uri = "/sms/v2/services/ncp:sms:kr:263092132141:sms/messages"
#     # uri 중간에 Console - Project - 해당 Project 서비스 ID 입력 (예시 = ncp:sms:kr:263092132141:sms)

    
#     message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
#     message = bytes(message, 'UTF-8')
#     signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
#     return signingKey

import sys
import os
import hashlib
import hmac
import base64
import requests
import time

def	make_signature(timestamp):

	access_key = "SdCSP6m7s7H4bba0QO3E"				# access key id (from portal or Sub Account)
	secret_key = "j2ZH44VF7CoGQNhANEdbJygDSbqJzAUDfcqBCTUg"				# secret key (from portal or Sub Account)
	secret_key = bytes(secret_key, 'UTF-8')

	method = "POST"
	uri = "/sms/v2/services/ncp:sms:kr:292298761053:buytogether/messages"

	message = method + " " + uri + "\n" + timestamp + "\n" + access_key
	message = bytes(message, 'UTF-8')
	signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
	return signingKey