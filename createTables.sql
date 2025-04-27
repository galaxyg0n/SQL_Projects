--------------------------- New tables ----------------------------------
CREATE TABLE users (
    workerID          INT NOT NULL AUTO_INCREMENT,
    workerName        VARCHAR(255),
    workerPassword    VARCHAR(255),
    workerFaculty     VARCHAR(255),
    workerPermissions INT,

    PRIMARY KEY (workerID)
);

CREATE TABLE transactions (
    transactionsID       INT NOT NULL AUTO_INCREMENT,
    workerID             INT,
    componentID          INT,

    transactionTime      DATETIME,
    transactionAmount    INT,

    PRIMARY KEY (transactionsID),

    FOREIGN KEY (workerID)
        REFERENCES users(workerID),

    FOREIGN KEY (componentID)
        REFERENCES components(componentID)
);

CREATE TABLE components (
    componentID          INT NOT NULL AUTO_INCREMENT,
    componentName        VARCHAR(255),
    componentAmount      INT,

    packageID            INT,
    categoryID           INT,

    PRIMARY KEY (componentID),

    FOREIGN KEY (categoryID)
        REFERENCES categories(categoryID),

    FOREIGN KEY (packageID)
        REFERENCES packages(packageID)
    
);

CREATE TABLE categories (
    categoryID        INT NOT NULL AUTO_INCREMENT,
    componentCategory VARCHAR(255),

    PRIMARY KEY (categoryID)
);
    
CREATE TABLE packages (
    packageID         INT NOT NULL AUTO_INCREMENT,
    componentPackage  VARCHAR(255),

    PRIMARY KEY (packageID)
);
