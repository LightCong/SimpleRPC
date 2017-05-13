# encoding=utf8
class ResultHandler(object):
	'''
	用于处理rpc 请求
	'''

	def __init__(self, user_context, xid):
		self._user_context = user_context
		self._xid = xid
		self.state = None
		self.result = None

	def get_result_sync(self,timeout):
		'''
		阻塞获取响应结果
		'''
		import error
		if self.state:
			#由于请求编码失败等情况,请求没有实发出
			return self.state,self.result

		rpc_response = self._user_context.get_response(self._xid, async=False,timeout=timeout)  # 阻塞

		if not rpc_response:
			#超时
			self.state=error.RPCTIMEOUT
		if rpc_response:
			self.deal_rpc_resposne(rpc_response)
		return self.state,self.result

	def get_result(self):
		'''
		异步获取响应结果
		'''
		if self.state:
			#由于请求编码失败等情况,请求没有实发出
			return self.state,self.result

		rpc_response = self._user_context.get_response(self._xid, async=True)
		if rpc_response:
			self.deal_rpc_resposne(rpc_response)

		return self.state,self.result

	def deal_rpc_resposne(self, rpc_response):
		'''
		从响应中提取响应状态,和结果
		'''
		self.state = rpc_response._state
		self.result = rpc_response._result

		pass
