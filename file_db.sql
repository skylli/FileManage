-- in shell : mysql -uroot -psky test < ./file_db.sql
-- in mysql commond : source ./file_db.sql
DROP TABLE IF EXISTS `refer_file_type`;
DROP TABLE IF EXISTS `refer_address_type`;
DROP TABLE IF EXISTS `file_map`;
DROP TABLE IF EXISTS `file_type`;
DROP TABLE IF EXISTS `address_type`;


CREATE TABLE `file_type` (
    `id` INT(12) PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL UNIQUE,
    `description` VARCHAR(128)
);
CREATE INDEX `i_file_type` ON `file_type`(`name`);

CREATE TABLE `address_type` (
    `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(32) NOT NULL UNIQUE,
    `description` VARCHAR(128)
);
CREATE INDEX `i_address_type` ON `address_type`(`name`);

CREATE TABLE `file_map` (
    `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `idex`VARCHAR(64) NOT NULL UNIQUE,
    `name` VARCHAR(64),
    `address` VARCHAR(128) NOT NULL,
    `description` VARCHAR(128)
);
CREATE INDEX `i_file_map` ON `file_map`(`idex`);
CREATE TABLE `refer_file_type`(
    `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `file_map_id` INT(11)  NOT NULL,
    `file_type_id` INT(11)  NOT NULL,

    FOREIGN KEY(`file_map_id`) REFERENCES `file_map`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`file_type_id`) REFERENCES `file_type`(`id`) ON DELETE CASCADE
);  

CREATE TABLE `refer_address_type`(
    `id` INT(11) PRIMARY KEY AUTO_INCREMENT,
    `file_map_id` INT(11)  NOT NULL,
    `address_type_id` INT(11)  NOT NULL,
    FOREIGN KEY(`file_map_id`) REFERENCES `file_map`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`address_type_id`) REFERENCES `address_type`(`id`) ON DELETE CASCADE
);

INSERT INTO file_type (name,description) VALUES ("pdf","adobe pdf");
INSERT INTO file_type (name,description) VALUES ("text","text document");
INSERT INTO file_type (name,description) VALUES ("other","unknow document");


INSERT INTO address_type (name,description) VALUES ("path","local file");
INSERT INTO address_type (name,description) VALUES ("ftp","ftp://");
INSERT INTO file_map (idex,address,name,description) VALUES ("001","/tmp/test","path","test");
INSERT INTO file_map (idex,address,name,description) VALUES ("002","/tmp/","path","test");
