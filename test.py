from vars import MAL_CLIENT_ID, PLEX_TOKEN, PLEX_URL, DESTINATION_MOVIES, DESTINATION_ANIMETV, DESTINATION_TV, LOG_LOCATION
from os.path import join
import logging
from datetime import datetime
import re
from plexapi.server import PlexServer

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