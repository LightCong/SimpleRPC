# encoding=utf8
class RPCServer(object):
	'''
	负责rpc_data 的编解码,验证,
	rpc 请求,应答对象的转发
	运行在主线程
	'''

	def __init__(self, host_addr, timeout, worker_num):
		import rpc_codec, SimpleReactor.logger, io_server, worker, rpc_service_center, rpc_user_center
		self.logger = SimpleReactor.logger.Logger()  # 日志记录
		self.io_server = io_server.IOServer(host_addr, timeout, self.logger)  # 运行在io线程中
		self.rpc_codec = rpc_codec.RPCCodec(self.logger)  # rpc 协议编解码
		self.worker_pool = worker.WorkerPool.create_worker_pool(worker_num)  # 含有worker_num 个进程的进程池

		self.service_register_center = rpc_service_center.RPCServiceCenter(self.logger, self.worker_pool.worker_map)  # 服务中心
		self.user_register_center = rpc_user_center.RPCUserCenter(self.logger)  # 用户中心

	def register_service(self, service_ins, worker_id):
		'''
		服务注册
		'''
		self.service_register_center.register_service(service_ins, worker_id)

	def register_user(self, user_id):
		'''
		用户注册
		'''
		self.user_register_center.register_user_id(user_id)

	def schedule(self):
		'''
		主线程调度逻辑
		'''
		while True:
			# 从io线程队列里取出一定数量的请求
			request_lst = self.get_request()
			for request_pair in request_lst:
				# handle这些请求
				tcp_connection = request_pair[0]
				request_data = request_pair[1]
				self.handle_request(tcp_connection, request_data)

			# 从后端队列里取出响应,并处理

			for worker_id in self.worker_pool.worker_map:
				response_lst = self.get_response(worker_id)
				for response in response_lst:
					self.handle_response(response)

	def get_request(self, max_num=100):
		'''
		读io线程队列
		'''
		num = 0
		request_pair_lst = []
		while num < max_num:
			recv_pair = self.io_server.get_recv_from_queue()
			if not recv_pair:
				# io server 的recv队列为空
				break
			request_pair_lst.append(recv_pair)
			num += 1

		return request_pair_lst

	def get_response(self, worker_id, max_num=100):
		'''
		读worker进程响应队列
		'''
		# 从worker 队列里读数据
		num = 0
		response_lst = []
		while num < max_num:
			response = self.worker_pool.worker_map[worker_id].get_rpc_response()
			if not response:
				# worker 的response队列为空
				break
			response_lst.append(response)

		return response_lst

	def handle_request(self, tcp_connection, request_data):
		'''
		处理rpc请求报文
		'''
		import protocol, error
		# 解码
		if_success, request = self.rpc_codec.decode_request(request_data)
		if not if_success:
			# 解码失败,直接构造response,发送回去
			response = protocol.RPCResponse(request._xid, request._uid, error.DECODEERROR, None)
			if_success,response_data = self.rpc_codec.encode_response(response)
			tcp_connection.send_data(response_data)
			pass
			return

		# 验证
		if not self.user_register_center.verify(request._uid):
			# 消息验证失败,直接构造response,发送回去
			response = protocol.RPCResponse(request._xid, request._uid, error.VERIFYERROR, None)
			if_success,response_data = self.rpc_codec.encode_response(response)
			tcp_connection.send_data(response_data)
			return

		# 路由
		worker = self.service_register_center.router(request._service_name)
		if not worker:
			# 路由失败,直接构造response,发送回去
			response = protocol.RPCResponse(request._xid, request._uid, error.SERVICELOSE, None)
			if_success,response_data = self.rpc_codec.encode_response(response)
			tcp_connection.send_data(response_data)
			pass
			return

		# 注册 connkey
		self.user_register_center.update_user_connection(request._uid, tcp_connection._conn_key)

		# 塞入后端进程队列
		worker.push_rpc_request(request)
		pass

	def handle_response(self, response):
		'''
		处理rpc 应答对象
		'''
		# 编码
		if_success,response_data = self.rpc_codec.encode_response(response)
		if not if_success:
			return
		# 查询connkey
		connkey = self.user_register_center.get_connection_key(response._uid)
		# 发送
		self.io_server.send_data(connkey, response_data)

	def start(self):
		# 后端进程池启动
		self.worker_pool.start()
		# io_server 线程启动
		self.io_server.start()
		self.schedule()  # 主线程处理循环启动
