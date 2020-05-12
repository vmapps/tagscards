
#-------------------------------------------------------------------
# main
#-------------------------------------------------------------------

APP_NAME	= 'tagsCards'
APP_TITLE 	= 'Store and tag your favorite contact cards'
APP_VERSION	= '0.1'

APP_AUTHOR	= 'VM Apps'
APP_CONTACT	= 'https://github.com/vmapps'

#-------------------------------------------------------------------
# setup
#-------------------------------------------------------------------

TAGSCARDS_DATABASE = 'test'
TAGSCARDS_PASSWORD = 'tagscards'
TAGSCARDS_FULLAUTH = False

#-------------------------------------------------------------------
# database
#-------------------------------------------------------------------

RETHINKDB_HOST = 'localhost'
RETHINKDB_PORT = 28015
RETHINKDB_BASE = TAGSCARDS_DATABASE

#-------------------------------------------------------------------
# do not touch
#-------------------------------------------------------------------

TEMPLATES_AUTO_RELOAD = True

STATIC_FOLDER = 'static'

UPLOAD_FOLDER = 'temp'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

SESSION_TIMEOUT     = 15
SESSION_TYPE		= 'filesystem'
SESSION_FILE_DIR	= 'tmp'
SESSION_FILE_THRESHOLD	= 100
SESSION_FILE_MODE	= 600

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'bcb8c96a30dd09ebb07c813feae0c7f1b5ddc627'

SECRET_KEY = 'd0e62b7faaae0a2fdf439b6dbca170eab0a37c66'

