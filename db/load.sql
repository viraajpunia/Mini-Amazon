\COPY UserInfo FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller FROM 'data/Sellers.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellProducts FROM 'data/SellProducts.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY UserCarts FROM 'data/Carts.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Feedback FROM 'data/Feedback.csv' WITH DELIMITER ',' NULL '' CSV
\COPY SellerReviews FROM 'data/SellerReviews.csv' WITH DELIMITER ',' NULL '' CSV