# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
from flask import Flask, g, session, render_template, redirect, url_for
from jinja2 import nodes
from jinja2.ext import Extension
from rethinkdb import r
from datetime import timedelta

# --------------------------------------------------------
# LAUNCH APP
# --------------------------------------------------------

app = Flask(__name__)

app.config.from_object('web.config')
app.url_map.strict_slashes = False
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')

from web.views import admin
from web.views import contacts
from web.views import export
from web.views import users

# --------------------------------------------------------
# DATABASE UTILS
# --------------------------------------------------------
@app.before_request
def before_request():
    # set session timeout
    session.permanent = True
    app.permanent_session_lifetime = timedelta( minutes=app.config['SESSION_TIMEOUT'] )
    # get global db handler
    if not hasattr(g,'rethinkdb'):
        g.rethinkdb = r.connect( \
            host=app.config['RETHINKDB_HOST'], \
            port=app.config['RETHINKDB_PORT'], \
            db=app.config['RETHINKDB_BASE'] \
        ).repl()

@app.teardown_appcontext
def teardown_appcontext(error):
    # close db
    if hasattr(g,'rethinkdb'):
        g.rethinkdb.close()

# --------------------------------------------------------
# 404 ERROR HANDLER
# --------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# --------------------------------------------------------
# SPECIFIC ROUTE HANDLER FOR STATIC CONTENT
# important hack to work both on WSGI and standalone mode
# --------------------------------------------------------
@app.route('/static/<path:path>')
def static_file(path):
    return app.send_static_file(path)

# --------------------------------------------------------
# HOME
# --------------------------------------------------------
@app.route('/')
def index():
    return redirect(url_for('contacts_list'))

# --------------------------------------------------------
# HELP PAGE
# --------------------------------------------------------
@app.route('/help')
def help():
    return render_template('help.html')

# --------------------------------------------------------
# IF MAIN
# --------------------------------------------------------
if __name__ == "__main__":
    app.run(threaded=true)
