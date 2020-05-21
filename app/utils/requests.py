"""SQL requests"""


CREATE_DB = "CREATE DATABASE IF NOT EXISTS `{}`;"

FK_CHECKS_0 = "SET FOREIGN_KEY_CHECKS = 0;"

FK_CHECKS_1 = "SET FOREIGN_KEY_CHECKS = 1;"

DROP_TABLE = "DROP TABLE {};"

SELECT_INIT_CAT = """
SELECT `name`
FROM `categories`
WHERE `parent_id` IS NULL;
"""

SELECT_CHILD_CAT = """
SELECT `name`
FROM `categories`
WHERE `parent_id`={};
"""

SELECT_CAT_BY_NAME = """
SELECT `id`
FROM `categories`
WHERE `name`="{}";
"""

SELECT_PROD_BY_CAT = """
SELECT `product_id`
FROM `cat_prod_connections`
WHERE `category_id`={};
"""

SELECT_PROD_BY_CODE = """
SELECT `name`, `brand`, `quantity`
FROM `products`
WHERE `code`="{}";
"""

"""SELECT * FROM `products` WHERE `code` = "{}" """

INSERT_CAT = """
INSERT INTO `categories`
    (`name`, `parent_id`)
VALUES
    ("{}", {});"""

INSERT_PROD_CAT_CONN = """
INSERT INTO `cat_prod_connections` (
    `product_id`,
    `category_id`
)
VALUES (
    "{}",
    {}
);
"""

INSERT_PROD = """
INSERT INTO `products`
    ({})
VALUES
    ({});
"""

SELECT_ALTERNATIVE = """
SELECT `code`, `name`
FROM `products`
INNER JOIN `cat_prod_connections`
    WHERE
        products.code = cat_prod_connections.product_id
        AND category_id = {}
        AND products.nutriscore <= "{}"
        AND products.code != {}
"""

INSERT_REGISTRATION = """
INSERT INTO
    `registrations`
    (
        `product`,
        `compared_product`
    )
VALUES
    (
        {},
        {}
    )
"""

SELECT_PROD_TEXT = """
SELECT `code`, `name`
FROM `products`
WHERE
    products.name LIKE "%{0}%"
    OR products.brand LIKE "%{0}%"
"""

SELECT_CAT_BY_PROD = """
SELECT `category_id`
FROM `cat_prod_connections`
WHERE `product_id` = "{}"
"""

SELECT_REGISTERED_COMPARISON = """
SELECT *
FROM `registrations`
WHERE
    `compared_product` IS NOT NULL
"""

SELECT_REGISTERED_PROD = """
SELECT *
FROM `registrations`
WHERE
    `compared_product` IS NULL
"""