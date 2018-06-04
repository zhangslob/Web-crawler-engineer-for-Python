---
title: 胡歌的男粉多还是女粉多 -- 谈谈爬取微博粉丝数据
date: 2018-06-04 23:11:31
tags:
     - 爬虫
     - 微博
category: 爬虫
copyright: true
---

	这是崔斯特的第五十二篇原创文章

本文就一个目的，胡歌微博上男粉多还是女粉多  (๑• . •๑)

![](http://wx1.sinaimg.cn/large/48e837eely1fmhxeqwby0j22ds1sg157.jpg)

<!--more-->

在真正获得数据前，我的猜测：**胡歌男粉多**！！！

# 问题来源


我是胡椒粉，男的，我就想知道，微博上胡歌男粉多还是女粉多。哈哈，这真是一个有趣的问题，大家可以先猜测下。

>老大镇楼
![](http://wx1.sinaimg.cn/large/48e837eegy1fe2dmkfsquj21tq1tqu0x.jpg)

下面开始正式分析。

![](https://i.imgur.com/h1TyXZ7.png)

这里可以看到胡歌微博粉丝总数约6千万，我的目标就是经历去找到胡歌**活跃粉丝**的用户画像。

所谓活跃粉丝，指的是除去“不转发、不评论、不点赞”这些“三不”用户，是活跃的、有参与的用户。

但是我们知道微博是有限制的，微博不会把所有数据都展示出来，如图

![](https://i.imgur.com/UxASfy6.png)

那么问题来了，我要怎样才能尽可能多的抓到粉丝数据？

# 两种思路

目前我有两种方法来解决这个问题，：

1. 全量采集。采集微博所有用户数据，包括关注、粉丝等。通过粉丝的粉丝、关注的关注、用户分类、推荐等等各种方法拿到微博全量用户数据。
2. 采样。采集胡歌的所有微博下有评论、点赞、转发的用户，凡是有参与过的亲密值加一，当这个值超过一定限度时，我们就认为该用户是胡歌的粉丝。


想了想，第一种方法短时间内是不现实的，方法2倒是可以尝试一波。

# 爬虫逻辑

爬虫分为三步：
1. 采集胡歌所有微博
2. 采集每条微博的三类数据（转发、评论、点赞）
3. 数据清洗

根据以往的经验，weibo.cn 和 m.weibo.cn 是最简单爬取的，weibo.com 是最难的。这次我们从 m.weibo.cn 入手，分析可以得到胡歌微博的接口，而且是无需登录的！！！很重要。其他入口都需要解决登录难题！

`https://m.weibo.cn/api/container/getIndex?containerid=1076031223178222&page={}`

返回数据：

```cmd
cardlistInfo: {
containerid: "1076031223178222",
v_p: 42,
show_style: 1,
total: 3643,
page: 2
},
```

这里告诉我们总共有3643条数据，每页10条，那么翻页就很清晰了。

其他接口

```cmd
转发： https://m.weibo.cn/api/statuses/repostTimeline?id=4238119278366780&page={}

评论：https://m.weibo.cn/api/comments/show?id=4238119278366780&page={}

点赞：https://m.weibo.cn/api/attitudes/show?id=4238119278366780&page={}

```

（想要爬其他人，替换这里的id即可）


采集用户信息接口

`https://m.weibo.cn/api/container/getIndex?containerid=1005051223178222`


代码在此，需要代理支撑
