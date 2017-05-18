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
  
## 依赖

  msgpack

## 示例

## todo list

  writing
