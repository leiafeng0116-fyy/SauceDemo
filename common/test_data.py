VALID_USER = {"username": "standard_user", "password": "secret_sauce"}

base_url = "https://www.saucedemo.com"
URLS = {
    "login_url": base_url,
    "inventory_url": f"{base_url}/inventory.html"
}

ITEMS_DETAILS = {
    "Bike Light": {"id":"0", "name": "Sauce Labs Bike Light", "price": "$9.99"},
    "Bolt T-Shirt": {"id":"1", "name": "Sauce Labs Bolt T-Shirt", "price": "$15.99"},
    "Onesie": {"id":"2", "name": "Sauce Labs Onesie", "price": "$7.99"},
    "T-Shirt (Red)": {"id":"3","name": "Test.allTheThings() T-Shirt (Red)", "price": "$15.99"},
    "Backpack": {"id":"4","name":"Sauce Labs Backpack", "price": "$29.99"},
    "Fleece Jacket": {"id":"5", "name": "Sauce Labs Fleece Jacket", "price": "$49.99"}
}

SORT_OPTIONS_MAP = {
    "az": "Name (A to Z)",
    "za": "Name (Z to A)",
    "lohi": "Price (low to high)",
    "hilo": "Price (high to low)"
}

