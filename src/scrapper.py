import urllib
import requests
from bs4 import BeautifulSoup as bs
from validator_collection import checkers


root_url = 'https://paperswithcode.com'
req = requests.get(root_url)

soup = bs(req.text, 'lxml')

#print(soup.title.string)

papers_dict = {}
papers = []
link_to_paper_page = None

items_divs = soup.find_all('div', {'class':'row infinite-item item'})

for item in items_divs:
    for child in item.children:
        # Image
        try:
            # Check if classes are in child attributes
            if set(child.attrs['class']) <= set(['col-lg-3', 'item-image-col']):
                # Image url
                #print(child.find('div', {'class':'item-image'})['style'])  
                papers_dict['image'] = root_url + str(child.find('div', {'class':'item-image'})['style'].split("('", 1)[1].split("')")[0])
                #print(papers_dict['image'])
        except:
            pass

        # Content
        try:
            if set(child.attrs['class']) <= set(['col-lg-9', 'item-col']):
                # Title
                #print(child.find('h1').a.string)
                papers_dict['title'] = child.find('h1').a.string
                # Nb stars
                #print(child.find('span', {'class':'badge badge-secondary'}).text.strip())
                papers_dict['nb_stars'] = child.find('span', {'class':'badge badge-secondary'}).text.strip()
                # Star/hour
                #print(child.find('div', {'class':'stars-accumulated text-center'}).text.strip())
                papers_dict['hourly_stars'] = child.find('div', {'class':'stars-accumulated text-center'}).text.strip();
                # Paper page link link
                #print(child.find('a', {'class':'badge badge-light'})['href'])
                link_to_paper_page = child.find('a', {'class':'badge badge-light'})['href']
        except:
            pass

    if link_to_paper_page != None:
        req = requests.get(root_url + link_to_paper_page)
        link_to_paper_page = None
        soup = bs(req.text, 'lxml')
        #print(soup.find('a', {'class':'badge badge-light'})['href'])
        pdf_link = soup.find('a', {'class':'badge badge-light'})['href']
        # Check if the link found is the pdf or a search query
        if checkers.is_url(pdf_link):
            r = requests.get(pdf_link)
        else:
            r = requests.get(root_url + pdf_link)
        
        content_type = r.headers.get('content-type')

        if 'application/pdf' in content_type:
            papers_dict['pdf'] = pdf_link
            # Github link
            #print(soup.find('a', {'class':'code-table-link'})['href'])
            papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href']
        elif 'text/html' in content_type:
            soup = bs(r.text, 'lxml')
            # PDF link
            #print(soup.find('a', {'class':'badge badge-light'})['href'])
            papers_dict['pdf'] = soup.find('a', {'class':'badge badge-light'})['href']
            # Github link
            #print(soup.find('a', {'class':'code-table-link'})['href'])
            papers_dict['github'] = soup.find('a', {'class':'code-table-link'})['href']

    papers.append(papers_dict)
    print('\n')

for paper in papers:
    print(paper)