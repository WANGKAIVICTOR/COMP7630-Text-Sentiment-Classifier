import requests
import re
import pandas as pd


def get_movies():
    url = 'https://www.rottentomatoes.com/browse/movies_at_home/sort:popular'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'content-type': 'text/html'
    }
    res = requests.get(url=url, headers=headers)
    pattern = r'alt="(.*?)"\s*class="posterImage"'
    matches = re.findall(pattern, res.text)
    # print(matches)
    if len(matches) > 0:
        # print('There are some movies')
        for i in range(len(matches)):
            matches[i] = matches[i].lower()
            matches[i] = re.sub(r"[^a-zA-Z0-9]+", "_", matches[i])
    return matches


def get_comment(name):
    url = f'https://www.rottentomatoes.com/m/{name}/reviews'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'content-type': 'text/html',
    }

    res = requests.get(url=url, headers=headers)

    # Define a regular expression pattern to match the phrase "review-quote"
    pattern = r'review-quote">(.*?)<\/p>'
    comments = re.findall(pattern, res.text)
    if len(comments) > 0:
        for i in range(len(comments)):
            comments[i] = re.sub(r'\d+', '', comments[i])
            comments[i] = re.sub(r'[&#;]', '', comments[i])
        # print(comments)
    pattern = r'hide" state="([^"]+)"'
    labels = re.findall(pattern, res.text)
    # print(labels)
    return comments, labels


if __name__ == '__main__':
    infor_dict = {
        'movie_name': [],
        'movie_comment': [],
        'movie_label': []
    }

    movies = get_movies()
    for i in range(len(movies)):
        comments, labels = get_comment(movies[i])
        for j in range(len(comments)):
            infor_dict['movie_name'].append(movies[i])
            infor_dict['movie_comment'].append(comments[j])
            infor_dict['movie_label'].append(labels[j])

    df = pd.DataFrame(infor_dict)
    df.to_csv('movies.csv', index=False)
    print(df)

