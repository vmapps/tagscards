# tagscards
Store and tag your favorite contact cards

## Purpose 
Purpose of this very simple tool is to :
- create contact cards 
- store cards into database
- search for contacts using tags

## Requirements
Some modules are packaged with application :
- [Bootstrap 4](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [jQuery](https://jquery.com/)
- [Jquery Suggestags](https://github.com/amsify42/jquery.amsify.suggestags)

Following python modules are required :
- [Flask](https://flask.palletsprojects.com/)
- [RethinkDB](https://rethinkdb.com/)

Modules could be installed using following command:
```
$ pip install -r requirements.txt
```
Then run the flask server using following command:
```
$ ./manage.py --help
Usage: ./manage.py [options]

Options:
       -b, --bind=ADDRESS  bind to specific ip ADDRESS (default 0.0.0.0)
       -d, --debug         run in debug mode (default False)
       -h, --help          display this help and exit
       -p, --port=PORT     listen to specific PORT (default 8000)
       -t, --thread        run in threaded mode (default False)

$ ./manage.py --thread
```
## Configuration
Settings have to be defined into `web/config.py` file :
```
...
# database
RETHINKDB_HOST = 'localhost'
RETHINKDB_PORT = 28015
RETHINKDB_BASE = 'test'# enable/disable debug mode
...
```
## Some features
- Bootstrap 4 reqdy
- Tags input with auto-completion
- Admin user authentication
- Sorting on columns

## Todo list
- ~~bootstrap 4 integration~~
- ~~autocompletion for tags input~~
- ~~search with multiple tags~~
- ~~actions to add/edit/delete records~~
- ~~add PGP field~~
- ~~add position field~~
- ~~add website field~~
- ~~add sort asc/desc on fields~~
- ~~add icons support~~
- ~~fields text search support~~
- ~~login/logout functions~~
- ~~add session timeout~~
- manage pagination
- permissions to add/edit/delete records
- syntax check when editing fields
- pretty nice things to enhace interface
- export to vCards
- export for bulk mode
- ...

## Samples 
![tagscards1](samples/tagscards1.png)
![tagscards2](samples/tagscards2.png)
![tagscards3](samples/tagscards3.png)
![tagscards4](samples/tagscards4.png)
