

最近在工作中一直使用 `redis` 来管理分发爬虫任务，让我对 `scrapy-redis` 有很深刻的理解，下面让我慢慢说来。

> 在所有的问题开始之前，要先有一个前提：你使用 `Scrapy` 框架做开发

# 结论

`scrapy-redis` 与 `Scrapy`的关系就像电脑与固态硬盘一样，是电脑中的一个插件，能让电脑更快的运行。

`Scrapy` 是一个爬虫框架，`scrapy-redis` 则是这个框架上可以选择的插件，它可以让爬虫跑的更快。

# 为什么使用 `scrapy-redis`

首先，在实际开发中，我们总会对爬虫速度表示不满，为啥这么慢，能不能跑快点。除了爬虫本身的优化，我们就要引入`分布式爬虫`的概念。

我自己对`分布式爬虫`的理解就是：**多个爬虫执行同一个任务**

>这里说下，`Scrapy`本身是不支持分布式的，因为它的任务管理和去重全部是在机器内存中实现的。

在 `Scrapy` 中最出名的分布式插件就是`scrapy-redis`了，`scrapy-redis`的作用就是让你的爬虫快、更快、超级快。

# `scrapy-redis` 如何工作

最简单的方式是使用`redis`替换机器内存，那么具体如何操作呢？非常简单，你只需要在 `settings.py` 中加上三代码，就能让你的爬虫变为分布式。

```python
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

REDIS_START_URLS_AS_SET = True
```
`SCHEDULER` 是任务分发与调度，把所有的爬虫开始的请求都放在redis里面，所有爬虫都去redis里面读取请求。
`DUPEFILTER_CLASS` 是去重队列，负责所有请求的去重，`REDIS_START_URLS_AS_SET`指的是使用redis里面的set类型（简单完成去重），如果你没有设置，默认会选用list。

如果你现在运行你的爬虫，你可以在redis中看到出现了这两个key:

```
spider_name:dupefilter
spider_name:requests
```
格式是set，即不会有重复数据。前者就是redis的去重队列，对应`DUPEFILTER_CLASS`，后者是redis的请求调度，把里面的请求分发给爬虫，对应`SCHEDULER`。（里面的数据不会自动删除，如果你第二次跑，需要提前清空里面的数据）

# `scrapy-redis` 优点

### 速度快
`scrapy-redis` 使用redis这个速度非常快的非关系型（NoSQL）内存键值数据库，**速度快**是最重要原因（但是也会产生负面想过，下面会说到）。

为什么是`scrapy-redis`而不是`scrapy-mongo`呢，大家可以仔细想想。

### 用法简单

前人已经造好轮子了，[scrapy-redis](https://github.com/rmax/scrapy-redis)。
我们直接拿来用就好，而用法也像上面提到的在 `settings.py` 文件中配置。在文档中还有另一种用法，即`Feeding a Spider from Redis`

1. run the spider:
`scrapy runspider myspider.py`
2. push urls to redis:
`redis-cli lpush myspider:start_urls http://google.com`（建议把`lpush`换为`zset`

其实这种用法就是先打开一个爬虫，他会一直在redis里面寻找key为 `myspider:start_urls`，如果存在，就提取里面的url。当然你也可以在爬虫中指定`redis_key`，默认的是爬虫的名字加上`:start_urls`

### 去重简单

爬虫中去重是一件大事，使用了`scrapy-redis`后就很简单了。上面提到过使用redis的set类型就可以很容易达到这个目标了，即`REDIS_START_URLS_AS_SET = True`

# `scrapy-redis` 缺点

### 内存问题

为什么使用分布式爬虫，当然是因为会有很多链接需要跑，或者说会存放很多个`myspider:start_urls`到redis中，Redis是key-value数据库，面对key的内存搜索，优势明显，但是Redis吃的是纯内存，`myspider:start_urls`是一个有一个像`https://www.zhihu.com/people/cuishite`的链接，会占用大量的内存空间。之前就因为这个原因redis崩溃过无数次，那么如何优化？

网络上有的方法是 [ scrapy_redis去重优化（已有7亿条数据），附Demo福利](https://blog.csdn.net/bone_ace/article/details/53099042)，可以参考下。如果你有好的解决方法，欢迎私信告诉我。（保密原因就不介绍我们的处理方法了）

### Usage

这个其实不算做问题，只是官方文档上我觉得的小BUG，在这里 [Usage](https://github.com/rmax/scrapy-redis#usage)

```python
# Store scraped item in redis for post-processing.
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
```
Pipeline是这样写的
```python
    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}
```

看不懂为什么要把数据储存在redis里面，这不又加大redis储存负担吗？对于新手来说真的不友好，或许可以考虑提一个pr。

# redis可视化工具

最后介绍两个redis可视化工具
1. [RedisDesktopManager](https://github.com/uglide/RedisDesktopManager) 比较出名的工具，但是经常会崩溃
2. [kedis](https://github.com/uniorder/kedis) 国人开发的免费工具，这个界面还是可以的

![](https://camo.githubusercontent.com/de76115b295d30222fa0d6a1b79ffc9b31fb04e5/687474703a2f2f7777772e6b656861772e636f6d2f696d616765732f73637265656e73686f742e706e67)


