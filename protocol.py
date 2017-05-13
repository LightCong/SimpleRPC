# encoding=utf8
class RPCHeader(object):
	'''
	rpc header 基类
	'''

	def __init__(self, xid, msg_type):
		self._xid = xid
		self._msg_type = msg_type


class RPCRequest(RPCHeader):
	'''
	rpc 请求
	'''
	MSG_TYPE = 0

	def __init__(self, xid, uid, service_name, command_name, args):
		super(RPCRequest, self).__init__(xid, RPCRequest.MSG_TYPE)
		self._uid = uid  # 用作用户验证
		self._service_name = service_name  # 类名,用于路由,和invoke
		self._command_name = command_name  # 方法名,用于invoke
		self._args = args

	@property
	def content(self):
		# 返回需要序列化的元组,for msgpack
		return (self._xid, self._msg_type, self._uid,
				self._service_name, self._command_name, self._args)


class RPCResponse(RPCHeader):
	'''
	rpc 应答
	'''
	MSG_TYPE = 1

	def __init__(self, xid, uid, state, result):
		super(RPCResponse, self).__init__(xid, RPCResponse.MSG_TYPE)
		self._uid = uid  # 用作用户验证
		self._state = state  # 响应状态
		self._result = result

	@property
	def content(self):
		# 返回需要序列化的元组,for msgpack
		return (self._xid, self._uid, self._msg_type, self._state, self._result)
