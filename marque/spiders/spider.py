import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import MarqueItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class MarqueSpider(scrapy.Spider):
	name = 'marque'
	start_urls = ['https://www.emarquettebank.com/about-us/media-center/']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//section/p/strong/text()').get().split()[2]
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//section/p[position()>1]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=MarqueItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
