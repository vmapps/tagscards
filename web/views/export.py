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
from web.decorators import login_required, if_full_auth, is_admin 
from web.utils import get_info, get_sort

# --------------------------------------------------------
# EXPORT - TAGS
# --------------------------------------------------------
@app.route('/export/tags')
@if_full_auth
def export_tags():
    info = get_info()

    k = info['tags'].keys()
    return json.dumps( {"tags":list(k)} )

# --------------------------------------------------------
# EXPORT - CONTACTS
# --------------------------------------------------------
@app.route('/export/contacts/<fmt>')
@if_full_auth
def export_contacts(fmt):
    res = r.table('contacts').run()

    if( fmt=='json' ):
        filename = '"contacts-{0}.json"'.format( datetime.date.today() )
        data = jsonify( list(res) )

        return( data, 200, {
            'ContentType':'application/json',
            'Content-Disposition': 'attachment; filename=' + filename
        }) 

    elif( fmt=='csv' ):
        filename = '"contacts-{0}.csv"'.format( datetime.date.today() )
        data = ''
        for c in res:
            data += '{0};{1};{2};{3};{4};{5};{6}\n'.format( 
                c['fullname'],
                c['role'],
                c['email'],
                c['pgp'],
                c['phone'],
                c['website'],
                ','.join(c['tags'])
            )

        return( data, 200, {
            'ContentType':'text/csv',
            'Content-Disposition': 'attachment; filename=' + filename
        }) 

# --------------------------------------------------------
# EXPORT - BULK
# --------------------------------------------------------
@app.route('/export/bulk',methods=['POST'])
@if_full_auth
def export_bulk():
    print(request.form)

    if( request.method=='POST' ):

        if( request.form['format']=='json' ):
            filename = '"contacts-{0}.json"'.format( datetime.date.today() )
            data = []
            for c in request.form['contacts'].split(','):
                res = r.table('contacts').get(c).run()
                data.append(res) 

            data = jsonify(data)
            return( data, 200, {
                'ContentType':'application/json',
                'Content-Disposition': 'attachment; filename=' + filename
            }) 

        elif( request.form['format']=='csv' ):
            filename = '"contacts-{0}.csv"'.format( datetime.date.today() )
            data = ''
            for c in request.form['contacts'].split(','):
                res = r.table('contacts').get(c).run()
                data += '{0};{1};{2};{3};{4};{5};{6}\n'.format( 
                    res['fullname'],
                    res['role'],
                    res['email'],
                    res['pgp'],
                    res['phone'],
                    res['website'],
                    ','.join(res['tags'])
                )

            return( data, 200, {
                'ContentType':'text/csv',
                'Content-Disposition': 'attachment; filename=' + filename
            }) 

# --------------------------------------------------------
# EXPORT - USERS
# --------------------------------------------------------
@app.route('/export/users')
@login_required
def export_users():
    res = r.table('users').run()

    filename = '"users-{0}.json"'.format( datetime.date.today() )
    return( jsonify( list(res) ), 200, {
        'ContentType':'application/json',
        'Content-Disposition': 'attachment; filename=' + filename
    }) 

# --------------------------------------------------------
# EXPORT - VCARD
# --------------------------------------------------------
@app.route('/export/vcard/<id>')
@if_full_auth
def export_vcard(id):
    res = r.table('contacts').get(id).run()

    vcf = '''BEGIN:VCARD
VERSION:3.0
FN;CHARSET=UTF-8:{0}
N;CHARSET=UTF-8:{1};;;;
EMAIL;CHARSET=UTF-8:{2}
TEL;TYPE=WORK,VOICE:{3}
ORG;CHARSET=UTF-8:{4}
URL;type=WORK;CHARSET=UTF-8:{5}
NOTE;CHARSET=UTF-8:PGP KEY ID={6}
REV:{7}Z
END:VCARD'''.format(
        res['fullname'],
        res['fullname'],
        res['email'],
        res['phone'],
        res['role'],
        res['website'],
        res['pgp'],
        datetime.datetime.now().isoformat()[:23]
    )

    filename = '"{0}.vcf"'.format( res['fullname'] )
    return( vcf, 200, {
        'ContentType':'text/directory',
        'Content-Disposition': 'attachment; filename=' + filename
    }) 
