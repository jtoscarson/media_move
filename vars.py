import yaml

# Parsing the config.yaml file and returning the variable values to be imported in the main sections of the code.
def all_vars():
    with open("config.yaml", "r") as var_yaml:
        config = yaml.safe_load(var_yaml)
    return config

def SOURCE_MOVIES():
    config = all_vars()
    SOURCE_DIR_MOVIE = config['APP']['SOURCE_MOVIES']
    return SOURCE_DIR_MOVIE

def DESTINATION_MOVIES():
    config = all_vars()
    DESTINATION_MOVIES = config['APP']['DESTINATION_MOVIES']
    return DESTINATION_MOVIES

def SOURCE_ANIMETV():
    config = all_vars()
    SOURCE_DIR_ANIMETV = config['APP']['SOURCE_ANIMETV']
    return SOURCE_DIR_ANIMETV

def DESTINATION_ANIMETV():
    config = all_vars()
    DESTINATION_ANIMETV = config['APP']['DESTINATION_ANIMETV']
    return DESTINATION_ANIMETV

def SOURCE_TV():
    config = all_vars()
    SOURCE_DIR_TV = config['APP']['SOURCE_TV']
    return SOURCE_DIR_TV

def DESTINATION_TV():
    config = all_vars()
    DESTINATION_TV = config['APP']['DESTINATION_TV']
    return DESTINATION_TV

def SOURCE_4K_MOVIES():
    config = all_vars()
    SOURCE_4K_MOVIES = config['APP']['SOURCE_4K_MOVIES']
    return SOURCE_4K_MOVIES

def DESTINATION_4K_MOVIES():
    config = all_vars()
    DESTINATION_4K_MOVIES = config['APP']['DESTINATION_4K_MOVIES']
    return DESTINATION_4K_MOVIES

def MAL_CLIENT_ID():
    config = all_vars()
    MAL_CLIENT_ID = config['APP']['MAL_CLIENT_ID']
    return MAL_CLIENT_ID

def PLEX_TOKEN():
    config = all_vars()
    PLEX_TOKEN = config['APP']['PLEX_TOKEN']
    return PLEX_TOKEN

def PLEX_URL():
    config = all_vars()
    PLEX_URL = config['APP']['PLEX_URL']
    return PLEX_URL

def LOG_LOCATION():
    config = all_vars()
    LOG_LOCATION = config['APP']['LOG_LOCATION']
    return LOG_LOCATION

