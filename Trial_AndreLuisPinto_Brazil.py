# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 18:52:37 2023

@author: andre
"""
import scrapy
import functools
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem, NotConfigured
from scrapy.pipelines.files import FileException, FilesPipeline
from scrapy.settings import Settings
from PIL import Image

class QuoteSpider(scrapy.Spider):
    name = 'quote-spider'
    start_urls = [
        'http://pstrial-2019-12-16.toscrape.com/browse/insunsh',
        'http://pstrial-2019-12-16.toscrape.com/browse/summertime',
    ]
    
class ImageScraperItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    

class ExamplePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[-1]
    
class NoimagesDrop(DropItem):
    """Product with no images exception"""


class ImageException(FileException):
    """General image error exception"""


class ImagesPipeline(FilesPipeline):
    """Abstract pipeline that implement the image thumbnail generation logic

    """

    MEDIA_NAME = 'image'

    # Uppercase attributes kept for backward compatibility with code that subclasses
    # ImagesPipeline. They may be overridden by settings.
    MIN_WIDTH = 0
    MIN_HEIGHT = 0
    EXPIRES = 90
    THUMBS = {}
    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'images'

    def __init__(self, store_uri, download_func=None, settings=None):
        try:
            
            self._Image = Image
        except ImportError:
            raise NotConfigured(
                'ImagesPipeline requires installing Pillow 4.0.0 or later'
            )

        super().__init__(store_uri, settings=settings, download_func=download_func)

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)

        resolve = functools.partial(self._key_for_pipe,
                                    base_class_name="ImagesPipeline",
                                    settings=settings)
        self.expires = settings.getint(
            resolve("IMAGES_EXPIRES"), self.EXPIRES
        )

        if not hasattr(self, "IMAGES_RESULT_FIELD"):
            self.IMAGES_RESULT_FIELD = self.DEFAULT_IMAGES_RESULT_FIELD
        if not hasattr(self, "IMAGES_URLS_FIELD"):
            self.IMAGES_URLS_FIELD = self.DEFAULT_IMAGES_URLS_FIELD

        self.images_urls_field = settings.get(
            resolve('IMAGES_URLS_FIELD'),
            self.IMAGES_URLS_FIELD
        )
        self.images_result_field = settings.get(
            resolve('IMAGES_RESULT_FIELD'),
            self.IMAGES_RESULT_FIELD
        )
        self.min_width = settings.getint(
            resolve('IMAGES_MIN_WIDTH'), self.MIN_WIDTH
        )
        self.min_height = settings.getint(
            resolve('IMAGES_MIN_HEIGHT'), self.MIN_HEIGHT
        )
        self.thumbs = settings.get(
            resolve('IMAGES_THUMBS'), self.THUMBS
        )
        
        
    def get_size(path='.'):
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            return Image(path)

    
def parse_item(self, response):
    image = scrapy.Field()
    image = image.xpath('//img') 
    for img in image: 
        item = ImageScraperItem()        

        item['url'] = response.url
        title = img.xpath('./@alt').extract() or ''
        item_title = title[0] if title else ''
        item['title'] = item_title

        iurl = img.xpath('./@src').extract() or ''            
        item_iurl = iurl[0] if iurl else ''
        item['iurl'] = item_iurl
        yield item

def parse(self, response):
        url = '.quote'
        Artist = '.text::text'.getall()
        Title = '.title::text'
        Image = response.css('img').getall(), {'scrapy.pipelines.images.ImagesPipeline': 1}
        Height = float.Image.size.getall()
        Width = float.Image.size.getall()
        self.store.persist_file(
                meta={'width': Width, 'height': Height},
                headers={'Content-Type': 'image/jpeg'}),
        Description = '.title + a::attr("href")'
        Categories = '.text::text'.getall()
        NEXT_SELECTOR = '.next a::attr("href")'

        for quote in response.css(url):
            yield {
                'text': quote.css(Artist).extract_first(),
                'title': quote.css(Title).extract_first(),
                'image': ['http://pstrial-2019-12-16.toscrape.com/browse/insunsh',
                          'http://pstrial-2019-12-16.toscrape.com/browse/summertime'] + 
                        quote.css(Image).extract_first(),
                'height': quote.css(Height).extract(),
                'width': quote.css(Width).extract(),
                'description': quote.css(Description).extract_first(),
                'categories': quote.css(Categories).extract_first(),
            }

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
            )