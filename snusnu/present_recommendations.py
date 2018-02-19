import sys
import os

from snusnu.helpers import output_command_arguments
import snusnu.data as data

def make_html(product_descriptions, img_dir = 'img', number_of_columns = 4):
    """
    Outputs a html based on a JSON list of product descriptions.
    """
    html = []
    html.append('<!DOCTYPE html><html><head><meta charset="utf-8">')
    html.append('<style>body{font-family:sans-serif;' +
                'font-size:10px}td{vertical-align:top}' +
                'table, th, td {border: 1px solid #ccc} </style>')
    html.append('</head><body><table><tr>')
    column_count = 0
    pd = product_descriptions
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    for i in range(len(pd)):
        if column_count >= number_of_columns:
            html.append('</tr><tr>')
            column_count = 0
        html.append('<td><div><strong>' + pd[i].name + '</strong>')
        html.append('<br/>' + '</div></td><td>')
        image_path = img_dir + '/' + pd[i].name[0:5] + str(i) + '.gif'
        html.append('<img src="'+ image_path + '">' + '</td>')
        data.base_64_gif_to_file(pd[i].image, image_path)
        column_count += 1
    html.append('</tr></table></body></html>')
    return ''.join(html)

def make_html_file_terminal():
    descriptions = data.product_descriptions_from_file(sys.argv[2])
    html = make_html(descriptions)
    data.string_to_file(html, sys.argv[3])
    
def make_html_file(path_to_descriptions, path_to_html, cols=4, imgdir='img'):
    descriptions = data.product_descriptions_from_file(path_to_descriptions)
    html = make_html(descriptions, imgdir, cols)
    data.string_to_file(html, path_to_html)

# Dictionary of dictionaries defining command arguments accepted by snu-snu
ARGS = {'html':
   {'description':'Makes a HTML table for a JSON list of product descriptions',
    'required arg count' : 4,
    'required args' :
    '   1. the command (i.e. "html") 2. path to source file (e.g. "in.json")'
    + '\n   3. path to destination file (eg. "out.html")',
    'function' : make_html_file_terminal}}

def initialise():
    """
    Checks arguments and calls appropriate functions.
    """
    print("""This is textpresent-recommendation: a utility for generating
user-friendly output from JSON lists of ProductDescriptons.\n""")

    proceed_with_args = False
    if len(sys.argv) > 1:
        includes_recognised_arg = False
        for recognised_arg in ARGS.keys():
            if sys.argv[1] == recognised_arg:
                includes_recognised_arg = True
        if includes_recognised_arg:
            print('You ran present-recommendations with the command argument: '
                                                        + sys.argv[1])
            print('This ' + ARGS[sys.argv[1]]['description'])
            if len(sys.argv) == ARGS[sys.argv[1]]['required arg count']:
                proceed_with_args = True
            else:
                error = ['Error: this command will only work with a total of ']
                error.append(str(ARGS[sys.argv[1]]['required arg count'] - 1))
                error.append(' arguments.')
                print(''.join(error))
                print('See "' + sys.argv[1] + '" in the below list...\n')
                output_command_arguments(ARGS)
        else:
            print('Command argument "' + sys.argv[1] + '" not recognised\n')
            output_command_arguments(ARGS)
    else:
        print('Error: present-recommendations requires terminal arguments '
                                                            +  'to run.\n')
        output_command_arguments(ARGS)
    if proceed_with_args:
        ARGS[sys.argv[1]]['function']()
    else:
        print('Please quit...')

initialise()
