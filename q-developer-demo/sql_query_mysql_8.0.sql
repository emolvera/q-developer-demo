-- reservedKeywordsCheck
CREATE TABLE IF NOT EXISTS `interval` (`begin` INT, `end` INT);

CREATE TABLE IF NOT EXISTS `users` (
    `key` INT NOT NULL,
    `username` VARCHAR(45) DEFAULT NULL,
    `location` VARCHAR(45) DEFAULT NULL,
    PRIMARY KEY (`key`)
);

-- utf8mb4Check
CREATE TABLE IF NOT EXISTS `demo_table` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `item` VARCHAR(45) DEFAULT NULL,
    `date` DATE DEFAULT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- zeroDatesCheck
INSERT INTO demo_table (`item`, `date`)
VALUES ('item_1', '0000-00-00')
    , ('item_2', NULL)
    , ('item_3', '2024-08-07');

SELECT `id`, `item`
FROM demo_table
WHERE `date` = '0000-00-00' OR `date` IS NULL;


-- Cleanup database
DROP TABLE IF EXISTS `interval`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `demo_table`;