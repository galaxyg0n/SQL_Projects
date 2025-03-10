-- Insert dummy data into users table
INSERT INTO users (workerName, workerPassword, workerPermissions) VALUES
('Alice Johnson', 'password123', 1),
('Bob Smith', 'securePass456', 0),
('Charlie Brown', 'helloWorld789', 0);

-- Insert dummy data into components table
INSERT INTO components (componentName, componentDescription, componentCategory, componentAmount) VALUES
('10k Ohm Resistor', 'Metal Film Resistors - Through Hole 0.6W 1Kohms 1% 50ppm CECC', 'Resistor', 500),
('100nF Capacitor', 'Multilayer Ceramic Capacitors MLCC - Leaded 0.1uF 50volts 10% X7R 5mm LS', 'Capacitor', 300),
('ATmega328p', '8-bit Microcontrollers - MCU AVR 32K FLSH 2K SRAM 1KB EE-20 MHZ 105C', 'Microcontroller', 150),
('Red LED 5mm', 'SparkFun Accessories LED - Basic Red 5mm', 'LED', 1000),
('1N4007 Rectifier Diode', 'Rectifiers Diode, DO-41, 1000V, 1A', 'Diode', 400);

-- Insert dummy data into transactions table
INSERT INTO transactions (workerID, transactionTime, transactionAmount) VALUES
(1, '2025-03-10 08:30:00', 10),
(2, '2025-03-10 09:15:00', 5),
(3, '2025-03-10 10:00:00', 20),
(1, '2025-03-10 11:45:00', 15),
(2, '2025-03-10 12:30:00', 8);