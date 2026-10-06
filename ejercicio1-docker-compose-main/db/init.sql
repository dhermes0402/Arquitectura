CREATE DATABASE authentication;
CREATE DATABASE shop;

USE authentication;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salted_pass VARCHAR(255) NOT NULL
);

INSERT INTO users (user_name, password, salted_pass)
VALUES ('mortadelo', SHA2(CONCAT('filemon', 'test_salt'), 256), 'test_salt');

USE shop;
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255),
    price DECIMAL(10, 2),
    stock INT NOT NULL
);

INSERT INTO products (name, description, image_url, price, stock)
VALUES ('Product 1', 'Description 1', 'https://m.media-amazon.com/images/I/81DwU9DYBvL.jpg', 19.99, 10),
       ('Product 2', 'Description 2', 'https://m.media-amazon.com/images/I/51uWZNm+bXL._SL500_.jpg', 29.99, 5);

