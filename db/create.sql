-- Feel free to modify this file to match your development goal.

CREATE TABLE UserInfo (
    uid INT GENERATED BY DEFAULT AS IDENTITY, -- defaults to primary key?
    first_name VARCHAR(255) NOT NULL,
    mid_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL,
    PRIMARY KEY (uid)
);

CREATE TABLE UserAcc (
    uid INT NOT NULL PRIMARY KEY,
    balance FLOAT NOT NULL,
    FOREIGN KEY (uid) REFERENCES UserInfo(uid)
);

CREATE TABLE Seller (
    uid INT NOT NULL PRIMARY KEY,
    FOREIGN KEY (uid) REFERENCES UserInfo(uid)
);

CREATE TABLE Products (
    product_id INT GENERATED BY DEFAULT AS IDENTITY,
    category VARCHAR(255) CHECK (category = 'a' OR category = 'b' OR category = 'c' OR category = 'd' OR category = 'e' OR category = 'f'),
    name VARCHAR(255) UNIQUE NOT NULL,
    descrip TEXT NOT NULL, -- medium or long?
    img_link VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE, -- add availability to schema
    -- FOREIGN KEY (seller_id) REFERENCES Seller(uid)
    PRIMARY KEY (product_id)
);

CREATE TABLE SellProducts (
    seller_id INT NOT NULL,
    product_id INT NOT NULL,
    current BOOLEAN DEFAULT TRUE,
    PRIMARY KEY(seller_id, product_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(uid),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Purchases (
    order_id INT GENERATED BY DEFAULT AS IDENTITY,
    seller_id INT NOT NULL,
    product_id INT NOT NULL,
    date timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    uid INT NOT NULL,
    --total_price FLOAT NOT NULL,
    num_items INT NOT NULL,
    fulfillment_status VARCHAR(255) NOT NULL,
    --FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (seller_id, product_id) REFERENCES SellProducts(seller_id, product_id),
    FOREIGN KEY (uid) REFERENCES UserInfo(uid)
);

-- primary key is combination of user and a specific product from a seller. 
-- Get everything in a user's cart using uid
CREATE TABLE UserCarts (
    uid INT NOT NULL,
    product_id INT NOT NULL,
    seller_id INT NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY (uid, seller_id, product_id),
    --FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (seller_id, product_id) REFERENCES SellProducts(seller_id, product_id),
    FOREIGN KEY (uid) REFERENCES UserInfo(uid)
);

CREATE TABLE Feedback (
    buyer_id INT NOT NULL,
    product_id INT NOT NULL,
    --seller_id INT NOT NULL PRIMARY KEY,
    rating INT NOT NULL,
    review TEXT NOT NULL,
    date timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    --FOREIGN KEY (seller_id) REFERENCES Seller(uid),
    FOREIGN KEY (buyer_id) REFERENCES UserInfo(uid),
    PRIMARY KEY (buyer_id, product_id)
);
CREATE TABLE SellerReviews (
    uid INT NOT NULL, --current user
    seller_id INT NOT NULL,
    review TEXT NOT NULL,
    rating INT NOT NULL,
    PRIMARY KEY (uid, seller_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(uid),
    FOREIGN KEY (uid) REFERENCES UserInfo(uid)
);