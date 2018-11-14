import sys
import os

filename = sys.argv[1]
conns = []
with open(filename) as f, open("hyccupscrawdad.txt", 'w') as out:
    for line in f:
        from_node, to_node, init, duration = [int(i) for i in line.split(',')]
        from_node -= 1
        to_node -= 1

        # ONE time is given in seconds
        init = init // 1000
        duration = duration // 1000
        end = init + duration
        conn = (from_node, to_node, init, end)
        conns.append(conn)

    # ordering by the init time
    conns.sort(key=lambda conn:conn[2])

    # the init time is the first init time
    init_time = conns[0][2]

    for conn in conns:
        # all time occurences must be subtracted by the init time
        out.write(f'{conn[0]}\t{conn[1]}\t{conn[2]-init_time}\t{conn[3]-init_time}{os.linesep}')

