
最近在工作中一直使用 `redis` 来管理分发爬虫任务，让我对 `scrapy-redis` 有很深刻的理解，下面让我慢慢说来。

> 在所有的问题开始之前，要先有一个前提：你使用 `Scrapy` 框架做开发

# 为什么使用 `scrapy-redis`

首先，在实际开发中，我们总会对爬虫速度表示不满，为啥这么慢，能不能跑快点。除了爬虫本身的优化，我们就要引入`分布式爬虫`的概念。

我自己对`分布式爬虫`的理解就是：**多个爬虫执行同一个任务**

>这里说下，`Scrapy`本身是不支持分布式的，因为它的任务管理和去重全部是在机器内存中实现的。

在 `Scrapy` 中最出名的分布式插件就是`scrapy-redis`了，`scrapy-redis`的作用就是让你的爬虫快、很快、更快。

# `scrapy-redis` 如何工作

最简单的方式是使用`redis`替换机器内存，那么具体如何操作呢？非常简单，你只需要在 `settings.py` 中加上两行代码，就能让你的爬虫变为分布式。

```python
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
```
`SCHEDULER` 是任务分发与调度，把所有的爬虫开始的请求都放在redis里面，所有爬虫都去redis里面读取请求。
`DUPEFILTER_CLASS` 是去重队列，负责所有请求的去重。

如果你现在运行你的爬虫，你可以在redis中看到出现了这两个key:

```
spider_name:dupefilter
spider_name:requests
```
格式是set，即不会有重复数据。前者就是redis的去重队列，对应`DUPEFILTER_CLASS`，后者是redis的请求调度，把里面的请求分发给爬虫，对应`SCHEDULER`
RFPDupeFilter
