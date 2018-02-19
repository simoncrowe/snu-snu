import json
import enum
from enum import Enum
import requests
import base64 
from io import BytesIO

from PIL import Image

import snusnu.errors as errors

TEMP_GIF_PATH = 'tmp/imageparsetemp'

class ProductAction(Enum):
    search = 0
    view = 1
    add_shopping_list = 2

# Dictionary used in text_process user interface
product_actions = { 0 : 'search for products',
                    1 : 'view products',
                    2 : 'add products to shopping list'}

class ProductDescription():
    def __init__(self, name, image = None):
        self.name = name
        self.image = image

class Command():
    '''Used as a parent class for all commands and
        to represent generic descriptions of commands'''
    def __init__(self, name, description, associated_action = None):
        self.name = name
        self.description = description
        self.associated_action = associated_action

class ProductCommand(Command):
    def __init__(self, name, description, associated_action,
                    search_category, search_string, number_of_items):
        super(ProductCommand, self).__init__(name, description,
                                            associated_action)
        self.search_string = search_string
        self.number_of_items = number_of_items
        self.search_category = search_category

class ProductCommandEncoder(json.JSONEncoder):
    """
    Outputs a JSON representation of a ProductCommand
    """
    def default(self, obj):
        if isinstance(obj, ProductCommand):
            return {
                'Name'              :   obj.name,
                'Description'       :   obj.description,
                'Associated action' :   obj.associated_action.value,
                'Search string'     :   obj.search_string,
                'Number of items'   :   obj.number_of_items,
                'Search category'   :   obj.search_category
                }
        return json.JSONEncoder.default(self, obj)

class ProductDescriptionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ProductDescription):
            return {'Name' :  (obj.name),
                    'Image' : (obj.image)}
        return json.JSONEncoder.default(self, obj)

def parse_product_command(obj):
    """
    Parses a JSON representation of a ProductCommand
    """
    if 'Search category' in obj:    # rather than identifiying each
                                    # ProductCommand as such
        return ProductCommand(  obj['Name'],
                                obj['Description'],
                                ProductAction(obj['Associated action']),
                                obj['Search category'],
                                obj['Search string'],
                                obj['Number of items'])

def parse_product_description(obj):
    """
    Parses a JSON representation of a ProductDescription
    """
    if 'Name' in obj:  # Rather than identifying each
                        # ProductDescription as such
        return ProductDescription(obj['Name'], obj['Image'])

def product_commands_to_file(commands, path):
    try:
        with open(path, 'w') as outfile:
            json.dump(commands, outfile, cls=ProductCommandEncoder)
    except FileNotFoundError:
        errors.file_not_found_error(path)


def product_descriptions_to_file(descriptions, path):
    try:
        with open(path, 'w') as outfile:
            json.dump(descriptions, outfile,
                            cls=ProductDescriptionEncoder)
    except FileNotFoundError:
        errors.file_not_found_error(path)

def product_commands_from_file(path):
    try:
        with open(path, 'r') as data_file:
            return json.load(data_file,
                             object_hook=parse_product_command)
    except FileNotFoundError:
        errors.file_not_found_error(path)

def product_descriptions_from_file(path):
    try:
        with open(path, 'r') as data_file:
            return json.load(data_file,
                             object_hook=parse_product_description)
    except FileNotFoundError:
        errors.file_not_found_error(path)

def string_from_text_file(path):
    try:
        with open(path, 'r') as textfile:
            return textfile.read()
    except FileNotFoundError:
        errors.file_not_found_error(path)

def string_to_file(out_string, path):
    with open(path, "w") as text_file:
        text_file.write(out_string)

def base_64_gif_from_web(url, file_suffix = ''):
    response = requests.get(url)
    temp_file_path = TEMP_GIF_PATH + str(file_suffix) + '.gif'
    img = Image.open(BytesIO(response.content))
    img.save(temp_file_path, 'gif')
    image_byt = open(temp_file_path, 'rb')
    image_b64 = base64.encodestring(image_byt.read())
    return image_b64.decode('ascii') # ascii string decode

def base_64_gif_to_file(img_data, path):
    img_bytes = bytes(img_data, 'utf-8')
    with open(path, 'wb') as f:
        f.write(base64.b64decode(img_bytes))
