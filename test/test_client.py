# encoding=utf8
import sys

sys.path.append(sys.path[0] + '/..')

import rpc_client, time

rpc_client_ins = rpc_client.RPCClient('test')
rpc_client_ins.connect(('127.0.0.1', 8080))  # 连接
time.sleep(0.1)

# 同步请求
state, result = rpc_client_ins.TestService.add_arg1(1,timeout=3)
assert (state, result) == (0, 2)
print state, result

# 异步请求
result_handler = rpc_client_ins.TestService.mul_arg2(2, async=True)
time.sleep(0.5)
result_handler.get_result()
state = result_handler.state
result = result_handler.result
assert (state, result) == (0, 4)
print state, result

# 调用失败
state, result = rpc_client_ins.TestService.wrong_args(1,timeout=3)
assert (state, result) == (1, None)
print state, result

state, result = rpc_client_ins.TestService.exc_func(1,timeout=3)
assert (state, result) == (1, None)
print state, result

# 找不到服务
state, result = rpc_client_ins.FakeService.add_arg1(1,timeout=3)
assert (state, result) == (4, None)
print state, result

# 找不到方法
state, result = rpc_client_ins.TestService.add_arg2(1,timeout=3)
assert (state, result) == (5, None)
print state, result

# 验证失败
rpc_client_ins.context._user_id = "verify_test"  # hack for test
state, result = rpc_client_ins.TestService.add_arg1(1,timeout=3)  # 同步
assert (state, result) == (6, None)
print state, result
