from selenium import webdriver
import time


def get_page_asins():
    all_products = chrome.find_elements_by_xpath('.//div[@class = "s-result-list s-search-results sg-row"]//div[@data-asin]')
    asins = []
    for item in all_products:
        asins.append(item.get_attribute("data-asin"))
    return asins


def get_my_asins_from_inventory_txt_file(inventory_filename):
    parsed_data = []
    with open(inventory_filename) as file:
        data = [line.strip() for line in file.readlines()]
    for line in data:
        parsed_data.append(line.split("\t"))
    my_asins = [parsed_data[i][10] for i in range(1, len(parsed_data))]
    my_asins = list(dict.fromkeys(my_asins))    # Removing duplications
    return my_asins


def look_my_product_in_page(my_asins, page_asins):
    for asin in my_asins:
        if asin in page_asins:
            print(f"ASIN {asin} is in page {i+1}, position: {page_asins.index(asin)}")


def go_to_next_page():
    next_button = chrome.find_elements_by_xpath('.//li[@class = "a-last"]')
    next_button[0].click()
    time.sleep(5)


inventory_filename = "inventory.txt"
amazon_url = "http://www.amazon.com"
results = 0
string_to_check = "Chihuahua Coffee Mug"
my_asins = get_my_asins_from_inventory_txt_file(inventory_filename)

chrome = webdriver.Chrome()
chrome.get(amazon_url)
chrome.find_element_by_id("twotabsearchtextbox").send_keys(string_to_check)
chrome.find_element_by_id("twotabsearchtextbox").submit()
for i in range(10):
    print(f"Checking page number {i+1}")
    page_asins = get_page_asins()
    look_my_product_in_page(my_asins, page_asins)
    go_to_next_page()
print("Done searching. Closing browser..")
chrome.quit()
