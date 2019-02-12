#coding:utf8
from flask import *
from flask_cors import *
from Controller import *
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5012
App = Flask(__name__)
CORS(App, supports_credentials=True)
if __name__ == '__main__':
	controller = Controller();
	App.add_url_rule(rule="/",view_func=controller.IndexShow,methods=['GET']);
	App.run(port=SERVER_PORT,host=SERVER_HOST,threaded=True);
	pass