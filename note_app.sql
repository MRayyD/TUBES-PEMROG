-- Create the database
CREATE DATABASE note_app;

-- Create a user with a password
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges to the user on the note_app database
GRANT ALL PRIVILEGES ON note_app.* TO 'your_username'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;

-- Use the newly created database
USE note_app;

-- Create the User table
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL
);

-- Create the Note table
CREATE TABLE note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- Create the Notebook table
CREATE TABLE notebook (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    content TEXT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);