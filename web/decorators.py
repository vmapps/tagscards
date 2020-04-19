# -*- coding: utf-8 -*-

# --------------------------------------------------------
# IMPORTS
# --------------------------------------------------------
from flask import session, redirect, url_for
from pprint import pprint, pformat
from functools import wraps

# --------------------------------------------------------
# DECORATORS
# --------------------------------------------------------
def logged(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session.get('logged'):
			# Default TLP for non logged users
			session['tlp']=1
			session['role']='guest'
			#return redirect('/login')
			return f(*args, **kwargs)
	return wrapped

def isadmin(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		if not session['role']=='admin':
			return redirect(url_for('prod.index'))
		return f(*args, **kwargs)
	return wrapped
