# encoding=utf8

def command(f):
	'''
	command 函数包装器
	'''
	f.__dict__['rpc_service_command'] = True
	return f


class RPCServiceBase(object):
	'''
	rpc服务基类
	'''

	def __init__(self):
		self.command_map = {
			# command_name:bound_method
		}
		self.register_command()

	def register_command(self):
		'''
		方法注册
		'''
		for member_name in type(self).__dict__:
			# 遍历service 类型的每个成员,
			member = type(self).__dict__[member_name]
			if type(member) == type(command) and member.__dict__.has_key('rpc_service_command'):
				# 如果这个成员被标记为rpc_service_command,则添加到command_map里
				self.command_map[member_name] = getattr(self, member_name)

	def handle(self, command_name, *args):
		'''
		方法执行
		'''
		import error
		if not command_name in self.command_map:
			# command 找不到
			return error.COMMANDLOSE, None

		try:
			result = self.command_map[command_name](*args)
		except:
			# 调用失败
			return error.CALLERROR, None

		return error.SUCCESS, result


if __name__ == '__main__':
	class test_service(RPCServiceBase):
		def __init__(self, arg1, arg2):
			super(test_service, self).__init__()
			self._arg1 = arg1
			self._arg2 = arg2

		@command  # 需要注册为服务的方法,标记为command
		def add_arg1(self, num):
			return num + self._arg1

		@command
		def add_arg2(self, num):
			return num + self._arg2


	a = test_service(1, 2)
	print a.add_arg1(1)
	print a.add_arg2(1)

	print a.command_map['add_arg1'](1)
	print a.command_map['add_arg2'](1)
	print a.handle('add_arg1', 1)

	print type(a).__name__
