# -*- coding: utf-8 -*-

# Scrapy settings for zx_network project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

BOT_NAME = 'zx_network'

SPIDER_MODULES = ['zx_network.spiders']
NEWSPIDER_MODULE = 'zx_network.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 10

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.8
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'zx_network.middlewares.ZxNetworkSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'zx_network.middlewares.RandomCompanyProxyMiddleware': 20,
    # 'zx_network.middlewares.RandomCompanyProxyMiddleware': 40,
    'zx_network.middlewares.ProcessException': 100,
    'zx_network.middlewares.FailResponseContentMiddleware': 40,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zx_network.pipelines.ZxNetworkPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# # --------------scrapy-reids 设置-----------------#
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 设置scrapy-redis调度器
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 设置scrapy-reids过滤器
# # 链接服务器本地redis
# # REDIS_URL = 'redis://root:axy@2019@127.0.0.1:6379/6'  # 制定redis链接设置
# # 链接本地redis
# REDIS_URL = 'redis://root:@127.0.0.1:6379/0'  # 制定redis链接设置
# # scrapy-redis 设置
# # DEPTH_PRIORITY = 1  # 广度优先
# DEPTH_PRIORITY = -1  # 深度优先
# # 指定排序爬取地址时使用的队列，
# # 默认的 按优先级排序(Scrapy默认)，由sorted set实现的一种非FIFO、LIFO方式。
# # SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# # 广度优先
# # SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# # 深度优先
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
# # 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复，也就是不清理redis queues
# SCHEDULER_PERSIST = True
# # SCHEDULER_FLUSH_ON_START = True  # 重刷redis过滤，重新爬取
# # 默认情况下,RFPDupeFilter只记录第一个重复请求。将DUPEFILTER_DEBUG设置为True会记录所有重复的请求。
# # DUPEFILTER_DEBUG = True


# 日志等级
# LOG_LEVEL = 'WARNING'
LOG_LEVEL = 'ERROR'

RETRY_ENABLED = True
RETRY_TIMES = 20
DOWNLOAD_TIMEOUT = 10
