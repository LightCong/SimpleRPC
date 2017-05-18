# SimpleRPC

rpc通讯框架

## 简介

SimpleRPC 是一个python编写的单点rpc双端框架，底层通讯基于[SimpleReactor](https://github.com/LightCong/SimpleReactor)框架。
在接口设计和序列化方案上参考了了zeroRPC。


## 特点介绍

- 支持同步异步两种rpc调用方式
- 基于msgpack的序列化操作，不需要额外的协议文件。
- 底层基于SimpleReactor，集成心跳，压缩，加密等服务和组件。
- 后端执行服务的worker，采用进程的形式，避免python GIL 对性能的影响，有效利用多核提高服务执行并发度 



## 双端架构

### 服务端架构
![服务端架构](https://github.com/LightCong/SimpleRPC/blob/master/pic/server.png)

### 客户端架构

![客户端架构](https://github.com/LightCong/SimpleRPC/blob/master/pic/client.png)

- 双端的io线程通过消息队列与主线程进行通讯。
- worker进程与主线程之间通过进程级队列传递请求与应答。
  
## 依赖

  msgpack

## 示例

### 服务端


```
import rpc_server, service_base


class TestService(service_base.RPCServiceBase): #通过继承RPCServiceBase,定义一个服务
	def __init__(self, arg1, arg2):
		super(TestService, self).__init__()
		self.arg1 = arg1
		self.arg2 = arg2

	@service_base.command #通过command装饰器,定义服务下属的一个方法
	def add_arg1(self, num):
		return num + self.arg1

	@service_base.command
	def mul_arg2(self, num):
		return num * self.arg2

	@service_base.command
	def wrong_args(self):
		return

	@service_base.command
	def exc_func(self):
		raise


rpc_server_ins = rpc_server.RPCServer(('127.0.0.1', 8080), 0.01, 4) #创建rpc服务端实例
rpc_server_ins.register_user('test') #用户注册
rpc_server_ins.register_service(TestService(1, 2), 0) #服务注册
rpc_server_ins.register_service(TestService(1, 2), 1)
rpc_server_ins.start() #服务开启
```



### 客户端


```
import rpc_client, time

rpc_client_ins = rpc_client.RPCClient('test') #创建一个用户名为test的rpc客户端实例
rpc_client_ins.connect(('127.0.0.1', 8080))  # 连接
time.sleep(0.1)

# 同步请求
state, result = rpc_client_ins.TestService.add_arg1(1,timeout=3)
print state, result

# 异步请求
result_handler = rpc_client_ins.TestService.mul_arg2(2, async=True)
time.sleep(0.5)
result_handler.get_result()
state = result_handler.state
result = result_handler.result
print state, result

```


## todo list

  writing
