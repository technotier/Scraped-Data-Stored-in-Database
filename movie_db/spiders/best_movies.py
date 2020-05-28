# -*- coding: utf-8 -*-
import scrapy


class BestMoviesSpider(scrapy.Spider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']

    def parse(self, response):
        movies = response.xpath("//*[@class='lister-item-header']/a")
        for movie in movies:
            link = movie.xpath(".//@href").get()
            yield response.follow(url=link, callback=self.parse_movie_info)
        # Deal with Pagination
        next_page = response.xpath("//a[@class='lister-page-next next-page']/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    def parse_movie_info(self, response):
        title = response.xpath("//*[@class='title_wrapper']/h1/text()").get()
        duration = response.xpath("normalize-space((//time)[1]/text())").get()
        yield {
            "Movie Name": title,
            "Duration": duration,
            "URL": response.url
        }
