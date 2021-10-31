\COPY UserInfo FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY UserAcc FROM 'data/UserAccounts.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellProducts FROM 'data/SellProducts.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
