import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        print(f"The data provided is {data_str}")
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Function converts strings to integers and raises a ValueError if it can't, or if there 
    aren't exactly six value.
    """
    try:
        [int(value) for value in values]

        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def calculate_surplus_data(sales_row):
    """
    Calculates surplus data - sales figure taken away from the stock
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    
    stock_row = stock[-1]

    stock_row = [int(num) for num in stock_row]

    print("stock_row:", stock_row)
    print("sales_row:", sales_row)

    surplus_data = []

    """
        stock_row       [5, 5, 5, 5, 5, 5]
        sales_row       [1, 2, 3, 4, 5, 6]
        zip(stock_row, sales_row) -> 
                        [(5, 1), (5, 2), (5, 3)...]
    """

    for stock_num,sales_num in zip(stock_row,sales_row):
        result = stock_num - sales_num
        surplus_data.append(result)

    return surplus_data

# --- Worksheet-updating functions ----

'''
def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """

    print("Updating sales worksheet...\n" )
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def update_surplus_worksheet(surplus_data):
    """
    Update surplus worksheet, add new row with the list data provided
    """

    print("Updating surplus worksheet...\n" )
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_data)
    print("surplus worksheet updated successfully.\n")

'''

def update_worksheet(data, worksheet):
    """
    Update any worksheet, add new row with the list data provided
    Usage example:
        update_worksheet(sales_data, "sales")
        update_worksheet(surplus_data, "surplus")
    """

    print(f"Updating {worksheet} worksheet...\n" )
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

# --- End of worksheet-updating functions ----

def get_last_5_entries_sales():
    """
    Get last 5 entires in sales column so that we can calculate the average sales.
    """

    sales = SHEET.worksheet("sales")

    columns = []

    for ind in range(1,7):
        
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def main():
    """
    Runs all the program’s functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] 
    #update_sales_worksheet(sales_data)

    #                 the data to be added
    #                     v
    update_worksheet(sales_data, "sales")
    #                               ^
    #                           which worksheet to add to

    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    #update_surplus_worksheet(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")



print("Welcome! Please follow the instructions shown below")
#main()
get_last_5_entries_sales()

sales_columns = get_last_5_entries_sales()
print(sales_columns) 