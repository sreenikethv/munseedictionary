#!/usr/bin/env python

#-----------------------------------------------------------------------
# runserver.py
# Author: Sreeniketh
#-----------------------------------------------------------------------


"""Module provides a simulation of the server,
which accepts multithreaded requests from the client."""

import sys
import argparse
import takwax

# python regserver.py 55560

#-----------------------------------------------------------------------
def main():
    # Create argument parser
    parser = argparse.ArgumentParser(prog="runserver.py",
        description="Munsee dictionary: server handling")
    parser.add_argument("port", type=int,
            help="the port at which the server is listening")
    args = vars(parser.parse_args())
    port = args.get("port")

    try:
        takwax.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
