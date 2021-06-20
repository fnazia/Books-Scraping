import scrapy
from scrapy import Request
from scrapy import Selector

class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
   # start_urls = ['http://goodreads.com/']
   # start_urls = ['https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_']

    def start_requests(self):
        start_urls = ['https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_']
        yield Request(start_urls[0], callback = self.author_requests)

    def author_requests(self, response):
        #startlink = Selector(text="https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_")
        #startlink = self.get_startlink("https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_")
        authorlinks = response.xpath('//*[@class="authorName"]/@href').getall()
        unique_authorlinks = list(set(authorlinks))
        for author in unique_authorlinks:
            yield Request(author, callback=self.join_url)

    def join_url(self, response):
        #base_url = ['http://goodreads.com/']
        morebooks = response.xpath('//*[@class="actionLink"]/@href').get()
        yield response.follow(morebooks, callback = self.parse)

    def parse(self, response):
        #morebooks = response.xpath('//*[@class="actionLink"]/@href').get()
	#fetch(response.urljoin(morebooks))
        #response = response.urljoin(morebooks) 
        booksdict = {}
        booklist = response.xpath('//*[@class="tableList"]/tr')

        for book in booklist:
            booksdict['name'] = book.xpath('td//*[@class="bookTitle"]/span/text()').get()
            booksdict['author'] = book.xpath('td//*[@class="authorName"]/span/text()').get()
            booksdict['booklink'] = book.xpath('td//*[@class="bookTitle"]/@href').get()
            rating = book.xpath('td//*[@class = "minirating"]/text()').get()
            #score = booklist[0].xpath('td//*[@class = "smallText uitext"]/a/text()').get()
            #booksdict['score'] = int(score[7:].replace(',', ''))
            booksdict['avg_rating'] = float(rating.split()[0])
            booksdict['num_ratings'] = int(rating.split()[4].replace(',', ''))

            yield booksdict

        nextpage = response.xpath('//*[@class="next_page"]/@href').get()

        if nextpage:
            yield Request(response.urljoin(nextpage), callback = self.parse)
