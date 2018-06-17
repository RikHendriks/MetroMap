import xml.etree.ElementTree as ET

import random


class XMLReader:
    def __init__(self, filename):
        self.filename = filename
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()


class NameListXMLReader(XMLReader):
    def __init__(self, filename):
        super().__init__(filename)
        self.name_lists = {}
        # Read the name lists from the xml file
        for name_list in self.root.findall('name_list'):
            self.name_lists[name_list.get('name')] = []
            for word in name_list.iter('word'):
                self.name_lists[name_list.get('name')].append(word.text)

    def get_random_name(self, name_list):
        if name_list in self.name_lists:
            return random.choice(self.name_lists[name_list])
        else:
            return None
