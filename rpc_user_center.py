# encoding=utf8
class RPCUserCenter(object):
	'''
	rpc服务的用户验证与连接记录
	'''

	def __init__(self, logger):
		self._logger = logger
		self.user_id_set = set()
		self.user_connection_map = {
			# user_id:tcp_connection_id
		}

	def register_user_id(self, user_id):
		self.user_id_set.add(user_id)

	def verify(self, user_id):
		'''
		验证是否为合法用户
		'''
		if not user_id in self.user_id_set:
			# 用户此前没有注册
			log_message = 'invalid user_id {}'.format(str(user_id))
			self._logger.write_log(log_message, 'error')
			return False
		return True

	def update_user_connection(self, user_id, tcp_connection_key):
		'''
		记录用户的tcp_connection_key,
		用于服务端rpc运算结果的发送
		'''
		self.user_connection_map[user_id] = tcp_connection_key

	def get_connection_key(self, user_id):
		'''
		获取用户的tcp_connection_key
		'''
		if not user_id in self.user_connection_map:
			# 找不到用户的connection id
			log_message = 'can not find connection key of user_id {}'.format(str(user_id))
			self._logger.write_log(log_message, 'error')
			return None

		return self.user_connection_map[user_id]
