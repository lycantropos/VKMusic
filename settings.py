import configparser
import os
from urllib.parse import quote_plus

CONFIGURATION_FILE_NAME = 'configuration.conf'
CURRENT_FILE_PATH = os.path.realpath(__file__)
CURRENT_FILE_ABSPATH = os.path.abspath(CURRENT_FILE_PATH)
BASE_DIR = os.path.dirname(CURRENT_FILE_ABSPATH)

MAX_FILE_NAME_LEN = os.pathconf(CURRENT_FILE_ABSPATH, 'PC_NAME_MAX')

CONFIGURATION_FILE_FOLDER = 'configurations'
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
DST_PATH = files.get('dst_path')

database = config['database']
DB_HOST = database.get('db_host')
DB_USER_NAME = database.get('db_user_name')
DB_USER_PASSWORD = database.get('db_user_password')
DB_NAME = database.get('db_name')
DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'.format(DB_USER_NAME, quote_plus(DB_USER_PASSWORD), DB_HOST, DB_NAME)

logger = config['logger']
LOGS_PATH = logger.get('logs_path')
LOGGING_CONFIG_PATH = logger.get('logging_config_path')
