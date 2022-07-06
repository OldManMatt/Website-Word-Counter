import requests
from bs4 import BeautifulSoup

# finds the links to most pages in a website and returns them as a set


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    list_of_links = [url]
    url_length = len(url)

    # adds the link to the list if it is an exetension of url
    for link in links:
        try:
            sub_url = link.get('href')
            if sub_url[:4] == 'http':
                if sub_url[:url_length] == url:
                    list_of_links.append(sub_url)

                # finds all links whithin this website
                sub_r = requests.get(sub_url)
                sub_soup = BeautifulSoup(sub_r.text, 'html.parser')
                sub_links = sub_soup.find_all('a')
                for sub_link in sub_links:
                    try:
                        sub_link_text = sub_link.get('href')
                        list_of_links.append(sub_link_text) if sub_link_text[
                            :url_length] == url else None
                    except:
                        pass
        except:
            pass

    unique_links = set(list_of_links)
    return(unique_links)
