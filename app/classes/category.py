"""Categories checks and imports"""
from app.utils.requests import SELECT_CAT_BY_NAME
from app.utils.requests import INSERT_CAT, INSERT_PROD_CAT_CONN

class Category():
    """
    Check if category is importable.
    Import category and connections with product.
    """

    def __init__(self, mydb, category):
        """
        Create a cursor. Search for category in db.
        nb_lines return :
            - 0 if category not exists yet in db
            - 1 if category already exists
            - > 1 if there are several categories with same name
                --> Should not happen.
        """
        self.cursor = mydb.cursor()

        self.nb_lines = self.cursor.execute(
            SELECT_CAT_BY_NAME.format(category)
        )


    def check_import(self, mydb, category, index, list_categories):
        """
        Check if category exists in db.
        Create or update parent_id line if necessary.
        """

        if self.nb_lines == 0:
            nb_parent = self.cursor.execute(
                SELECT_CAT_BY_NAME.format(
                    list_categories[index - 1]
                )
            )
            if nb_parent == 1:
                parent_id = self.cursor.fetchone()[0]
            elif nb_parent == 0:
                parent_id = "NULL"
            else:
                print("Too many parents")
            self.cursor.execute(
                INSERT_CAT.format(
                    category,
                    parent_id
                )
            )
            line_id = self.cursor.lastrowid

        elif self.nb_lines == 1:
            line_id = self.cursor.fetchone()[0]

        else:
            print('Too many categories')
            line_id = None

        # Save categories in db
        mydb.commit()

        return line_id

    def product_connection(self, mydb, code, id_cat):
        """Create link between product and given category"""

        self.cursor.execute(
            INSERT_PROD_CAT_CONN.format(
                code,
                int(id_cat)
            )
        )

        # Save db
        mydb.commit()
