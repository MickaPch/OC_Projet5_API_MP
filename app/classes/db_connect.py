"""DB creation, importation and connection"""
import sys

import pymysql
import requests
from tqdm import tqdm

from app.settings import HOST, USER, PWD, DATABASE, COUNTRY
from app.utils.requests import CREATE_DB, FK_CHECKS_0, FK_CHECKS_1, DROP_TABLE
from app.utils.requests import SELECT_INIT_CAT, SELECT_CHILD_CAT, SELECT_CAT_BY_NAME
from app.utils.requests import SELECT_PROD_BY_CAT, SELECT_PROD_BY_CODE


from app.classes.product import ProductImportation
from app.utils.methods import Statics



class Connection():
    """Connection to database with given parameters."""

    def __init__(self, keep):
        """
        Print connexion parameters for user validation.
        Input YES or NO.
        Modify if necessary.
        Test of connection and initalization of db.
        Create tables and import products.
        """

        # Retrieve the app strings from JSON
        self.strings = Statics.json_dict('./app/utils/json/app_msg.json')
        input(self.strings['appMessages']['welcome'])

        # Retrieve default settings
        settings_var = {
            "host": HOST,
            "user": USER,
            "passwd": PWD,
            "database": DATABASE
        }

        # Validate default settings or enter news
        # Keep selected settings in attribute
        self.settings_var = self.set_settings(settings_var)

        # Connection test
        self.mydb, self.cursor, self.connection = self.db_connection()

        # Create DB and tables if not exists yet
        if self.connection and not keep:
            # Creation of tables
            self.tables_creation()
            self.import_products()

        # Else, stop the program
        elif not self.connection:
            sys.exit()


    def sep(self):
        """Separator attribute for terminal display"""
        print(self.strings['appMessages']['separator'])


    def set_settings(self, settings):
        """
        Connect with default settings or ask user for choose others.
        (host, user, password and database name)
        """

        # Show default settings
        self.sep()
        print(self.strings['appMessages']['connection']['default'])
        for setting, value in settings.items():
            print(" -", setting, " : '" + value + "'")
        print(self.strings['appMessages']['connection']['confirmation'])

        # Ask user for keep or change default settings
        user_choice = Statics.input_y_n(self.strings['appMessages']['inputYN'])

        if not user_choice:
            print(self.strings['appMessages']['connection']['changeSettings'])
            for setting in settings.keys():
                while True:
                    setting_value = input(setting + '  >>>  ')
                    val_setting = Statics.input_y_n(self.strings['appMessages']['inputYN'])
                    if val_setting:
                        settings[setting] = setting_value
                        break

            print("New settings are :")
            for setting, value in settings.items():
                print(" -", setting, " : '" + value + "'")

        return settings


    def db_connection(self):
        """
        Connect to MySQL.
        Create database if not exists.
        Default DB name is 'yaka'.
        """

        self.sep()
        print(self.strings['appMessages']['connection']['connectionMsg'])
        connection = False
        while not connection:
            try:
                mydb = pymysql.connect(**self.settings_var)
                cursor = mydb.cursor()
                connection = True
                print("Connection OK")
                self.sep()

            # ID error / print error in terminal. Stop the program.
            except pymysql.err.DatabaseError as error:
                print("Database connexion failed :")
                error_string = str(error)[1:-1].replace(',', ':')
                print(error_string)

                if error_string[:4] == "1049":
                    print("\nDo you want to create '{}' database ?".format(
                        self.settings_var['database']
                    ))
                    db_creation = Statics.input_y_n(self.strings['appMessages']['inputYN'])
                    # User want to create the new db
                    if db_creation:
                        mydb = pymysql.connect(
                            host=self.settings_var['host'],
                            user=self.settings_var['user'],
                            passwd=self.settings_var['passwd']
                        )
                        cursor = mydb.cursor()
                        self.create_db(cursor)
                        connection = False
                    # User don't want to create the db
                    else:
                        sys.exit()
                # Host, user or pwd is wrong
                else:
                    sys.exit()

            # Unknown error. Stop the program.
            except:
                print('An error occured in connexion test.')
                connection = False
                break

        return mydb, cursor, connection


    def create_db(self, cursor):
        """Create database if not exists."""

        cursor.execute(
            CREATE_DB.format(
                self.settings_var['database']
            )
        )


    def tables_creation(self, table_path="./app/utils/json/tables.json"):
        """
        Check if tables exists and drop them.
        Creation of database with tables request strings.
        """
        print("CREATION OF TABLES\n")


        tables = Statics.json_dict(table_path)

        # Remove foreign key checks if drop is necessary
        self.cursor.execute(FK_CHECKS_0)

        # Create all tables

        for table_name, fields_parameters in tables.items():

            # Drop table if exists
            try:
                self.cursor.execute(
                    DROP_TABLE.format(table_name)
                )
                print('{} : Droped'.format(table_name))
            except:
                print("{} : Not exists".format(table_name))

            # Create table
            create_table_request = 'CREATE TABLE IF NOT EXISTS `{}` ('.format(
                table_name
            )

            # create_table_request : STRING FOR FIELD PARAMETERS
            list_fk = []
            for field in fields_parameters:
                # Foreign keys
                if "fk" in field:
                    list_fk.append((field['field'], field['fk']['table'], field['fk']['field']))

                # DateField
                if field['type'] == 'date':
                    create_table_request += "`{}` DATE DEFAULT CURDATE(), ".format(
                        field['field']
                    )
                else: # INT or VARCHAR
                    create_table_request += "`{}` {}({}) ".format(
                        field['field'],
                        field['type'],
                        field['len']
                    )

                    # Default null or not
                    if field['null']:
                        create_table_request += 'DEFAULT NULL'
                    else:
                        create_table_request += 'NOT NULL'

                    # SET primary key
                    if field['pk']:
                        primary_key = field['field']

                        # If PK is id --> AUTO_INCREMENT
                        # Not for product_code
                        if field['field'] == 'id':
                            create_table_request += ' AUTO_INCREMENT'
                    create_table_request += ', '

            create_table_request += 'PRIMARY KEY({})'.format(primary_key)

            # Set Foreign keys
            for foreign_key in list_fk:
                create_table_request += ', FOREIGN KEY (`{0}`) REFERENCES `{1}`(`{2}`)'.format(
                    foreign_key[0],
                    foreign_key[1],
                    foreign_key[2]
                )

            create_table_request += ');'

            # Execute request
            self.cursor.execute(create_table_request)
            print('    {} created.'.format(table_name))

        self.cursor.execute(FK_CHECKS_1)
        print('\n--> All tables are created and ready for import.')
        self.sep()

    def import_products(self, country=COUNTRY):
        """
        Import products.
        Default country is France
        1. Read categories from {country}.openfoofacts.org/categories.json
        2. Select only categories where contains more than 2500 products.
        3. Search in this category with OpenFoodFacts API for importable products
        4. Import products with ProductImportation class
        """
        # 1. GET all categories
        categories_url = "https://{}.openfoodfacts.org/categories.json".format(
            country
        )
        resp = requests.get(categories_url)
        all_categories = resp.json()

        # 2. More than 2500 products in this category
        importable_categories = []
        count = 0
        while count < len(all_categories['tags']):
            if all_categories['tags'][count]['products'] > 2500:
                category_name = all_categories['tags'][count]['id'].split(':')[1]
                if category_name not in importable_categories:
                    importable_categories.append(category_name)
            else:
                break
            count += 1

        # 3. Search in each category for importable product

        conditions = Statics.json_dict("./app/utils/json/api_read.json")
        # CONDITIONS in API REQUEST :
        # load from JSON
            # categories contains "category"
            # countries contains "country"
            # states not contains 'to-be-completed'
            # Sort by popularity
            # Page_size : 50
            # Format : JSON

        for category_name in tqdm(importable_categories):
            # REQUEST URL
            resp = requests.get(
                self.url_request_category(conditions, category_name, country)
            )
            products = resp.json()['products']

            for product_to_check in products:
                # Check if product is importable
                product = ProductImportation(self.cursor, product_to_check, country)

                # Check if product is found and available for selected country
                if product.importable:
                    # Import product and categories
                    # Create link between product and its categories
                    product.import_product(self.mydb, self.cursor)
                    self.mydb.commit()

        print('all products imported')

    def url_request_category(self, conditions, category_name, country):
        """
        Format URL request for retrieve products
        by category name
        and filtered by criterias
        """
        request_url = "https://{}.openfoodfacts.org/cgi/search.pl?action=process".format(
            country
        )

        # Add each filter to api request
        i = 0
        while i < len(conditions['criteria']):
            request_url += "&tagtype_{index}={tagtype}".format(
                index=str(i),
                tagtype=conditions['criteria'][i]['tagtype']
            )
            request_url += "&tag_contains_{index}={contains}".format(
                index=str(i),
                contains=conditions['criteria'][i]['tag_contains']
            )
            if conditions['criteria'][i]['tagtype'] == 'categories':
                request_url += "&tag_{index}={category}".format(
                    index=str(i),
                    category=category_name
                )
            elif conditions['criteria'][i]['tagtype'] == 'countries':
                request_url += "&tag_{index}={country}".format(
                    index=str(i),
                    country=country
                )
            else:
                request_url += "&tag_{index}={tag}".format(
                    index=str(i),
                    tag=conditions['criteria'][i]['fixed_tag']
                )

            i += 1

        # Add sorting
        request_url += "&sort_by={}".format(
            conditions['sort_by']
        )

        # Add page size
        request_url += "&page_size={}".format(
            conditions['page_size']
        )

        # Add file format
        request_url += "&{}=1".format(
            conditions['format']
        )

        return request_url


    def list_categories(self, parent_id='NULL'):
        """
        Get a list of categories from parent_id.
        Default parent_id = 'NULL'.
        """
        list_cat = []
        if parent_id == 'NULL':
            cat_list_req = SELECT_INIT_CAT
        else:
            cat_list_req = SELECT_CHILD_CAT.format(parent_id)
        self.cursor.execute(cat_list_req)
        for row in self.cursor:
            list_cat.append(row[0])

        return list_cat


    def id_cat(self, category):
        """Return id of given category"""
        self.cursor.execute(
            SELECT_CAT_BY_NAME.format(category)
        )
        id_cat = self.cursor.fetchone()[0]

        return id_cat

    def list_products_by_cat(self, id_cat):
        """Return list of products code related to category id"""
        list_products = []
        self.cursor.execute(
            SELECT_PROD_BY_CAT.format(id_cat)
        )

        for row in self.cursor:
            if row[0] not in list_products:
                list_products.append(row[0])

        return list_products


    def get_product_list(self, list_codes):
        """Get a list of products names from a list of codes."""

        list_of_products = []

        for code in list_codes:

            self.cursor.execute(
                SELECT_PROD_BY_CODE.format(code)
            )

            row = self.cursor.fetchone()
            product_name = "{} - {} [{}]".format(
                row[0],
                row[1],
                row[2]
            )

            list_of_products.append(product_name)

        return list_of_products
