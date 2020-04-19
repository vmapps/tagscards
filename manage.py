#!/usr/bin/env python

import sys
import getopt

from web import app

def usage():
    print( "Usage: %s [options]\n" % sys.argv[0] )
    print( """Options:
       -b, --bind=ADDRESS	bind to specific ip ADDRESS (default 0.0.0.0)
       -d, --debug		run in debug mode (default False)
       -h, --help		display this help and exit
       -p, --port=PORT	listen to specific PORT (default 8000)
       -t, --thread  	run in threaded mode (default False)
    """)

def main(argv):

    opt_host = '0.0.0.0'
    opt_port = 8000

    opt_debug = False
    opt_thread = False

    try:
        opts, args = getopt.getopt(argv,'hdtb:p:',['help','debug','thread','bind=','port='])

    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        if opt in ('-d', '--debug'):
            opt_debug = True
        if opt in ('-t', '--thread'):
            opt_thread = True
        if opt in ('-b', '--bind'):
            opt_host = arg
        if opt in ('-p', '--port'):
            opt_port = int(arg)
        
    print( "HOST=%s\nPORT=%d\nTHREAD=%r\nDEBUG=%r\n" % (opt_host,opt_port,opt_thread,opt_debug) )

    app.run(host=opt_host,port=opt_port,threaded=opt_thread,debug=opt_debug)

if __name__ == "__main__":
    main(sys.argv[1:])

