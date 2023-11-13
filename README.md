# Books-Scraping
Goodreads Bengali books scraping using Scrapy

### Overview:

Website: www.goodreads.com <br/>
Target data: Books written by Bengali authors or written in Bangla <br/>
Framework: Scrapy <br/>
Start URL: https://www.goodreads.com/list/show/126394.Top_100_Bengali_Books_Translated_in_other_language_ <br/>
Scraped data: Books info, Users info <br/>
Books info contains: Book's name, Author, Link to its goodreads webpage, 
Average rating, Number of ratings <br/>
Users info contains: Book's name, Author, Date of first publication, ID of 
each user who rated it, Date of rating, Rating given by the user <br/>
Data wrangling: Data cleaning, removes duplicates and non-Bengali books, 
finds entries common between Books info and Users info, transforms raw 
data into interpretable format, gets top k writers <br/>

### Findings:

Number of unique book entries: 4,548 <br/>
Number of authors: 79 <br/>
Number of authors above 70% threshold (having more books than the rest): 23 <br/>
Books by the rest (below 70% threshold) of the authors constitute: 4% of the total books <br/>
Author having highest percentage of books (21.6%): Rabindranath Tagore <br/>
Authors below 56% threshold have: 1-3 books only <br/>
Number of books with user ratings: 108,284 <br/>
Author with the most user ratings (14.3%): Rabindranath Tagore <br/>
Authors of the most rated books: Nabarun Bhattacharya, 
Manik Bandopadhyay, 
Kazi Nazrul Islam, 
তারাশঙ্কর বন্দোপাধ্যায়, 
Sunil Gangopadhyay, 
Buddhadeb Guha, 
Bibhutibhushan Bandyopadhyay, 
Syed Mustafa Siraj, 
Syed Mujtaba Ali, 
Mahasweta Devi. <br/>

![alt text](https://github.com/fnazia/Books-Scraping/blob/main/imgs/books_per_author_dist.png?raw=true)

### Conclusion:

Scraping technique of this project needs to be improved because it failed to
extract all the books of some authors. For example, 'Muhammed Zafar Iqbal' 
has only 1 book in the scraped data, whereas there are approximately 300 
books listed under his name on goodreads. Moreover, most of the books' 'first
published date' was not extracted with this method. 

Although an author's many writings can be appreciated or read by many 
readers in a cumulative way, another author's single (or few specific) 
work can be read by more people compared to what any single work of the 
previous author can be read by.
