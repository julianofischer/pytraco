__author__ = "Juliano Fischer Naves"


# ESTÁ CONSUMINDO MUITA MEMÓRIA
# CRIAR ENTRADAS NOS DICIONÁRIOS SOMENTE SE MUDOU O ESTADO
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


dict_avg_in_degree = {}
dict_avg_out_degree = {}
nodes_in_degree = {}
nodes_out_degree = {}
nodes = set()


def init_dicts():
    for node in nodes:
        nodes_in_degree.setdefault(node, dict())
        nodes_out_degree.setdefault(node, dict())
        dict_avg_in_degree.setdefault(node, 0)
        dict_avg_out_degree.setdefault(node, 0)


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


def log_info(d, sufix):
    outfile = f'{args.filename}.{sufix}'
    with open(outfile, 'w') as f:
        for index in d:
            f.write(f'{index}\t{d[index]}\n')


def main():
    logstep = args.logstep
    filename = args.filename

    total_edges = 0
    dict_total_edges = {}

    events = get_events(filename)

    init_dicts()

    print("The number of nodes is %d" % (len(nodes),))

    # sorting the events by the time they occurred
    events.sort(key=lambda x: x[2])

    current_time = logstep

    # where there are events to process
    while len(events) > 0:
        # looking for events within the desired range
        # while event.time <= current_time
        while len(events) > 0 and events[0][2] <= current_time:
            # since events are ordered by time, it are always popped from the head of the queue
            event = events.pop(0)
            # if is_opening
            if event[3]:
                total_edges = total_edges + 1
                # from node
                dict_avg_out_degree[event[0]] += 1
                # to node
                dict_avg_in_degree[event[1]] += 1
            else:
                total_edges -= 1
                dict_avg_out_degree[event[0]] -= 1
                dict_avg_in_degree[event[1]] -= 1

            # updating node degree for current time
            nodes_out_degree[event[0]][current_time] = dict_avg_out_degree[event[0]]
            nodes_in_degree[event[1]][current_time] = dict_avg_in_degree[event[1]]

        dict_total_edges[current_time] = total_edges
        current_time = current_time + logstep

    log_info(dict_total_edges, 'total_edges')
    for node in nodes:
        log_info(nodes_in_degree[node], str(node)+'.in')
        log_info(nodes_out_degree[node], str(node) + '.out')


if __name__ == '__main__':
    main()
