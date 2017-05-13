# encoding=utf8
class IOServer(object):
	'''
	网络通讯
	运行在io线程
	'''

	def __init__(self, host_addr, timeout, logger):
		from SimpleReactor import tcp_server
		import threading, Queue
		self.logger = logger
		self.tcp_server = tcp_server.TcpServer(host_addr, timeout, self.logger)
		self.tcp_server.set_app_data_callback(self.on_app_data)
		self.io_thread = threading.Thread(target=self.io_thread_func)
		self.io_thread.setDaemon(True)
		self.recv_queue = Queue.Queue()

	def io_thread_func(self):
		'''
		开启服务器
		'''
		self.tcp_server.run()

	def on_app_data(self, tcp_connection, data):
		'''
		定义连接接收到消息时的操作
		'''
		recv_pair = (tcp_connection, data)
		self.recv_queue.put(recv_pair)
		pass

	def get_recv_from_queue(self):
		'''
		非io线程从接受队列里取recv_pair
		'''
		import Queue
		try:
			recv_pair = self.recv_queue.get_nowait()
		except Queue.Empty:
			return None
		return recv_pair

	def send_data(self, tcp_connection_key, data):
		'''
		向指定连接,发送数据,线程不安全,但是影响不大
		'''
		if not tcp_connection_key in self.tcp_server.tcpconnection_map:
			log_message = 'tcp connection {} not exist'.format(tcp_connection_key)
			self.logger.write_log(log_message, 'info')
			return False
		try:
			# 发送瞬间可能正好连接被io线程删除
			self.tcp_server.tcpconnection_map[tcp_connection_key].send_data(data)
			return True
		except:
			return False

	def start(self):
		self.io_thread.start()

