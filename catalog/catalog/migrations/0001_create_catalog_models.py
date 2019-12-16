from yoyo import step

step(
    "CREATE TABLE IF NOT EXISTS product( \
        id SERIAL NOT NULL PRIMARY KEY, \
        name VARCHAR(256) NOT NULL, \
        price INTEGER \
    )",
    "DROP TABLE product",
)

step("INSERT INTO product(id, name, price) VALUES(1, 'Apple', 50)")
step("INSERT INTO product(id, name, price) VALUES(2, 'Banana', 60)")
step("INSERT INTO product(id, name, price) VALUES(3, 'Pear', 40)")
step("INSERT INTO product(id, name, price) VALUES(4, 'Apricot', 80)")
step("INSERT INTO product(id, name, price) VALUES(5, 'Orange', 25)")
