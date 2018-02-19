import re

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):    
    try:
        float(value)
        return True
    except ValueError:
        return False

def yes_no_input_prompt():
    while True:
        user_input = input('Enter Y or N...\n')
        if user_input.lower() == 'y':
            return True
        elif user_input.lower() == 'n':
            return False
        else:
            print('Input not recognised')

def int_input_prompt(message):
    value_set = False
    while not value_set:
        new_value = input(message)
        if is_int(new_value):
            return int(new_value)
        else:
            print('Please enter an integer.')
            
def keep_strings_matching(string_list, patterns):
    """ Takes a list of strings and a list of regex patterns.
        returns only those strings that match at least one regex"""
    regex_patterns = []
    for p in patterns:
        regex_patterns.append(re.compile(p))
    matched_strings = []
    for s in string_list:
        matched = False
        pattern_index = 0
        while not matched and pattern_index < len(regex_patterns):
            if regex_patterns[pattern_index].search(s) != None:
                matched_strings.append(s)
                matched = True
            pattern_index += 1
    return matched_strings

def output_command_arguments(arg_descriptions):
    print('These are the recognised command arguments:')
    print(' {0:10}{1}'.format('NAME', 'DESCRIPTION'))
    for a in arg_descriptions.keys():
        print(' {0:10}{1}'.format(a, arg_descriptions[a]['description']))
        print('   Required arguments:')
        print(arg_descriptions[a]['required args'] + '\n')
