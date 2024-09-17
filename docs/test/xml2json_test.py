from lxml.etree import Element, ElementTree
import json
from lxml import etree


class XML2JSON:
    def __init__(self, file_path):
        self.file_path = file_path
        self.xml_string = self._read_file_as_bytes()
        self.root = etree.fromstring(self.xml_string)

    def _read_file_as_bytes(self):
        """Read the XML file as bytes to handle encoding declarations properly.
        """
        with open(self.file_path, 'rb') as file:  # Open as binary
            return file.read()

    def xml_to_dict(self, element):
        """Recursively convert XML elements to dictionary,
         preserving escape characters.
        """
        data = {}
        if element.attrib:
            data.update({k: self._preserve_escape_chars(v) for k, v in element.attrib.items()})
        if element.text and element.text.strip():
            data['text'] = self._preserve_escape_chars(element.text.strip())
        children = list(element)
        if children:
            data['mxfile'] = [self.xml_to_dict(child) for child in children]
        return data

    def _preserve_escape_chars(self, text):
        """Preserve escape characters by returning text as is."""
        return text

    def convert_to_json(self, output_path):
        """Convert XML data to JSON and write to file."""
        xml_dict = self.xml_to_dict(self.root)
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(xml_dict, json_file, indent=4, ensure_ascii=False)


# Usage
xml_file_path = '../data/xml_files/Video_CP108_2codec.drawio.xml'
json_file_path = 'converted.json'

converter = XML2JSON(xml_file_path)
converter.convert_to_json(json_file_path)


def json_to_dict(json_data):
    """Convert JSON data to Python dictionary."""
    return json.loads(json_data)


def dict_to_xml(tag, d):
    """Convert a dictionary to XML, handling CDATA and preserving structure."""
    elem = Element(tag)
    for key, val in d.items():
        if isinstance(val, dict):
            child = dict_to_xml(key, val)
            elem.append(child)
        elif isinstance(val, list):
            for sub_d in val:
                child = dict_to_xml(key, sub_d)
                elem.append(child)
        elif key == 'text':  # Handle text content separately
            elem.text = etree.CDATA(val)  # Wrap text in CDATA if needed
        else:
            elem.set(key, val)
    return elem


def update_json(json_file_path):
    """Update JSON data based on the provided updates."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Apply updates to the data
    # for key, value in updates.items():
        # Implement more complex logic as needed for nested updates
        # if isinstance(value, dict):
            # data[key].update(value)
        # else:
            # data[key] = value

    # Write the updated JSON back to the file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)


def json_to_xml(json_file_path, xml_file_path):
    """Convert JSON file to XML file."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json_file.read()

    data = json_to_dict(json_data)

    root_tag = "root"  # Adjust as needed based on your data
    xml_root = dict_to_xml(root_tag, data)

    tree = ElementTree(xml_root)
    tree.write(xml_file_path,
               encoding='utf-8',
               xml_declaration=True,
               pretty_print=True)


# Usage
json_file_path = 'converted.json'
xml_file_path = '../data/xml_files/updated_diagram.xml'

# Example updates: adjust according to JSON structure
updates = {
    'mxCell': [
        {'id': 'new_id', 'value': 'new_value'}
    ]
}

# update_json(json_file_path)
json_to_xml(json_file_path, xml_file_path)
