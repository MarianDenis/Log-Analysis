import numpy as np
import os


def get_list_of_frequent_items(item_sets):
    el = []
    for element in item_sets:
        for x in item_sets[element]:
            el = np.append(el, x)

    el2 = []
    for element in el:
        if len(element) > 1:
            el2 = np.append(el2, [set(element)])

    return el2


def get_dictionary_from_item_sets(item_sets):
    item_dict = {}
    for item_set in item_sets:
        ok = 0
        referer = ''
        while ok < len(item_set):
            for item in item_set:
                if str(item).startswith("http"):
                    if item not in item_dict.keys():
                        item_dict[item] = set()
                        ok = ok + 1
                    referer = item
                else:
                    if referer != '':
                        item_dict[referer].add(item)
                        ok = ok + 1
    return item_dict


class Utility:
    def __init__(self):
        current_directory = os.path.dirname(os.getcwd())
        file = current_directory + '\\Intrusions\\DosDetection.txt'
        self.intrusion_file = open(file, 'w+')

    def get_ip_callers(self, item_set, logs, _date):
        self.intrusion_file.write("Day: " + str(_date) + "\n")

        ip_dict = {}

        freq_sets = get_list_of_frequent_items(item_set)
        item_dict = get_dictionary_from_item_sets(freq_sets)

        for referer in item_dict:
            items = item_dict[referer]
            for log in logs:
                if log[1] == referer and log[2] in items:  # log[0] = client_ip, log[1] = referer, log[2] = request
                    client_ip = log[0]
                    if referer in ip_dict:
                        ip_dict[referer].add(client_ip)
                    else:
                        ip_dict[referer] = set()
                        ip_dict[referer].add(client_ip)

            if referer in ip_dict:
                self.intrusion_file.write("Referer: " + str(referer) + "\n")
                self.intrusion_file.write("Requests:\n")

                for x in item_dict[referer]:
                    self.intrusion_file.write("\t- " + str(x) + "\n")

                self.intrusion_file.write("\n")

                self.intrusion_file.write("IP adresses:\n")
                index = 0
                for x in ip_dict[referer]:
                    index = index + 1
                    self.intrusion_file.write(str(x) + "; ")
                    if index % 5 == 0:
                        self.intrusion_file.write("\n")
                self.intrusion_file.write("\n")

        self.intrusion_file.write('\n')
