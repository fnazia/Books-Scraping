import scrapy
from scrapy import Request
from ..pipelines import GoodbooksPipeline
from scrapy import Selector


class GoodreadsSpider(scrapy.Spider):
    name = 'goodreads'
    allowed_domains = ['goodreads.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            GoodbooksPipeline: 300
        }
    }

    def start_requests(self):
        start_urls = ['https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_']
        yield Request(start_urls[0], callback = self.author_requests)

    def author_requests(self, response):
        authorlinks = response.xpath('//*[@class="authorName"]/@href').getall()
        unique_authorlinks = list(set(authorlinks))
        for author in unique_authorlinks:
            yield Request(author, callback=self.join_url)

    def join_url(self, response):
        morebooks = response.xpath('//*[@class="rightContainer"]//*[@class="bigBoxBody"]//*[@class="actionLink"]/@href').get()
        if morebooks:
            yield response.follow(morebooks, callback = self.parse)

    def parse(self, response):
        booksdict = {}
        usersdict_list = []
        booklist_tr = response.xpath('//*[@class="tableList"]/tr')

        for book in booklist_tr:
            booksdict['name'] = book.xpath('td//*[@class="bookTitle"]/span/text()').get()
            booksdict['author'] = book.xpath('td//*[@class="authorName"]/span/text()').get()
            booksdict['booklink'] = book.xpath('td//*[@class="bookTitle"]/@href').get()
            rating = book.xpath('td//*[@class = "minirating"]/text()').get()
            booksdict['avg_rating'] = float(rating.split()[0])
            booksdict['num_ratings'] = int(rating.split()[4].replace(',', ''))

            users_url = booksdict['booklink'] #response.urljoin(booksdict['booklink'])
            if users_url:
                usersdict_list.append(response.follow(users_url, callback = self.users_details))
            
                for usersdict in usersdict_list:
                    yield usersdict

            booksdict['item-type'] = 'books'

            yield booksdict

        nextpage = response.xpath('//*[@class="next_page"]/@href').get()

        if nextpage:
            yield Request(response.urljoin(nextpage), callback = self.parse)

    def users_details(self, response):
        usersdict = {}
        
        #userslinks = response.xpath('//div[@class="ReviewsList"]/article//*[@class="Avatar Avatar--medium"]/@href').getall()
        #userslinks = response.xpath('//div[@id="other_reviews"]//*[@id="bookReviews"]//div//div[@itemprop="reviews"]//a[@class="left imgcol"]/@href').getall()
        #ratinglines = response.xpath('//div[@class="ReviewsList"]/article//*[@class="ShelfStatus"]/span[@class="RatingStars RatingStars__small"]/@aria-label').getall()
        #datelist = response.xpath('//div[@class="ReviewsList"]/article//*[@class="Text Text__body3"]/a/text()').getall()
        #rating_dates = [d.strip() for d in datelist if d.strip() != 'Edited']
        #rating_dates = response.xpath('//div[@id="other_reviews"]//*[@id="bookReviews"]//div//div[@itemprop="reviews"]//*[@class="reviewDate createdAt right"]/text()').getall()

        #n_users = len(userslinks) if userslinks else 1
    
        #for i in range(n_users):
        #    usersdict['name'] = response.xpath('//h1[@data-testid="bookTitle"]/text()').get()
        #    usersdict['author'] = response.xpath('//div[@class="ContributorLinksList"]/a/span/text()').get()
        #    usersdict['first-published'] = response.xpath('//div[@class="BookDetails"]//p[@data-testid="publicationInfo"]/text()').get()
        #    usersdict['user_id'] = userslinks[i].split('/')[-1].split('-')[0] if userslinks else 'NA'
        #    usersdict['user_rating'] = ratinglines[i].split(' ')[1] if userslinks else 'NA'
        #    usersdict['user_rating_date'] = rating_dates[i] if userslinks else 'NA'
        #    usersdict['item-type'] = 'users'

        #    yield usersdict

        users = response.xpath('//div[@id="other_reviews"]//*[@id="bookReviews"]//div//div[@itemprop="reviews"]')
        
        n_users = len(users) if users else 1

        for i in range(n_users):
            usersdict['name'] = response.xpath('//*[@id="topcol"]//*[@id="metacol"]//*[@id="bookTitle"]/text()').get().strip()
            usersdict['author'] = response.xpath('//*[@id="topcol"]//*[@id="metacol"]//*[@class="authorName"]//span//text()').get().strip()
            usersdict['first-published'] = response.xpath('//*[@id="topcol"]//*[@id="metacol"]//*[@id="details"]//*[@class="greyText"]//text()').get().strip()
            #user_link = users[i].attrib['href'].split('/')[-1].split('-')[0] if users else 'NA'
            user_link = users[i].xpath('//*[@id="%s"]//*[@class="left imgcol"]/@href' % users[i].attrib['id']).get()
            usersdict['user_id'] = user_link.split('/')[-1].split('-')[0] if users else 'NA'
            usersdict['user_rating_date'] = users[i].xpath('//*[@id="%s"]//*[@class="reviewDate createdAt right"]/text()' % users[i].attrib['id']).get() if users else 'NA'
            usersdict['user_rating'] = users[i].xpath('//*[@id="%s"]//*[@class=" staticStars notranslate"]/@title' % users[i].attrib['id']).get() if users else 'NA'
            usersdict['item-type'] = 'users'

            yield usersdict

        


            
