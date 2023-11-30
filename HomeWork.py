import re
import json
from datetime import datetime
from pprint import pprint
import requests
from bs4 import BeautifulSoup


#           http://quotes.toscrape.com/page/10/
base_url = "http://quotes.toscrape.com"

pages_url = []
quotes = []
url_page_author_list = []

quote_page = []

author_page = []

quote_page_str = []
author_page_str = []
quotes_list = []
authors_list = []

author_page_name = []
author_value = []
author_born = []
author_born_town = []
author_description = []

author_key = []
Author_value = []

result_quote = {}
result_author_information = {}

test = []

slash = "/"
prefix_page = "/page/"
prefix_author = "/author/"

def get_result():
    pages_url.append(base_url)
    for i in range(2, 11):
        page_url = base_url + prefix_page + str(i) + slash
        pages_url.append(page_url)
    #pprint(pages_url)
    for url in pages_url:
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        quote = soup.find_all('span', class_='text')
        for i in quote:
            q = i.text.split('>')
            quote_page.append(q)
        for i in quote_page:
            for inner_i in i:
                quote_string = inner_i
                quote_page_str.append(quote_string)

        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        author = soup.find_all('small', class_='author')
        #pprint(author)
        for i in author:
            q = i.text.split('>')
            author_page.append(q)
        #pprint(author_page)
        for i in author_page:
            for inner_i in i:
                author_string = inner_i
                author_page_str.append(author_string)
        
        for i in range(len(quote_page_str)):
            result_quote[quote_page_str[i]] = author_page_str[i]
        
    for i in range(len(author_page_str)):
        string = author_page_str[i]
        if len(string.split(' ')) == 2:
            first, second = string.split(' ')
            new_string = first + '-' + second
            author_key.append(new_string)
        elif len(string.split(' ')) == 3:
            first, second, third = string.split(' ')
            new_string = first + '-' + second + '-' + third
            author_key.append(new_string)
        else:
            first, second, third, fourth = string.split(' ')
            new_string = first + '-' + second + '-' + third + '-' + fourth
            author_key.append(new_string)
    #print(len(author_key))
    new_author_key = list(set(author_key))
    #print(len(new_author_key))
    for i in new_author_key:
        url_page_author_string = base_url + prefix_author + i + slash
        url_page_author_list.append(url_page_author_string)
    #pprint(url_page_author_list)

    for url in url_page_author_list:
        responce = requests.get(url)
        soup = BeautifulSoup(responce.text, 'html.parser')
        author = soup.find_all('h3', class_='author-title')
        for i in author:
            author_str = i.text
            if author_str != '':
                author_value.append(author_str)
    
        soup = BeautifulSoup(responce.text, 'html.parser')
        born = soup.find_all('span', class_='author-born-date')
        for i in born:
            born_str = i.text
            if born_str != '':
                author_born.append(born_str)
    
        born_town = soup.find_all('span', class_='author-born-location')
        for i in born_town:
            born_town_str = i.text
            if born_town_str != '':
                author_born_town.append(born_town_str)
    
        description = soup.find_all('div', class_='author-description')
        for i in description:
            description_str = i.text
            if description_str != '\n':
                author_description.append(description_str)
        for i in range(len(author_value)):
            value_string = author_born[i] + ', ' + author_born_town[i] + ', ' + author_description[i]
            result_author_information[author_value[i]] = value_string
    #pprint(result_author_information)

    #pprint(author_value)
    #pprint(len(author_born))
    #pprint(len(author_born_town))
    #pprint(len(author_description))

    return result_quote, result_author_information

   
if __name__ == '__main__':
    r1, r2 = get_result()
    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(r1, fd, ensure_ascii=False)
    with open('authors.json', 'w', encoding='utf-8') as fd:
        json.dump(r2, fd, ensure_ascii=False)
                
    