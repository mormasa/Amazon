url = "http://quotes.toscrape.com/js/page/" + str(page) + "/"

driver.get(url)

items = len(driver.find_elements_by_class_name("quote"))

total = []
for item in range(items):
    quotes = driver.find_elements_by_class_name("quote")
    for quote in quotes:
        quote_text = quote.find_element_by_class_name('text').text
        author = quote.find_element_by_class_name('author').text
        new = ((quote_text,author))
        total.append(new)
df = pd.DataFrame(total,columns=['quote','author'])
df.to_csv('quoted.csv')
