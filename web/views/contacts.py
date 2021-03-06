# -*- coding: utf-8 -*-

# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
import re, time
import hashlib
import urllib
import json
import datetime
import csv
import codecs

from flask import render_template, flash, request, redirect, session, url_for, jsonify
from json import dumps
from pprint import pprint, pformat
from rethinkdb import r
from collections import defaultdict
from werkzeug.utils import secure_filename

from web import app
from web.decorators import login_required, if_full_auth, is_admin 
from web.utils import get_info, get_sort

# --------------------------------------------------------
# CONTACTS - LIST
# --------------------------------------------------------
@app.route('/contacts')
@if_full_auth
def contacts_list():
    vsort = get_sort()

    info = get_info()
    res = r.table('contacts').order_by(vsort).run()

    return render_template('contacts/list.html',contacts=res,info=info)

# --------------------------------------------------------
# CONTACTS - GET
# --------------------------------------------------------
@app.route('/contacts/<id>')
@if_full_auth
def contacts_get(id):

    res = r.table('contacts').get(id).run()

    return render_template('contacts/get.html',contact=res)

# --------------------------------------------------------
# CONTACTS - TAG
# --------------------------------------------------------
@app.route('/contacts/tag/<id>')
@if_full_auth
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
@if_full_auth
def contacts_search(id):
    id = id.lower()
    lid = id.split(',')

    vsort = get_sort()    
    info = get_info(id)

    res = r.table('contacts').filter(lambda c:
        c["tags"].contains( r.args(lid) )
        | c["fullname"].downcase().match(id)
        | c["role"].downcase().match(id)
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
        contact['role'] = data['contact_role']
        contact['email'] = data['contact_email']
        contact['pgp'] = data['contact_pgp']
        contact['phone'] = data['contact_phone']
        contact['website'] = data['contact_website']
        if( data['contact_tags'] ):
            contact['tags'] = data['contact_tags'].lower().split(',')
        else:
            contact['tags'] = []
        contact['notes'] = data['contact_notes']

        res = r.table('contacts').insert(contact).run()
        if( not res['errors'] ):
            flash('new contact added !','success')
            return redirect(url_for('contacts_list'))

        flash('error when adding new contact !','danger')

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
        contact['role'] = data['contact_role']
        contact['email'] = data['contact_email']
        contact['pgp'] = data['contact_pgp']
        contact['phone'] = data['contact_phone']
        contact['website'] = data['contact_website']
        if( data['contact_tags'] ):
            contact['tags'] = data['contact_tags'].lower().split(',')
        else:
            contact['tags'] = []
        contact['notes'] = data['contact_notes']

        if( data['contact_id'] ):
            res = r.table('contacts').get(id).update(contact).run()
            if( not res['errors'] ):
                flash('contact updated !','success')
                return redirect(url_for('contacts_list'))
    
        flash('error when updating contact !','danger')

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
        flash('contact deleted !','success')
        return redirect(url_for('contacts_list'))

    flash('error when deleting contact !','danger')
    return redirect(url_for('contacts_list'))

# --------------------------------------------------------
# CONTACTS - IMPORT
# --------------------------------------------------------
@app.route('/contacts/import',methods=['POST','GET'])
@login_required
def contacts_import():
    if( request.method=='POST' ):
        csvfile = request.files['import_csvfile']
        extfile = csvfile.filename.rsplit('.',1)[1].lower()

        if( extfile=='csv' ):
            stream = codecs.iterdecode(csvfile.stream,'utf-8')

            for row in csv.reader(stream,delimiter=";",dialect=csv.excel):
                contact = {}
                contact['fullname'] = row[0]
                contact['role'] = row[1]
                contact['email'] = row[2]
                contact['pgp'] = row[3]
                contact['phone'] = row[4]
                contact['website'] = row[5]
                if( row[6] ):
                    contact['tags'] = row[6].lower().split(',')
                else:
                    contact['tags'] = []

                res = r.table('contacts').insert(contact).run()
                if( not res['errors'] ):
                    continue
                
            return redirect(url_for('contacts_list'))
                
    return render_template('contacts/import.html')

# --------------------------------------------------------
# CONTACTS - BULK
# --------------------------------------------------------
@app.route('/contacts/bulk',methods=['POST'])
@login_required
def contacts_bulk():
    if( request.method=='POST' ):

        if( request.form['method'] and not request.form['tags']=='' ):
            for c in request.form.getlist('contacts[]'):
                # get tags from contact
                res = r.table('contacts').get(c).run()
                # nerge tags with tags to add
                tags1 = list(res['tags']) 
                tags2 = request.form['tags'].split(',')

                if( request.form['method']=='add'):
                    # update contact with tags (union)
                    res = r.table('contacts').get(c).update({
                        'tags': set(tags1).union( set(tags2) )
                    }).run()

                if( request.form['method']=='del'):
                    # update contact with tags (union)
                    res = r.table('contacts').get(c).update({
                        'tags': {element for element in tags1 if element not in tags2}
                    }).run()

            flash('contacts updated with tags!','success')
            return redirect(url_for('contacts_list'))

        flash('error when updating contacts with tags !','danger')

    return redirect(url_for('contacts_list'))

