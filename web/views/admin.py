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
from werkzeug.security import check_password_hash
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
# ADMIN - LOGIN
# --------------------------------------------------------
@app.route('/admin/login',methods=['POST','GET'])
def admin_login():
    if( request.method=='POST' ):
        data = request.form

        res = r.table('users').filter({
            'username': data['admin_username']
        }).run()

        res = list(res)
        if( len(res)==1 and check_password_hash(res[0]['password'],data['admin_password']) ):
            session['logged'] = True
            session['username'] = data['admin_username']
            flash('you are now logged in !','success')
            return redirect(url_for('index'))

        flash('error when logging in !','danger')

    return render_template('admin/login.html')

# --------------------------------------------------------
# ADMIN - LOGOUT
# --------------------------------------------------------
@app.route('/admin/logout')
def admin_logout():
    session['session'] = None
    session['username'] = None
    session.clear()

    flash('you are now logged out !','success')
    return redirect(url_for('index'))
