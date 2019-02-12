#coding:utf8
import json,hashlib,requests,uuid,time,re
class PaymentUtils:
	@staticmethod
	def Config(name=None):
		confisString_ = '';
		with open('payment.config.json','r') as f:
			confisString_ = f.read();
		if not name:
			return json.loads(confisString_);
		confisString_ = json.loads(confisString_);
		tmpObject = None;
		for _ in confisString_['PaymentConfig']['Configs']:
			if _['Name'] == name:
				tmpObject = _;
				break;
		return tmpObject;
	@staticmethod
	def MD5(sourceString):
		if type(sourceString).__name__ == 'str':
			return hashlib.new('md5',str(sourceString).encode(encoding='utf-8')).hexdigest();
		else:
			return None;
	@staticmethod
	def Sort(source):
		sourceTmp_ = source;
		if type(sourceTmp_).__name__ == 'dict':
			keysList_ = [];
			dictTmp_ = {};
			for _key_ in sourceTmp_:
				keysList_.append(_key_);
			keysList_ = PaymentUtils.Sort(keysList_);
			for _ in range(len(keysList_)):
				dictTmp_[keysList_[_]] = sourceTmp_[keysList_[_]];
			return dictTmp_;
			pass
		elif type(sourceTmp_).__name__ == 'list':
			sourceTmp_ = sorted(sourceTmp_);
			return sourceTmp_;
			pass
		else:
			return None;
		pass
	@staticmethod
	def DictToXml(Object_=None):
		if Object_:
			XmlStr_ = '<xml>';
			for p_ in Object_:
				XmlStr_ += ('<' + p_ + '>' + str(Object_[p_]) + '</' + p_ + '>');
			XmlStr_ += '</xml>'
			return XmlStr_;
		return None;
		pass
	@staticmethod
	def DictToQueryString(dictObject):
		if dictObject:
			hashStr_ = '';
			for _key_ in dictObject:
				hashStr_ += (_key_ + '=' + str(dictObject[_key_]) if dictObject[_key_] else '' + '&');
			hashStr_ = hashStr_[:-1];
			return hashStr_;
			pass
		return None;
	@staticmethod
	def XmlToObject(xmlString):
		sourceString_ = ''
		if xmlString.find('xml') >= 0:
			sourceString_ = xmlString[5:-6]
		else:
			sourceString_ = xmlString
		sourceString_ = sourceString_.replace('<![CDATA[','').replace(']]>','')
		p_ = re.compile(r'<(.*?)>(.*?)<\/.*?>')
		rs_ = re.findall(p_,sourceString_)
		tmp_ = {}
		for _ in rs_:
			tmp_[_[0]] = _[1]
		return tmp_
	@staticmethod
	def RandomString(head=None,footer=None,count=32):
		realCount = count;
		realHead = head;
		realFooter = footer;
		if realHead:
			realCount -= len(realHead);
		else:
			realHead = '';
		if realFooter:
			realCount -= len(realFooter);
		else:
			realFooter = '';
		if realCount < 0:
			return None;
		sourceString = PaymentUtils.MD5(str(uuid.uuid4()));
		return ((str(realHead) if realHead else '') + sourceString[:realCount] + (str(realFooter) if realFooter else ''));
		pass
	@staticmethod
	def CreateOrder(soucerType='WECHAT',datas=None):
		if not datas or (not 'name' in datas):
			return None;
		if soucerType.upper() == 'WECHAT':
			configObject = PaymentUtils.Config(datas['name']);
			requestParams = {};
			if not configObject:
				return None;
			CREATE_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder';
			requestParams = {
				'appid':configObject['WX_ID'],
				'attach':datas['title'] if 'title' in datas else '在线支付',
				'body':datas['context'] if 'context' in datas else '网上在线支付',
				'mch_id':configObject['WX_MCH_ID'],
				'nonce_str':PaymentUtils.RandomString(),
				'trade_type':'JSAPI' if (datas['name'].upper().find('WAP') <= 0) else 'APP',
				'notify_url':datas['notifyUrl'] if 'notifyUrl' in datas else None,
				'out_trade_no':datas['tradeId'] if 'tradeId' in datas else PaymentUtils.RandomString('WESPAY'),
				'spbill_create_ip':datas['ip'] if 'ip' in datas else '127.0.0.1',
				'total_fee':datas['money'] if 'money' in datas else 3,
				'sign_type':'MD5',
				'openid':datas['openId'] if 'openId' in datas else None
			};
			requestParams = PaymentUtils.Sort(requestParams);
			requestQueryString = PaymentUtils.DictToQueryString(requestParams);
			requestQueryString += ('&key=' + configObject['WX_KEY']);
			requestHash = PaymentUtils.MD5(requestQueryString);
			requestParams['sign'] = requestHash;
			resp_ = requests.post(CREATE_URL,PaymentUtils.DictToXml(requestParams).encode(encoding='utf-8'));
			return PaymentUtils.XmlToObject(resp_.text);
			pass
		elif soucerType.upper() == 'ALIPAY':
			pass
		pass