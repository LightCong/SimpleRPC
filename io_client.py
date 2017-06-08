# encoding=utf8
class IOClient(object):
	'''
	网络通讯
	运行在io线程
	'''

	def __init__(self, timeout, logger, rpc_codec, context):
		from SimpleReactor import tcp_client
		import threading
		self._logger = logger
		self._rpc_codec = rpc_codec
		self._context = context
		self.tcp_client = tcp_client.TcpClient(timeout, self._logger)
		self.tcp_client.set_app_data_callback(self.on_app_data)
		self.io_thread = threading.Thread(target=self.io_thread_func)
		self.io_thread.setDaemon(True)

	def on_app_data(self, tcp_connection, data):
		# decode
		if_success, response = self._rpc_codec.decode_response(data)
		if not if_success:
			# 解码失败
			return
		# 更新上下文
		self._context.set_response(response._xid, response)

	def io_thread_func(self):
		self.tcp_client.run()
		pass

	def start(self):
		self.io_thread.start()

	def connnect(self, dst_addr):
		self.tcp_client.connect(dst_addr)

	def check_connected(self):
		if len(self.tcp_client.tcpconnection_map)==0:
			return False

		conn_key=self.tcp_client.tcpconnection_map.keys()[0]
		return self.tcp_client.check_connected(conn_key)

	def send_data(self, data):
		if len(self.tcp_client.tcpconnection_map) == 0:
			return

		conn_key = self.tcp_client.tcpconnection_map.keys()[0]
		self.tcp_client.send_data(conn_key,data)
