import xlsxwriter
import pandas as pd
sales_file = "Sales.csv"
inventory_file = "FBA_Inventory.csv"
report_file = "FBA_Inventory_Alert_Report.xlsx"
skus_to_ignore = ['1001']

def get_info_from_csv(filename):

    updated_output = []

    # if filename == sales_file:
    with open(filename) as f:
        file_out = [line.strip().split('"') for line in f.readlines()]
    for j in range(len(file_out)):
        if j ==0:
            continue
        new_line = []
        line_to_check = file_out[j]
        for i in range(len(line_to_check)):
            if not (',' in line_to_check[i] and len(line_to_check[i]) == 1):
                new_line.append(line_to_check[i])
        updated_output.append(new_line)
    return updated_output


def update_fba_info_with_sales(fba_info, sales_info, skus_to_ignore):
    report = [['ASIN', 'SKU', 'TITLE', '14 Days Sales', '28 Days Sales', 'Inventory', 'Incoming', 'Inventory/28 Days Sales']]

    for i in range(len(fba_info)):
        product_sku = fba_info[i][1]
        if product_sku in skus_to_ignore:
            continue
        product_name = fba_info[i][4]
        fba_report_asin = fba_info[i][3]
        inventory_qty = int(fba_info[i][10])
        incoming = int(fba_info[i][17])

        for j in range(len(sales_info)):
            updated = False
            sales_report_asin = sales_info[j][2]

            if fba_report_asin == sales_report_asin:
                last_14_days_sales = int(sales_info[j][9])
                last_28_days_sales = last_14_days_sales * 2
                updated = True
                break
        if not updated:
            last_14_days_sales = 0
            last_28_days_sales = 0
            if inventory_qty > 0:
                ratio = 999999
            else:
                ratio = 0
        else:
            if last_14_days_sales == 0:
                ratio = 999999
            elif inventory_qty > 0:
                ratio = round(float(inventory_qty / last_28_days_sales), 2)
            else:
                ratio = 0
        report.append([fba_report_asin, product_sku, product_name, last_14_days_sales, last_28_days_sales, inventory_qty, incoming, ratio])
    return report



def build_report(data):
    workbook = xlsxwriter.Workbook(report_file)
    worksheet1 = workbook.add_worksheet()
    red = workbook.add_format({'bg_color': '#FF0000'})
    yellow = workbook.add_format({'bg_color': '#F7FE2E'})
    i = 0
    for row, row_data in enumerate(data):
        worksheet1.write_row(row, 0, row_data)
        i += 1

    worksheet1.conditional_format(f'F2:F{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.01,
                                      'maximum': 0.5,
                                      'format': red})
    worksheet1.conditional_format(f'F2:F{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.501,
                                      'maximum': 1,
                                      'format': yellow})

    workbook.close()


def build_report_panda(data):
    asin = []
    sku = []
    sales14 = []
    sales28 = []
    inventory = []
    incoming = []
    ratio = []
    title = []
    for i in range(len(data)):
        if i == 0:
            continue
        asin.append(data[i][0])
        title.append(data[i][2])
        sku.append(data[i][1])
        sales14.append(data[i][3])
        sales28.append(data[i][4])
        inventory.append(data[i][5])
        incoming.append(data[i][6])
        ratio.append(data[i][7])
    writer = pd.ExcelWriter(report_file, engine='xlsxwriter')
    df = pd.DataFrame({'Asin': asin,
                       'Title': title,
                       'SKU': sku,
                       'Sales 14 days': sales14,
                       'Sales 30 days': sales28,
                       'Inventory': inventory,
                       'Incoming': incoming,
                       'Inventory/Monthly Sales': ratio})
    df = df.sort_values('Inventory/Monthly Sales')
    print(df)
    df.to_excel(writer, sheet_name='Sheet1')
    workbook = writer.book
    worksheet1 = writer.sheets['Sheet1']
    red = workbook.add_format({'bg_color': '#FF0000'})
    yellow = workbook.add_format({'bg_color': '#F7FE2E'})


    worksheet1.conditional_format(f'I2:I{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.01,
                                      'maximum': 0.5,
                                      'format': red})
    worksheet1.conditional_format(f'I2:I{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.501,
                                      'maximum': 1,
                                      'format': yellow})

    writer.save()
    # workbook.close()

sales_info = get_info_from_csv(sales_file)
fba_info = get_info_from_csv(inventory_file)
report = update_fba_info_with_sales(fba_info, sales_info, skus_to_ignore)
build_report_panda(report)
# print(report)
print("Done!")
