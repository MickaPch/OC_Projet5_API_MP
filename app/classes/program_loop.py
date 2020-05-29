"""Program loop with menu options"""
import sys

from app.utils.methods import Statics
from app.classes.product import ProductGet

from app.utils.requests import SELECT_PROD_TEXT, SELECT_CAT_BY_PROD
from app.utils.requests import INSERT_REGISTRATION
from app.utils.requests import SELECT_REGISTERED_COMPARISON, SELECT_REGISTERED_PROD


class ProgramLoop():
    """
    Program methods.
    """

    def __init__(self, db_connect):
        """Program initialization."""

        # Home message
        self.msgs = Statics.json_dict('./app/utils/json/app_msg.json')
        self.connect = db_connect

        # self attributes initialization
        self.category_id = None
        self.list_products = None
        self.alternative = None
        self.compared_product = None

        self.main_menu()

    def main_menu(self):
        """
        Show main menu.
        Input choice from user.
        """
        print(self.msgs['appMessages']['separator'])
        print(self.msgs['appMessages']['mainMenu'])
        list_menu = []
        list_menu += self.msgs['appChoices']['mainMenu']
        list_menu += self.msgs['appChoices']['exit']

        user_choice = Statics.input_list(list_menu)

        if user_choice == 0:
            self.category_select()

        elif user_choice == 1:
            self.search_select()

        elif user_choice == 2:
            self.registered_menu()

        elif user_choice == 3:
            sys.exit()


    def category_select(self):
        """Category selection loop"""

        self.category_id, self.list_products = self.select_by_category()
        product = self.select_product(self.list_products)

        self.product_loop(product)


    def search_select(self):
        """Text search loop"""

        print(self.msgs['appMessages']['separator'])
        self.list_products, matching = self.text_search()

        if matching:
            product = self.select_product(self.list_products)
            self.category_id = self.text_search_category(product)
            self.product_loop(product)
        else:
            self.search_select()


    def select_by_category(self):
        """
        Program loop for selection by category.
        Return list of code products.
        """

        print(self.msgs['appMessages']['separator'])
        list_categories = self.connect.list_categories()

        init = True

        nb_products = 'UNDEFINED'
        category = str()

        while True:
            if init:
                cat_choice = Statics.input_list(list_categories)
                init = False
            else:
                select_all_products = "{} : Select all {} products".format(
                    category,
                    nb_products
                )
                cat_choice = Statics.input_list(
                    list_categories,
                    select_all_products
                )


            if cat_choice != -1:
                category = list_categories[cat_choice]
                index_cat = self.connect.id_cat(category)
                list_categories = self.connect.list_categories(parent_id=index_cat)
                list_products = self.connect.list_products_by_cat(index_cat)
                nb_products = len(list_products)

                if len(list_categories) == 0:
                    return index_cat, list_products

            else:
                return index_cat, list_products


    def select_product(self, list_codes):
        """Select a product in a list"""
        print(self.msgs['appMessages']['separator'])

        list_of_products = self.connect.get_product_list(list_codes)

        product_choice = Statics.input_list(list_of_products)
        code = list_codes[product_choice]

        product = ProductGet(self.connect, code)

        return product

    def select_comparison(self, list_codes, list_compared):
        """Select product in comparison list"""

        print(self.msgs['appMessages']['separator'])

        list_of_products = self.connect.get_product_list(list_codes)
        list_of_compared_products = self.connect.get_product_list(list_compared)

        list_comparison = []
        if len(list_of_products) == len(list_of_compared_products):
            i = 0
            while i < len(list_of_products):
                comparison = list_of_products[i] + ' / ' + list_of_compared_products[i]
                list_comparison.append(comparison)
                i += 1

        comparison_choice = Statics.input_list(list_comparison)

        product_code = list_codes[comparison_choice]
        compared_code = list_compared[comparison_choice]

        product = ProductGet(self.connect, product_code)
        compared_product = ProductGet(self.connect, compared_code)

        return product, compared_product


    def product_loop(self, product, product_info=False, registered_product=False):
        """Product loop."""

        product_menu = []
        if not product_info:
            product_menu += self.msgs['appChoices']['productDetails']

        product_menu += self.msgs['appChoices']['compareBetter']
        if not registered_product:
            product_menu += self.msgs['appChoices']['saveProduct']
        product_menu += self.msgs['appChoices']['returnToMenu']
        product_menu += self.msgs['appChoices']['exit']

        user_choice = Statics.input_list(product_menu)

        if product_info:
            user_choice += 1

        if registered_product and user_choice > 1:
            user_choice += 1

        if user_choice == 0:
            # Show product infos
            product.show_infos()
            self.product_loop(product, product_info=True)

        elif user_choice == 1:
            # Compare with better product
            self.alternative, self.compared_product = self.compare_with_better_product(product)

        elif user_choice == 2:
            # Save
            self.save_product(product)

        elif user_choice == 3:
            # Return to main menu
            self.main_menu()
        elif user_choice == 4:
            # Exit
            sys.exit()


    def compare_with_better_product(self, product):
        """
        Comparison function :
            - Search for products with better nutriscore
            - Show better products in list for user choice
            - Select a product
            - Show result in table
        """

        # Selection of alternative product
        # Limit to better product
        # By category
        # Selection of category
        alternative_codes, alternative = product.get_alternative(
            self.category_id,
            self.connect
        )

        if alternative:
            compared_product = self.select_product(alternative_codes)

            # Show the table of the 2 products
            product.show_infos(compared_product=compared_product)

            list_comparison = []
            list_comparison += self.msgs['appChoices']['productComparison']
            list_comparison += self.msgs['appChoices']['returnToMenu']
            list_comparison += self.msgs['appChoices']['exit']

            user_choice = Statics.input_list(list_comparison)

            if user_choice == 0:
                # Save
                self.save_product(
                    product,
                    compared_product=compared_product
                )

            elif user_choice == 1:
                # Return to category selection
                self.compare_with_better_product(product)

            elif user_choice == 2:
                # Return to main menu
                self.main_menu()

            elif user_choice == 3:
                # Exit
                sys.exit()

        else:
            print("\nThere no products better than selected one in db :\n")

            list_no_better = []
            list_no_better += self.msgs['appChoices']['noAlternative']
            list_no_better += self.msgs['appChoices']['returnToMenu']
            list_no_better += self.msgs['appChoices']['exit']

            user_choice = Statics.input_list(list_no_better)

            if user_choice == 0:
                # Save
                self.save_product(self.connect, product)

            elif user_choice == 1:
                # Return to category selection
                self.category_select()

            elif user_choice == 2:
                # Return to main menu
                self.main_menu()

            elif user_choice == 3:
                # Exit
                sys.exit()

        return alternative, compared_product

    def save_product(self, product, compared_product=None):
        """
        Save the product
        and its compared better product if given
        into database.
        """

        cursor = self.connect.mydb.cursor()

        if compared_product is None:
            compared_value = "NULL"
        else:
            compared_value = compared_product.code

        cursor.execute(
            INSERT_REGISTRATION.format(
                product.code,
                compared_value
            )
        )
        self.connect.mydb.commit()

        print(self.msgs['appMessages']['separator'])
        print("WELL REGISTERED")


    def text_search(self):
        """Text search for matching products"""

        user_text = input(
            "\nType text to search for matching products :  >>>  "
        )

        cursor = self.connect.mydb.cursor()

        nb_products = cursor.execute(
            SELECT_PROD_TEXT.format(user_text)
        )

        if nb_products > 0:
            list_codes = []
            for row in cursor:
                list_codes.append(row[0])

            matching = True

        else:
            print("\nThere no products matching with : '", user_text, "'")

            list_codes = []
            matching = False

        return list_codes, matching

    def text_search_category(self, product):
        """
        Return category id to compare with better product
        when select product by text search
        """

        cursor = self.connect.mydb.cursor()

        cursor.execute(
            SELECT_CAT_BY_PROD.format(product.code)
        )

        list_cat = []
        for row in cursor:
            list_cat.append(row[0])

        category_id = list_cat[-1]

        return category_id


    def registered_menu(self):
        """Show registered menu"""

        print(self.msgs['appMessages']['separator'])

        registered_menu = []
        registered_menu += self.msgs['appChoices']['registeredMenu']
        registered_menu += self.msgs['appChoices']['returnToMenu']
        registered_menu += self.msgs['appChoices']['exit']

        user_choice = Statics.input_list(registered_menu)

        if user_choice == 0:
            self.registered_products()
        elif user_choice == 1:
            self.registered_products(comparison=True)
        elif user_choice == 2:
            self.main_menu()
        elif user_choice == 3:
            sys.exit()


    def registered_products(self, comparison=False):
        """
        Show list of registered products
        stored in database
        """

        cursor = self.connect.mydb.cursor()

        if comparison:
            select_registration_request = SELECT_REGISTERED_COMPARISON
            compared_item = "comparison"
        else:
            select_registration_request = SELECT_REGISTERED_PROD
            compared_item = "product"

        nb_products = cursor.execute(select_registration_request)

        if nb_products > 0:

            if not comparison:
                list_codes = []
                for row in cursor:
                    list_codes.append(row[1])

                product = self.select_product(list_codes)
                self.category_id = self.text_search_category(product)

                self.product_loop(product, registered_product=True)

            else:
                list_codes = []
                list_compared = []
                for row in cursor:
                    list_codes.append(row[1])
                    list_compared.append(row[2])

                product, compared_product = self.select_comparison(
                    list_codes,
                    list_compared
                )
                product.show_infos(compared_product=compared_product)

        else:
            print('There is no {} registered in database'.format(compared_item))

            self.registered_menu()
