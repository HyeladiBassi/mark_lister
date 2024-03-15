import os
import sys
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options

class Lister:
    # Constants for URLs and indices
    POSHMARK_LOGIN_URL = "https://poshmark.com/login"
    POSHMARK_LOGIN_SUCCESS_URL = "https://poshmark.com/feed?login=true"
    POSHMARK_HOME_URL = "https://poshmark.com"
    POSHMARK_CREATE_LISTING_URL = "https://poshmark.com/create-listing"
    CATEGORY_DELIMITER = '>'

    PRICE_INDEX = 0
    LISTING_ID_INDEX = 1
    BRAND_INDEX = 2
    TITLE_INDEX = 3
    COLOR_INDEX = 4
    MATERIAL_INDEX = 5
    DESC_TITLE_INDEX = 6
    CM_ADDL_SIZING_INFO_INDEX = 7
    INCH_ADDL_SIZING_INFO_INDEX = 8
    ACCESSORY_INDEX = 9
    SERIAL_NUMBER_INDEX = 10
    EXTERIOR_INDEX = 11
    INSIDE_INDEX = 12
    POCKETS_INDEX = 13
    CORNERS_INDEX = 14
    POLICY_INDEX = 15
    STYLE_INDEX = 16
    CATEGORY_PATH_INDEX = 17
    LISTED_STATUS_INDEX = 18
    

    LOGIN_NAME_INPUT_XPATH = "//input[@name='login_form[username_email]']"
    LOGIN_PASSWORD_INPUT_XPATH = "//input[@name='login_form[password]']"
    LOGIN_SUBMIT_XPATH = "//button[@type='submit']"

    LISTING_PHOTO_INPUT_XPATH = "//*[@class='listing-editor__input-img-files']"
    APPLY_PHOTO_BUTTON_XPATH = "//button[@data-et-name='apply']"
    APPLY_PHOTO_BUTTON_CSS = "div.modal__footer:nth-child(2) > div:nth-child(1) > button:nth-child(2)"

    LISTING_TITLE_XPATH = "//input[@data-vv-name='title']"
    LISTING_DESCRIPTION_XPATH = "//textarea[@class='form__text form__text--input listing-editor__description__input p--3']"
    
    CATEGORY_DROPDOWN_XPATH = "//div[@class='dropdown__selector dropdown__selector--select-tag dropdown__selector--select-tag--large ellipses']"
    EXPANDED_DROPDOWN_XPATH = "//div[@class='width--100 dropdown__menu dropdown__menu--expanded ws--nowrap']"
    EXPANDED_DROPDOWN_SELECTOR = ".dropdown__menu--expanded"
    SUBCATEGORY_DROPDOWN_XPATH = "//div[@class='dropdown__selector dropdown__selector--select-tag dropdown__selector--select-tag--large']"
    SUB_EXPANDED_DROPDOWN_XPATH = "//div[@class='dropdown__menu dropdown__menu--top dropdown__menu--expanded']"
    SUB_EXPANDED_DROPDOWN_SELECTOR = ".dropdown__menu--expanded"

    SIZE_DROPDOWN_XPATH = "//div[@data-test='size']"
    SIZE_CHART_XPATH = "//div[@class='p--3']"

    NO_NEW_TAGS_BUTTON_XPATH = "//button[@class='btn listing-editor__condition-btn btn--tertiary']"
    YES_NEW_TAGS_BUTTON_XPATH = "//button[@class='btn listing-editor__condition-btn m--r--3 btn--tertiary']"

    BRAND_INPUT_XPATH = "//input[contains(@placeholder, 'Enter the Brand/Designer')]"

    COLOR_DROPDOWN_XPATH = "//div[@class='dropdown__selector dropdown__selector--select-tag dropdown__selector--select-tag--large listing-editor__input--half']"
    COLOR_CHOICES_EXPANDED_XPATH = "//div[@class='p--3 dropdown__menu dropdown__menu--dark dropdown__menu--top dropdown__menu--expanded']"

    STYLE_TAG_DROPDOWN_XPATH = "//input[@data-vv-name='style-tag-input']"
    TAG_CHOICES_EXPANDED_XPATH = "//ul[@class='dropdown__menu dropdown__menu--expanded type-ahead__list listing-editor__suggestions-list width--100']"

    ORIGINAL_PRICE_INPUT_XPATH = "//input[@data-vv-name='originalPrice']"
    NEW_LISITING_PRICE_XPATH = "//input[@data-vv-name='listingPrice']"

    NEXT_BUTTON_XPATH = "//button[@data-et-name='next']"

    def __init__(self, listing_csv_path, allow_manual_photo_adjustment, auto_run):
        self.listing_csv_path = listing_csv_path
        self.allow_manual_photo_adjustment = allow_manual_photo_adjustment
        self.auto_run = auto_run
        self.driver = None
        self.raw_listings = []

        self._run_setup()

    def _set_driver(self):
        """Create Driver and add user data directory"""
        print("Setting driver...")
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        print("Driver set!")

    def _visit_poshmark(self):
        self.driver.get(self.POSHMARK_LOGIN_URL)

    def _visit_create_listing(self):
        self.driver.get(self.POSHMARK_CREATE_LISTING_URL)
        time.sleep(3)

    def _login_user(self):
        print("Logging in user...")
        username = ''
        pw = ''

        wait = WebDriverWait(self.driver, 20)
        username_input = wait.until(ec.visibility_of_element_located((By.XPATH, self.LOGIN_NAME_INPUT_XPATH)))
        username_input.send_keys(username)

        pw_element = self.driver.find_element(By.XPATH, self.LOGIN_PASSWORD_INPUT_XPATH)
        pw_element.send_keys(pw)

        submit_button = self.driver.find_element(By.XPATH, self.LOGIN_SUBMIT_XPATH)
        self.driver.execute_script("arguments[0].click();", submit_button)

        try:
            wait = WebDriverWait(self.driver, 40)
            wait.until(ec.url_to_be(self.POSHMARK_LOGIN_SUCCESS_URL))
            print("User successfully logged in!")

        except TimeoutException: 
            
            user_input = input("Solve captcha")
            
    def _run_setup(self):
        print("Running setup...")
        self._set_driver()

        self._visit_poshmark()

        self._login_user()
        print("Setup complete!")
    
    def _enter_listing_title(self, listing_title):
        listing_title_input = self.driver.find_element(By.XPATH, self.LISTING_TITLE_XPATH)
        listing_title_input.send_keys(listing_title)
    
    def _enter_listing_description(self, listing_description_title, listing_accessory, listing_serial_number, listing_exterior, listing_inside, listing_pockets, listing_policy, listing_material, listing_style, cm_addl_sizing_info, inch_addl_sizing_info, listing_corners):
        description_input = self.driver.find_element(By.XPATH, self.LISTING_DESCRIPTION_XPATH)

        full_description = ''

        if listing_description_title:
            full_description += ('\n' + f"{listing_description_title}")

        if cm_addl_sizing_info:
            full_description += ('\n' + '\n' + f"Sizing Info (cm): {cm_addl_sizing_info}")

        if inch_addl_sizing_info:
            full_description += ('\n' + f"Sizing Info (inch): {inch_addl_sizing_info}")

        if listing_accessory:
            full_description += ('\n' + '\n' + f"Accessories: {listing_accessory}")

        if listing_serial_number:
            full_description += ('\n' + '\n' + f"Serial Number: {listing_serial_number}")

        if listing_material:
            full_description += ('\n' + '\n' + f"Material / Blend: {listing_material}")

        if listing_exterior:
            full_description += ('\n' + '\n' + f"Exterior: {listing_exterior}")

        if listing_inside:
            full_description += ('\n' + '\n' + f"Inside: {listing_inside}")

        if listing_pockets:
            full_description += ('\n' + '\n' + f"Pockets: {listing_pockets}")

        if listing_corners:
            full_description += ('\n' + '\n' + f"Corners: {listing_corners}")

        if listing_policy:
            full_description += ('\n' + '\n' + f"Policy: {listing_policy}")

        description_input.send_keys(full_description)

    def _send_text_to_element(self, element_identifier_string, element_xpath, text_to_send):
        try:
            found_element = self.driver.find_element(By.XPATH, element_xpath)
            found_element.send_keys(text_to_send)

        except NoSuchElementException:
            print(f"'NoSuchElementException' raised when trying to find {element_identifier_string} element!")
            raise NoSuchElementException

    def _enter_prices(self, original_price, listing_price):
        self._send_text_to_element("listing_original_price", self.ORIGINAL_PRICE_INPUT_XPATH, original_price)
        self._send_text_to_element("listing_listed_price", self.NEW_LISITING_PRICE_XPATH, listing_price)
     
    def _enter_size(self, listing_size_text):
        size_dropdown = self.driver.find_element(By.XPATH, self.SIZE_DROPDOWN_XPATH)
        self.driver.execute_script("arguments[0].click();", size_dropdown)

        wait = WebDriverWait(self.driver, 10)
        size_chart = wait.until(ec.visibility_of_element_located((By.XPATH, self.SIZE_CHART_XPATH)))

        print(f"Listing size text: {listing_size_text}")

        matched_listing_size = size_chart.find_element(By.XPATH, f".//button[contains(text(), '{listing_size_text}')]")
        self.driver.execute_script("arguments[0].click();", matched_listing_size)
    
    def _click_next_button(self):
        next_button_element = self.driver.find_element(By.XPATH, self.NEXT_BUTTON_XPATH)
        self.driver.execute_script("arguments[0].click();", next_button_element)

    def _match_item_in_dropdown(self, expanded_dropdown_selector, text_to_match):
        wait = WebDriverWait(self.driver, 5)
        expanded_menu = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, expanded_dropdown_selector)))

        list_items_of_menu = expanded_menu.find_elements(By.XPATH, ".//li")
        list_items_text = [item.text for item in list_items_of_menu]

        match_index = list_items_text.index(text_to_match)

        parent_element_to_click = list_items_of_menu[match_index]

        try:
            element_to_click = parent_element_to_click.find_element(By.XPATH, ".//a")

        except NoSuchElementException:
            element_to_click = parent_element_to_click

        self.driver.execute_script("arguments[0].click();", element_to_click)

    def _click_dropdown_and_match_item(self, initial_dropdown_xpath, expanded_dropdown_selector, text_to_match):
        dropdown_button = self.driver.find_element(By.XPATH, initial_dropdown_xpath)
        self.driver.execute_script("arguments[0].click();", dropdown_button)

        self._match_item_in_dropdown(expanded_dropdown_selector, text_to_match)

    def _enter_category(self, listing_category_path):
        category_split = listing_category_path.split(self.CATEGORY_DELIMITER)
        categories = [cat.strip() for cat in category_split]

        #Select First Category
        print("Looking for first category...")
        first_category = categories[0]
        initial_dropdown_xpath = self.CATEGORY_DROPDOWN_XPATH
        expanded_dropdown_xpath = self.EXPANDED_DROPDOWN_SELECTOR
        self._click_dropdown_and_match_item(initial_dropdown_xpath, expanded_dropdown_xpath, first_category)
        print("First category found!")

        #Select Second Category
        print("Looking for second category...")
        second_category = categories[1]
        self._match_item_in_dropdown(expanded_dropdown_xpath, second_category)
        print("Second category found!")

    def _enter_brand(self, listing_brand):
        brand_input_element  = self.driver.find_element(By.XPATH, self.BRAND_INPUT_XPATH)
        brand_input_element.send_keys(listing_brand)


    def _select_color_from_dropdown(self, color_dropdown_element, color_text):
        """Component/utility method of '_enter_color()'"""
        color_text = str.title(color_text)
        print(f"Looking for color: {color_text} in color dropdown...")
        color_dict = {
            'Red' : 0,
            'Pink' : 1,
            'Orange' : 2,
            'Yellow' : 3,
            'Green' : 4,
            'Blue' : 5,
            'Purple' : 6,
            'Gold' : 7,
            'Silver' : 8,
            'Black' : 9,
            'Gray' : 10,
            'White' : 11,
            'Cream' : 12,
            'Brown' : 13,
            'Tan' : 14
        }

        try:
            translated_element_index_from_color = color_dict[color_text]
            print(f"Index retrieved for color {color_text} --> {translated_element_index_from_color}.")

        except KeyError:
            print(f"Color not matched in internal dicitionary: {color_text}!")
            sys.exit(0)

        print("Searching for expanded color choices table...")
        wait = WebDriverWait(self.driver, 5)
        color_choices_expanded = wait.until(ec.visibility_of_element_located((By.XPATH, self.COLOR_CHOICES_EXPANDED_XPATH)))
        print("Expanded color choices dropdown found!")

        print("Selecting color...")
        all_colors = color_choices_expanded.find_elements(By.XPATH, ".//li[@class='listing-editor__tile--color d--if ja--c fd--c p--2 va--t']")
        color_choice = all_colors[translated_element_index_from_color]
        self.driver.execute_script("arguments[0].click();", color_choice)
        print("Color selected!")

    def _click_color_done_button(self):
        done_button = self.driver.find_element(By.CSS_SELECTOR, "div.form__actions:nth-child(2) > button:nth-child(1)")
        self.driver.execute_script("arguments[0].click();", done_button)

    def _enter_color(self, color_string):
        print("Looking for color dropdown...")
        color_dropdown_element = self.driver.find_element(By.XPATH, self.COLOR_DROPDOWN_XPATH)
        self.driver.execute_script("arguments[0].click();", color_dropdown_element)
        print("Color dropdown found and clicked!")

        split_colors = color_string.split(';')
        
        for color in split_colors:
            self._select_color_from_dropdown(color_dropdown_element, color)

        #Click 'Done' button
        self._click_color_done_button()

    @staticmethod
    def _file_name_is_jpeg(file_name):
        accept_extensions = ['.jpeg', '.JPEG', '.jpg', '.JPG', '.png', '.PNG']

        for ext in accept_extensions:
            if ext in file_name:
                return True

        return False

    def list_all_photos_in_folder(self, folder_path):
        photo_names = os.listdir(folder_path)
        photo_names = [name for name in photo_names if self._file_name_is_jpeg(name)]
        assert len(photo_names) > 0, f"No photos found in {folder_path}"
        assert len(photo_names) < 17, f"Too many photos found in following path: {folder_path}. Limit is 16 photos!"
        return photo_names
        
    def _list_first_photo(self, photo_index, photo_path):
        photo_box_element = self.driver.find_element(By.XPATH, self.LISTING_PHOTO_INPUT_XPATH)
        photo_box_element.send_keys(photo_path)

        wait = WebDriverWait(self.driver, 15)
        apply_button = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, self.APPLY_PHOTO_BUTTON_CSS)))
        apply_button.click()
        print("First photo added.")
        print("'Apply' button clicked!")

    def _list_other_photo(self, photo_index, photo_path):
        first_photo_array_indices = [n for n in range(1,9)]
        second_photo_array_indices = [n for n in range(9,17)]

        if photo_index in first_photo_array_indices:
            index_offset = 1
            wait = WebDriverWait(self.driver, 10)
            first_array_element = wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#imagePlaceholder > div > div > label > div.col-x16'))) 
            image_placeholders = first_array_element.find_elements(By.XPATH, ".//div[@class='col-x6']")

            placeholder = image_placeholders[photo_index - index_offset]

            placeholder_droppable = placeholder.find_element(By.XPATH, ".//input[@class='listing-editor__file-list']")

            placeholder_droppable.send_keys(photo_path)

        elif photo_index in second_photo_array_indices:
            index_offset = 9
            second_array_element = self.driver.find_element(By.CSS_SELECTOR, "#imagePlaceholder > div > div > label > div.col-x24")
            image_placeholders = second_array_element.find_elements(By.XPATH, ".//div[@class='col-x4']")

            placeholder = image_placeholders[photo_index - index_offset]

            placeholder_droppable = placeholder.find_element(By.XPATH, ".//input[@class='listing-editor__file-list']")

            placeholder_droppable.send_keys(photo_path)

        else:
            print("Error in call to '_list_other_photo'. Photo index not recognized properly!")
            sys.exit(0)

    def _send_photo_to_box_element(self, photo_index, photo_path):
        if photo_index == 0:
            self._list_first_photo(photo_index, photo_path)

        else:
            self._list_other_photo(photo_index, photo_path)

    def _enter_listing_photos(self, listing_photos_path):
        #Get photos for listing from photo_path folder
        listing_photos_path = listing_photos_path + '/'
        photos_in_folder = self.list_all_photos_in_folder(listing_photos_path)
        photo_paths = [listing_photos_path + photo_name for photo_name in photos_in_folder]

        #Upload photos
        wait = WebDriverWait(self.driver, 15)
        photo_input_box = wait.until(ec.presence_of_element_located((By.XPATH, self.LISTING_PHOTO_INPUT_XPATH)))
        print("Photo input box found!")

        for photo_count, photo_path in enumerate(photo_paths):
            print(photo_path)
            self._send_photo_to_box_element(photo_count, photo_path)

    def _list_item(self):
        wait = WebDriverWait(self.driver, 10)

        list_item_button = wait.until(ec.visibility_of_element_located((By.XPATH, "//button[@data-et-name='list_item']")))
        list_item_button.click()

    def _make_individual_listing(self, listing):
        listing_id = listing[self.LISTING_ID_INDEX]

        print(f"Creating Listing for inventory with ID: {listing_id}...")

        listing_title = listing[self.TITLE_INDEX]
        listing_description_title = listing[self.DESC_TITLE_INDEX]
        listing_accessory = listing[self.ACCESSORY_INDEX]
        listing_serial_number  = listing[self.SERIAL_NUMBER_INDEX]
        listing_exterior = listing[self.EXTERIOR_INDEX]
        listing_inside = listing[self.INSIDE_INDEX]
        listing_pockets = listing[self.POCKETS_INDEX]
        listing_corners = listing[self.CORNERS_INDEX]
        listing_policy = listing[self.POLICY_INDEX]
        listing_category_path = listing[self.CATEGORY_PATH_INDEX]
        listing_brand = listing[self.BRAND_INDEX]
        color_string = listing[self.COLOR_INDEX]
        listing_original_price = listing[self.PRICE_INDEX]
        new_listing_price = listing[self.PRICE_INDEX]
        listing_material = listing[self.MATERIAL_INDEX]
        listing_style = listing[self.STYLE_INDEX]
        cm_addl_sizing_info = listing[self.CM_ADDL_SIZING_INFO_INDEX]
        inch_addl_sizing_info = listing[self.INCH_ADDL_SIZING_INFO_INDEX]
        base_photo_path = './photos/'

        listing_photo_path = base_photo_path + listing_id

        full_photo_path = os.path.abspath(listing_photo_path)

        self._enter_listing_photos(full_photo_path)

        self._enter_listing_title(listing_title)

        self._enter_listing_description(listing_description_title, listing_accessory, listing_serial_number, listing_exterior, listing_inside, listing_pockets, listing_policy, listing_material, listing_style, cm_addl_sizing_info, inch_addl_sizing_info, listing_corners)

        self._enter_category(listing_category_path)

        self._enter_brand(listing_brand)

        self._enter_color(color_string)

        self._enter_prices(listing_original_price, new_listing_price)

        if self.auto_run:
            user_in = input("PRESS ENTER IF THERE ARE NO ISSUES")

        self._click_next_button()

        self._list_item()
        
        listing[self.LISTED_STATUS_INDEX] = 'TRUE'

        with open(self.listing_csv_path, 'w', newline='', encoding='utf-8') as out_file:
            csv_writer = csv.writer(out_file)
            csv_writer.writerows(self.raw_listings)

        print("Item listed!")

    def list_all_listings(self):
        self._read_listings_csv()

        for listing in self.raw_listings:
            
            already_listed = listing[self.LISTED_STATUS_INDEX]
            print(already_listed)
            if already_listed == 'FALSE':
                already_listed = False

            if not already_listed:
                self._make_individual_listing(listing)
                time.sleep(5)
                self._visit_create_listing()

            #Change state of listing to 'listed'
        
        print('Listing complete!')

    def _read_listings_csv(self):
        print('reading csv file...')
        with open(self.listing_csv_path, 'r', encoding='latin-1') as in_file:
            csv_reader = csv.reader(in_file)
            for row in csv_reader:
                self.raw_listings.append(row)

if __name__ == "__main__":
    LISTING_PATH = "./poshmark_inventory.csv"
    ALLOW_MANUAL_PHOTO_ADJUST = False
    AUTO_RUN = True

    lister = Lister(LISTING_PATH, ALLOW_MANUAL_PHOTO_ADJUST, AUTO_RUN)

    lister._visit_create_listing()
    lister.list_all_listings()
