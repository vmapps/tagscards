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

# --------------------------------------------------------
# ADMIN - LOGIN
# --------------------------------------------------------
@app.route('/admin/login',methods=['POST','GET'])
def admin_login():
    if( request.method=='POST' ):
        data = request.form

        res = r.table('users').filter({
            'username': data['admin_username'],
            'password': data['admin_password']
        }).count().run()

        if( res==1 ):
            session['logged'] = True
            session['username'] = data['admin_username']
            return redirect(url_for('index'))

    return render_template('admin/login.html')

# --------------------------------------------------------
# ADMIN - LOGOUT
# --------------------------------------------------------
@app.route('/admin/logout')
def admin_logout():
    session['session'] = None
    session['username'] = None
    session.clear()

    return redirect(url_for('index'))
