import requests
from bs4 import BeautifulSoup

# finds the links to most pages in a website and returns them as a set


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')  # finds all links in the html document
    list_of_links = [url]  # creates the list of links and adds the url
    url_length = len(url)  # finds the length of the url

    for link in links:  # iterates through all links in the document
        try:
            # enables the sub_link object to be treated as a string
            sub_url = link.get('href')
            if sub_url[:4] == 'http':  # checks if the link is an absolute link
                list_of_links.append(sub_url) if sub_url[
                    :url_length] == url else None  # adds the link to the list if it is an exetension of the original url

                # finds all links whithin this website
                sub_r = requests.get(sub_url)
                sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
                sub_links = sub_soup.find_all('a')
                for sub_link in sub_links:  # iterates through all links in the sub website
                    try:
                        # enables the sub_link object to be treated as a string
                        sub_link_text = sub_link.get('href')
                        list_of_links.append(sub_link_text) if sub_link_text[
                            :url_length] == url else None  # adds the link to the list if it is an exetension of the original url
                    except:
                        pass
        except:
            pass

    unique_links = set(list_of_links)  # removes duplicate links
    return(unique_links)
