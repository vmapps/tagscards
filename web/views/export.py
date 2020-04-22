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
from web.utils import get_info, get_sort

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
    return( jsonify( list(res) ), 200, {
        'ContentType':'application/json',
        'Content-Disposition': 'attachment; filename=' + filename
    }) 

# --------------------------------------------------------
# EXPORT - VCARD
# --------------------------------------------------------
@app.route('/export/vcard/<id>')
def export_vcard(id):
    res = r.table('contacts').get(id).run()

    vcf = '''BEGIN:VCARD
VERSION:3.0
FN;CHARSET=UTF-8:%s
N;CHARSET=UTF-8:%s;;;;
EMAIL;CHARSET=UTF-8:%s
TEL;TYPE=WORK,VOICE:%s
ORG;CHARSET=UTF-8:%s
URL;type=WORK;CHARSET=UTF-8:%s
NOTE;CHARSET=UTF-8:PGP KEY ID=%s
REV:%sZ
END:VCARD''' % (
        res['fullname'],
        res['fullname'],
        res['email'],
        res['phone'],
        res['role'],
        res['website'],
        res['pgp'],
        datetime.datetime.now().isoformat()[:23]
    )

    filename = '"%s.vcf"' % res['fullname']
    return( vcf, 200, {
        'ContentType':'text/directory',
        'Content-Disposition': 'attachment; filename=' + filename
    }) 
