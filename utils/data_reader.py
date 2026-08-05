import openpyxl

def read_excel_data(sheet_name):
    wb = openpyxl.load_workbook(r"C:\Users\gpika\Desktop\demo\test_data.xlsx")
    ws = wb[sheet_name]
    headers = [cell.value for cell in ws[1]]
    data = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_dict = dict(zip(headers, row))
        data.append(row_dict)
    return data

if __name__ == "__main__":
    login_data = read_excel_data("LoginData")
    print("Login Test Data:")
    for row in login_data:
        print(row)
