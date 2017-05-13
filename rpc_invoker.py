# encoding=utf8
class RPCInvoker(object):
	'''
	rpc调用核心
	'''

	def __init__(self, context, logger, rpc_codec, io_client):
		self._context = context
		self._logger = logger
		self._rpc_codec = rpc_codec
		self._io_client = io_client
		pass

	def call(self, service_name, command_name, *args):
		'''
		构造rpc 请求并发送
		构造rpc result 句柄,并返回
		'''
		import protocol, result_handler,error

		# 在上下文中注册调用
		self._context.register_invoke()
		# 组装 request
		rpc_request = protocol.RPCRequest(self._context.now_xid,
										  self._context._user_id,
										  service_name,
										  command_name,
										  args)

		# 编码
		if_success,rpc_request_data = self._rpc_codec.encode_request(rpc_request)
		if not if_success:
			# 编码失败
			result_handler = result_handler.ResultHandler(self._context, rpc_request._xid)
			result_handler.state=error.ENCODEERROR
			return result_handler
		# 发送数据
		self._io_client.send_data(rpc_request_data)

		# 构造response_handler
		result_handler = result_handler.ResultHandler(self._context, rpc_request._xid)
		return result_handler
