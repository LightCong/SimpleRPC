# encoding=utf8

class RPCWorker(object):
	'''
	服务计算进程
	'''
	worker_seq = 0  # 静态变量

	def __init__(self):
		import multiprocessing
		self.worker_id = RPCWorker.worker_seq  # worker 标识
		RPCWorker.worker_seq += 1

		self.rpc_request_queue = multiprocessing.Queue()  # 进程级通讯队列
		self.rpc_response_queue = multiprocessing.Queue()  # 进程级通讯队列

		self.service_map = {
			# service_name:service
			# 同一个service 只能在一个进程里出现一次
		}

		self.subprocess = multiprocessing.Process(target=self.subprocess_work)
		self.subprocess.daemon = True

	def subprocess_work(self):
		'''
		工作线程逻辑
		'''
		import protocol, service_base, error
		while True:
			# 获取请求对象
			rpc_request = self.rpc_request_queue.get()
			assert (isinstance(rpc_request, protocol.RPCRequest))

			service_name = rpc_request._service_name
			command_name = rpc_request._command_name
			args = rpc_request._args

			# 获取服务实例
			service_ins = self.service_map[service_name]
			assert (isinstance(service_ins, service_base.RPCServiceBase))

			# 调用rpc 方法
			state, result = service_ins.handle(command_name, *args)

			# 返回状态
			rpc_response = protocol.RPCResponse(rpc_request._xid, rpc_request._uid, state, result)
			self.rpc_response_queue.put(rpc_response)

	def register_service(self, service_name, service_ins):
		'''
		在worker中,注册服务
		'''
		# 将service 填充到service_map中
		self.service_map[service_name] = service_ins
		pass

	def push_rpc_request(self, rpc_request):
		'''
		向子进程传递请求对象
		'''
		self.rpc_request_queue.put(rpc_request)

	def get_rpc_response(self):
		'''
		从子线程传取出应答对象,取出失败,则返回None
		'''
		import multiprocessing, Queue
		try:
			response = self.rpc_response_queue.get_nowait()
		except Queue.Empty:
			return None

		return response

	def start(self):
		self.subprocess.start()


class WorkerPool(object):
	'''
	工作进程池
	'''

	def __init__(self):
		self.worker_map = {
			# worker_id:worker
		}
		pass

	@staticmethod
	def create_worker_pool(worker_num):
		'''
		创造worker_num 个worker 进程放入到进程池中
		'''
		worker_pool = WorkerPool()
		i = 0
		while i < worker_num:
			worker = RPCWorker()
			worker_pool.worker_map[worker.worker_id] = worker
			i += 1
		return worker_pool

	def start(self):
		for worker_id in self.worker_map:
			self.worker_map[worker_id].start()


