# -*- coding: utf-8 -*-

# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
from flask import session, redirect, url_for
from functools import wraps
from pprint import pprint, pformat
from web import app

# --------------------------------------------------------
# DECORATORS
# --------------------------------------------------------
def login_required(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session.get('logged'):
			# Default TLP for non logged users
			session['role']='guest'
			return redirect(url_for('admin_login'))
		return f(*args, **kwargs)
	return wrapped

def if_full_auth(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session.get('logged') and app.config['TAGSCARDS_FULLAUTH']:
			return redirect(url_for('admin_login'))
		return f(*args, **kwargs)
	return wrapped

def is_admin(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session['role']=='admin':
			return redirect(url_for('index'))
		return f(*args, **kwargs)
	return wrapped
