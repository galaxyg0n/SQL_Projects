CREATE TABLE users (
    workerID          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    workerName        VARCHAR(255),
    workerPassword    VARCHAR(255),
    workerPermissions INT
);

CREATE TABLE components (
    componentID          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    componentName        VARCHAR(255),
    componentDescription VARCHAR(255),
    componentCategory    VARCHAR(255),
    componentAmount      INT
);

CREATE TABLE transactions (
    transactionsID     INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    workerID           INT,
    transactionTime    DATETIME,
    componentName      VARCHAR(255),
    transactionAmount  INT
);