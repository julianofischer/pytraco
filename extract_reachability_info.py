__author__ = "Juliano Fischer Naves"

import argparse
import networkx as nx


parser = argparse.ArgumentParser(description="Descrição")
parser.add_argument("-f", "--file", dest="filename", help="the trace file which will be analyzed",
                    metavar="FILENAME")
parser.add_argument("-s", "--step", dest="log_step", help="The step for logging information (every x seconds)",
                    metavar="STEP")
parser.add_argument("--indegree", dest="indegree", action='store_true')
parser.add_argument("--outdegree", dest="outdegree", action='store_true')
parser.add_argument("--inoutratio", dest="outdegree", action='store_true')
parser.set_defaults(indegree=False, outdegree=False, inoutratio=False, log_step=1)
args = parser.parse_args()


dict_avg_in_degree = {}
dict_avg_out_degree = {}


class Event:
    def __init__(self, from_node, to_node, time, is_opening):
        self.from_node = from_node
        self.to_node = to_node
        self.time = time
        self.is_opening = is_opening

    def opening_status(self):
        return "up" if self.is_opening else "down"

    def __str__(self):
        return "event [%d,%d,%d,%s]" % (self.time, self.from_node, self.to_node, self.opening_status())


def get_events(f):
    events = []
    with open(f, 'r') as myfile:
        for line in myfile:
            line = line.split()
            from_node = int(line[0])
            to_node = int(line[1])
            init_time = float(line[2])
            end_time = float(line[3])

            # end_time is the last instant for which the node has reachability to other node, so, the connection is
            # closed in the second immediately after the end_time
            close_time = end_time + 1
            up_event = Event(from_node, to_node, init_time, True)
            down_event = Event(from_node, to_node, close_time, True)
            events.append([up_event, down_event])
    return events


def compute_avg_in_degree(graph, time):
    nodes = graph.nodes()
    in_degrees = [graph.in_degree(node) for node in nodes]
    avg = float(sum(in_degrees))/len(nodes)
    dict_avg_in_degree[time] = avg


def compute_avg_out_degree(graph, time):
    nodes = graph.nodes()
    out_degrees = [graph.in_degree(node) for node in nodes]
    avg = float(sum(out_degrees))/len(nodes)
    dict_avg_out_degree[time] = avg


def extract_info(graph, time):
    if args.indegree:
        compute_avg_in_degree(graph, time)

    if args.outdegree:
        compute_avg_out_degree(graph, time)


def log_info():
    if args.indegree:
        outfile = f'{args.filename}.avgindegree'
        with open(outfile) as f:
            for index in dict_avg_in_degree:
                f.write(f'{index}\t{dict_avg_in_degree[index]}\n')

    if args.outdegree:
        outfile = f'{args.filename}.avgoutdegree'
        with open(outfile) as f:
            for index in dict_avg_out_degree:
                f.write(f'{index}\t{dict_avg_out_degree[index]}\n')

    if args.inoutratio:
        outfile = f'{args.filename}.inoutratio'
        ratio = [(index, float(dict_avg_in_degree[index])/dict_avg_out_degree[index]) for index in dict_avg_in_degree]
        with open(outfile) as f:
            for t in ratio:
                f.write(f'{t[0]}\t{t[1]}\n')


def main():
    logstep = args.logstep

    filename = args.filename

    events = get_events(filename)
    nodes = set()
    for event in events:
        nodes.add(event.from_node)
        nodes.add(event.to_node)

    g = nx.DiGraph()
    g.add_nodes_from(nodes)

    # sorting the events by the time they occurred
    events.sort(key=lambda x: x.time)

    current_time = logstep

    # where there are events to process
    while len(events) > 0:
        # looking for events within the desired range
        while events[0].time <= current_time:
            # since eventes are ordered by time, it are always popped from the head of the queue
            event = events.pop(0)
            if event.is_opening:
                g.add_edge(event.from_node, event.to_node)
            else:
                g.remove_edge(event.from_node, event.to_node)

        extract_info(g, current_time)
        current_time = current_time + logstep






if __name__ == '__main__':
    main()