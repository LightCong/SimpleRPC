# encoding=utf8
class Context(object):
	'''
	rpc 调用的上下文
	用于记录rpc调用结果
	'''

	def __init__(self, user_id):
		import threading, random
		self._user_id = user_id
		self.xid_start = random.randint(0, 65535)
		self.now_xid = self.xid_start - 1
		self.rpc_res_map = {
			# xid:rpc_response
		}
		self.condition = threading.Condition()

	def register_invoke(self):
		'''
		调用的记录
		主线程调用
		'''
		self.now_xid += 1
		self.rpc_res_map[self.now_xid] = None

	def set_response(self, xid, result):
		'''
		在context 里存储rpc 调用结果
		在io 线程里调用
		'''
		with self.condition:
			self.rpc_res_map[xid] = result
			self.condition.notify()

	def get_response(self, xid, async=True,timeout=None):
		'''
		在主线程里调用
		'''
		import time
		if async:
			# 异步
			if xid in self.rpc_res_map:
				response = self.rpc_res_map[xid]
				del self.rpc_res_map[xid]
				return response
			else:
				return None
		else:
			# 同步
			with self.condition:
				start_time=time.time()
				while not xid in self.rpc_res_map or not self.rpc_res_map[xid]:
					self.condition.wait(timeout)

					if not xid in self.rpc_res_map or not self.rpc_res_map[xid]:
						if time.time()-start_time>timeout:
							#超时
							break#超时不再等待

				if not xid in self.rpc_res_map or not self.rpc_res_map[xid]:
					#超时
					response=None
				else:
					response = self.rpc_res_map[xid]
					del self.rpc_res_map[xid]
			return response
