# @author Alex Gomes
# @create date 2020-11-09 22:10:27
# @modify date 2020-12-01 22:29:48
# @desc [Database specific data like queries, connection, engine, etc...]

from sqlalchemy.engine import create_engine

from modules.config import config

url = f"{config['SQL_DIALECT']}+{config['SQL_DRIVER']}://{config['USERNAME']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['SID']}"

engine = create_engine(url, max_identifier_length=128)

stamp_queries = {
    'CREATE': r"""CREATE TABLE LoginInformation (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    username CHAR(255) NOT NULL,
    user_password CHAR(255) NOT NULL
);

CREATE TABLE CreditCardInformation (
    card_number VARCHAR(255) NOT NULL PRIMARY KEY,
    expiration_date date NOT NULL,
    name_on_card CHAR(255) NOT NULL
);

CREATE TABLE Accounts (
    account_id int NOT NULL PRIMARY KEY,
    account_email VARCHAR(255) NOT NULL REFERENCES LoginInformation(email),
    birth_date date
);

CREATE TABLE Customers (
    customer_id int NOT NULL PRIMARY KEY,
    profile_name VARCHAR(255) NOT NULL,
    account_id int NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    ON DELETE CASCADE
);

CREATE TABLE Vendors (
    vendor_id int NOT NULL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    rating int,
    account_id int NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    ON DELETE CASCADE
);

CREATE TABLE AccountWallet (
    wallet_id int NOT NULL PRIMARY KEY,
    balance DECIMAL DEFAULT 0,
    account_id int NOT NULL,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
    ON DELETE CASCADE
);

CREATE TABLE FinancialInformation (
    card_id int NOT NULL PRIMARY KEY,
    fin_card_number VARCHAR(255) NOT NULL REFERENCES CreditCardInformation(card_number),
    wallet_id int NOT NULL,
    FOREIGN KEY (wallet_id) REFERENCES AccountWallet(wallet_id)
    ON DELETE CASCADE
);

CREATE TABLE Products (
    product_id int NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    developer VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    supported_systems VARCHAR(255) NOT NULL,
    price DECIMAL(5,2) NOT NULL,
    size_of_download int NOT NULL,
    system_requirements VARCHAR(255),
    vendor_id int NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id)
    ON DELETE CASCADE
);

CREATE TABLE Games (
    game_id int NOT NULL PRIMARY KEY,
    reccomendations VARCHAR(255),
    achievements VARCHAR(255),
    ersb_rating VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    supported_languages VARCHAR(255) NOT NULL,
    product_id int NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE
);


CREATE TABLE DLCs (
    dlc_id int NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    ratings int,
    price DECIMAL(5,2) NOT NULL,
    size_of_download int NOT NULL,
    game_id int NOT NULL,
    FOREIGN KEY (game_id) REFERENCES Games(game_id)
    ON DELETE CASCADE
);

CREATE TABLE Software (
    software_id int NOT NULL PRIMARY KEY,
    documentations CHAR(255),
    product_id int NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
    ON DELETE CASCADE
);

CREATE TABLE Reviews (
    review_id int NOT NULL PRIMARY KEY,
    date_added date NOT NULL,
    rating int NOT NULL,
    comments CHAR(255),
    customer_id int NOT NULL,
    product_id int NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Transactions (
    transaction_id int NOT NULL PRIMARY KEY,
    transaction_date date NOT NULL,
    customer_id int NOT NULL,
    product_id int NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE VIEW accounts_transactions AS (   
SELECT customers.*, (SELECT COUNT(*) 
    FROM transactions 
    WHERE transactions.customer_id = customers.customer_id) 
    AS TOTAL_CUSTOMER_TRANSACTIONS
    FROM customers);

CREATE VIEW game_products as (
SELECT products.* 
    FROM products 
    INNER JOIN games 
    ON products.product_id = games.product_id
);

CREATE VIEW accounts_age AS (
SELECT accounts.account_email,
accounts.birth_date,
    accounts.account_id,
    TRUNC(((CURRENT_DATE - accounts.birth_date) / 365.25)) 
    as age FROM accounts);""",

    'POPULATE': r"""INSERT INTO logininformation VALUES ('jordan.quan@ryerson.ca', 'jordanquannn', 'edccb61d3da1ba223a1fbaf105360b25a9b284803706f425d36677e1a1023838');
INSERT INTO logininformation VALUES ('amassin@ryerson.ca', 'amassin', '9a3f6f15a0c08807311bb89548465f9f2cccea52b427128c5a08c4968dbebb77');
INSERT INTO logininformation VALUES ('alex.gomes@ryerson.ca', 'glex', 'b7a4d7f0fd11f4cf305895f7de1661047744f0744b4cb4dd54e43b9f49c3dd1d');
INSERT INTO logininformation VALUES ('sony@gmail.ca', 'sony', 'bf350b3918ab239d4755a72a723c4974818830aa9e47c9c826864d67face556c');
INSERT INTO logininformation VALUES ('marvel@gmail.ca', 'marvel', '6544425b86d3bf1cfba7fa83d9728e9eccff64c8d513484cbee1991b7985c60e');

INSERT INTO accounts VALUES (1, 'jordan.quan@ryerson.ca', '09-Jul-1999');
INSERT INTO accounts VALUES (2, 'amassin@ryerson.ca', '09-Sep-1999');
INSERT INTO accounts VALUES (3, 'alex.gomes@ryerson.ca', '26-Mar-1999');
INSERT INTO accounts VALUES (4, 'sony@gmail.ca', null);
INSERT INTO accounts VALUES (5, 'marvel@gmail.ca', null);

INSERT INTO customers VALUES (1, 'jordanq5', 1);
INSERT INTO customers VALUES (2, 'amassin8', 2);
INSERT INTO customers VALUES (3, 'glex26', 3);

INSERT INTO vendors VALUES (1, 'Sony', 5, 4);
INSERT INTO vendors VALUES (2, 'Marvel', 5, 5);

INSERT INTO accountwallet VALUES (1, 0, 1);
INSERT INTO accountwallet VALUES (2, 10, 2);
INSERT INTO accountwallet VALUES (3, 50, 3);
INSERT INTO accountwallet VALUES (4, 13, 4);
INSERT INTO accountwallet VALUES (5, 7, 5);

INSERT INTO CreditCardInformation VALUES ('1234567890123456', '30-Sep-2022', 'Jordan Quan');
INSERT INTO CreditCardInformation VALUES ('1234567890123457', '30-Aug-2022', 'Alex Massin');
INSERT INTO CreditCardInformation VALUES ('1234567890123458', '30-Jul-2022', 'Alex Gomes');
INSERT INTO CreditCardInformation VALUES ('1234567890123459', '30-Jul-2023', 'Sony');
INSERT INTO CreditCardInformation VALUES ('1234567890123450', '30-Mar-2023', 'Marvel');

INSERT INTO financialinformation VALUES (1,'1234567890123456', 1);
INSERT INTO financialinformation VALUES (2,'1234567890123457', 2);
INSERT INTO financialinformation VALUES (3,'1234567890123458', 3);
INSERT INTO financialinformation VALUES (4,'1234567890123459', 4);
INSERT INTO financialinformation VALUES (5, '1234567890123450', 5);

INSERT INTO products VALUES (1, 'Spiderman VR', 'CreateVR', 'Sony Pictures Virtual Reality', 'PC', 0.00, 2100, 'OS: Windows 10 or higher, Proccessor: Intel Core i5 or higher', 1);
INSERT INTO products VALUES (2, 'Marvel''s Avengers', 'Crystal Dynamics', 'Square Enix', 'PC', 79.99, 75000, 'OS: Windows 10 64 bit, Proccessor: i3-4160 or AMD equivalent', 2);
INSERT INTO products VALUES (3, 'ShareX', 'ShareX Team', 'ShareX Team', 'PC', 0.00, 150, 'OS: Windows 7 Service Pack 1', 1);
INSERT INTO products VALUES (4, 'Civilization VI', 'Firaxis Games', ' 2k', 'PC', 79.99, 150, 'OS: Windows 7 Service Pack 1', 1);

INSERT INTO games VALUES (1, null, null, 'E', 'VR, Action', 'English, French, Spanish', 1);
INSERT INTO games VALUES (2, null, null, 'teen', 'Action, Adventure', 'English, French, Spanish, German', 2);

INSERT INTO dlcs VALUES (1, 'Marvel''s Avengers: Deluxe Upgrade', null, 26.99, 5000, 2);

INSERT INTO software VALUES(1, null, 3);
INSERT INTO software VALUES(2, null, 3);
INSERT INTO software VALUES(3, null, 2);

INSERT INTO transactions VALUES(1, '18-Jul-2020', 1, 2);
INSERT INTO transactions VALUES(2, '7-Sep-2020', 2, 2);
INSERT INTO transactions VALUES(3, '18-Aug-2019', 3, 1);
INSERT INTO transactions VALUES(4, '15-Sep-2020', 2, 4);
INSERT INTO transactions VALUES(5, '15-Sep-2020', 1, 2);

INSERT INTO reviews VALUES(1, '21-Jul-2020', 5, 'Great Game!', 1, 2);""",

    "DESTROY": r"""DROP TABLE Accounts CASCADE CONSTRAINTS;
DROP TABLE Customers CASCADE CONSTRAINTS;
DROP TABLE Vendors CASCADE CONSTRAINTS;
DROP TABLE AccountWallet CASCADE CONSTRAINTS;
DROP TABLE FinancialInformation CASCADE CONSTRAINTS;
DROP TABLE Products CASCADE CONSTRAINTS;
DROP TABLE Games CASCADE CONSTRAINTS;
DROP TABLE DLCs CASCADE CONSTRAINTS;
DROP TABLE Software CASCADE CONSTRAINTS;
DROP TABLE Reviews CASCADE CONSTRAINTS;
DROP TABLE Transactions CASCADE CONSTRAINTS;
DROP TABLE LoginInformation CASCADE CONSTRAINTS;
DROP TABLE CreditCardInformation CASCADE CONSTRAINTS;
DROP VIEW accounts_transactions;
DROP VIEW game_products;
DROP VIEW accounts_age;""",

    "QUERIES": [
        r"SELECT * FROM accounts ORDER BY account_id ASC;",
        r"SELECT * FROM accountwallet WHERE balance > 10;",
        r"SELECT * FROM customers WHERE customer_id = 1;",
        r"SELECT * FROM dlcs;",
        r"SELECT * FROM creditcardinformation WHERE expiration_date BETWEEN DATE'2020-01-01' AND DATE'2022-12-31';",
        r"SELECT * FROM GAMES WHERE genre LIKE '%VR%';",
        r"SELECT title, developer, publisher FROM products ORDER BY size_of_download DESC;",
        r"SELECT * FROM vendors WHERE rating > 3 ORDER BY company_name;",
        r"SELECT transaction_id, transaction_date, product_id FROM transactions WHERE product_id = 2;",
        r"SELECT software_id, product_id FROM software;",
        r"SELECT * FROM reviews WHERE comments IS NOT NULL;",
        r"""SELECT price, title, developer, product_id
   FROM game_products
   WHERE price = 0
   ORDER BY title DESC;""",
        r"""SELECT products.title, COUNT(transactions.transaction_id) AS CopiesSold FROM transactions
LEFT JOIN products ON transactions.product_id = products.product_id
GROUP BY title;""",
        r"""SELECT *
   FROM products
   INNER JOIN games ON products.product_id = games.product_id
   INNER JOIN software ON products.product_id = software.product_id
   WHERE products.developer = 'Crystal Dynamics';""",
        r"""SELECT DISTINCT title FROM (
SELECT * FROM Products
INNER JOIN (
    SELECT * FROM (
        SELECT Games.product_id FROM Games
        UNION
        SELECT Software.product_id FROM Software
        ) GamesAndSoftware
    INTERSECT
    SELECT Transactions.product_id FROM Transactions
) SoldProducts
ON Products.product_id = SoldProducts.product_id)
ORDER BY title DESC;""",
        r"""SELECT accounts_age.age, ROUND(2, AVG(accounts_transactions.TOTAL_CUSTOMER_TRANSACTIONS))
   FROM accounts_age
   INNER JOIN accounts_transactions
   ON accounts_transactions.account_id = accounts_age.account_id
   GROUP BY age;""",
    ]
}