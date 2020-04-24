#!/usr/bin/env python

import sys
import getopt

from rethinkdb import r
from web import app

def usage():
    print( "Usage: %s [options]\n" % sys.argv[0] )
    print( """Options:
       -b, --bind=ADDRESS   bind to specific ip ADDRESS (default 0.0.0.0)
       -d, --debug          run in debug mode (default False)
       -i, --init           initialize database, tables and user admin
       -h, --help           display this help and exit
       -p, --port=PORT      listen to specific PORT (default 8000)
       -t, --thread         run in threaded mode (default False)
    """)

def main(argv):

    # variables
    opt_host = '0.0.0.0'
    opt_port = 8000
    opt_debug  = False
    opt_init   = False
    opt_thread = False

    # manage options
    try:
        opts, args = getopt.getopt(argv,'hditb:p:',['help','debug','init','thread','bind=','port='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    # setup variables with options
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-d', '--debug'):
            opt_debug = True
        if opt in ('-i', '--init'):
            opt_init = True
        if opt in ('-t', '--thread'):
            opt_thread = True
        if opt in ('-b', '--bind'):
            opt_host = arg
        if opt in ('-p', '--port'):
            opt_port = int(arg)
    
    # if initialization required
    if( opt_init ):
        # connection to RethinkDB 
        rdb = r.connect(
            host=app.config['RETHINKDB_HOST'],
            port=app.config['RETHINKDB_PORT'],
        ).repl()

        # check if RETHINK_BASE already exists
        if( not app.config['RETHINKDB_BASE'] in r.db_list().run() ):
            # setup minimal configuration
            res = r.db_create( app.config['RETHINKDB_BASE'] ).run()
            rdb.use( app.config['RETHINKDB_BASE'] )
            print('[1/4] Database "%s" created !' % app.config['RETHINKDB_BASE'])

            r.table_create('contacts').run()
            print('[2/4] Table "contacts" created !')

            r.table_create('users').run()
            print('[3/4] Table "users" created !')

            r.table('users').insert({
                'username': 'admin', 
                'email': '',
                'password': 'sha256$rKuw19OQ$df9f3737a5d6310e3e35b2a987155c22d535d2cd6d6bd507a07b9d9b3b0dd6f3'
            }).run();
            print('[4/4] User "admin" created !')
            
        else:
            print('[ERROR] Database "%s" already exists !' % app.config['RETHINKDB_BASE'])

        # close connection
        rdb.close()

    else:
        # verbose
        print( "HOST=%s\nPORT=%d\nTHREAD=%r\nDEBUG=%r\n" % (opt_host,opt_port,opt_thread,opt_debug) )

        # run application
        app.run(host=opt_host,port=opt_port,threaded=opt_thread,debug=opt_debug)

if __name__ == "__main__":
    main(sys.argv[1:])

