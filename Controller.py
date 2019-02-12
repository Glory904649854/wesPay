#coding:utf8
from flask import *
from Utils import *
class Controller(object):
	def __init__(self):
		pass
	def IndexShow(self):
		# print(PaymentUtils.Sort('HH2'))
		# print(PaymentUtils.DictToQueryString(PaymentUtils.Sort({
		# 	"H":"1",
		# 	"A":"21251",
		# 	"SF":"@!321"
		# 	})))
		# print(PaymentUtils.Sort([45,78,12,65,3,748,12,874,5,781,8,51,515]))
		print(PaymentUtils.CreateOrder("WECHAT",{
				"name":"GXSC_WX_APPLICATION"
			}))
		return "This is Init Page For WES+ Pay SDK."
		pass