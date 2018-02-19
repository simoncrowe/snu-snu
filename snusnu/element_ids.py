# General
AMAZON_UK_URL = 'https://www.amazon.co.uk'
AMAZON_US_URL = 'https://www.amazon.com'
NAV_LOGO_ID = 'nav-logo'

# Sign-in related:
SIGN_IN_XPATHS_UK =         ['//*[@id="nav-signin-tooltip"]/a',
                            '//*[@id="nav-link-yourAccount"]',
                            '//*[@id="a-autoid-0-announce"]',
                            '//*[@id="nav-flyout-ya-signin"]/a']
EMAIL_FIELD_XPATH_UK =      '//*[@id="ap_email"]'
PASSWORD_FIELD_XPATH_UK =   '//*[@id="ap_password"]'
SIGN_IN_BUTTON_XPATH_UK =   '//*[@id="signInSubmit"]'
SIGN_OUT_LINK_XPATH_UK =    '//*[@id="nav-item-signout"]'

# Search related:
CAT_DROPDOWN_XPATH = '//*[@id="searchDropdownBox"]'
SEARCH_FIELD_XPATH = '//*[@id="twotabsearchtextbox"]'
SEARCH_SUBMIT_XPATH = '//*[@id="nav-search"]/form/div[2]/div/input'

# Product-list related:
PRODUCT_PAGE_LINK_CLASS = 's-access-detail-page'
NEXT_PAGE_STRING_ID = 'pagnNextString'
NEXT_PAGE_LINK_ID = 'pagnNextLink'
NEXT_PAGE_ARROW_XPATH = '//*[@id="pagnNextLink"]/span[2]'

PREVIOUS_PAGE_STRING_ID = 'pagnPrevString'
PREVIOUS_PAGE_LINK_ID = 'pagnPrevLink'
PREVIOUS_PAGE_ARROW_XPATH = '//*[@id="pagnPrevLink"]/span[1]'
MORE_RESULTS_LINK_XPATH = '//*[@id="quartsPagelet"]/a'

# Product page related:
ADD_TO_LIST_BUTTON_ID = 'add-to-wishlist-button-submit'
ADD_WATCHLIST_BUTTON_XPATH = '//*[@id="dv-action-box"]/form/span/input'
SHOPPING_LIST_SELECT_ID = 'WLNEW_newsl_section'
WISH_LIST_SELECT_ID = 'WLNEW_newwl_section'
LIST_SELECTION_SUBMIT_ID = 'WLNEW_valid_submit'

# Wishlists related
WISHLISTS_LINK_ID = 'nav-link-wishlist'
WISHLISTS_MENU_LINK_XPATH = '//*[@id="nav-flyout-yourAccount"]/div[2]/a[3]'
WISHLISTS_SETTINGS_LINK_XPATH = '//*[@id="wishlist-page"]/ul/div/a[2]'
WISHLISTS_SHOPPING_DEFAULT_SELECT_XPATH = '//*[@id="g-manage-table-wishlist"]/tbody/tr[2]/td[2]/div/label'
WISHLISTS_SETTINGS_SUMBIT_BUTTON_XPATH = '//*[@id="g-manage-form"]/div[2]/span/span/span/input'

# Recommendation list related:
NAV_YOUR_AMAZON_ID = 'nav-your-amazon'
NAV_RECOMMENDED_FOR_YOU_XPATH = '//*[@id="nav-subnav"]/a[3]'
MENU_YOUR_RECOMMENDATIONS_XPATH = '//*[@id="nav-flyout-yourAccount"]/div[2]/a[4]'
PARTIAL_PRODUCT_NAME_XPATH = '//*[contains(@id,"ysProdLink")]'
PARTIAL_PRODUCT_IMAGE_XPATH = '//*[contains(@id,"ysProdImage")]'
PRICE_SPAN_CLASS = 'price'
MORE_RESULTS_BUTTON_ID = 'ysMoreResults'
MORE_RESULTS_LINK_XPATH = '//*[@id="main-body"]/table/tbody/tr/td[2]/div[1]/table[2]/tbody/tr[1]/td/table/tbody/tr/td[2]/span/a[2]'
PREVIOUS_RESULTS_BOTTON_ID = 'ysPrevResults'

