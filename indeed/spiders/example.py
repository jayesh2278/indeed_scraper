import scrapy
import csv
import re
from datetime import date

class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    start_urls = ['https://www.indeed.com/jobs?q=fashion%20design&l=United%20States']
    role_check ={}

    def parse(self, response):
        all_urls = response.xpath('.//*[@id="mosaic-provider-jobcards"]//a[@class="jcs-JobTitle"]')
        headers = {
                    'authority': 'www.indeed.com',
                    'cache-control': 'max-age=0',
                    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    'sec-ch-ua-mobile': '?0',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'sec-fetch-site': 'none',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-user': '?1',
                    'sec-fetch-dest': 'document',
                    'accept-language': 'en-US,en;q=0.9',
                    }
        for data in all_urls:
            # roles = response.meta.get('roles')
            url = data.xpath('./@href').extract_first()
            # posted_ago = data.xpath('.//*[@class="date"]/text()').extract_first()
            url = response.urljoin(url)
            yield scrapy.Request(url, callback=self.details)

        # next_page = response.xpath('.//*[@aria-label="Next"]/@href').extract_first()
        # if next_page:
        #     next_url = response.urljoin(next_page)
        #     yield scrapy.Request(next_url, callback=self.parse)

            # yield scrapy.Request(url, meta={'posted_ago':posted_ago},callback=self.details)
            # if role_csv == role_lower: 
            #     if role_csv in self.role_check:
            #         self.role_check[f'{role_csv}'] += 1
            #         # print(f'\n\n\nIF ROLE_CSV',{self.role_check[f'{role_csv}']},'\n\n\n')
            #     else:
            #         self.role_check[f'{role_csv}'] = 0
            #         # print('\n\n\n\nROLE CHECK',self.role_check,'\n\n\n\n')
            #     if self.role_check[f'{role_csv}']<5: 
                # next_page = response.xpath('.//*[@aria-label="Next"]/@href').extract_first()
                # if next_page:
                #     url = response.urljoin(next_page)
                #     pp = response.xpath('.//*[@aria-label="Next"]/@data-pp').extract_first()
                #     url = f'{url}&pp={pp}'
                #     yield scrapy.Request(url, meta = response.meta, headers=headers, callback=self.parse)

    

    def details(self, response):
        # inspect_response(response, self)
        item = {}
        # title = response.xpath('.//h1/text()').extract_first()
        source = 'Indeed'
        region = 'US'
        # job_category = 'IT'
        location = response.xpath('.//*[@class="jobsearch-RelatedLinks-linkWrapper"]/a/text()').re_first(r'jobs in (.*)$')
        sub_job_category = None
        today = date.today()
        date_collected = today.strftime("%d/%m/%Y")
        # posted_date = response.xpath('.//*[contains(text(),"Posted")]/following::b[1]/text()').extract_first()
        posted_ago = None
        company_name = response.xpath('.//*[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]//text()').extract_first()
        description = response.xpath('.//*[@id="jobDescriptionText"]//*//text()').extract()
        html_description = response.xpath('.//*[@id="jobDescriptionText"]').extract()
        description = [a.strip() for a in description if a.strip()]
        description = [a.replace('\xa0','').replace('\r','').replace('\t','').replace('â€œ', '“')\
                                    .replace('â€', '”').replace('â€™', '’').replace('â€˜', '‘')\
                                    .replace('â€”', '–').replace('â€“', '—').replace('â€¢', '-')\
                                    .replace('â€¦', '…') for a in description if a]
        html_description = [a.replace('\xa0','').replace('\r','').replace('\t','').replace('â€œ', '“')\
                                    .replace('â€', '”').replace('â€™', '’').replace('â€˜', '‘')\
                                    .replace('â€”', '–').replace('â€“', '—').replace('â€¢', '-')\
                                    .replace('â€¦', '…') for a in html_description if a]
        time = None
        salary = response.xpath('.//*[text()="Salary"]/following-sibling::*[contains(text(),"year")]/text()').extract_first()
        if salary:
            salary = salary.replace(' a year',' year')
        industry = 'Fashion'
        role = response.xpath('.//h1/text()').extract_first()
        # search_query = roles['role']        
        # key_words = response.xpath('.//*[@name="keywords"]/@content').extract_first()
        domain = None
        
        employment_type = response.xpath('.//*[@class="jobsearch-JobMetadataHeader-item  icl-u-xs-mt--xs"]/text()[2]').extract_first()
        redirect_url = response.xpath('.//*[text()="Apply On Company Site"]/@href').extract_first()
        education = None
        what_learn = response.xpath('.//*[@id="jobDescriptionText"]//*//text()').extract()
        what_learn = [a.strip() for a in what_learn if a.strip()]
        experience = ' '.join(what_learn)
        experience = re.findall(r'(\d+) [Yy]ear', experience)
        if experience:
            experience = max(experience)
            experience = f'{experience} Years'
        else:
            # inspect_response(response, self)
             experience = None
        # hard_skill = open('./../../../hard-skills.csv', 'r')
        # hard_data = list(csv.reader(hard_skill))
        # # open soft-skills csv file
        # soft_skill = open('./../../../soft-skills.csv', 'r')
        # soft_data = list(csv.reader(soft_skill))
        # hard_skill1 = open('./../../../updated_hard_skills.csv', 'r')
        # hard_data1 = list(csv.reader(hard_skill1))
        # # open compentency-skills csv file
        # compentency_skill = open('./../../../compentency.csv', 'r')
        # compentency_data = list(csv.reader(compentency_skill))
        # hard_skills = []
        # soft_skills = []
        # compentency_skills = []
        # hard_skills1 = []
        # if what_learn:
        #     for one_line in what_learn:
        #         punctuations = '''!()-[]{};:'"<>./?@#$%^&*_~・'''
        #         no_punct = ""
        #         for char in one_line:
        #             if char not in punctuations:
        #                 no_punct = no_punct + char
        #         no_punct = f' {no_punct} '
        #         # code for hard-skills
        #         for l_csv in hard_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in hard_skills:
        #                     hard_skills.append(char_word)

        #         for l_csv in hard_data1:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in hard_skills1:
        #                     hard_skills1.append(char_word)

        #         # code for soft-skills            
        #         for l_csv in soft_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_soft = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_soft += char
        #             char_ = f' {no_punct_char_soft} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in soft_skills:
        #                     soft_skills.append(char_word)

        #         # code for compentency-skills
        #         for l_csv in compentency_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in compentency_skills:
        #                     compentency_skills.append(char_word)

        # if role:
        #     for one_line in [role]:
        #         punctuations = '''!()-[]{};:'"<>./?@#$%^&*_~・'''
        #         no_punct = ""
        #         for char in one_line:
        #             if char not in punctuations:
        #                 no_punct = no_punct + char
        #         no_punct = f' {no_punct} '
        #         # code for hard-skills
        #         for l_csv in hard_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in hard_skills:
        #                     hard_skills.append(char_word)

        #         for l_csv in hard_data1:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in hard_skills1:
        #                     hard_skills1.append(char_word)

        #         # code for soft-skills            
        #         for l_csv in soft_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_soft = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_soft += char
        #             char_ = f' {no_punct_char_soft} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in soft_skills:
        #                     soft_skills.append(char_word)

        #         # code for compentency-skills
        #         for l_csv in compentency_data:
        #             char_word = l_csv[0]
        #             char_ = char_word.lower().split(' (',1)[0]
        #             no_punct_char_hard = ""
        #             for char in char_:
        #                 if char not in punctuations:
        #                     no_punct_char_hard += char

        #             char_ = f' {no_punct_char_hard} '
        #             if char_ in no_punct.lower():
        #                 if char_word not in compentency_skills:
        #                     compentency_skills.append(char_word)


        # # close both csv files
        # hard_skill.close()
        # soft_skill.close()        
        # compentency_skill.close()
        # hard_skill1.close()
        # if hard_skills:
        #     hard_skills = ','.join(hard_skills)
        # else:
        #     hard_skills = None
        # if soft_skills:
        #     soft_skills = ','.join(soft_skills)
        # else:
        #     soft_skills = None
        # if compentency_skills:
        #     compentency_skills = ','.join(compentency_skills)
        # else:
        #     compentency_skills = None

        item['Ref_JD_ID'] = None
        item['Ref_Skills_ID'] = None
        item['Date_Collected'] = date_collected
        item['Data_Source'] = source
        item['Region'] = region
        item['Industry_Sub_Domain'] = None
        item['Industry'] = industry
        item['Role'] = role
        item['Generic_Profile'] = None
        item['Knowledge_Domain'] = None
        item['UG'] = None
        item['PG'] = None
        item['Doctorate'] = None
        item['Education'] = None
        item['Educational_Institute'] = None
        # item['Soft_Skills_and_Behaviours'] = soft_skills
        # item['Competencies'] = compentency_skills
        # item['Technical_Skills'] = hard_skills
        item['Related_Technical_Skills'] = None
        item['Professional_Certification'] = None
        item['Related_Certifications'] = None
        item['Professional_Certification_Body'] = None
        item['Key_Skills'] = None
        item['Company_Name'] = company_name
        item['Company_Logo'] = None
        item['Redirect_URL'] = redirect_url
        item['Experience'] = experience
        item['Salary'] = salary
        item['Location'] = location
        item['Vacancies'] = None
        item['Job_Applicants'] = None
        item['Posted'] = posted_ago
        item['Posted_Date'] = None
        item['Closing_date'] = None
        item['Description'] = description
        item['HTML_Description'] = html_description
        item['Job_type'] = None
        item['Company_URL'] = None
        item['Company_Location'] = None
        item['Company_Description'] = None
        item['URL'] = response.url
        yield item