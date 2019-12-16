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
    my_asins = [[parsed_data[i][10], parsed_data[i][2]] for i in range(1, len(parsed_data))]

# Remove duplications
    for asin in my_asins:
        orig = True
        for j in range(0, len(my_asins)):
            if asin[0] == my_asins[j][0]:
                if not orig:
                    my_asins.remove(asin)
                    break
                orig = False
    return my_asins


def look_my_product_in_page(my_asins, page_asins, page_number):
    for asin in my_asins:
        if asin[0] in page_asins:
            print(f"{asin[1]} ASIN {asin[0]} is in page {page_number}, position: {page_asins.index(asin[0])}")


def go_to_next_page():
    next_button = chrome.find_elements_by_xpath('.//li[@class = "a-last"]')
    next_button[0].click()
    time.sleep(2)

try:
    inventory_filename = "inventory.txt"
    amazon_url = "http://www.amazon.com"
    results = 0
    string_to_check = ["Yorkie Coffee Mug", "Chihuahua Coffee Mug", "Labrador Coffee Mug", "Dachshund Coffee Mug",
                       "German Shepherd Coffee Mug", "Border Collie Coffee Mug", "Pitbull Coffee Mug", "Pit Bull Coffee Mug"]
    my_asins = get_my_asins_from_inventory_txt_file(inventory_filename)

    chrome = webdriver.Chrome()
    chrome.get(amazon_url)
    for keyword in string_to_check:
        search_bar = chrome.find_element_by_id("twotabsearchtextbox")
        search_bar.send_keys(keyword)
        search_bar.submit()
        print(f"---------------- printing ranking for keyword: {keyword}")
        for i in range(3):
            print(f"Checking page number {i+1}")
            page_asins = get_page_asins()
            look_my_product_in_page(my_asins, page_asins, i+1)
            go_to_next_page()
        chrome.find_element_by_id("twotabsearchtextbox").clear()
    print("Done searching. Closing browser..")
    chrome.quit()
except IndexError as e:
    print("Last page. Done")
    print(str(e))
    chrome.quit()
