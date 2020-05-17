import requests
from tabulate import tabulate

from classes.category import Category
from classes.utils import Statics


class ProductImportation():
    """
    Check if product is importable.
    Import a product in database.
    """

    def __init__(self, cursor, product, country):
        """Check if product is importable"""
        self.importable = False

        self.code = product['code']

        nb_prod = cursor.execute("""SELECT * FROM `products` WHERE `code` = "{}" """.format(
            self.code
        ))
        if nb_prod == 0:
            # Check if country,
            # categories language
            # and nutrition grade
            # are completed for this product

            if (
                    'countries_lc' in product
                    and 'categories_lc' in product
                    and 'nutrition_grade_fr' in product
            ):
                self.country = product['countries_lc']
                category_lc = product['categories_lc']

                # Check if country is same as defined
                if (
                        self.country == country
                        and category_lc == country
                ):
                    self.list_cat = product['categories'].split(',')
                    self.product = product
                    self.importable = True


    def import_product(self, mydb, cursor):
        """Import product in DB"""

        product_values = {
            'code': self.product['code'],
            'name': self.product['product_name'],
        }

        product_infos = Statics.json_dict('./lib/resources/product_infos.json')

        for product_field, product_value_name in product_infos.items():
            if not isinstance(product_value_name, dict):
                if product_value_name in self.product.keys():
                    if self.product[product_value_name] != '':
                        product_values[product_field] = self.product[product_value_name]
                    else:
                        product_values[product_field] = 'NULL'
            else:
                for nutriment_field, nutriment in product_value_name.items():
                    if nutriment in self.product[product_field].keys():
                        product_values[nutriment_field] = self.product[product_field][nutriment]

        fields = []
        values = []
        for field_name, value in product_values.items():
            fields.append(field_name)
            values.append('"' + str(value) + '"')
        
        request_str = '''INSERT INTO products ({}) VALUES ({});'''.format(
            ', '.join(fields),
            ', '.join(values)
        )

        cursor.execute(request_str)
        mydb.commit()

        # Import categories in DB
        self.categories(mydb)
    
        return product_values['name']


    def categories(self, mydb):
        """Check and create categories and its dependances in database.
Create relation instance in db."""
        i = 0
        j = 5
        if j > len(self.list_cat):
            j = len(self.list_cat)
        while i < j:
            self.list_cat[i] = self.list_cat[i].strip()
            category = Category(mydb, self.list_cat[i])
            id_cat = category.check_import(mydb, self.list_cat[i], i, self.list_cat)
            category.product_connection(mydb, self.code, id_cat)

            i += 1

        return self.list_cat[i - 1]

class ProductGet():
    """
Search for a product in db with its code.
Return its informations."""
    
    def __init__(self, db_object, code):
        """Initialization of ProductGet.
Information retrieval."""

        cursor = db_object.cursor

        product_req = """
    SELECT *
    FROM `products`
    WHERE `code`="{}";
    """.format(code)
        cursor.execute(product_req)

        row = cursor.fetchone()
        
        self.code = row[0]
        self.name = row[1]
        self.url = row[2]
        self.quantity = row[3]
        self.brand = row[4]
        self.country = row[5]
        self.stores = row[6]
        self.ingredients = row[7]
        self.energy = row[8]
        self.fat = row[9]
        self.satured_fat = row[10]
        self.carbohydrates = row[11]
        self.sugar = row[12]
        self.fibers = row[13]
        self.proteins = row[14]
        self.salt = row[15]
        self.sodium = row[16]
        self.nutrition_score = row[17]
        self.nutriscore = row[18]

        print(self)


    def __repr__(self):
        """Redefinition of __repr__ function to display product informations."""


        name = self.name + ' - ' + self.brand

        underline = "".join(["-" for letter in name])

        nutriscore = "Nutriscore :  {}".format(
            self.nutriscore.upper()
        ).center(100)

        product_infos = """
{name}
{underl}

{nutriscore}

URL :           {url}
Quantity:       {qt}
Store(s):       {stores}
Ingredients:    {ingredients}

""".format(
    name=name.center(100),
    underl=underline.center(100),
    url = self.url,
    qt=self.quantity,
    nutriscore=nutriscore,
    stores=self.stores,
    ingredients=self.ingredients
)

        return product_infos


    def init_tabulate(self):
        """Init tabulate lists"""

        headers = ["Products"]

        table = [
            ["Brand"],
            ["Quantity"],
            ["Nutriscore"],
            ["Energy (kcal)"],
            ["Fat"],
            ["  - Saturated fat"],
            ["Carbonhydrates"],
            ["  - Sugar"],
            ["Fibers"],
            ["Proteins"],
            ["Salt"],
            ["  - Sodium"],
            ["Nutrition Score"]
        ]

        return headers, table

    def product_infos(self):
        """Return list of product infos to add to tabulate lists."""

        title = self.name + '\n(g for 100 g / ml for 100 ml)'

        product_infos = [
            self.brand,
            self.quantity,
            self.nutriscore.upper(),
            self.energy,
            self.fat,
            self.satured_fat,
            self.carbohydrates,
            self.sugar,
            self.fibers,
            self.proteins,
            self.salt,
            self.sodium,
            self.nutrition_score
        ]

        return title, product_infos


    def show_infos(self, compared_product=None):
        """
Show detailed information with tabulate.
If compared_product is given:
    Compare product with product to compare.
Show the table."""

        headers, table = self.init_tabulate()

        title_1, product_infos_1 = self.product_infos()

        headers.append(title_1)

        i = 0
        while i < len(table):
            table[i].append(product_infos_1[i])
            if isinstance(compared_product, ProductGet):
                if i == 0:
                    title_2, product_infos_2 = compared_product.product_infos()
                    headers.append(title_2)
                table[i].append(product_infos_2[i])
                

            i += 1

        print(tabulate(table, headers, tablefmt="grid"))

        return headers, table

    def get_alternative(self, category_id, db_object):
        """
Return a list of alternative products.
Compare products where have the same selected category."""
        
        cursor = db_object.mydb.cursor()

        str_request = """
        SELECT `code`, `name`
        FROM `products`
        INNER JOIN `cat_prod_connections`
            WHERE
                products.code = cat_prod_connections.product_id
                AND category_id = {}
                AND products.nutriscore < "{}"
                AND products.code != {}
        """.format(
            category_id,
            self.nutriscore,
            self.code
        )

        nb_products = cursor.execute(str_request)

        if nb_products > 0:
            list_codes = []
            for row in cursor:
                list_codes.append(row[0])
            
            alternative = True

            return list_codes, alternative

        else:

            list_codes = []
            alternative = False

            return list_codes, alternative
