# coding: utf-8
__author__ = "Juliano Fischer Naves"

import sys


def main():
    filename = sys.argv[1]
    opened_connections = set()

    with open(filename) as f:
        for line in f:
            time, action, fromnode, tonode, status = line.split()
            '''Connections aren't simplex'''
            # maxnode = max(int(fromnode), int(tonode))
            # minnode = min(int(fromnode), int(tonode))
            conn_id = "%s:%s" % (fromnode, tonode)

            if status == "up":
                if conn_id in opened_connections:
                    print("Connection %s already up at instant %s" % (conn_id, time))
                opened_connections.add(conn_id)
            elif status == "down":
                if conn_id not in opened_connections:
                    print("Trying to close a closed connection %s at instant %s" % (conn_id, time))
                else:
                    opened_connections.remove(conn_id)
            else:
                print("Something is going very wrong at instant %s" % (time,))


if __name__ == "__main__":
    main()
