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

# --------------------------------------------------------
# GET INFO
# --------------------------------------------------------
def get_info(key=''):
    res = r.table('contacts').pluck('tags').run()
    tot = r.table('contacts').count().run()

    tags = defaultdict(int)
    for c in res:
        for t in c['tags']:
            tags[t] += 1

    # for key,val in tags.items():
    #     print( '{0} : {1} '.format(key,val) )
    # return (tot,tags)
    info = {}
    info['records'] = tot
    info['key'] = key.split(',')
    info['tags'] = tags

    return( info )

# --------------------------------------------------------
# GET SORT
# --------------------------------------------------------

def get_sort():
    vsort = request.args.get('sort')

    if( vsort==None ): 
        return( 'fullname' )
    elif( vsort[0]=='A' ):
        return( r.asc(vsort[1:]) )
    elif( vsort[0]=='D' ):
        return( r.desc(vsort[1:]) )

    return('')
