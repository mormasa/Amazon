from selenium import webdriver
import telegram
import logging
import time
from pathlib import Path
from datetime import datetime
URL = "https://icy.tools/"
INTERVAL_REPEAT_TIME_MINUTES = 120


def init_loggers():
    now = str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d:%H:%M:%S",
        level=logging.INFO
    )
    home = str(Path.home())
    logs_folder = home + str(Path("/logs"))
    filename = logs_folder + str(Path("/")) + f"nft_scrapper_{now}.txt"

    # Log file name
    test_handler = logging.FileHandler(filename)
    test_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"
        )
    )
    logger.addHandler(test_handler)
    return logger


def construct_message(chrome):
    all_nfts_elements = chrome.find_elements_by_xpath(
        "//tbody[@class='bg-white dark:bg-darker divide-y divide-gray-200 dark:divide-dark']/*")
    message = ["***LAST 1 HOUR ***\n"]
    for nft_elem in all_nfts_elements:
        try:
            name_elements, price_elements, sales_elements, average_elements, volume_elements = \
                [nft_elem.find_element_by_xpath(f"./td[{elem_index}]/a[1]") for elem_index in range(1, 6)]
            name_text, price_text, sales_text, avg_text, vol_text = [elem.get_attribute("innerText")
                                                                     for elem in
                                                                     [name_elements, price_elements, sales_elements,
                                                                      average_elements, volume_elements]]
            [name, quantaty], [sales, sales_change], [price, price_change], [avg, avg_change], [vol, vol_change] = \
                [elem.split("\n\n") for elem in [name_text, sales_text, price_text, avg_text, vol_text]]
            quantaty = quantaty.replace('Circulating supply:', '')
            price_change_elem, sales_chage_elem, avg_change_elem, vol_change_elem = \
                [elem.find_element_by_xpath("./p[1]/div[1]/span")
                 for elem in [price_elements, sales_elements, average_elements, volume_elements]]
            price_change_color, sales_chage_color, avg_change_color, vol_change_color = \
                ["green" if "green" in elem.get_attribute("class") else "red" if "red" in elem.get_attribute("class")
                else "gray" for elem in [price_change_elem, sales_chage_elem, avg_change_elem, vol_change_elem]]
            colors = [price_change_color, sales_chage_color, avg_change_color, vol_change_color]
            value_change = [sales_change, price_change, avg_change, vol_change]
            for i in range(0, len(colors)):
                value_change[i] = "-" + value_change[i] if colors[i] == "red" \
                    else "+" + value_change[i] if colors[i] == "green" else ''
            sales_change, price_change, avg_change, vol_change = value_change
            data = f"---\n{name}\n---\nquantity {quantaty}\nfloor = {price} change {price_change}\n" \
                f"sales = {sales} change {sales_change}\navg = {avg} change {avg_change}\n" \
                f"vol = {vol} change {vol_change}"
            filtered_data = data.replace('Ξ', '')
            # logger.info(filtered_data)
            message.append(filtered_data)
        except Exception as e:
            logger.warning(f"{str(e)} + {type(e).__name__}")
    logger.info(message)
    str_message = "\n".join(e for e in message)
    # logger.info(str_message)
    return str_message


def send_msg_to_telegram_bot(message):
    telegram_bot = telegram.Bot(token="5151726262:AAEdX_1ZeYNRV3dsjwxjGsB6V65aB0rvvQo")

    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            telegram_bot.send_message('637189504', message[x:x + 4096])
    else:
        telegram_bot.send_message('637189504', message)


if __name__ == "__main__":
    logger = init_loggers()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    chrome = webdriver.Chrome(options=options)
    chrome.get(URL)
    while True:
        logger.info("Starting new iteration")
        try:
            message_to_send = construct_message(chrome)
            send_msg_to_telegram_bot(message_to_send)
        except Exception as e:
            logger.warning(f"Exception during the flow. Exception details = {str(e)} + {type(e).__name__}")
        logger.info('---------------UPDATED DONE -------------------')
        logger.info("Waiting 2 hours")
        time.sleep(INTERVAL_REPEAT_TIME_MINUTES * 60)
        chrome.refresh()
