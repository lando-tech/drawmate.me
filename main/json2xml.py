import json
import re

from lxml.etree import Element, ElementTree

try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    import xml.etree.ElementTree as etree
    print("running with Python's standard xml.etree.ElementTree")


def json_to_dict(json_data):
    """Convert JSON data to Python dictionary."""
    return json.loads(json_data)


def dict_to_xml(tag, d):
    """Convert a dictionary to XML, handling CDATA and preserving structure."""
    elem = Element(tag)
    for key, val in d.items():
        # remove number id from mxCell and mxPoint
        if re.match(r'mxCell-\d+', key):
            key = 'mxCell'
        elif re.match(r'mxPoint-\d+', key):
            key = 'mxPoint'

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


def json_to_xml(json_file_path, xml_file_path):
    """Convert JSON file to XML file."""
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json_file.read()

    data = json_to_dict(json_data)

    root_tag = "mxfile"  # Adjust as needed based on data
    xml_root = dict_to_xml(root_tag, data)

    tree = ElementTree(xml_root)
    tree.write(xml_file_path,
               encoding='utf-8',
               xml_declaration=True,
               pretty_print=True)


