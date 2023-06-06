import json
import os
import shutil
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
django.setup()

DATA_DIR = 'C:\\Users\\Maciej\\Downloads\\data' # CHANGE THIS
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
FIXTURE_FILEPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'userview', 'fixtures', 'sample.json')
MOVIES_DATA_DIR = os.path.join(DATA_DIR, 'picked_movies')
RATINGS_DATA_DIR = os.path.join(DATA_DIR, 'picked_ratings')
USERS_DATA_DIR = os.path.join(DATA_DIR, 'picked_users')

if not os.path.exists(os.path.join(MEDIA_DIR, 'movie_images')):
    os.makedirs(os.path.join(MEDIA_DIR, 'movie_images'))


all_ganres_dict = {}
all_genres = []
all_movies = {}
all_movie_images = []
all_ratings = []
all_users = []
all_comments = []

def get_all_data():
    return all_genres + list(all_movies.values()) + all_movie_images + all_ratings + all_users + all_comments

cnt = 1
for filename in os.listdir(MOVIES_DATA_DIR):
    print(f'movies and images: {cnt}\r', end='')
    cnt += 1
    filepath = os.path.join(MOVIES_DATA_DIR, filename)
    if os.path.isfile(filepath):
        basename, ext = os.path.splitext(os.path.basename(filepath))
        pk = int(basename)
        with open(filepath) as f:
            if ext == '.json':
                movie = json.load(f)

                genreNames = movie['genre'].replace(' ', '').split(',')
                genreIdxs = []
                for genre in genreNames:
                    if genre not in all_ganres_dict:
                        all_genres.append({'model': 'userview.genre', 'pk': len(all_genres) + 1, 'fields': {'name': genre}})
                        all_ganres_dict[genre] = {'model': 'userview.genre', 'pk': len(all_genres) + 1, 'fields': {'name': genre}}

                for genre in genreNames:
                    genreIdxs.append(all_ganres_dict[genre]['pk'])

                movie['genres'] = genreIdxs
                movie['image'] = pk
                del movie['genre']

                movie = {'model': 'userview.movie', 'pk': pk, 'fields': movie}

                all_movies[pk] = (movie)
            else:
                relative_path = 'movie_images/' + filename
                image = {'model': 'userview.movieimage', 'pk': pk, 'fields':
                         {'movie': pk,
                          'image': relative_path}}
                
                path = os.path.join(MEDIA_DIR, 'movie_images', filename)
                shutil.copyfile(filepath, path)
                all_movie_images.append(image)

print('')
cnt = 1
for filename in os.listdir(RATINGS_DATA_DIR):
    print(f'ratings: {cnt}\r', end='')
    cnt += 1
    filepath = os.path.join(RATINGS_DATA_DIR, filename)
    if os.path.isfile(filepath):
        basename = os.path.splitext(os.path.basename(filepath))[0]
        pk = int(basename) + 1

        rating = {}
        with open(filepath) as f:
            rating = json.load(f)

        rating['user'] = rating['user_id']
        rating['movie'] = rating['movie_id']
        rating['value'] = int(float(rating['rating']))
        if rating['value'] == 0:
            rating['value'] = 1
        del rating['rating']
        del rating['user_id']
        del rating['movie_id']
        rating = {'model': 'userview.rating', 'pk': pk, 'fields': rating}
        all_ratings.append(rating)

cnt_ratings = {}
for rating in all_ratings:
    movie_id = int(rating['fields']['movie'])
    if 'average_rating' not in all_movies[movie_id]['fields']:
        all_movies[movie_id]['fields']['average_rating'] = rating['fields']['value']
    else:
        all_movies[movie_id]['fields']['average_rating'] += rating['fields']['value']
    if movie_id not in cnt_ratings:
        cnt_ratings[movie_id] = 1
    else:
        cnt_ratings[movie_id] += 1

for movie_id, cnt in cnt_ratings.items():
    all_movies[movie_id]['fields']['average_rating'] /= cnt
    all_movies[movie_id]['fields']['average_rating'] = round(all_movies[movie_id]['fields']['average_rating'], 3)

print('')
cnt = 1
for filename in os.listdir(USERS_DATA_DIR):
    print(f'users: {cnt}\r', end='')
    cnt += 1
    filepath = os.path.join(USERS_DATA_DIR, filename)
    if os.path.isfile(filepath):
        user = {}
        with open(filepath) as f:
            user = json.load(f)

        pk = user['user_id']
        user['password'] = make_password(user['password'])

        del user['user_id']
        user = {'model': 'auth.user', 'pk': pk, 'fields': user}
        all_users.append(user)

print('')
filepath = os.path.join(DATA_DIR, 'picked_comments.json')
with open(filepath) as f:
    comments = json.load(f)
    for i, comment in enumerate(comments):
        comment['text'] = comment['comment']
        del comment['comment']
        print(f'comments: {i+1}\r', end='')
        all_comments.append({'model': 'userview.comment', 'pk': i+1, 'fields': comment})
        

print('')
print('dumping...')
with open(FIXTURE_FILEPATH, 'w') as f:
    json.dump(get_all_data(), f)

print('done!')