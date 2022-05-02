from vars import SOURCE_MOVIES, SOURCE_ANIMETV, SOURCE_TV, LOG_LOCATION, SOURCE_4K_MOVIES, DESTINATION_MOVIES, DESTINATION_4K_MOVIES
import main
from os import listdir, path
from os.path import isfile, join
import glob
import os
import logging
from datetime import datetime

LOG_LOCATION = LOG_LOCATION()
logging.basicConfig(filename=LOG_LOCATION, level=logging.INFO)

def movie_start(file_source, file_destination):
    # Starting the movie file search and move based on files
    counter = 0
    SOURCE_DIR_MOVIE = file_source
    PARENT_DIR = file_destination
    media_files = [f for f in listdir(SOURCE_DIR_MOVIE) if path.isfile(path.join(SOURCE_DIR_MOVIE, f))]
    if media_files:
        logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
        for file in media_files:
            movie = main.Movies(file, SOURCE_DIR_MOVIE, PARENT_DIR)
            movie.move_file()
            counter += 1

    # Starting the movie file search and move based on files in directories
    media_files = glob.glob(SOURCE_DIR_MOVIE + "*/*.mkv")
    if media_files:
        logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
        for movie in media_files:
            if "Backed_Up" not in movie:
                movie_path_list = movie.split("/")
                movie_file = movie_path_list[-1]
                del movie_path_list[-1]
                movie_path = "/".join(movie_path_list)
                Movie = main.Movies(movie_file, movie_path, PARENT_DIR)
                Movie.move_file()
                counter += 1
    if "radarr4k" not in SOURCE_DIR_MOVIE:
        file_type = "Movies"
    else: 
        file_type = "4K Movies"
    if counter > 0:
        logging.info(str(datetime.now()) + " - Total " + file_type + " Copied: " + str(counter))
    else:
        logging.info(str(datetime.now()) + " - No " + file_type + " found")

# # Starting the movie search and move based on files
# counter = 0
# SOURCE_DIR_MOVIE = SOURCE_MOVIES()
# PARENT_DIR = DESTINATION_MOVIES()
# media_files = [f for f in listdir(SOURCE_DIR_MOVIE) if path.isfile(path.join(SOURCE_DIR_MOVIE, f))]
# if media_files:
#     logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
#     for file in media_files:
#         movie = main.Movies(file, SOURCE_DIR_MOVIE, PARENT_DIR)
#         movie.move_file()
#         counter += 1

# # Starting the movie search and move based on files in directories
# media_files = glob.glob(SOURCE_DIR_MOVIE + "*/*.mkv")
# if media_files:
#     logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
#     for movie in media_files:
#         if "Backed_Up" not in movie:
#             movie_path_list = movie.split("/")
#             movie_file = movie_path_list[-1]
#             del movie_path_list[-1]
#             movie_path = "/".join(movie_path_list)
#             Movie = main.Movies(movie_file, movie_path, PARENT_DIR)
#             Movie.move_file()
#             counter += 1
# logging.info(str(datetime.now()) + " - Total Movies Copied: " + str(counter))

SOURCE_DIR_MOVIE = SOURCE_MOVIES()
PARENT_DIR = DESTINATION_MOVIES()
movie_start(SOURCE_DIR_MOVIE, PARENT_DIR)

# Starting anime tv show search and move
counter = 0
SOURCE_DIR_ANIMETV = SOURCE_ANIMETV()
media_files = [f for f in listdir(SOURCE_DIR_ANIMETV) if isfile(join(SOURCE_DIR_ANIMETV, f))]
if media_files:
    logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
    for file in media_files:
        anime = main.Anime(file, SOURCE_DIR_ANIMETV)
        anime.move_file()
        counter += 1
media_files = glob.glob(SOURCE_DIR_ANIMETV + "*/*.mkv")
if media_files:
    logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
    for file in media_files:
        if "Backed_Up" not in file:
            anime_path_list = file.split("/")
            anime_file = anime_path_list[-1]
            del anime_path_list[-1]
            anime_path = "/".join(anime_path_list)
            anime = main.Anime(anime_file, anime_path)
            anime.move_file()
            counter += 1
logging.info(str(datetime.now()) + " - Total Anime Episodes Copied: " + str(counter))

# Starting the TV show move
counter = 0
SOURCE_DIR_TV = SOURCE_TV()
media_files = [f for f in listdir(SOURCE_DIR_TV) if isfile(join(SOURCE_DIR_TV, f))]
if media_files:
    logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
    for file in media_files:
        tv_show = main.TVShows(file, SOURCE_DIR_TV)
        tv_show.move_file()
        counter += 1

media_files = glob.glob(SOURCE_DIR_TV + "*/*.mkv")
if media_files:
    logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
    for tv_show in media_files:
        if "Backed_Up" not in tv_show:
            tv_path_list = tv_show.split("/")
            tv_file = tv_path_list[-1]
            del tv_path_list[-1]
            tv_path = "/".join(tv_path_list)
            tv_show = main.TVShows(tv_file, tv_path)
            tv_show.move_file()
            counter += 1
logging.info(str(datetime.now()) + " - Total TV Show Episodes Copied: " + str(counter))

# # Starting the 4K movie search and move based on files
# counter = 0
# SOURCE_DIR_MOVIE = SOURCE_4K_MOVIES()
# PARENT_DIR = DESTINATION_4K_MOVIES()
# media_files = [f for f in listdir(SOURCE_DIR_MOVIE) if path.isfile(path.join(SOURCE_DIR_MOVIE, f))]
# if media_files:
#     logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
#     for file in media_files:
#         movie = main.Movies(file, SOURCE_DIR_MOVIE, PARENT_DIR)
#         movie.move_file()
#         counter += 1

# # Starting the 4K movie search and move based on files in directories
# media_files = glob.glob(SOURCE_DIR_MOVIE + "*/*.mkv")
# if media_files:
#     logging.info(str(datetime.now()) + " - Files Found: " + str(media_files))
#     for movie in media_files:
#         if "Backed_Up" not in movie:
#             movie_path_list = movie.split("/")
#             movie_file = movie_path_list[-1]
#             del movie_path_list[-1]
#             movie_path = "/".join(movie_path_list)
#             Movie = main.Movies(movie_file, movie_path, PARENT_DIR)
#             Movie.move_file()
#             counter += 1
# logging.info(str(datetime.now()) + " - Total Movies Copied: " + str(counter))

SOURCE_DIR_MOVIE = SOURCE_4K_MOVIES()
PARENT_DIR = DESTINATION_4K_MOVIES()
movie_start(SOURCE_DIR_MOVIE, PARENT_DIR)

# Once all files are uploaded then it kicks off a scan
docker_cmd = "docker exec -dt plex /config/plex_scanner.sh "
os.system(docker_cmd)
