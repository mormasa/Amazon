import xlsxwriter
import os
import pandas as pd

docs_folder = os.path.dirname(os.path.realpath(__file__)) + "\Docs"
bank_statement_file = docs_folder + "\statement.xlsx"


def boa_analysis(statement_file=bank_statement_file):
    aliexpress_balance = 0
    aliexpress_trans = []
    fb_balance = 0
    fb_trans = []
    shopify_balance = 0
    shopify_trans = []
    shopify_refunds = 0
    amazon_sales = 0
    amazon_trans = []
    gb = 0
    gb_trans = []
    todo_description = []
    todo_amount = []
    etsy_balance = 0
    etsy_trans = []
    cf_balance = 0
    cf_trans = []
    klaviyo_balance = 0
    klaviyo_trans = []
    stamped_balance = 0
    stamped_trans = []
    reveal_balance = 0
    reveal_trans = []
    adwords_balance = 0
    adwords_trans = []
    stripe_refunds = 0
    stripe_balance = 0
    stripe_balance_trans = []
    dropified_balance = 0
    dropified_trans = []
    shopify_apps = 0
    apps_and_platforms = []
    advertising_costs = []
    cogs = []
    refunds = []


    file = pd.read_excel(statement_file)
    description = file['Description']
    amount = file['Amount']

    for i in range(len(file['Description'])):
        if "aliexpress" in description[i].lower():
            aliexpress_balance = aliexpress_balance + amount[i]
            aliexpress_trans.append(amount[i])
            cogs.append(amount[i])
        elif "face" in description[i].lower():
            fb_balance = fb_balance + amount[i]
            fb_trans.append(amount[i])
            advertising_costs.append(amount[i])
        elif "shopify" in description[i].lower():
            shopify_trans.append(amount[i])
            if amount[i] < 0:
                if amount[i] < -30:
                    shopify_apps = shopify_apps + amount[i]
                    apps_and_platforms.append(amount[i])
                else:
                    shopify_refunds = shopify_refunds + amount[i]
                    refunds.append(amount[i])
            else:
                shopify_balance = shopify_balance + amount[i]
        elif "stripe" in description[i].lower():
            stripe_balance_trans.append(amount[i])
            if amount[i] < 0:
                stripe_refunds = stripe_refunds + amount[i]
                refunds.append(amount[i])
            else:
                stripe_balance = stripe_balance + amount[i]
        elif "amzn" in description[i].lower():
            amazon_sales = amazon_sales + amount[i]
            amazon_trans.append(amount[i])
        elif "gearbubble" in description[i].lower():
            gb = gb + amount[i]
            gb_trans.append(amount[i])
            cogs.append(amount[i])
        elif "etsy" in description[i].lower():
            etsy_balance = etsy_balance + amount[i]
            etsy_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "clickfunnels" in description[i].lower():
            cf_balance = cf_balance + amount[i]
            cf_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "klaviyo" in description[i].lower():
            klaviyo_balance = klaviyo_balance + amount[i]
            klaviyo_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "stamped" in description[i].lower():
            stamped_balance = stamped_balance + amount[i]
            stamped_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "reveal" in description[i].lower():
            reveal_balance = reveal_balance + amount[i]
            reveal_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "GOOGLE *ADS" in description[i]:
            adwords_balance = adwords_balance + amount[i]
            adwords_trans.append(amount[i])
            advertising_costs.append(amount[i])
        elif "dropified" in description[i].lower():
            dropified_balance = dropified_balance + amount[i]
            dropified_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        else:
            todo_description.append(description[i])
            todo_amount.append(amount[i])


    items_to_print = ["aliexpress_balance", "Aliexpress trans", "FB balance", "FB trans", "Shopify sales", "Shopify trans",
                      "Shopify refunds", "Shopify apps", "Amazon sales", "Amazon trans", "GB", "GB trans",
                      "Etsy balance", "Etsy trans", "CF balance", "Stamped.io balance", "Klaviyo balance", "Reveal balance",
                      "Adwords balance", "Adwords trans", "Stripe refunds", "stripe balance",
                      "stripe balance trans", "Dropified balance"]
    items_amount = [aliexpress_balance, aliexpress_trans, fb_balance, fb_trans, shopify_balance, shopify_trans,
                    shopify_refunds, shopify_apps, amazon_sales, amazon_trans, gb, gb_trans, etsy_balance,
                    etsy_trans, cf_balance, stamped_balance, klaviyo_balance, reveal_balance, adwords_balance, adwords_trans,
                    stripe_refunds, stripe_balance, stripe_balance_trans, dropified_balance]
    for i in range(len(items_to_print)):
        print(f"{items_to_print[i]} = {items_amount[i]}")

    print("\n********************************** TO DO **********************************************************************\n")
    for i in range(len(todo_description)):
        print(f"{todo_description[i]} = {todo_amount[i]} \n")


    print("\n********************************** SUMMARY **********************************************************************\n")
    summary_items = ["Sales Amazon", "Sales Shopify", "Refunds", "COGS", "Advertisment", "Apps"]
    summary_values = [[amazon_sales], [shopify_balance], refunds, cogs, advertising_costs, apps_and_platforms]

    for i in range(len(summary_items)):
        print(f"{summary_items[i]} = {sum(summary_values[i])} = {summary_values[i]}\n")

boa_analysis()