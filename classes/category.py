import requests


class Category():
    """ """

    def __init__(self, mydb, category):
        """Create a cursor. Search for category in db.
nb_lines return :
    - 0 if category not exists yet in db
    - 1 if category already exists
    - > 1 if there are several categories with same name
        --> Should not happen."""
        self.cursor = mydb.cursor()
        str_req = """SELECT * FROM `categories` WHERE `name`="{}";""".format(category)

        self.nb_lines = self.cursor.execute(str_req)
        
    def check_import(self, mydb, category, index, list_categories):
        """Check if category exists in db. Create or update parent_id line if necessary."""

        if self.nb_lines == 0:
            parent_line = """SELECT `id` FROM `categories` WHERE `name`="{}";""".format(
                list_categories[index - 1]
            )
            nb_parent = self.cursor.execute(parent_line)
            if nb_parent == 1:
                for parent in self.cursor:
                    parent_id = parent[0]
                insert_req = """INSERT INTO `categories` (`name`, `parent_id`) VALUES ("{}", {});""".format(
                    category,
                    parent_id
                )
            elif nb_parent == 0:
                insert_req = """INSERT INTO `categories` (`name`, `parent_id`) VALUES ("{}", NULL);""".format(
                    category
                )
            else:
                print("Too many parents")
            self.cursor.execute(insert_req)
            line_id = self.cursor.lastrowid
            return line_id
        elif self.nb_lines == 1:
            line = self.cursor.fetchone()
            return line[0]
        else:
            print('Too many categories')

        # Save categories in db
        mydb.commit()

    def product_connection(self, mydb, code, id_cat):
        """Create link between product and given category"""
        insert_prod_cat = """
INSERT INTO `cat_prod_connections` (
    `product_id`,
    `category_id`
)
VALUES (
    "{}",
    {}
);
""".format(
    code,
    int(id_cat)
)
        # print(insert_prod_cat)

        self.cursor.execute(insert_prod_cat)

        mydb.commit()