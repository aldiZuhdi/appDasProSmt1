Font Color:
30m = Black color
31m = Red color
32m = Green color
33m = Yellow color
34m = Blue color
35m = Purple color
36m = Cyan color
37m = White color

Background Color:
40m = Black background
41m = Red background
42m = Green background
43m = Yellow background
44m = Blue background
45m = Purple background
46m = Cyan background
47m = White background

Fonts Style:
0m = Normal fonts
1m = Bold fonts
3m = Italic fonts
4m = Underline fonts
9m = Strikethrough fonts

CREATE DATABASE db_minimarket;
USE db_minimarket;

CREATE TABLE tb_product (
id INT(11) AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255) NOT NULL,
category VARCHAR(255) NOT NULL,
weight INT(11) NOT NULL,
quantity INT(11) NOT NULL,
supplier VARCHAR(255) NOT NULL
);

CREATE TABLE users (
id INT(11) AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(16) NOT NULL,
password VARCHAR(16) NOT NULL,
position VARCHAR(25) NOT NULL
);

INSERT INTO `users` (`id`, `username`, `password`, `position`) VALUES (NULL, 'admin', 'admin', 'admin');

INSERT INTO tb_product (id)
VALUES (
CONCAT(
CHAR(FLOOR(65 + (RAND() _ 26))), -- Huruf acak (A-Z)
LPAD(FLOOR(RAND() _ 9999) + 1, 4, '0') -- Nomor acak (1-9999)
)
);
