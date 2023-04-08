import json
import requests
from bs4 import BeautifulSoup
import re

# Setup
# -----------------------------------------------------------------------------

checkpoint_file = 'data/marginal-revolution.json'
data_directory = 'data/txt/marginal-revolution'

template = """{title}

URL: {url}
Posted on: {date}
    
{content}
"""

# Helpers
# -----------------------------------------------------------------------------

def write_post(post_data):
    safe_title = re.sub('[^A-Za-z0-9]+', '_', post_data['title'])
    with open(f'{data_directory}/{safe_title}.txt', 'w') as txt_file:
        txt_file.write(template.format(**post_data))

def get_posts(url):
    print(f'Scraping {url}')

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    posts = soup.find_all('article', class_='post')
    for post in posts:
        title = post.find('h2', class_='entry-title').text.strip()
        url = post.find('h2', class_='entry-title').find('a')['href']
        date = post.find('time', class_='entry-date').text.strip()
        content = post.find('div', class_='entry-content').text.strip()

        post_data = {
            'title': title,
            'url': url,
            'date': date,
            'content': content
        }

        write_post(post_data)

        print(f'Scraped {title}')

    pagination = soup.find('div', class_='tool-pagination')
    next_page_link = pagination.find('a', class_='next')
    if next_page_link:
        next_page_url = next_page_link['href']

        try:
            get_posts(next_page_url)
        except RecursionError:
            print("Too many recursive calls. Saving progress.")
            with open(checkpoint_file, 'w') as config_file:
                config = {
                    'resume_at_url': next_page_url
                }
                json.dump(config, config_file)
    else:
        print("Scraping complete.")


# Main
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        with open(checkpoint_file, 'r') as config_file:
            config = json.load(config_file)
            resume_at_url = config['resume_at_url']

            get_posts(resume_at_url)
    except FileNotFoundError:
        get_posts('https://marginalrevolution.com/')
