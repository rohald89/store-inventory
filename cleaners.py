import datetime

def clean_price(price_str):
    try:
        price = float(price_str.split('$')[1])
    except ValueError:
        input('''
                \n**** PRICE ERROR ****
                \rThe price should be a number with a currency symbol
                \rEx: $10.99
                \rPress enter to try again.
                \r********************''')
    except IndexError:
        input('''
                \n**** PRICE ERROR ****
                \rThe price should be a number with a currency symbol
                \rEx: $10.99
                \rPress enter to try again.
                \r********************''')
    else:
        return int(price * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        date = datetime.date(year, month, day)
    except ValueError:
        input('''
                \n**** DATE ERROR ****
                \rThe date format should include a valid DD/MM/YYYY format from the past
                \rEx: 4/28/2021
                \rPress enter to try again.
                \r*******************''')
        return
    else:
        return date


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
                \n**** ID ERROR ****
                \rThe id should be a number.
                \rPress enter to try again.
                \r********************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
                \n**** ID ERROR ****
                \rOptions: {options}
                \rPress enter to try again.
                \r********************''')
            return