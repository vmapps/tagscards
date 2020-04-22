
#-------------------------------------------------------------------
# main
#-------------------------------------------------------------------

APP_NAME	= 'tagsCards'
APP_TITLE 	= 'Store and tag your favorite contact cards'
APP_VERSION	= '0.1'

APP_AUTHOR	= 'VM Apps'
APP_CONTACT	= 'https://github.com/vmapps'

#-------------------------------------------------------------------
# database
#-------------------------------------------------------------------

RETHINKDB_HOST = 'localhost'
RETHINKDB_PORT = 28015
RETHINKDB_BASE = 'test'

#-------------------------------------------------------------------
# do not touch
#-------------------------------------------------------------------

TEMPLATES_AUTO_RELOAD = True

STATIC_FOLDER	= 'static'

SESSION_TIMEOUT     = 5
SESSION_TYPE		= 'filesystem'
SESSION_FILE_DIR	= 'tmp'
SESSION_FILE_THRESHOLD	= 100
SESSION_FILE_MODE	= 600

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'bcb8c96a30dd09ebb07c813feae0c7f1b5ddc627'

SECRET_KEY = 'd0e62b7faaae0a2fdf439b6dbca170eab0a37c66'

