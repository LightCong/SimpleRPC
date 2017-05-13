# encoding=utf8
class RPCClient(object):
	'''
	RPC 客户端
	'''

	def __init__(self,user_id):
		import SimpleReactor.logger, context, rpc_codec, rpc_invoker, io_client
		self.logger = SimpleReactor.logger.Logger()  # 日志
		self.user_id = user_id
		self.context = context.Context(self.user_id)  # 上下文,注册请求,存储响应
		self.rpc_codec = rpc_codec.RPCCodec(self.logger)  # 编解码
		self.io_client = io_client.IOClient(0.01, self.logger, self.rpc_codec, self.context)  # 客户端io

		self.io_client.start()  # 启动

		self.rpc_invoker = rpc_invoker.RPCInvoker(self.context, self.logger, self.rpc_codec,
												  self.io_client)  # rpc invoker

	def __getattr__(self, service_name):
		'''
		获取服务句柄
		'''
		import remote_handler
		service = remote_handler.RemoteService(service_name, self.rpc_invoker)
		return service

	def connect(self, dst_addr):
		self.io_client.connnect(dst_addr)


if __name__ == '__main__':
	pass
