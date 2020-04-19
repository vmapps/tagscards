# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
from flask import Flask, render_template, g
from jinja2 import nodes
from jinja2.ext import Extension
from rethinkdb import r
# --------------------------------------------------------
# LAUNCH APP
# --------------------------------------------------------

app = Flask(__name__)

app.config.from_object('web.config')
app.url_map.strict_slashes = False
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

from web import views

# --------------------------------------------------------
# DATABASE UTILS
# --------------------------------------------------------
@app.before_request
def db_get():
    if not hasattr(g,'rethinkdb'):
        g.rethinkdb = r.connect( \
            host=app.config['RETHINKDB_HOST'], \
            port=app.config['RETHINKDB_PORT'], \
            db=app.config['RETHINKDB_BASE'] \
        ).repl()

@app.teardown_appcontext
def db_close(error):
    if hasattr(g,'rethinkdb'):
        g.rethinkdb.close()

# --------------------------------------------------------
# 404 ERROR HANDLER
# --------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# --------------------------------------------------------
# IF MAIN
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(threaded=true)
