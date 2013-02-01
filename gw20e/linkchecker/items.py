# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LinkcheckerPage(Item):
    url = Field()
    title = Field()
    status_code = Field()
    http_status = Field()
    portal_type = Field()
    error_message = Field()
    error_url = Field()
