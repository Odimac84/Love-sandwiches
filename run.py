import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    get sales data
    """
    while True:
        print("Please enter sales data from last market")
        print("Data should be six numbers, seperated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
    
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, Converts to integers. Raises ValueError if strings cannot be 
    converted to int, or if there are to many numbers
    """
    try:
        if len(values)!= 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

"""
def update_sales_worksheet(data):

    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated succsessfully.\n")

def update_surplus_worksheet(data):
    
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated succsessfully.\n")
"""

def update_worksheets(data, worksheet):
    """
    Updates the worksheet, add new row for with the list data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succsessfully\n")

def calculate_surplus_data(sales_row):

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects the data from last 5 sales
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    calculating the average stock data
    """
    print("Calculating Stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Runs all main functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheets(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheets(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheets(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()

