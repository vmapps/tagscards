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
# MISC
# --------------------------------------------------------
def get_info(key=''):
    res = r.table('contacts').pluck('tags').run()
    tot = r.table('contacts').count().run()

    tags = defaultdict(int)
    for c in res:
        for t in c['tags']:
            tags[t] += 1

    # for key,val in tags.items():
    #     print( "%s : %d" % (key,val) )
    # return (tot,tags)
    info = {}
    info['records'] = tot
    info['key'] = key.split(',')
    info['tags'] = tags

    return( info )

def get_sort():
    vsort = request.args.get('sort')

    if( vsort==None ): 
        return( 'fullname' )
    elif( vsort[0]=='A' ):
        return( r.asc(vsort[1:]) )
    elif( vsort[0]=='D' ):
        return( r.desc(vsort[1:]) )

    return('')

# --------------------------------------------------------
# CONTACTS
# --------------------------------------------------------
@app.route('/contacts')
def contacts_all():
    vsort = get_sort()

    info = get_info()
    res = r.table('contacts').order_by(vsort).run()

    return render_template('contacts/list.html',contacts=res,info=info)

# --------------------------------------------------------
# CONTACTS - TAG
# --------------------------------------------------------
@app.route('/contacts/tag/<id>')
def contacts_tag(id):
    lid = id.lower().split(',')

    vsort = get_sort()
    info = get_info(id)
    res = r.table('contacts').filter(lambda c:
        c["tags"].contains( r.args(lid) )
    ).order_by(vsort).run()

    return render_template('contacts/list.html',contacts=res,info=info)

# --------------------------------------------------------
# CONTACTS - SEARCH
# --------------------------------------------------------
@app.route('/contacts/search/<id>')
def contacts_search(id):
    id = id.lower()
    lid = id.split(',')

    vsort = get_sort()    
    info = get_info(id)

    res = r.table('contacts').filter(lambda c:
        c["tags"].contains( r.args(lid) )
        | c["fullname"].downcase().match(id)
        | c["position"].downcase().match(id)
    ).order_by(vsort).run()

    return render_template('contacts/list.html',contacts=res,info=info)

# --------------------------------------------------------
# CONTACTS - ADD
# --------------------------------------------------------
@app.route('/contacts/add',methods=['POST','GET'])
@login_required
def contacts_add():
    if( request.method=='POST' ):
        data = request.form

        contact = {}
        contact['fullname'] = data['contact_fullname']
        contact['position'] = data['contact_position']
        contact['email'] = data['contact_email']
        contact['pgp'] = data['contact_pgp']
        contact['phone'] = data['contact_phone']
        contact['website'] = data['contact_website']
        if( data['contact_tags'] ):
            contact['tags'] = data['contact_tags'].lower().split(',')
        else:
            contact['tags'] = []

        res = r.db('test').table('contacts').insert(contact).run()
        if( not res['errors'] ):
            return redirect(url_for('contacts_all'))

    info = get_info()
    return render_template('contacts/edit.html',contact={},info=info)

# --------------------------------------------------------
# CONTACTS - MOD
# --------------------------------------------------------
@app.route('/contacts/mod/<id>',methods=['POST','GET'])
@login_required
def contacts_mod(id):
    if( request.method=='POST' ):
        data = request.form

        contact = {}
        contact['fullname'] = data['contact_fullname']
        contact['position'] = data['contact_position']
        contact['email'] = data['contact_email']
        contact['pgp'] = data['contact_pgp']
        contact['phone'] = data['contact_phone']
        contact['website'] = data['contact_website']
        if( data['contact_tags'] ):
            contact['tags'] = data['contact_tags'].lower().split(',')
        else:
            contact['tags'] = []

        if( data['contact_id'] ):
            res = r.table('contacts').get(id).update(contact).run()
            if( not res['errors'] ):
                return redirect(url_for('contacts_all'))
    
    info = get_info()
    res = r.table('contacts').get(id).run()
    return render_template('contacts/edit.html',contact=res,info=info)

# --------------------------------------------------------
# CONTACTS - DEL
# --------------------------------------------------------
@app.route('/contacts/del/<id>',methods=['GET'])
@login_required
def contacts_del(id):
    res = r.table('contacts').get(id).delete().run()
    if( not res['errors'] ):
        return redirect(url_for('contacts_all'))

    return redirect(url_for('contacts_all'))
