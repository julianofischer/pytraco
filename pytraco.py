import argparse
import importlib
import os

parser = argparse.ArgumentParser(description='Converts traces to ONE format.')
parser.add_argument("input", help="the trace file which will be analyzed")
parser.add_argument("-o", "--output", dest="output_file", default="output.txt",
                    help="the name for the output generated file")
parser.add_argument("extracter", help="the extracter to be used")
parser.add_argument("--set-init-time", dest='set_init_time', help="set init time to zero", action='store_true')
parser.set_defaults(set_init_time=False)
args = parser.parse_args()


def parse_to_one(event):
    return f"{event.time} CONN {event.from_node} {event.to_node} {event.opening_status()}{os.linesep}"


def main():
    module, theclass = args.extracter.split('.')
    Extracter = getattr(importlib.import_module(module), theclass)
    extracter = Extracter()
    all_events = []

    # convert all lines to events
    with open(args.input, 'r') as f:
        for line in f:
            events = extracter.extract_events(line)
            if isinstance(events, list):
                all_events += events
            else:
                # it is only one event
                all_events.append(events)

    all_events = sorted(all_events, key=lambda event: event.time)
    init_time = all_events[0].time

    with open(args.output_file, 'w') as f:
        for event in all_events:
            if args.set_init_time:
                event.time = event.time - init_time

            f.write(parse_to_one(event))


if __name__ == "__main__":
    main()
