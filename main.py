from vars import MAL_CLIENT_ID, PLEX_TOKEN, PLEX_URL, DESTINATION_MOVIES, DESTINATION_ANIMETV, DESTINATION_TV, LOG_LOCATION
from plexapi.server import PlexServer
import re
from os import path
from os.path import join
import string
import logging
from datetime import datetime
import urllib3
import certifi
import json
import sharedFunc

LOG_LOCATION = LOG_LOCATION()
logging.basicConfig(filename=LOG_LOCATION, level=logging.INFO)

"""
This class takes a file name and its path. Parses the filename
then creates the directory in the correct path and checks if
the movie is already in plex, and then moves it to the newly
made directory
"""
class Movies:
    def __init__(self, movie_file, SOURCE_DIR, PARENT_DIR):
        self.PARENT_DIR = PARENT_DIR
        self.SOURCE_DIR = SOURCE_DIR
        self.movie_file = movie_file
        self.source_path = join(self.SOURCE_DIR, self.movie_file)
    
    """
    Parsing the filename, and then formating it to: Movie Title (YEAR)
    Example: 
    Raw file: Laws.of.Attraction.2004.1080p.AMZN.WEB-DL.DDP2.0.x264-ABM.mkv
    Output: Laws Of Attraction (2004)
    """
    def format_name(self):
        year_index = ""
        year_regex = re.compile("^(19|20)\d{2}$")
        logging.info(str(datetime.now()) + " - Formatting: " + self.movie_file)
        movie_file_list = re.split(r'\W+', self.movie_file)
        for i in range(len(movie_file_list)):
            if year_regex.search(movie_file_list[i]):
                year_index = i + 1
                break
        if year_index == "":
            logging.error(str(datetime.now()) + " - Unable to find year for: " + self.SOURCE_DIR + "/" + self.movie_file)
            logging.error(str(datetime.now()) + " - Skipping file: " + self.SOURCE_DIR + "/" + self.movie_file)
            return False
        # removing everything from the file name after the year.
        del movie_file_list[year_index:]
        self.movie_year = movie_file_list[-1]
        movie_file_list[-1] = "(" + movie_file_list[-1] + ")"
        self.movie_dir = ' '.join(movie_file_list)
        self.movie_dir = string.capwords(self.movie_dir)
        # getting rid of the year in the title as it was throwing plex off
        del movie_file_list[-1]
        self.movie_name = ' '.join(movie_file_list)
        logging.info(str(datetime.now()) + " - Formatted the movie title to: " + self.movie_name)
        return

    """
    Query Plex with the formatted title without the year
    This is to check to see if the movie is already added to plex.
    """
    def plex_query(self):
        # connecting to plex so I can query it
        baseurl = PLEX_URL()
        token = PLEX_TOKEN()
        plex = PlexServer(baseurl, token)

        # search plex to make sure that the movie isn't already in plex.
        logging.info(str(datetime.now()) + " - Querying Plex: " + self.movie_name)
        for video in plex.search(self.movie_name):
            if video.TYPE == "movie":
                if video.year == self.movie_year:
                    if video.title == self.movie_name:
                        logging.info(str(datetime.now()) + " - Plex matched: " + video.title + " " + video.year)
                        return False
        logging.info(str(datetime.now()) + " - No match found in Plex")
        return True

    """
    This is the main function that is called, that then calls the
    other functions. It confirms if the movie was added to plex
    and if it is then skips the upload part.
    """
    def move_file(self):
        self.format_name()
        des_path = sharedFunc.create_directory(self.PARENT_DIR, self.movie_dir)
        plexQuery = self.plex_query()
        if plexQuery:
            sharedFunc.rsync_file(self.source_path, des_path)
        else:
            logging.info(str(datetime.now()) + " - Skipping File As Movie is already in Plex")
        return True

"""
This class takes a file name and its path. Parses the filename
then, queries MAL API to get the English title for the anime.
Creates the directory in the correct path and then moves it to 
the newly made directory
"""
class Anime:
    def __init__(self, file_name, SOURCE_DIR):
        self.file_name = file_name
        self.SOURCE_DIR = SOURCE_DIR
        self.DESTINATION_PATH = DESTINATION_ANIMETV()
        self.source_path = join(self.SOURCE_DIR, self.file_name)

    """
    This is the function that is querying MyAnimeList API
    """
    def getAPIresponse(self):
        URL = "https://api.myanimelist.net/v2/anime?q="
        CLIENT_ID = MAL_CLIENT_ID()
        query = self.parseFileName()
        ADDITIONAL_FIELDS = "&limit=1&fields=alternative_titles"
        FULL_URL = URL + query + ADDITIONAL_FIELDS

        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        logging.info(str(datetime.now()) + " - Querying MyAnimeList API")
        r = http.request('GET', 
            FULL_URL,
            headers={
                "X-MAL-CLIENT-ID": CLIENT_ID
            })

        data = json.loads(r.data.decode('utf-8'))
        logging.info(str(datetime.now()) + " - Raw output from MyAnimeList API request: " + str(data))
        return data

    """
    Takes the file name and parses it to create a string that the MAL API can use
    Example:
    Raw File: [SubsPlease] Fantasy Bishoujo Juniku Ojisan to - 09 (1080p) [4D81F64F].mkv
    Output: Fantasy%20Bishoujo%20Juniku%20Ojisan%20to
    """
    def parseFileName(self):
        logging.info(str(datetime.now()) + " - Parsing File Name: " + self.file_name)
        parsedName = re.sub(r'^.*?] ', '', self.file_name)
        parsedName = re.sub(r' - .*.mkv', '', parsedName)
        self.parsed_file = parsedName
        query = parsedName.replace(" ", "%20")
        logging.info(str(datetime.now()) + " - Query string: " + query)
        return query 

    """
    The API response is not json, So I had to parse it like a string. It is looking for
    the EN title, synonyms, or just uses the File Name.
    Example:
    Query String: Fantasy%20Bishoujo%20Juniku%20Ojisan%20to
    Response: 'en': 'Life with an Ordinary Guy Who Reincarnated into a Total Fantasy Knockout'
    Parsed: Life with an Ordinary Guy Who Reincarnated into a Total Fantasy Knockout
    """
    def parseAPI(self):
        check = 0
        data = self.getAPIresponse()
        splitList = re.split(', |: ', str(data))
        length = len(splitList)
        for i in range(length):
            if "'en'" in splitList[i]:
                title = i + 1
                titleName = splitList[title]
                logging.info(str(datetime.now()) + " - Anime Name Parsed from API request MAL listed EN Title: " + titleName)
                # Checking to make sure that the EN title has something in it if not checking the synonyms section
                if titleName == "''":
                    for s in range(length):
                        if "{'synonyms'" in splitList[s]:
                            title = s + 1
                            titleName = splitList[title].replace('[', '')
                            logging.info(str(datetime.now()) + " - Anime Name Parsed from API request MAL listed 'synonyms': " + titleName)
                # checking if the title set by the synonyms is empty
                if titleName == "''" or titleName == "]":
                    check+=1
                    titleName = self.parsed_file
                    logging.info(str(datetime.now()) + " - Anime Name Parsed from API request: " + titleName)
                    break
                check+=1
                break
        # So this is basically just for if there is no response from the api call.
        if check == 0:
            titleName = self.parsed_file
        self.anime_dir = re.sub('\'|\"|\[|\]', '', titleName)
        logging.info(str(datetime.now()) + " - Anime Name Parsed from API request: " + self.anime_dir)
        return

    """
    This is the main function that is called, that then calls the
    other functions.
    """
    def move_file(self):
        self.parseAPI()
        des_path = sharedFunc.create_directory(self.DESTINATION_PATH, self.anime_dir)
        sharedFunc.rsync_file(self.source_path, des_path)

"""
This class takes a file name and its path. Parses the filename
then creates the directory in the correct path and then moves it to 
the newly made directory
"""
class TVShows:
    def __init__(self, file_name, SOURCE_DIR):
        self.DESTINATION_PATH = DESTINATION_TV()
        self.SOURCE_DIR = SOURCE_DIR
        self.file_name = file_name
        self.source_path = path.join(self.SOURCE_DIR, self.file_name)

    """
    Takes the file name and parses it to get the show name, and season number, so it can have the path for both.
    Example:
    Raw File: The.Endgame.S01E03.1080p.WEB.h264-GOSSIP.mkv
    Output: The Endgame/Season 01
    """
    def format_tv(self):
        se_ep_regex = re.compile("^(s|S)\d{2}(\.|)(((e|E)\d{2}){2}|(e|E)\d{2})$")
        logging.info(str(datetime.now()) + " - Parsing File Name: " + self.file_name)
        tv_list = re.split(r'\W+', self.file_name)
        for i in range(len(tv_list)):
            if se_ep_regex.search(tv_list[i]):
                seaEpi = i + 1
        try:
            del tv_list[seaEpi:]
        except:
            logging.error(str(datetime.now()) + " - Unable to parse the file: " + self.file_name)
            return False
        season_episode = tv_list[-1]
        season_num = season_episode[1:3]
        logging.info(str(datetime.now()) + " - Season Number: " + season_num)
        self.season_dir = "Season " + season_num
        del tv_list[-1]
        tv_show_dir = ' '.join(tv_list)
        tv_show = string.capwords(tv_show_dir)
        self.tv_show_dir = tv_show + "/" + self.season_dir
        logging.info(str(datetime.now()) + " - Show Name: " + tv_show)
        return True

    """
    This is the main function that is called, that then calls the
    other functions.
    """
    def move_file(self):
        format_show = self.format_tv()
        if format_show:
            des_path = sharedFunc.create_directory(self.DESTINATION_PATH, self.tv_show_dir)
            sharedFunc.rsync_file(self.source_path, des_path)
