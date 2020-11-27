# @author Alex Gomes
# @create date 2020-11-09 22:10:27
# @modify date 2020-11-25 05:51:39
# @desc [Database specific data like queries, connection, engine, etc...]

from sqlalchemy.engine import create_engine

from modules.config import config

url = f"{config['SQL_DIALECT']}+{config['SQL_DRIVER']}://{config['USERNAME']}:{config['PASSWORD']}@{config['HOST']}:{config['PORT']}/{config['SID']}"

engine = create_engine(url, max_identifier_length=128)
con = engine.connect()

stamp_queries = {
    'CREATE': r"""CREATE TABLE Accounts (
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

    CREATE TABLE LoginInformation (
        email CHAR(255) NOT NULL UNIQUE PRIMARY KEY,
        username CHAR(255) NOT NULL,
        user_password CHAR(255) NOT NULL
    );

    CREATE TABLE CreditCardInformation (
        card_number CHAR(255) NOT NULL PRIMARY KEY,
        expiration_date date NOT NULL,
        name_on_card CHAR(255) NOT NULL
    );""",

    'POPULATE': r"""INSERT INTO accounts VALUES (1, 'jordan.quan@ryerson.ca', 'jordanquannn', '12345678', '1999-Jul-9');
    INSERT INTO accounts VALUES (2, 'amassin@ryerson.ca', 'amassin', 'abcdefg', '1999-Sep-8');
    INSERT INTO accounts VALUES (3, 'alex.gomes@ryerson.ca', 'glex', 'a1b2c3d4', '1999-Mar-26');
    INSERT INTO accounts VALUES (4, 'sony@gmail.ca', 'sony', 'playstation', null);
    INSERT INTO accounts VALUES (5, 'marvel@gmail.ca', 'marvel', 'ironman', null);

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

    INSERT INTO financialinformation VALUES (1, '1234567890123456', '2022-Sep-30', 'Jordan Quan', 1);
    INSERT INTO financialinformation VALUES (2, '1234567890123457', '2022-Aug-30', 'Alex Massin', 2);
    INSERT INTO financialinformation VALUES (3, '1234567890123458', '2022-Jul-30', 'Alex Gomes', 3);
    INSERT INTO financialinformation VALUES (4, '1234567890123459', '2023-Jul-30', 'Sony', 4);
    INSERT INTO financialinformation VALUES (5, '1234567890123450', '2023-Mar-30', 'Marvel', 5);

    select * from vendors;

    INSERT INTO products VALUES (1, 'Spiderman VR', 'CreateVR', 'Sony Pictures Virtual Reality', 'PC', 0.00, 2100, 'OS: Windows 10 or higher, Proccessor: Intel Core i5 or higher', 1);
    INSERT INTO products VALUES (2, 'Marvel''s Avengers', 'Crystal Dynamics', 'Square Enix', 'PC', 79.99, 75000, 'OS: Windows 10 64 bit, Proccessor: i3-4160 or AMD equivalent', 2);
    INSERT INTO products VALUES (3, 'ShareX', 'ShareX Team', 'ShareX Team', 'PC', 0.00, 150, 'OS: Windows 7 Service Pack 1', 1);

    INSERT INTO games VALUES (1, null, null, 'E', 'VR, Action', 'English, French, Spanish', 1);
    INSERT INTO games VALUES (2, null, null, 'teen', 'Action, Adventure', 'English, French, Spanish, German', 2);

    INSERT INTO dlcs VALUES (1, 'Marvel''s Avengers: Deluxe Upgrade', null, 26.99, 5000, 2);

    INSERT INTO software VALUES(1, null, 3);

    INSERT INTO transactions VALUES(1, '2020-Jul-18', 1, 2);
    INSERT INTO transactions VALUES(2, '2020-Sep-7', 2, 2);
    INSERT INTO transactions VALUES(3, '2019-Aug-18', 3, 1);

    INSERT INTO reviews VALUES(1, '2020-Jul-21', 5, 'Great Game!', 1, 2);""",

    "DESTROY": r"""DROP TABLE Accounts CASCADE CONSTRAINTS;
DROP TABLE Customers CASCADE CONSTRAINTS;
DROP TABLE Software CASCADE CONSTRAINTS; 
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
DROP TABLE CreditCardInformation CASCADE CONSTRAINTS;""",

    "RESET": r"""delete from Accounts;
delete from Customers;
delete from Software; 
delete from Vendors;
delete from AccountWallet;
delete from FinancialInformation;
delete from Products;
delete from Games;
delete from DLCs;
delete from Reviews;
delete from Transactions;"""
}