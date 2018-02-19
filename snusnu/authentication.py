from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from snusnu.element_ids import *

IMPLICIT_WAIT = 3; # seconds for the driver to wait for elements to load
# elements ids used on Amazon.co.uk home page that link to sign-in page

def sign_in(drv, username, password, amazon_url = AMAZON_UK_URL):
    drv.implicitly_wait(IMPLICIT_WAIT)
    drv.get(amazon_url)
    print(drv.page_source)
    already_signed_in = True
    try:
        sign_out_link = drv.find_element_by_xpath(SIGN_OUT_LINK_XPATH_UK)
        print('Your drv appears to be signed in already.')
        print('Signing out...')
        drv.get(str(sign_out_link.get_attribute('href')))
    except NoSuchElementException:
        already_signed_in = False

    if not already_signed_in:
        # attempt to locate an element that links to the sign-in page
        for i  in range(len(SIGN_IN_XPATHS_UK)):
            try:
                print('Trying sign-in link ' + str(i) + '...')
                sign_in_link = drv.find_element_by_xpath(
                                                SIGN_IN_XPATHS_UK[i])
                if sign_in_link.is_displayed() :
                    sign_in_link.click()
                else:
                    #print(sign_in_link.get_attribute('href'))
                    drv.get(str(sign_in_link.get_attribute('href')))
                print('Sign-in link ' + str(i) + ' works!')
                break
            except NoSuchElementException:
                error_message = ['Sign-in link ']
                error_message.append(str(i))
                error_message.append(' (identified by Xpath "')
                error_message.append(str(SIGN_IN_XPATHS_UK[i]))
                error_message.append('") not found on homepage.')
                print(''.join(error_message))
                if len(SIGN_IN_XPATHS_UK) == i + 1:
                    error_message = ['All sign-in links failed! \n']
                    error_message.append('This script will not function ')
                    error_message.append('until its Xpath list matches ')
                    error_message.append('the current Amazon homepage.')
                    print(''.join(error_message))
                    print(drv.page_source)
                    return False

    print('Attempting to sign in...')
    # locate sign-in elements
    try:
        email_field = drv.find_element_by_xpath(EMAIL_FIELD_XPATH_UK)
        password_field = drv.find_element_by_xpath(PASSWORD_FIELD_XPATH_UK)
    except NoSuchElementException:
        print("Unable to locate email/password fields!"
            + " Stored Xpaths do not match webpage.")
        print("This script will not function "
            + "until its Xpaths match the Amazon login page.")
        print(drv.page_source)
        return False

    # submit authentification information
    email_field.send_keys(username)
    password_field.send_keys(password)
    try:
        sign_in_button = drv.find_element_by_xpath(SIGN_IN_BUTTON_XPATH_UK)
        print('Loading home page...')
        sign_in_button.click()
    except NoSuchElementException:
        print('Loading home page...')
        password_field.send_keys(Keys.ENTER)

    # Try to get array containing sign-out menu item.
    # Array should be empty if sign-in unsuccesful.
    if len(drv.find_elements_by_xpath(SIGN_OUT_LINK_XPATH_UK)) > 0 :
        print('Sign in succesful!\n')
        return True
    else :
        print('Failed to sign in. Check username and password.')
        print(drv.page_source)
        return False
