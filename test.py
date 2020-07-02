import xlrd
from openpyxl import load_workbook


new_row_data = [
    ['8', '9', '10']]

file_location = 'test.xlsx'
workbook = load_workbook(file_location)
# Select First Worksheet
sheet = workbook.worksheets[0]

# Append 2 new Rows - Columns A - D
for row_data in new_row_data:
    # Append Row Values
    sheet.append(row_data)

workbook.save("test.xlsx")
