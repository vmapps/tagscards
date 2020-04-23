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
from werkzeug.security import check_password_hash, generate_password_hash
from json import dumps
from pprint import pprint, pformat
from rethinkdb import r
from collections import defaultdict

from web import app
from web.decorators import login_required, isadmin

# --------------------------------------------------------
# MISC
# --------------------------------------------------------

# --------------------------------------------------------
# USERS
# --------------------------------------------------------
@app.route('/users')
@login_required
def users_list():

    res = r.table('users').order_by('username').run()

    return render_template('users/list.html',users=res)

# --------------------------------------------------------
# USERS - ADD
# --------------------------------------------------------
@app.route('/users/add',methods=['POST','GET'])
@login_required
def users_add():
    if( request.method=='POST' ):
        data = request.form

        if( data['user_password1']==data['user_password2'] ):

            user = {}
            user['username'] = data['user_username']
            user['email'] = data['user_email']
            user['password'] = generate_password_hash(data['user_password1'],"sha256")

            res = r.table('users').insert(user).run()
            if( not res['errors'] ):
                flash('new user added !','success')
                return redirect(url_for('users_list'))

        flash('error when adding new user !','danger')

    return render_template('users/edit.html',user={})

# --------------------------------------------------------
# USERS - MOD
# --------------------------------------------------------
@app.route('/users/mod/<id>',methods=['POST','GET'])
@login_required
def users_mod(id):
    if( request.method=='POST' ):
        data = request.form

        if( data['user_id'] ):
        
            if( data['user_password1']==data['user_password2'] ):
                user = {}
                user['username'] = data['user_username']
                user['email'] = data['user_email']
                user['password'] = generate_password_hash(data['user_password1'],"sha256")

            if( not data['user_password1']):
                user = {}
                user['username'] = data['user_username']
                user['email'] = data['user_email']
                
            res = r.table('users').get(id).update(user).run()
            if( not res['errors'] ):
                flash('user updated !','success')
                return redirect(url_for('users_list'))
    
        flash('error when updating user !','danger')

    res = r.table('users').get(id).run()
    return render_template('users/edit.html',user=res)

# --------------------------------------------------------
# USERS - DEL
# --------------------------------------------------------
@app.route('/users/del/<id>',methods=['GET'])
@login_required
def users_del(id):
    res = r.table('users').get(id).delete().run()
    if( not res['errors'] ):
        flash('user deleted !','success')
        return redirect(url_for('users_list'))

    flash('error when deleting user !','danger')
    return redirect(url_for('users_list'))