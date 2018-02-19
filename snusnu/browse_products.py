#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException

import snusnu.authentication as authentication
from snusnu.element_ids import *
from snusnu.helpers import is_int
from snusnu.errors import category_xpath_error

IMPLICIT_WAIT = 3; # seconds for the driver to wait for elements to load

# Controls whether set_shopping_list_default_product_view is called
DEFAULT_WISHLIST_SET = False

def get_product_link(product_element):
    """Returns the link element inside a product listing element"""
    try:
        return product_element.find_element_by_class_name(
                                                PRODUCT_PAGE_LINK_CLASS)
    except NoSuchElementException:
        print('Unable to find product page link. Skipping item.')
        return None

def go_home(drv):
    try:
        logo_link = drv.find_element_by_id(NAV_LOGO_ID)
        logo_link.click()
    except NoSuchElementException:
        drv.get(AMAZON_UK_URL)

def search( drv, 
            search_term, 
            category_index = 0, 
            amazon_url = AMAZON_UK_URL
           ):
    '''
    Initiates a search in the main Amazon search field, with an optional
    argument specifiying a product category.
    Returns True if successful.
    '''

    drv.get(amazon_url)
    
    print('Searching for "', search_term, '"...')
    use_custom_category = False
    if not category_index == 0:
        use_custom_category = True
        try:
            cat_select = Select(drv.find_element_by_xpath(
                                        CAT_DROPDOWN_XPATH))
            cat_select.select_by_index(category_index)
        except NoSuchElementException:
            #if category_xpath_error():
            # ^ depricated as this assumes a terminal interface
            use_custom_category = False
    try:
        search_field = drv.find_element_by_xpath(SEARCH_FIELD_XPATH)
    except NoSuchElementException:
        print('Stored Xpath does not match search text box'
                +' element on page.')
        print('Aborting search...')
        return False
    search_field.send_keys(search_term)
    try:
        submit_button = drv.find_element_by_xpath(SEARCH_SUBMIT_XPATH)
        submit_button.click()
    except NoSuchElementException:
        search_field.send_keys(keys.ENTER)
    except NullPointerException:
        print('Search failed due to NullPointerException. Aborting...')
        return False
    except:
        print('Search failed. Unknown error. Aborting...')
        return False
    return True

def get_category_names(drv):
    '''
    Returns a list of string corresponding to Amazon's category select.
    '''
    drv.get(AMAZON_UK_URL)
    cat_select = Select(drv.find_element_by_xpath(
                                                CAT_DROPDOWN_XPATH))
    cat_options = cat_select.options
    category_names = []
    for i in range(len(cat_options)):
        category_names.append(
            cat_options[i].get_attribute('innerHTML').replace('&amp;','&'))
    return category_names

def choose_category(drv):
    '''
    Provides a command-line interface for choosing a category from
    Amazon's drop-down list. Returns the index of the chosen category.
    '''
    cat_index = 0
    cat_unselected = True
    while cat_unselected:
        cat_names = get_category_names(drv)
        print('Select from the following search categories:\n')
        print(' {0:7}{1}'.format('INDEX', 'NAME'))
        #print(' {0:7}{1}'.format('`````', '````'))
        for i in range(len(cat_names)):
            cat_option_text = [' {:7}'.format(str(i))]
            cat_option_text.append(cat_names[i])
            print(''.join(cat_option_text))
        print('\nEnter the index of the category you wish to search.')
        user_input = input()
        if is_int(user_input) and 0<=int(user_input)<=(len(cat_names)-1):
            cat_index = int(user_input)
            selected_cat_name = cat_names[cat_index]
            cat_unselected = False
        else:
            print('Invalid category index!')
            print('Please enter a number between 0 and '
                                + str(len(cat_names)-1))
    return cat_index

def view_items( drv, 
                search_string, 
                number_products, 
                category,
                item_function = None,
                amazon_url = AMAZON_UK_URL):
    drv.implicitly_wait(IMPLICIT_WAIT)
    search(drv, search_string, category, amazon_url)
    drv.set_page_load_timeout(30)
    current_result = 0
    products_viewed_count = 0
    item_function_success_count = 0
    completed = False
    starting_next_page = False
    # The entire product-viewing process is wrapped in a try clause.
    # This is to prevent the webdriver hangining, particularly for RARS.
    #try:
    # seeing if there are any results
    try:
        drv.find_element_by_id('result_0')
    except:
        print('No products found. Aborting...')
        return {'products viewed'    :  products_viewed_count,
            'function success count' :  item_function_success_count}
    while not completed:
        product_elements = [] # Setting empty in case of error
        try:
            product_elements = drv.find_elements_by_id(
                                'result_' + str(current_result))
        except TimeOutException:
            print('WebDriver timed out.', 
                  'Could not find next product listing')
        except StaleElementReferenceException:
            print('WebDriver found stale reference to product.',
                  'Skipping...')
        except WebDriverException:
            print('Unknown error. Skipping product listing...')
        # Is there a product element
        # matching the desired on the page?
        if len(product_elements) > 0:
            product_page_url = drv.current_url
            if starting_next_page:
                starting_next_page = False
            try:
                product_link = get_product_link(product_elements[0])
                product_loaded = False 
                if not product_link == None:
                    try:
                        print('Viewing product ' +
                             str(current_result) + '...')
                        product_link.click()
                        product_loaded = True
                        products_viewed_count += 1
                    except:
                        print('Could not click product element. ' +
                                        ' Manually getting link.')
                        try:
                            drv.get(product_link.get_attribute(
                                                            'href'))
                            product_loaded = True
                            products_viewed_count += 1
                        except:
                            print('Could not manually' +
                                  'get link to product!')
                            
                    # If present, a function is called
                    # to do something on the product page
                    if product_loaded and item_function != None:
                        function_successful = item_function(drv)
                        if function_successful:
                            item_function_success_count += 1
                    # Ensure that driver returns to the results page
                    # (possibly more robust than drv.back())
                    while not drv.current_url ==  product_page_url:
                        drv.get(product_page_url)
            except TimeoutException:
                print('Item page timed out.' +
                        'Returning to product page...')
                drv.get(product_page_url)
            current_result += 1
        elif starting_next_page :
            print('No products found on mostrecent page. '
                + ' Ending search...')
            completed = True
        else:
            next_page_links = drv.find_elements_by_id(
                                                NEXT_PAGE_LINK_ID)
            if len(next_page_links) > 0:
                successful = False
                try:
                    next_page_text = drv.find_element_by_id(
                                                NEXT_PAGE_STRING_ID)
                    next_page_text.click()
                    successful = True
                except NoSuchElementException:
                    print('Error: next page link not found.')
                except ElementNotVisibleException:
                    print('Error: next page link not visible.')
                except WebDriverException:
                    print('Unknown error in navigating to next'+
                          'result page.')
                if not successful:
                    try:
                        next_page_arrow = drv.find_element_by_xpath(
                                            NEXT_PAGE_ARROW_XPATH)
                        next_page_arrow.click()
                        successful = True
                    except NoSuchElementException:
                        print('Error: next page arrow not found.')
                    except ElementNotVisibleException:
                        print('Error: next page arrow not visible.')
                    except WebDriverException:
                        print('Unknown error in navigating to next'+
                                                    ' result page.')
                if not successful:
                    try:
                        drv.get(next_page_links[0].get_attribute(
                                                            'href'))
                        successful = True
                    except WebDriverException:
                        print('Error: failed to navigate to next '
                                                    + 'result page')
                if not successful:
                    end_string = ['End of results reached']
                    end_string.append(" for search ")
                    end_string.append(search_string)
                    end_string.append('". Only ')
                    end_string.append(str(current_result - 1))
                    end_string.append(' of the specified ')
                    end_string.append(str(number_products))
                    end_string.append(' products viewed.')
                    print(''.join(end_string))
                    completed = True
                else:
                    starting_next_page = True
            else:
                end_string = ['End of results reached']
                end_string.append(" for search ")
                end_string.append(search_string)
                end_string.append('". Only ')
                end_string.append(str(current_result - 1))
                end_string.append(' of the specified ')
                end_string.append(str(number_products))
                end_string.append(' products viewed.')
                print(''.join(end_string))
                completed = True
                    
        if products_viewed_count == number_products:
            completed = True
    #except:
        #print('Unknown error! Aborting...')
    #finally:
    return {'products viewed'       :   products_viewed_count,
                'function success count':   item_function_success_count}

def set_shopping_list_default_product_view(drv):
    # Trying to select the shopping list
    print('Attempting to set default wishlist to "shopping list"...')
    try:
        shopping_list_select = drv.find_element_by_id(
                                SHOPPING_LIST_SELECT_ID)
        shopping_list_select.click()
    except NoSuchElementException:
        print('Failed to select "shopping list". No button on page '
                                + 'found m atching stored element id.')
    except ElementNotVisibleException:
        print('Failed to select "shopping list". '
                + 'List add button is not visible.')
    # Trying to submit selection
    try:
        list_submit = drv.find_element_by_id(LIST_SELECTION_SUBMIT_ID)
        list_submit.click()
    except NoSuchElementException:
        print('Failed to find "list selection submit". No button on '
                            + 'page found matching stored element id.')
    except ElementNotVisibleException:
        print('Failed to click "list selection submit". '
                            + 'Button is not visible.')
    global DEFAULT_WISHLIST_SET
    DEFAULT_WISHLIST_SET = True

def add_item_list(drv):
    """
    Assumes driver is on a product page. Adds the product to 
    the shopping list.
    """
    try:
        print('Attempting to add product to "shopping list"...')
        list_add_button = drv.find_element_by_id(ADD_TO_LIST_BUTTON_ID)
        list_add_button.click()
        global DEFAULT_WISHLIST_SET
        if not DEFAULT_WISHLIST_SET:
            set_shopping_list_default_product_view(drv)
        print('Sucessful.')
        return True
    except NoSuchElementException:
        print('Failed to add item to list. No button on page found '
                                + 'matching stored element ids.')
    except ElementNotVisibleException:
        print('Failed to add item to list. '
                + 'List add button is not visible.')
    except WebDriverException:
        print('Unknown error. Failed to add item to wishlist.')
        
    try:
        print('Attempting to add video to "watchlist"...')
        list_add_button = drv.find_element_by_xpath(
                        ADD_WATCHLIST_BUTTON_XPATH)
        list_add_button.click()
        print('Successful.')
        return True
    except NoSuchElementException:
        print('Failed to add video to list. No button on page found '
                                + 'matching stored element ids.')
    except ElementNotVisibleException:
        print('Failed to add video to list. '
                + 'List add button is not visible.')
    except WebDriverException:
        print('Unknown error. Failed to add video to watchlist.')
        
    return False
