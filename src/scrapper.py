import urllib
import requests
from bs4 import BeautifulSoup as bs


url = 'https://paperswithcode.com/'
req = requests.get(url)

soup = bs(req.text, 'lxml')

print(soup.title.string)

papers_dict = {}
papers = []

items_divs = soup.find_all('div', {'class':'row infinite-item item'})

for item in items_divs:
    for child in item.children:
        # Image
        try:
            # Check if classes are in child attributes
            if set(child.attrs['class']) <= set(['col-lg-3', 'item-image-col']):
                # Image url
                print(child.find('div', {'class':'item-image'})['style'])  
                # TODO : parse url
                papers_dict['image'] = '';    
        except:
            pass

        # Content
        try:
            if set(child.attrs['class']) <= set(['col-lg-9', 'item-col']):
                # Title
                print(child.find('h1').a.string)
                papers_dict['title'] = child.find('h1').a.string
                # Nb stars
                print(child.find('span', {'class':'badge badge-secondary'}).text.strip())
                papers_dict['nb_stars'] = child.find('span', {'class':'badge badge-secondary'}).text.strip()
                # Star/hour
                print(child.find('div', {'class':'stars-accumulated text-center'}).text.strip())
                papers_dict['hourly_stars'] = child.find('div', {'class':'stars-accumulated text-center'}).text.strip();
                # Paper page link link
                print(child.find('a', {'class':'badge badge-light'})['href'])
                link_to_paper_page = child.find('a', {'class':'badge badge-light'})['href']
        except:
            pass
            link_to_paper_page
    papers.append(papers_dict)
    print('\n')