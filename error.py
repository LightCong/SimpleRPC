# encoding=utf8

SUCCESS = 0  # 成功
CALLERROR = 1  # 调用失败
DECODEERROR = 2  # 解码失败
ENCODEERROR = 3  # 编码失败
SERVICELOSE = 4  # 找不到服务
COMMANDLOSE = 5  # 找不到方法
VERIFYERROR = 6  # 验证失败
RPCTIMEOUT = 7  # 超时

errorcode = {
	SUCCESS: "success",
	CALLERROR: "call error",
	DECODEERROR: "decode error",
	ENCODEERROR: "encode error",
	SERVICELOSE: 'can not find service',
	COMMANDLOSE: 'can not find command',
	VERIFYERROR: 'invalid user',
	RPCTIMEOUT: 'timeout',
}
