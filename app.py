from models import (Base, session, 
                    Product, engine)
from cleaners import clean_price, clean_date, clean_id
import csv
import datetime


def menu():
    while True: 
        print('''
            \nPRODUCT INVENTORY
            \rV) View a single product
            \rA) Add a new Product
            \rB) Make a backup of the inventory
            \rE) Exit''')
        choice = input("What would you like to do? ").lower()
        if choice in ['v', 'a', 'b', 'e']:
            return choice
        else:
            input('''
                \rPlease choose one of the options above..
                \rPress enter to try again''')


def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
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


# def update_duplicate_product(product):
#     if session.query(Product).filter(Product.product_name == product.product_name):
#         print("This should be updated")


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            #View single product
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
            print(product)
        elif choice == 'a':
            #Add new product
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
            if session.query(Product).filter(Product.product_name == new_product.product_name).one_or_none():
                old_product = session.query(Product).filter(Product.product_name == new_product.product_name).first()
                old_product.product_name = name
                old_product.product_price = price
                old_product.product_quantity = quantity
                old_product.date_updated = date
            else:
                session.add(new_product)
            session.commit()
        elif choice == 'b':
            #create backup
            pass
        else:
            # Exit
            print("Goodbye!")
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()