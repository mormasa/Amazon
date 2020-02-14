import xlsxwriter
import pandas as pd
sales_file = "Sales.csv"
inventory_file = "FBA_Inventory.csv"
report_file = "FBA_Inventory_Alert_Report.xlsx"


def get_info_from_csv(filename):
    with open(filename) as f:
        file_out = [line.strip().split(',') for line in f.readlines()]
    updated_output = []
    for i in range(1, len(file_out)):
        new_line = []
        if filename == sales_file:
            new_line.append([file_out[i][1], '', file_out[i][7], int(file_out[i][7]) * 2, '', ''])
        elif filename == inventory_file:
            try:
                if int(file_out[i][0]) < 1000 or int(file_out[i][0]) > 1100:
                    continue
            except Exception as e:
                print(f"Exception {str(e)}")
                if "1013A" in file_out[i][0] or "GB-4288389-20-White_FBA" in file_out[i][0]:
                    new_line.append([file_out[i][2], file_out[i][0], '', '', file_out[i][9], ''])
                continue
            new_line.append([file_out[i][2], file_out[i][0], '', '', file_out[i][9], ''])
        updated_output.append(new_line[0])
    return updated_output


def update_fba_info_with_sales(fba_info, sales_info):
    for i in range(len(fba_info)):
        for j in range(len(sales_info)):
            if fba_info[i][0] == sales_info[j][0]:
                fba_info[i][2] = sales_info[j][2]
                fba_info[i][3] = sales_info[j][3]
    return fba_info


def update_alert_ratio(report):
    for i in range(len(report)):
        if not report[i][3]:
            report[i][2] = 0
            report[i][3] = 0
        if int(report[i][3]) == 0:
            report[i][5] = 999999
        else:
            report[i][5] = float(int(report[i][4])/report[i][3])
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
    sales30 = []
    inventory = []
    ratio = []
    for line in data:
        asin.append(line[0])
        sku.append(line[1])
        sales14.append(line[2])
        sales30.append(line[3])
        inventory.append(line[4])
        ratio.append(line[5])
    writer = pd.ExcelWriter(report_file, engine='xlsxwriter')
    df = pd.DataFrame({'Asin': asin,
                       'SKU': sku,
                       'Sales 14 days': sales14,
                       'Sales 30 days': sales30,
                       'Inventory': inventory,
                       'Inventory/Monthly Sales': ratio})
    df = df.sort_values('Inventory/Monthly Sales')
    print(df)
    df.to_excel(writer, sheet_name='Sheet1')
    workbook = writer.book
    worksheet1 = writer.sheets['Sheet1']
    red = workbook.add_format({'bg_color': '#FF0000'})
    yellow = workbook.add_format({'bg_color': '#F7FE2E'})


    worksheet1.conditional_format(f'G2:G{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.01,
                                      'maximum': 0.5,
                                      'format': red})
    worksheet1.conditional_format(f'G2:G{len(data)}', {'type': 'cell',
                                      'criteria': 'between',
                                      'minimum': 0.501,
                                      'maximum': 1,
                                      'format': yellow})

    writer.save()
    # workbook.close()

sales_info = get_info_from_csv(sales_file)
fba_info = get_info_from_csv(inventory_file)
report = update_fba_info_with_sales(fba_info, sales_info)
report = update_alert_ratio(report)
# report.insert(0, ["ASIN", "SKU", "Sales 14 days", "Prediction for 30 days", "Current Inventory", "Inventory/Monthly Sales"])
build_report_panda(report)
# print(report)
# build_report(report)
print("Done!")
