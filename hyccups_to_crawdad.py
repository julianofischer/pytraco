import sys
import os

filename = sys.argv[1]
with open(filename) as f, open("hyccupscrawdad.txt", 'w') as out:
    for line in f:
        from_node, to_node, init, duration = [int(i) for i in line.split(',')]
        from_node -= 1
        to_node -= 1

        # ONE time is given in seconds
        init = init // 1000
        duration = duration // 1000
        end = init + duration
        out.write(f'{from_node}\t{to_node}\t{init}\t{end}{os.linesep}')

