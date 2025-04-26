-- First insert into 'categories'
INSERT INTO categories (componentCategory) VALUES
('Resistors'),
('Capacitors'),
('Microcontrollers'),
('Connectors');

-- Then insert into 'packages'
INSERT INTO packages (componentPackage) VALUES
('SMD 0805'),
('SMD 0603'),
('DIP-40'),
('Through Hole');

-- Now insert into 'components'
INSERT INTO components (componentName, componentAmount, packageID, categoryID) VALUES
('10k Ohm Resistor', 500, 1, 1),
('100nF Capacitor', 300, 2, 2),
('ATmega328P', 150, 3, 3),
('Male Header 40-pin', 200, 4, 4);

-- Insert into 'users'
INSERT INTO users (workerName, workerPassword, workerFaculty, workerPermissions) VALUES
('Alice Smith', 'password123', 'Electronics', 1),
('Bob Johnson', 'securePass', 'Robotics', 2),
('Charlie Davis', 'charlieD', 'Embedded Systems', 1);

-- Now insert into 'transactions'
INSERT INTO transactions (workerID, componentName, transactionTime, transactionAmount) VALUES
(1, '10k Ohm Resistor', '2025-04-25 10:30:00', 20),
(2, '100nF Capacitor', '2025-04-25 11:15:00', 15),
(3, 'ATmega328P', '2025-04-25 12:45:00', 5),
(1, 'Male Header 40-pin', '2025-04-26 09:00:00', 10);
