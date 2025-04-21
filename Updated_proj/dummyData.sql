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
('1N4007 Rectifier Diode', 'Rectifiers Diode, DO-41, 1000V, 1A', 'Diode', 400),
('1k Ohm Resistor', 'Carbon Film Resistors - Through Hole 1K Ohm 1/4W 5%', 'Resistor', 600),
('22pF Capacitor', 'Ceramic Capacitors 22pF 50V 5% Radial', 'Capacitor', 250),
('STM32F103C8T6', '32-bit ARM Cortex-M3 Microcontroller 64KB Flash 20KB SRAM', 'Microcontroller', 120),
('Blue LED 5mm', 'LED - Basic Blue 5mm 3.2V 20mA', 'LED', 900),
('Schottky Diode 1N5819', 'Schottky Barrier Diode, DO-41, 40V, 1A', 'Diode', 350),
('470uF Electrolytic Capacitor', 'Aluminum Electrolytic Capacitor 470uF 25V Radial', 'Capacitor', 180),
('ESP8266 WiFi Module', 'Wi-Fi Module with 32-bit MCU and TCP/IP Stack', 'Module', 75),
('BC547 NPN Transistor', 'NPN Bipolar Junction Transistor, TO-92, 45V, 100mA', 'Transistor', 500),
('LM7805 Voltage Regulator', 'Linear Voltage Regulator 5V 1A TO-220', 'Voltage Regulator', 220),
('74HC595 Shift Register', '8-bit Serial-In Parallel-Out Shift Register', 'IC', 300),
('LM358 Op-Amp', 'Operational Amplifier Dual 32V 1MHz 0.7V/us', 'IC', 400),
('Push Button Switch', 'Tactile Switch SPST 6mm x 6mm 5mm Height', 'Switch', 800),
('Piezo Buzzer', 'Electronic Buzzer 3-24V 4kHz', 'Buzzer', 150),
('MQ-2 Gas Sensor', 'Gas Sensor Module for LPG, CO, Smoke Detection', 'Sensor', 100),
('DHT11 Temperature Sensor', 'Temperature and Humidity Sensor 3-5V', 'Sensor', 130);


-- Insert dummy data into transactions table
INSERT INTO transactions (workerID, transactionTime, transactionAmount) VALUES
(1, '2025-03-10 08:30:00', 10),
(2, '2025-03-10 09:15:00', 5),
(3, '2025-03-10 10:00:00', 20),
(1, '2025-03-10 11:45:00', 15),
(2, '2025-03-10 12:30:00', 8);