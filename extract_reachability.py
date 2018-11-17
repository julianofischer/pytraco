__author__ = "Juliano Fischer Naves"

import argparse


parser = argparse.ArgumentParser(description="Extracts information from reachability traces")
parser.add_argument(dest="filename", help="the trace file which will be analyzed",
                    metavar="FILENAME", nargs='?')
parser.add_argument("-s", "--step", dest="logstep", default=1, help="The step for logging information (every x seconds)",
                    metavar="STEP")
# parser.add_argument("--indegree", dest="indegree", action='store_true')
# parser.add_argument("--outdegree", dest="outdegree", action='store_true')
# parser.add_argument("--inoutratio", dest="outdegree", action='store_true')
# parser.set_defaults(indegree=True, outdegree=True, inoutratio=True, log_step=1)
parser.set_defaults(log_step=1)
args = parser.parse_args()


# dict_avg_in_degree = {}
# dict_avg_out_degree = {}
nodes = set()


def get_events(f):
    events = []
    with open(f, 'r') as myfile:
        for line in myfile:
            line = line.split()
            from_node = int(line[0])
            to_node = int(line[1])
            init_time = float(line[2])
            end_time = float(line[3])

            nodes.add(from_node)
            nodes.add(to_node)

            # end_time is the last instant for which the node has reachability to other node, so, the connection is
            # closed in the second immediately after the end_time
            close_time = end_time + 1
            up_event = (from_node, to_node, init_time, True)
            down_event = (from_node, to_node, close_time, False)
            events.extend([up_event, down_event])
    return events


def log_info(d):
    outfile = f'{args.filename}.avgindegree2'
    with open(outfile, 'w') as f:
        for index in d:
            f.write(f'{index}\t{float(d[index])/len(nodes)}\n')


def main():
    logstep = args.logstep
    filename = args.filename

    total_edges = 0
    dict_total_edges = {}

    events = get_events(filename)
    '''nodes = set()
    for event in events:
        # from node
        nodes.add(event[0])
        # to node
        nodes.add(event[1])'''

    # g = nx.DiGraph()
    # g.add_nodes_from(nodes)
    print("The number of nodes is %d" % (len(nodes),))

    # sorting the events by the time they occurred
    events.sort(key=lambda x: x[2])

    current_time = logstep

    # where there are events to process
    while len(events) > 0:
        # looking for events within the desired range
        # while event.time <= current_time
        while len(events) > 0 and events[0][2] <= current_time:
            # since eventes are ordered by time, it are always popped from the head of the queue
            event = events.pop(0)
            # if is_opening
            if event[3]:
                total_edges = total_edges + 1
            else:
                total_edges = total_edges - 1

        dict_total_edges[current_time] = total_edges
        current_time = current_time + logstep

    log_info(dict_total_edges)


if __name__ == '__main__':
    main()