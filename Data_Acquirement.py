import requests
import re
import pandas as pd


def get_movies(name):
    url = f'https://www.rottentomatoes.com/browse/{name}/?page=5'
    # url = 'https://www.rottentomatoes.com/browse/movies_in_theaters/?page=5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'content-type': 'text/html'
    }
    res = requests.get(url=url, headers=headers)
    pattern = r'alt="(.*?)"\s*class="posterImage"'
    matches = re.findall(pattern, res.text)
    print(len(matches), 'Movies')
    if len(matches) > 0:
        for i in range(len(matches)):
            matches[i] = matches[i].lower()
            matches[i] = re.sub(r"[^a-zA-Z0-9]+", "_", matches[i])
    return matches


def get_comments_movies(name):
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


def movie_data():
    infor_dict = {
        'movie_name': [],
        'movie_comment': [],
        'movie_label': []
    }
    movies = []
    movies_type = [
        'movies_at_home',
        'movies_at_home/sort:popular',
        'movies_at_home/sort:audience_highest',
        'movies_at_home/sort:audience_lowest',
        'movies_at_home/sort:critic_highest',
        'movies_at_home/sort:critic_lowest',
        'movies_in_theaters',
        'movies_in_theaters/sort:popular',
        'movies_in_theaters/sort:audience_highest',
        'movies_in_theaters/sort:audience_lowest',
        'movies_in_theaters/sort:critic_highest',
        'movies_in_theaters/sort:critic_lowest',
        'tv_series_browse',
        'tv_series_browse/sort:popular',
        'tv_series_browse/sort:audience_highest',
        'tv_series_browse/sort:audience_lowest',
        'tv_series_browse/sort:critic_highest',
        'tv_series_browse/sort:critic_lowest'
    ]
    for name in movies_type:
        movies += get_movies(name)
    print(len(movies), 'total')
    for i in range(len(movies)):
        comments, labels = get_comments_movies(movies[i])
        if i % 100 == 0:
            print(i, 'movies be processed')
        for j in range(len(comments)):
            infor_dict['movie_name'].append(movies[i])
            infor_dict['movie_comment'].append(comments[j])
            infor_dict['movie_label'].append(labels[j])

    df = pd.DataFrame(infor_dict)
    df.to_csv('movies.csv', index=False)


def get_games(name):
    url = f'https://store.steampowered.com/saleaction/ajaxgetsaledynamicappquery?cc=HK&l=english&clanAccountID=41316928&clanAnnouncementGID=3128313422564004283&flavor=popularpurchased&start={name}&count=150&tabuniqueid=8&sectionuniqueid=93094&return_capsules=true&origin=https:%2F%2Fstore.steampowered.com&bForceUseSaleTag=true&strContentHubType=freetoplay&strTabFilter=&strSectionFilter=%7B%22type%22:0,%22bNegated%22:true,%22rgSubexpressions%22:[%7B%22type%22:7,%22value%22:%22dlc%22%7D]%7D&bPrioritizeDiscounts=false'
    headers = {
        'Content-Type': 'application/json'
    }
    res = requests.get(url=url, headers=headers)
    res_dict = res.json()
    games = res_dict['appids']
    return games


def get_comments_games(name):
    url = f'https://steamcommunity.com/app/{name}/reviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=english'
    headers = {
        'Content-Type': 'text/html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    res = requests.get(url=url, headers=headers)
    # print(res.text)
    pattern = r'</div>\s+(.*?)\s+</div>\s+</div>\s+<div class="UserReviewCardContent_Footer">'
    comments = re.findall(pattern, res.text)
    # if len(comments) > 0:
    #     for i in range(len(comments)):
    #         comments[i] = re.sub(r"[^a-zA-Z\s]+", '', comments[i])
    pattern = r'<div class="title">(.+?)</div>'
    labels = re.findall(pattern, res.text)
    return comments, labels


def game_data():
    infor_dict = {
        'game_name': [],
        'game_comment': [],
        'game_label': []
    }
    games = []
    games_type = [i for i in range(0, 2001, 100)]
    for name in games_type:
        games += get_games(name)
    print(len(games), 'total games')
    for i in range(len(games)):
        comments, labels = get_comments_games(games[i])
        if i % 100 == 0:
            print(i, 'games be processed')
        for j in range(len(comments)):
            infor_dict['game_name'].append(games[i])
            infor_dict['game_comment'].append(comments[j])
            infor_dict['game_label'].append(labels[j])

    df = pd.DataFrame(infor_dict)
    print(df.shape[0], 'total data')
    df.to_csv('games.csv', index=False)


if __name__ == '__main__':
    # movie_data()
    game_data()