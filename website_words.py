import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from complete_website_finder import get_links

url = input('url: ').strip()
ignore_words = ['the', 'be', 'to', 'of', 'and',
                'a', 'in', 'as', 'at', 'but', 'or',
                'an', 'so', 'is', 'are', 'was', 'were',
                'being', 'been', 'some', 'for', 'i', 'me',
                'mine', 'my', 'we', 'our', 'ours', 'ourselves',
                'you', 'your', 'yours', 'yourself', 'yourselves',
                'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
                'theirs', 'themselves', 'what', 'do', 'does', 'did', 'doing',
                'while', 'just', 'that', 'this', 'these', 'those', 'then']
list_of_words = []
list_of_ignored_words = []
list_of_lines = []

# finds all words in the website and store them in list_of_words
for item in get_links(url):
    response = requests.get(item)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('p')

    for link in links:
        line = link.text
        if line not in list_of_lines:
            list_of_lines.append(line)
            line_words = re.findall(r'\w+', line.lower())
            for word in line_words:
                if word not in ignore_words:
                    list_of_words.append(word)
                else:
                    list_of_ignored_words.append(word)

# ranks the list of words from most common to least common
unique_words = set(list_of_words)
words_ranked_tuples = []
for word in unique_words:
    words_ranked_tuples.append((word, list_of_words.count(word)))
words_ranked_tuples.sort(key=lambda x: x[1], reverse=True)

unique_ignored_words = set(list_of_ignored_words)
ignored_words_ranked_tuples = []
for word in unique_ignored_words:
    ignored_words_ranked_tuples.append(
        (word, list_of_ignored_words.count(word)))
ignored_words_ranked_tuples.sort(key=lambda x: x[1], reverse=True)

print('WORDS RANKED **********')
try:
    pprint(words_ranked_tuples)
except UnicodeEncodeError:
    pass
print('\n', 'IGNORED WORDS RANKED **********')
pprint(ignored_words_ranked_tuples)

# line 64 prints all of the links used in the website, but is not required
# print(get_links(url))
