pantry = {
    "potatoes": 2,
    "bread": 6,
    "beans": 3
}


def add_items(amount, item_name):
    print(f"Adding {amount} {item_name} to pantry...")
    pantry[item_name] += amount
    print(f"There are now {pantry[item_name]} {item_name}")




def print_inventory():
    '''
        2 potatoes
        6 bread
        10 beans
    '''
    for key, value in pantry.items():
        print(f"{value} {key}")

add_items(7, "beans")
print_inventory()