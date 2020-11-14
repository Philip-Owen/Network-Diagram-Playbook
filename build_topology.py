import os
import json
import sys

if sys.argv[1] == 'sample':
    network = os.listdir('sample_facts')
else:
    network = os.listdir('facts')
neighbors_list = {}
nodes = []
links = []


def create_nodes_and_neighbors(device_list):
    """
    Load JSON files and create inital dictionaries to filter data
    """
    for device in device_list:
        with open(f"facts/{device}") as f:
            # Load data
            data = json.loads(f.read())
            hostname = data[0]['net_hostname']
            # Create node dict
            nodes.append({'id': len(nodes), 'label': hostname})

            interface_list = list(data[0]['net_neighbors'].keys())
            device_neighbors = []
            for interface in interface_list:
                neighbor_info = data[0]['net_neighbors'][interface]
                for neighbor in neighbor_info:
                    device_neighbors.append(neighbor['host'].split('.')[0])

            # Create neighbors list object
            neighbors_list.update({hostname: device_neighbors})


def map_ids_to_neighbors():
    """
    Map neighbors to IDs and create a unique list of network links
    """
    for neighbor in list(neighbors_list.keys()):
        for device in neighbors_list[neighbor]:
            dest = list(filter(lambda d: d['label'] == device, nodes))
            if len(dest) > 0:
                source = list(filter(lambda d: d['label'] == neighbor, nodes))[
                    0]['id']
                link = [source, dest[0]['id']]
                link.sort()
                link_dict = {'from': link[0], 'to': link[1]}
                if link_dict not in links:
                    links.append(link_dict)


def create_json_file(filename):
    """
    Create formatted JSON file for network graph 
    """
    with open(filename, 'w') as f:
        f.truncate(0)
        json.dump({'nodes': nodes, 'links': links}, f)


def main():
    global network
    global neighbors_list
    global nodes
    global links
    create_nodes_and_neighbors(network)
    map_ids_to_neighbors()
    create_json_file('network_graph.json')


if __name__ == "__main__":
    main()
