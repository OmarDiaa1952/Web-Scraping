import scrapy


class WorldometersSpider(scrapy.Spider):
    name = "worldometers"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        #titles=response.xpath("//h1//text()").get()
        countries=response.xpath("//td/a")
        for country in countries:
            country_name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()
            absolute_link=response.urljoin(link)
            #yield{
            #    'title':titles,
            #    'country_name':country_name,
            #    'link':absolute_link,
            #}
            yield response.follow(url=absolute_link , callback=self.parse_country,meta={'country':country_name})
    def parse_country(self,response):
        country=response.request.meta['country']
        rows=response.xpath("(//table[contains(@class,'table')])[1]/tbody/tr")
        for row in rows:
            year=row.xpath(".//td[1]/text()").get()
            population=row.xpath(".//td[2]/strong/text()").get()

            yield{
                'year':year,
                'population':population,
                'country':country,
            }
