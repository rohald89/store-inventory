import csv
import datetime
import os

from models import (Base, session, 
                    Product, engine)
from cleaners import clean_price, clean_date, clean_id


def menu():
    '''
    Show the main menu and returns the users choice
    '''
    while True: 
        print('''
            \n**** PRODUCT INVENTORY ****
            \rV) View a single product
            \rA) Add a new Product
            \rB) Make a backup of the inventory
            \nI) Import data from a backup.csv file
            \rD) Delete product
            \rE) Exit''')
        choice = input("What would you like to do? ").lower()
        if choice in ['v', 'a', 'b', 'e', 'i', 'd']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above..
                \rPress enter to try again''')


def import_csv():
    '''
    import the provided inventory.csv data
    '''
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                price = clean_price(row[1])
                quantity = row[2]
                date_updated = clean_date(row[3])
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date_updated)
                session.add(new_product)
                print(new_product)
            else:
                # EXCEEDS REQUIREMENT: If a duplicate product is found update the existing record to the most recently updated data
                if product_in_db.date_updated < clean_date(row[3]):
                    product_in_db.product_name = row[0]
                    product_in_db.product_price = clean_price(row[1])
                    product_in_db.product_quantity = row[2]
                    product_in_db.date_updated = clean_date(row[3])
                    session.commit()
                    print(f'{product_in_db.product_name} updated')
        session.commit()


def print_single_product(product):
    print(f'''
    * * * PRODUCT: {product.product_id} * * *
    \nName: {product.product_name}
    \rQuantity: {product.product_quantity}
    \rPrice: {product.product_price}
    \rUpdated: {product.date_updated}
    ''')


def view_single_product():
    '''
    shows the user a list of present product id's 
    user is then able to pick one of those ids to show more information about the product
    '''
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    while id_error:
        id_choice = input(f'''
        \nID options: {id_options}
        \rProduct id: ''')
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
            id_error = False
    product = session.query(Product).filter(Product.product_id == id_choice).first()
    print_single_product(product)
    return product


def add_new_product():
    '''
    Lets the user add a new product to the database
    When a productname is already present in the database this will be overwritten
    '''
    name = input("Product name: ")
    quantity = input("Quantity: ")
    price_error = True
    while price_error:
        price = input("Price (Ex: $3.99): ")
        price = clean_price(price)
        if type(price) == int:
            price_error = False
    date = datetime.datetime.now().date()
    new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date)   
    # EXCEEDS REQUIREMEND: When a product is found with the same name update that product with the new data
    if session.query(Product).filter(Product.product_name == new_product.product_name).one_or_none():
        old_product = session.query(Product).filter(Product.product_name == new_product.product_name).first()
        old_product.product_name = name
        old_product.product_price = price
        old_product.product_quantity = quantity
        old_product.date_updated = date
    else:
        session.add(new_product)
    session.commit()


def delete_menu():
    while True:
        print('''
            \n**** DELETE PRODUCT ****
            \r1) Delete product by id
            \r2) Search by name
            \r3) Delete everything! 💥
            \rE) Exit''')
        choice = input("What would you like to do? ").lower()
        if choice in ['1', '2', '3', 'e']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above..
                \rPress enter to try again''')


def create_backup():
    '''
    create a backup of the database
    '''
    with open('backup.csv', 'w') as file:
        fieldnames = ['product_name', 'product_price', 'product_quantity', 'date_uploaded']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        products = session.query(Product).all()
        for product in products:
            writer.writerow({fieldnames[0]:product.product_name, fieldnames[1]:product.product_price, fieldnames[2]:product.product_quantity, fieldnames[3]:product.date_updated})
    print("\nBackup successfully created!")    
    input("Press enter to go back to the main menu ")


def import_backup():
    '''
    import a previously created backup into the database
    '''
    backup_file = os.path.exists('./backup.csv')
    if backup_file:
        print('backup.csv file found!')
        with open('backup.csv') as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                print(row)
                name = row[0]
                price = int(row[1])
                quantity = int(row[2])
                date_updated = datetime.date.fromisoformat(row[3])
                new_product = Product(product_name=name, product_price=price, product_quantity=quantity, date_updated=date_updated)
                session.add(new_product)
    else: 
        print('There is no backup.cvs file present, make sure it is located in the right directory')


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            view_single_product()
        elif choice == 'a':
            add_new_product()
        elif choice == 'b':
            create_backup()
        elif choice == 'i':
            import_backup()
        elif choice == 'd':
            del_choice = delete_menu()
            if del_choice == "1":
                product = view_single_product()
                delete_confirm = input("Are you sure you want to delete this product? Y/N ")
                if delete_confirm.lower() == 'y':
                    session.delete(product)
                    session.commit()
        else:
            print("Goodbye!")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    import_csv()
    app()