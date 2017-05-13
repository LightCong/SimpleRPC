# encoding=utf8
class RPCServiceCenter(object):
	'''
	rpc服务的注册于路由
	'''

	def __init__(self, logger, worker_map):
		self.service_map = {
			# service_name:worker_id_lst
			# 同一个service 可以有多个worker对应
		}
		self._logger = logger
		self._worker_map = worker_map

	def router(self, service_name):
		'''
		返回对应的服务进程worker对象
		'''
		import random
		if not service_name in self.service_map:
			# 找不到服务
			log_message = 'can not find service : %s' % service_name
			self._logger.write_log(log_message, 'error')
			return None

		# todo 在同一个服务有多个worker时,分配到哪个worker中的策略

		# 暂时采用随机策略
		worker_id_lst = self.service_map[service_name]
		index = random.randint(0, len(worker_id_lst) - 1)

		return self._worker_map[worker_id_lst[index]]

	def register_service(self, service_ins, worker_id):
		'''
		注册服务到指定的worker
		'''
		if not worker_id in self._worker_map:
			# 指定的worker 进程不存在
			log_message = 'worker id %d not exist' % worker_id
			self._logger.write_log(log_message, 'error')
			return False

		service_name = type(service_ins).__name__

		# 在service_center 里注册worker_id
		if not service_name in self.service_map:
			self.service_map[service_name] = []

		self.service_map[service_name].append(worker_id)

		# 将服务注册到worker里
		self._worker_map[worker_id].register_service(service_name, service_ins)

		return True


if __name__ == '__main__':
	pass
