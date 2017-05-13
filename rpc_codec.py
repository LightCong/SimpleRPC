# encoding=utf8
class RPCCodec(object):
	'''
	使用msgpack 对rpc报文进行序列化和反序列化
	'''

	def __init__(self, logger):
		self._logger = logger

	def encode_request(self, rpc_request):
		# 对rpc请求做序列化
		import protocol, msgpack
		if_success = False
		if not isinstance(rpc_request, protocol.RPCRequest):
			# 传入对象类型不对
			log_message = 'can not serlize non-rpc_request obj'
			self._logger.write_log(log_message, 'error')
			return if_success, None
		try:
			rpc_request_data = msgpack.Packer(use_bin_type=True).pack(rpc_request.content)
			if_success = True
			return if_success, rpc_request_data
		except:
			# 序列化失败
			log_message = 'rpc request serialize failed'
			self._logger.write_log(log_message, 'error')
			return if_success, None

	def decode_request(self, rpc_request_data):
		'''
		对rpc 请求数据做反序列化,解码生成对象
		'''
		import protocol, msgpack
		if_success = False

		try:
			unpacker = msgpack.Unpacker(encoding='utf-8')
			unpacker.feed(rpc_request_data)
			xid, msg_type, uid, service_name, command_name, args = unpacker.unpack()
		except:
			# 反序列化失败
			log_message = 'rpc request deserialize failed'
			self._logger.write_log(log_message, 'error')
			return if_success, None

		if msg_type != protocol.RPCRequest.MSG_TYPE:
			# 消息类型不对
			log_message = 'msg type is not rpc request'
			self._logger.write_log(log_message, 'error')
			return if_success, None

		if_success = True
		rpc_request = protocol.RPCRequest(xid, uid, service_name, command_name, args)
		return if_success, rpc_request

	def encode_response(self, rpc_response):
		# 对rpc请求做序列化
		import protocol, msgpack
		if_success = False
		if not isinstance(rpc_response, protocol.RPCResponse):
			# 传入对象类型不对
			log_message = 'can not serlize non-rpc_response obj'
			self._logger.write_log(log_message, 'error')
			return if_success, None

		try:
			rpc_response_data = msgpack.Packer(use_bin_type=True).pack(rpc_response.content)
			if_success = True
			return if_success, rpc_response_data
		except:
			# 序列化失败
			log_message = 'rpc response serlize failed'
			self._logger.write_log(log_message, 'error')
			return if_success, None
		pass

	def decode_response(self, rpc_response_data):
		'''
		对rpc 应答数据做反序列化,解码生成对象
		'''
		import protocol, msgpack
		if_success = False

		try:
			unpacker = msgpack.Unpacker(encoding='utf-8')
			unpacker.feed(rpc_response_data)
			xid, uid, msg_type, state, result = unpacker.unpack()
		except:
			# 反序列化失败
			log_message = 'rpc response deserialize failed'
			self._logger.write_log(log_message, 'error')
			return if_success, None

		if msg_type != protocol.RPCResponse.MSG_TYPE:
			# 消息类型不对
			log_message = 'msg type is not rpc response'
			self._logger.write_log(log_message, 'error')
			return if_success, None

		if_success = True
		rpc_response = protocol.RPCResponse(xid, uid, state, result)
		return if_success, rpc_response


if __name__ == '__main__':
	import SimpleReactor.logger as logger, protocol

	codec = RPCCodec(logger.Logger())

	a = protocol.RPCRequest(1, 1, 'test_service', 'test_func', [1, 2, 3])
	if_success, data = codec.encode_request(a)
	print if_success, data

	if_success, req = codec.decode_request(data)
	print if_success, req.content

	b = protocol.RPCResponse(1, 0, 4, 5)
	if_success, data = codec.encode_response(b)

	print if_success, data

	if_success, res = codec.decode_response(data)
	print if_success, res.content
