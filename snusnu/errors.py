from snusnu.element_ids import *

def category_xpath_error():
    '''
    Informs user in command-line that stored Xpath doesn't match
    search category drop-down list element on page.
    Returns True if user chooses to continue with default category.
    '''
    error_message = ['Stored Xpath ']
    error_message.append(CAT_DROPDOWN_XPATH)
    error_message.append('does not match category dropdown box.')
    print(''.join(error_message))
    print('Category selection will not work until Xpath is updated ' +
                                            'to match page element.')
    undecided = True
    while undecided:
        user_choice = input('Enter Y below to continue with ' +
                            'default category or N to abort.\n')
        if user_choice  == 'n' or user_choice == 'N':
            print('Search aborted due to unmatching Xpath.')
            return False
        elif user_choice == 'y' or user_choice == 'Y':
            print('Continuing with default search category...')
            return True

def file_not_found_error(path):
    print('The file specified by path: ' + path + ' does not exist.')
    print('Quitting...')
    quit()
