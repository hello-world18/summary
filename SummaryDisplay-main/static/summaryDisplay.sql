CREATE DATABASE flask_auth_new;
USE flask_auth_new;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);
INSERT INTO users (username, password, role)
VALUES
('admin', 'admin123', 'admin');

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file1_path VARCHAR(255) NOT NULL, -- opd
    file2_path VARCHAR(255) NOT NULL, -- lis
    file3_path VARCHAR(255) NOT NULL, -- OT
    file4_path VARCHAR(255) NOT NULL, -- Biopsy
    file5_path VARCHAR(255) NOT NULL, -- bedOccupancy_path
    file6_path VARCHAR(255) NOT NULL, -- ipdDischarge_path
    file7_path VARCHAR(255) NOT NULL, -- Ris_path
    date DATE NOT NULL
);

INSERT INTO files (file1_path, file2_path, file3_path, file4_path, file5_path, file6_path, file7_path, `date`)
VALUES
('uploads\\Daily Patient List - OPD.xlsx',
'uploads\\TestBasedInvestigationReport.xlsx',
'uploads\\OT Register.xlsx',
'uploads\\Departmnet wise statisctic Report.xlsx',
'uploads\\Bed Occupancy Report.xlsx',
'uploads\\IPD Patient Discharge List.xlsx',
'uploads\\RIS Register.xlsx',
'2024-12-31'),

('uploads\\Daily Patient List - OPD (1).xlsx',
'uploads\\TestBasedInvestigationReport (1).xlsx',
'uploads\\OT Register (1).xlsx',
'uploads\\Departmnet wise statisctic Report (1).xlsx',
'uploads\\Bed Occupancy Report (1).xlsx',
'uploads\\IPD Patient Discharge List (1).xlsx',
'uploads\\RIS Register (1).xlsx',
'2025-01-01'),

('uploads\\Daily Patient List - OPD (2).xlsx',
'uploads\\TestBasedInvestigationReport (2).xlsx',
'uploads\\OT Register (2).xlsx',
'uploads\\Departmnet wise statisctic Report (2).xlsx',
'uploads\\Bed Occupancy Report (2).xlsx',
'uploads\\IPD Patient Discharge List (2).xlsx',
'uploads\\RIS Register (2).xlsx',
'2025-01-02'),

('uploads\\Daily Patient List - OPD (3).xlsx',
'uploads\\TestBasedInvestigationReport (3).xlsx',
'uploads\\OT Register (3).xlsx',
'uploads\\Departmnet wise statisctic Report (3).xlsx',
'uploads\\Bed Occupancy Report (3).xlsx',
'uploads\\IPD Patient Discharge List (3).xlsx',
'uploads\\RIS Register (3).xlsx',
'2025-01-03'),

('uploads\\Daily Patient List - OPD (4).xlsx',
'uploads\\TestBasedInvestigationReport (4).xlsx',
'uploads\\OT Register (4).xlsx',
'uploads\\Departmnet wise statisctic Report (4).xlsx',
'uploads\\Bed Occupancy Report (4).xlsx',
'uploads\\IPD Patient Discharge List (4).xlsx',
'uploads\\RIS Register (4).xlsx',
'2025-01-04'),

('uploads\\Daily Patient List - OPD (5).xlsx',
'uploads\\TestBasedInvestigationReport (5).xlsx',
'uploads\\OT Register (5).xlsx',
'uploads\\Departmnet wise statisctic Report (5).xlsx',
'uploads\\Bed Occupancy Report (5).xlsx',
'uploads\\IPD Patient Discharge List (5).xlsx',
'uploads\\RIS Register (5).xlsx',
'2025-01-05'),

('uploads\\Daily Patient List - OPD (6).xlsx',
'uploads\\TestBasedInvestigationReport (6).xlsx',
'uploads\\OT Register (6).xlsx',
'uploads\\Departmnet wise statisctic Report (6).xlsx',
'uploads\\Bed Occupancy Report (6).xlsx',
'uploads\\IPD Patient Discharge List (6).xlsx',
'uploads\\RIS Register (6).xlsx',
'2025-01-06'),

('uploads\\Daily Patient List - OPD (7).xlsx',
'uploads\\TestBasedInvestigationReport (7).xlsx',
'uploads\\OT Register (7).xlsx',
'uploads\\Departmnet wise statisctic Report (7).xlsx',
'uploads\\Bed Occupancy Report (7).xlsx',
'uploads\\IPD Patient Discharge List (7).xlsx',
'uploads\\RIS Register (7).xlsx',
'2025-01-07'),

('uploads\\Daily Patient List - OPD (8).xlsx',
'uploads\\TestBasedInvestigationReport (8).xlsx',
'uploads\\OT Register (8).xlsx',
'uploads\\Departmnet wise statisctic Report (8).xlsx',
'uploads\\Bed Occupancy Report (8).xlsx',
'uploads\\IPD Patient Discharge List (8).xlsx',
'uploads\\RIS Register (8).xlsx',
'2025-01-08');



CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    opd_required INT NOT NULL
);
INSERT INTO departments (name, opd_required)
VALUES
('Dermatology', 75),
('Dentistry', 35),
('General Medicine', 80),
('General Surgery', 85),
('Gynaecology And Obstetrics', 85),
('Orthopaedics', 65),
('Pediatrics', 70),
('Plastic Surgery', 35),
('Psychiatry', 65),
('Respiratory Medicine', 72),
('Urology', 40);
