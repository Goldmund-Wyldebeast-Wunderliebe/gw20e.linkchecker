from scrapy.spider import BaseSpider

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from linkchecker.items import LinkcheckerPage
from linkchecker.settings import SPIDER_BLACKLIST


class LinkSpider(InitSpider, CrawlSpider):
    name = "link_spider"
    allowed_domains = ["localhost"]
    start_urls = [
        "http://localhost:9080/Plone"
        "/",
    ]
    handle_httpstatus_list = [404, 500]

    # Application auth
    login_page = 'http://localhost:9080/Plone/login'
    login_user = 'admin'
    login_password = 'admin'

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor( allow=('.*', ), deny=SPIDER_BLACKLIST), callback='parse_item'),
    )

    def init_request(self):
        """This function is called before crawling starts."""

        return Request(url=self.login_page, callback=self.login)

    def parse_item(self, response):
        def get_portal_type(value):
            cls = None
            if type(value) == list:
                value = value[0]

            for css_class in value.split():
                if css_class.startswith('portaltype'):
                    cls = css_class.replace('portaltype-', '')
                    break
            return cls


        hxs = HtmlXPathSelector(response)

        item = LinkcheckerPage()

        title = hxs.select("//title/text()").extract()
        item['title'] = title and title[0] or None
        item['url'] = response.url
        item['http_status'] = response.status
        item['portal_type'] = get_portal_type(hxs.select('//body/@class').extract())

        if response.status == 500:
            exceptionlines = hxs.select("//div[@id='content-core']//ul/li/text()").extract()
            item['error_message'] = "\n".join(exceptionlines)
            item['error_url'] = hxs.select("//a[starts-with(@href, 'error_log')]/@href").extract()

        return item

    def init_request(self):
        """This function is called before crawling starts."""

        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        form_data = {'__ac_name': self.login_user, '__ac_password': self.login_password}
        return FormRequest.from_response(
            response,
            formdata=form_data,
            formnumber=1,
            callback=self.check_login_response
        )

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if """<li id="personaltools-logout">""" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            return self.initialized()
        else:
            self.log(u'Could not log in')
            # Something went wrong, we couldn't log in, so nothing happens.

