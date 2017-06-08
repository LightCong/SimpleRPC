# encoding=utf8
import sys

sys.path.append(sys.path[0] + '/..')

import rpc_server, service_base


class TestService(service_base.RPCServiceBase): #通过继承RPCServiceBase,定义一个服务
	def __init__(self, arg1, arg2):
		super(TestService, self).__init__()
		self.arg1 = arg1
		self.arg2 = arg2

	@service_base.command #通过command装饰器,定义服务下属的一个方法
	def add_arg1(self, num):
		return num + self.arg1

	@service_base.command
	def mul_arg2(self, num):
		return num + self.arg2

	@service_base.command
	def wrong_args(self):
		return

	@service_base.command
	def exc_func(self):
		raise


rpc_server_ins = rpc_server.RPCServer(('127.0.0.1', 8080), 0.01, 4) #创建rpc服务端实例
rpc_server_ins.register_user('test') #用户注册
rpc_server_ins.register_service(TestService(1, 2), 0) #服务注册
rpc_server_ins.register_service(TestService(1, 2), 1)
rpc_server_ins.start() #服务开启
