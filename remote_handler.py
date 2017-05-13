# encoding=utf8
class RemoteService(object):
	'''
	服务句柄
	'''

	def __init__(self, service_name, invoker):
		self._service_name = service_name  # 服务名
		self._invoker = invoker  # 调用代理

	def __getattr__(self, command_name):
		'''
		获取方法句柄
		'''
		command = RemoteCommand(self._service_name, command_name, self._invoker)
		return command


class RemoteCommand(object):
	'''
	方法句柄
	'''

	def __init__(self, service_name, command_name, invoker):
		self._service_name = service_name  # 服务名
		self._command_name = command_name  # 方法名
		self._invoker = invoker  # 调用代理

	def __call__(self, *args, **kwargs):
		'''
		方法的调用
		'''

		result_handler = self._invoker.call(self._service_name, self._command_name, *args)


		if 'async' in kwargs and kwargs['async'] == True:
			# 异步返回result句柄
			return result_handler

		#同步直接返回调用结果
		if 'timeout'in kwargs:
			timeout=kwargs['timeout']
		else:
			timeout=None # 条件变量wait的默认值
		state,result=result_handler.get_result_sync(timeout)
		return state,result


if __name__ == '__main__':
	pass
