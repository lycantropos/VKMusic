import configparser
import os
from urllib.parse import quote_plus

from sqlalchemy.engine import url

CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_FILE_ABSPATH = os.path.abspath(CURRENT_FILE_PATH)
BASE_DIR = os.path.dirname(CURRENT_FILE_ABSPATH)

CONFIGURATION_FILE_FOLDER = 'configurations'
CONFIGURATION_FILE_NAME = 'configuration.conf'
CONFIGURATION_FILE_PATH = os.path.join(BASE_DIR, CONFIGURATION_FILE_FOLDER, CONFIGURATION_FILE_NAME)
config = configparser.ConfigParser()
config.read(CONFIGURATION_FILE_PATH)

user = config['user']
USER_LOGIN = user.get('user_login')
USER_PASSWORD = user.get('user_password')

app = config['app']
APP_ID = app.get('app_id')
SCOPE = app.get('scope')

files = config['files']
DST_ABSPATH = files.get('dst_abspath')
MAX_FILE_NAME_LEN = os.pathconf(DST_ABSPATH, 'PC_NAME_MAX')

database = config['database']
DB_HOST = database.get('db_host')
DB_USER_NAME = database.get('db_user_name')
DB_USER_PASSWORD = quote_plus(database.get('db_user_password'))
DB_NAME = database.get('db_name')

DATABASE_URL = url.URL(
    drivername='mysql',
    host=DB_HOST,
    port=3306,
    username=DB_USER_NAME,
    password=DB_USER_PASSWORD,
    database=DB_NAME,
    query={'charset': 'utf8mb4'}
)


lastfm_api = config['lastfm_api']
LASTFM_API_KEY = lastfm_api.get('lastfm_api_key')
LASTFM_API_SHARED_SECRET = lastfm_api.get('lastfm_api_shared_secret')
LASTFM_USER_NAME = lastfm_api.get('lastfm_user_name')
LASTFM_USER_PASSWORD = lastfm_api.get('lastfm_user_password')

logger = config['logger']
LOGS_PATH = logger.get('logs_path')
LOGGING_CONFIG_PATH = logger.get('logging_config_path')
