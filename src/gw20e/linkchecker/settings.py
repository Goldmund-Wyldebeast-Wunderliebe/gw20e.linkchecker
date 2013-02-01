# Scrapy settings for linkchecker project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'gw20e.linkchecker'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['linkchecker.spiders']
NEWSPIDER_MODULE = 'linkchecker.spiders'

USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DOWNLOADER_MIDDLEWARE = [ 'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware' ]

SPIDER_BLACKLIST = (
    'logout',
    'portal_factory',
)
