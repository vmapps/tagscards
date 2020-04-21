# -*- coding: utf-8 -*-

# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
import re, time
import hashlib
import urllib
import json
import datetime

from flask import render_template, flash, request, redirect, session, url_for, jsonify
from json import dumps
from pprint import pprint, pformat
from rethinkdb import r
from collections import defaultdict

from web import app
from web.decorators import login_required, isadmin

# --------------------------------------------------------
# EXPORT - TAGS
# --------------------------------------------------------
@app.route('/export/tags')
def export_tags():
    info = get_info()

    k = info['tags'].keys()
    return json.dumps( {"tags":list(k)} )

# --------------------------------------------------------
# EXPORT - CONTACTS
# --------------------------------------------------------
@app.route('/export/contacts')
def export_json():
    res = r.table('contacts').run()

    filename = '"contacts-%s.json"' % datetime.date.today()
    return( jsonify( list(res) ), 
            200, 
            {
                'ContentType':'application/octet-stream',
                'Content-Disposition': 'attachment; filename=' + filename
            }
    ) 
