import xlsxwriter
import os
import pandas as pd
import math

docs_folder = os.path.dirname(os.path.realpath(__file__)) + "\Docs"
bank_statement_file = docs_folder + "\BOA.xlsx"
paypal_statement_file = docs_folder + "\Paypal.xlsx"


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
    klaviyo_balance = 0
    klaviyo_trans = []
    adwords_balance = 0
    adwords_trans = []
    stripe_refunds = 0
    stripe_balance = 0
    stripe_balance_trans = []
    dropified_balance = 0
    dropified_trans = []
    custom_happy = 0
    custom_happy_trans = []
    shopify_apps = 0
    bank_fees = 0
    bank_fees_trans = []
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
            if amount[i] < 0:
                if amount[i] < -30:
                    shopify_apps = shopify_apps + amount[i]
                    apps_and_platforms.append(amount[i])
                else:
                    shopify_refunds = shopify_refunds + amount[i]
                    refunds.append(amount[i])
                    shopify_trans.append(amount[i])
            else:
                shopify_balance = shopify_balance + amount[i]
                shopify_trans.append(amount[i])
        elif "stripe" in description[i].lower():
            if "CUSTOMHAPPY" not in description[i]:
                if amount[i] < 0:
                    stripe_refunds = stripe_refunds + amount[i]
                    refunds.append(amount[i])
                else:
                    stripe_balance = stripe_balance + amount[i]
                    stripe_balance_trans.append(amount[i])
            else:
                custom_happy = custom_happy + amount[i]
                custom_happy_trans.append(amount[i])
                cogs.append(amount[i])
        elif "amzn" in description[i].lower():
            amazon_sales = amazon_sales + amount[i]
            amazon_trans.append(amount[i])
        elif "gearbubble" in description[i].lower():
            if amount[i] < 0:
                if "dropship" in description[i].lower():
                    shopify_apps = shopify_apps + amount[i]
                    apps_and_platforms.append(amount[i])
                else:
                    cogs.append(amount[i])
            else:
                gb = gb + amount[i]
                gb_trans.append(amount[i])
                stripe_balance = stripe_balance + amount[i]
        elif "etsy" in description[i].lower():
            etsy_balance = etsy_balance + amount[i]
            etsy_trans.append(amount[i])
        elif "klaviyo" in description[i].lower():
            klaviyo_balance = klaviyo_balance + amount[i]
            klaviyo_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "GOOGLE" in description[i] and "*ADS" in description[i]:
            adwords_balance = adwords_balance + amount[i]
            adwords_trans.append(amount[i])
            advertising_costs.append(amount[i])
        elif "dropified" in description[i].lower():
            dropified_balance = dropified_balance + amount[i]
            dropified_trans.append(amount[i])
            apps_and_platforms.append(amount[i])
        elif "Online Banking transfer to SAV" in description[i] or "Online Banking transfer from SAV" in description[i] \
                or "beginning balance" in description[i].lower() or "Online scheduled transfer to CHK" in description[i]\
                or "MASARANO GROUP DES:PAYPAL IAT ID:" in description[i]:
            continue
        elif "external transfer fee" in description[i].lower() or "Online scheduled transfer to" in description[i].lower()\
                or "OVERDRAFT ITEM FEE" in description[i] or "Monthly Fee for Business Advantage" in description[i] \
                or "Monthly Fee Business Adv Relationship" in description[i]:
            bank_fees = bank_fees + amount[i]
            bank_fees_trans.append(amount[i])
        else:
            todo_description.append(description[i])
            todo_amount.append(amount[i])


    items_to_print = ["aliexpress_balance", "Aliexpress trans", "FB balance", "FB trans", "Shopify sales", "Shopify trans",
                      "Shopify refunds", "Shopify apps", "Amazon sales", "Amazon trans", "GB Sales", "GB trans",
                      "Etsy balance", "Etsy trans", "Klaviyo balance",
                      "Adwords balance", "Adwords trans", "Stripe refunds", "stripe balance",
                      "stripe balance trans", "Dropified balance", "Bank fees", "Bank fees trans", "Custom Happy", "Custom Happy Trans"]
    items_amount = [aliexpress_balance, aliexpress_trans, fb_balance, fb_trans, shopify_balance, shopify_trans,
                    shopify_refunds, shopify_apps, amazon_sales, amazon_trans, gb, gb_trans, etsy_balance,
                    etsy_trans, klaviyo_balance, adwords_balance, adwords_trans,
                    stripe_refunds, stripe_balance, stripe_balance_trans, dropified_balance, bank_fees, bank_fees_trans,
                    custom_happy, custom_happy_trans]
    for i in range(len(items_to_print)):
        print(f"{items_to_print[i]} = {items_amount[i]}")

    print("\n********************************** TO DO **********************************************************************\n")
    for i in range(len(todo_description)):
        print(f"{todo_description[i]} = {todo_amount[i]} \n")


    print("\n********************************** SUMMARY **********************************************************************\n")
    summary_items = ["Sales Amazon", "Sales Shopify", "Stripe Sales", "Sales GB", "Sales Etsy", "Refunds (Stripe + Shopify)", "COGS", "Advertisment", "Apps", "Bank Fees"]
    summary_values = [amazon_trans, shopify_trans, stripe_balance_trans, gb_trans, etsy_trans, refunds, cogs, advertising_costs, apps_and_platforms, bank_fees_trans]

    for i in range(len(summary_items)):
        print(f"{summary_items[i]} = {sum(summary_values[i])} = {summary_values[i]}\n")


def paypal_analysis(statement_file=paypal_statement_file):

    paypal_sales = 0
    paypal_sales_trans = []
    paypal_fees = 0
    paypal_fees_trans = []
    ebay_balance = 0
    ebay_trans = []
    mor_payment = 0
    mor_payment_trans = []
    paypal_refunds = 0
    paypal_refunds_trans = []
    staff_payment = 0
    staff_payment_trans = []
    apps_and_platforms_fees = 0
    apps_and_platforms = []
    cogs = []
    professional_fees = []
    todo_description = []
    todo_amount = []
    todo_name = []
    fb_balance = 0
    fb_trans = []

    file = pd.read_excel(statement_file)
    fee = file['Fee']
    gross = file['Gross']
    payment_type = file['Type']
    name = file['Name']
    status = file['Status']
    currency = file['Currency']

    for i in range(len(file['Gross'])):
        if currency[i] != "USD" and status[i] != "Denied":
            todo_name.append(name[i])
            todo_description.append(payment_type[i])
            todo_amount.append(gross[i])
            continue
        if fee[i] and not math.isnan(fee[i]):
            paypal_fees = paypal_fees + fee[i]
            paypal_fees_trans.append(fee[i])
        if gross[i] < 0:
            if payment_type[i] == "eBay Auction Payment":
                ebay_balance = ebay_balance + gross[i]
                ebay_trans.append(gross[i])
                cogs.append(gross[i])
            elif payment_type[i] == "General Credit Card Withdrawal" and status[i] == "Completed":
                mor_payment = mor_payment + gross[i]
                mor_payment_trans.append(gross[i])
                professional_fees.append(gross[i])
            elif payment_type[i] == "General Currency Conversion" or payment_type[i] == "Hold on Balance for Dispute Investigation" \
                    or payment_type[i] == "Chargeback Fee":
                paypal_fees = paypal_fees + gross[i]
                paypal_fees_trans.append(gross[i])
            elif payment_type[i] == "General Payment":
                staff_payment = staff_payment + gross[i]
                staff_payment_trans.append(gross[i])
            elif payment_type[i] == "Payment Refund":
                paypal_refunds = paypal_refunds + gross[i]
                paypal_refunds_trans.append(gross[i])
            elif payment_type[i] == "PreApproved Payment Bill User Payment":
                if name[i] == "USZoom" or name[i] == "Golan Telecom Ltd" or "skype" in name[i].lower() or "spotify" in name[i].lower():
                    apps_and_platforms_fees = apps_and_platforms_fees + gross[i]
                    apps_and_platforms.append(gross[i])
                elif "face" in name[i].lower():
                    fb_balance = fb_balance + gross[i]
                    fb_trans.append(gross[i])
                elif "fiverr" in name[i].lower():
                    staff_payment = staff_payment + gross[i]
                    staff_payment_trans.append(gross[i])
                else:
                    todo_name.append(name[i])
                    todo_description.append(payment_type[i])
                    todo_amount.append(gross[i])
            elif payment_type[i] == "Website Payment":
                if name[i] == "Ileen Jasmine Lajo":
                    staff_payment = staff_payment + gross[i]
                    staff_payment_trans.append(gross[i])
                else:
                    todo_name.append(name[i])
                    todo_description.append(payment_type[i])
                    todo_amount.append(gross[i])
            elif payment_type[i] == "Express Checkout Payment":
                cogs.append(gross[i])
            elif payment_type[i] == "Reserve Hold" or payment_type[i] == "Chargeback" or payment_type[i] == "General Authorization" \
                    or payment_type[i] == "Account Hold for Open Authorization" or payment_type[i] == "Payment Reversal":
                paypal_sales = paypal_sales + gross[i]
                paypal_sales_trans.append(gross[i])
            elif payment_type[i] == "General Withdrawal":
                continue
            else:
                todo_name.append(name[i])
                todo_description.append(payment_type[i])
                todo_amount.append(gross[i])
        else:
            if status[i] == "Denied" or payment_type[i] == "General Credit Card Deposit":
                continue
            if payment_type[i] == "Express Checkout Payment" or payment_type[i] == "Mass Pay Payment" \
                    or payment_type[i] == "Void of Authorization" or payment_type[i] == "General Authorization" or \
                    payment_type[i] == "Mobile Payment" or payment_type[i] == "Reserve Release" or \
                    payment_type[i] == "Reversal of General Account Hold" or payment_type[i] == "General Payment" or payment_type[i] == "Chargeback Reversal":
                paypal_sales = paypal_sales + gross[i]
                paypal_sales_trans.append(gross[i])
            elif payment_type[i] == "Fee Reversal" or "PayPal Protection Bonus" in payment_type[i]:
                paypal_fees = paypal_fees + gross[i]
                paypal_fees_trans.append(gross[i])
            elif payment_type[i] == "Payment Refund":
                ebay_balance = ebay_balance + gross[i]
                ebay_trans.append(gross[i])
                cogs.append(gross[i])
            elif payment_type[i] == "Cancellation of Hold for Dispute Resolution" or payment_type[i] == "General Currency Conversion":
                paypal_fees = paypal_fees + gross[i]
                paypal_fees_trans.append(gross[i])
            elif payment_type[i] == "Invoice Received" or payment_type[i] == "Request Received":
                continue
            else:
                todo_name.append(name[i])
                todo_description.append(payment_type[i])
                todo_amount.append(gross[i])


    items_to_print = ["Paypal sales", "Paypal sales trans", "Paypal fees", "Paypal fees trans", "Ebay expense", "Ebay expense trans",
                      "Mor payment", "Mor payment trans", "Paypal refunds", "Paypal refunds trans", "Staff payment",
                      "Staff payment trans", "Apps payments", "Apps payments trans", "FB Ads Spent", "FB trans"]
    items_amount = [paypal_sales, paypal_sales_trans, paypal_fees, paypal_fees_trans, ebay_balance, ebay_trans,
                    mor_payment, mor_payment_trans, paypal_refunds, paypal_refunds_trans, staff_payment, staff_payment_trans,
                    apps_and_platforms_fees, apps_and_platforms, fb_balance, fb_trans]

    for i in range(len(items_to_print)):
        print(f"{items_to_print[i]} = {items_amount[i]}")

    print("\n********************************** TO DO **********************************************************************\n")
    for i in range(len(todo_description)):
        print(f"{todo_name[i]}, {todo_description[i]} = {todo_amount[i]} \n")


    print("\n********************************** SUMMARY **********************************************************************\n")
    summary_items = ["Paypal Sales", "Paypal Refunds", "COGS", "Apps", "Paypal Fees", "Hired Help", "Mor Payment", "Advertisment"]
    summary_values = [[paypal_sales], [paypal_refunds], cogs, apps_and_platforms, paypal_fees_trans, staff_payment_trans, mor_payment_trans, fb_trans]

    for i in range(len(summary_items)):
        print(f"{summary_items[i]} = {sum(summary_values[i])} = {summary_values[i]}\n")


# boa_analysis()
paypal_analysis()
