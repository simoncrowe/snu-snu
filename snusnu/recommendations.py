import json

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

from snusnu.element_ids import *
from snusnu.helpers import keep_strings_matching
import snusnu.data as data
import snusnu.authentication as authentication


def get_recommendations_json(driver,
                            number_of_recommendations,
                            base64_images = False):
    """ Wrapper for get_recommendations that returns JSON"""
    recommendations = get_recommendations(driver,
                                          number_of_recommendations,
                                          base64_images)
    json_recommendations = []
    for r in recommendations:
        json_recommendations.append(json.dumps(r, 
                        cls=data.ProductDescriptionEncoder))
    return json_recommendations


def get_recommendations(drv,
                        number_of_recommendations,
                        base64_images= False):
    """ Assumes Amazon user is authenticated.
        Gets a specified number of recommendations """
    print('Navigating to recommendations...')
    # First phase of navigating to recommendations
    successful = False
    try:
        your_amazon_button = drv.find_element_by_id(NAV_YOUR_AMAZON_ID)
        your_amazon_button.click()
        successful = True
    except ElementNotVisibleException:
        print('Error: element used to navigate to "your Amazon" not visible.')
    except NoSuchElementException:
        print('Error: element used to navigate to "your Amazon" not found.')
    if not successful:
        try:
            recommendations_link = drv.find_element_by_xpath(
                                            MENU_YOUR_RECOMMENDATIONS_XPATH)
            drv.get(str(recommendations_link.get_attribute('href')))
            successful = True
        except ElementNotVisibleException:
            print('Error: element linking to "your Amazon" not visible.')
        except NoSuchElementException:
            print('Error: element linking to "your Amazon" not found.')
    if not successful:
        print('Failure: cannot navigate to "your Amazon". Check element ids.')
        return [] # empty list
    # Second phase of navigating to recommendations
    successful = False
    try:
        recommendations_link = drv.find_element_by_xpath(
                                                NAV_RECOMMENDED_FOR_YOU_XPATH)
        recommendations_link.click()
        successful = True
    except ElementNotVisibleException:
        print('Error: element linking to recommendations not visible.')
        print('Trying to follow the link directly...')
        try:
            drv.get(str(recommendations_link.get_attribute('href')))
            sucessful = True
        except:
            print('Error: failed to follow link to recommendations')
    except NoSuchElementException:
        print('Error: element used to navigate to recommendations'
        + 'not found.')
    if not successful:
        print("Failure: can't navigate to recommendations. Check element ids.")
        return [] # empty list

    # Scrape the recommendations
    scraped_names = []
    scraped_images = []
    recommendations_scraped = 0
    failed_scraping = False
                             # precautionary "buffer-zone" of 20 v
    while (recommendations_scraped < (number_of_recommendations + 20)
            and not failed_scraping):
        names = drv.find_elements_by_xpath(PARTIAL_PRODUCT_NAME_XPATH)
        print ('Selenium found ', 
                str(len(names)), 
                ' product name elements')
        names_text = []
        for n in names:
            names_text.append(n.get_attribute('innerHTML'))
        names_text_stripped = []
        i = 0
        for n in names_text:
            print('Product '  + str(i) + ' name: ' + n)
            name = n.replace('<strong>', '')
            name = name.replace('</strong>', '')
            name = name.replace('&amp;','&')
            names_text_stripped.append(name)
            print('Stripping HTML...\n' + name)
            i += 1
        images = drv.find_elements_by_xpath(PARTIAL_PRODUCT_IMAGE_XPATH)
        image_urls = []
        for i in images:
            image_urls.append(i.get_attribute('src'))
        image_data = []

        if base64_images:
            i = 0
            for u in image_urls:
                image_data.append(data.base_64_gif_from_web(u))
                image_message = ['Base64 encoded GIF of image for ']
                image_message.append(names_text_stripped[i])
                image_message.append('\n')
                image_message.append(image_data[i][0:220])
                image_message.append('...')
                print(''.join(image_message))
                i += 1
        else:
            image_data = image_urls

        print ('Selenium found ' + str(len(images))
            +' product image elements')
        for n in names_text_stripped:
            scraped_names.append(n)
        for i in image_data:
            scraped_images.append(i)
        recommendations_scraped += len(names)
        # Navigate to next page of recommendations
        successful = False
        try:
            more_results_button = drv.find_element_by_id(
            MORE_RESULTS_BUTTON_ID)
            more_results_button.click()
            successful = True
        except WebDriverException:
            print('Possible error clicking more results button. '
                    + ' Trying parent element...')
        if not successful:
            try:
                more_results_button = drv.find_element_by_id(
                    MORE_RESULTS_BUTTON_ID)
                link = more_results_button.find_element_by_xpath('..')
                link.click()
                successful = True
            except WebDriverException:
                try:
                    print('Possible error finding "more results" link. '
                            + 'Trying alternative xpath...')
                    more_results_link = drv.find_element_by_xpath(
                        MORE_RESULTS_LINK_XPATH)
                    more_results_link.click()
                    successful = True
                except WebDriverException:
                    print('Error clicking element based on alternative',
                          'xpath')
        if not successful:
            print('Failed to get recommendations!') # <<< REVISIT THIS
            failed_scraping = True

    recommended_products = []
    for i in range(number_of_recommendations):
        recommended_products.append(data.ProductDescription(
                                        scraped_names[i],
                                        scraped_images[i]))
    return recommended_products
