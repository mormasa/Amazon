from selenium import webdriver
import time

amazon_url = "http://www.amazon.com"
results = 0
string_to_check = "Chihuahua Coffee Mug"
my_product = f"Funny {string_to_check}"
print(my_product)
chrome = webdriver.Chrome()
chrome.get(amazon_url)
chrome.find_element_by_id("twotabsearchtextbox").send_keys(string_to_check)
chrome.find_element_by_id("twotabsearchtextbox").submit()
for i in range(10):
    print(f"Checking page number {i+1}")
    all_products = chrome.find_elements_by_xpath('.//span[@class = "a-size-base-plus a-color-base a-text-normal"]')
    num_of_all_products = len(all_products)
    # print(f" Number of results for page {i+1}: {num_of_all_products}")
    for product in all_products:
        product_name = product.text
        if my_product in product_name:
            print(f"product was found on page {i+1}")
    # if results:
    #     break
    # print(f"{my_product} wasn't found on page {i+1}. Moving to page {i+2}")
    next_button = chrome.find_elements_by_xpath('.//li[@class = "a-last"]')
    next_button[0].click()
    time.sleep(5)
print("Done searching. Closing browser..")
chrome.quit()
