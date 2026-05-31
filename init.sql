DROP TABLE IF EXISTS Teacher_Discipline_Group CASCADE;
DROP TABLE IF EXISTS Dean CASCADE;
DROP TABLE IF EXISTS Teacher CASCADE;
DROP TABLE IF EXISTS Student CASCADE;
DROP TABLE IF EXISTS StudentGroup CASCADE;
DROP TABLE IF EXISTS Person CASCADE;
DROP TABLE IF EXISTS Discipline CASCADE;
DROP TABLE IF EXISTS Department CASCADE;
DROP TABLE IF EXISTS Faculty CASCADE;
DROP TABLE IF EXISTS University CASCADE;

CREATE TABLE University (
    Name VARCHAR(100) PRIMARY KEY
);

INSERT INTO University VALUES ('Київський національний університет');

CREATE TABLE Faculty (
    Name VARCHAR(100) PRIMARY KEY,
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    FoundationDate DATE,
    UniName VARCHAR(100),
    FOREIGN KEY (UniName) REFERENCES University(Name) ON DELETE CASCADE
);

INSERT INTO Faculty VALUES ('ФКНК', 'пр. Академіка Глушкова, 4д', '044-204-91-13', 'csc@knu.ua', '1969-09-01', 'Київський національний університет');

CREATE TABLE Department (
    Name VARCHAR(100) PRIMARY KEY,
    HeadName VARCHAR(100),
    Office VARCHAR(10),
    Email VARCHAR(100),
    FacultyName VARCHAR(100),
    FOREIGN KEY (FacultyName) REFERENCES Faculty(Name) ON DELETE CASCADE
);

INSERT INTO Department VALUES ('ТК', 'Крак Ю.В.', '401', 'kafedratk@unicyb.kiev.ua', 'ФКНК');

CREATE TABLE Discipline (
    DeptName VARCHAR(100), 
    Name VARCHAR(100),     
    Credits INT,
    HasExam BOOLEAN,
    PRIMARY KEY (DeptName, Name),
    FOREIGN KEY (DeptName) REFERENCES Department(Name) ON DELETE CASCADE
);

INSERT INTO Discipline VALUES 
('ТК', 'Бази даних', 5, TRUE),
('ТК', 'Python', 6, TRUE);

CREATE TABLE Person (
    PassportID VARCHAR(20) PRIMARY KEY,
    FullName VARCHAR(100),
    BirthDate DATE,
    Email VARCHAR(100),
    Phone VARCHAR(20)
);

INSERT INTO Person VALUES 
('ID001', 'Іваненко Іван Іванович', '2005-05-15', 'ivan@mail.com', '0931112233'),
('ID002', 'Петренко Петро Петрович', '1975-10-20', 'petrenko@kpi.ua', '0504445566'),
('ID004', 'Мельник Олексій Степанович', '1970-01-01', 'melnyk@knu.ua', '0671112233');

CREATE TABLE StudentGroup (
    Name VARCHAR(20) PRIMARY KEY,
    EnrollmentYear INT,
    Course INT,
    DeptName VARCHAR(100),
    FOREIGN KEY (DeptName) REFERENCES Department(Name)
);

INSERT INTO StudentGroup VALUES ('ТК-31', 2023, 2, 'ТК');

CREATE TABLE Student (
    PassportID VARCHAR(20) PRIMARY KEY,
    RecordBookID VARCHAR(20) UNIQUE,
    AdmissionYear INT,
    StudyForm VARCHAR(20),
    GroupName VARCHAR(20),
    FOREIGN KEY (PassportID) REFERENCES Person(PassportID) ON DELETE CASCADE,
    FOREIGN KEY (GroupName) REFERENCES StudentGroup(Name)
);

INSERT INTO Student VALUES ('ID001', 'КВ-123456', 2022, 'Денна', 'ТК-31');

CREATE TABLE Teacher (
    PassportID VARCHAR(20) PRIMARY KEY,
    Position VARCHAR(50),
    AcademicDegree VARCHAR(50),
    DeptName VARCHAR(100),
    FOREIGN KEY (PassportID) REFERENCES Person(PassportID) ON DELETE CASCADE,
    FOREIGN KEY (DeptName) REFERENCES Department(Name)
);

INSERT INTO Teacher VALUES 
('ID002', 'Доцент', 'Кандидат техн. наук', 'ТК'),
('ID004', 'Завідувач кафедри', 'Доктор техн. наук', 'ТК');

CREATE TABLE Dean (
    OrderNumber VARCHAR(50) PRIMARY KEY,
    PassportID VARCHAR(20),
    FacultyName VARCHAR(100) UNIQUE,
    FOREIGN KEY (PassportID) REFERENCES Person(PassportID),
    FOREIGN KEY (FacultyName) REFERENCES Faculty(Name)
);

INSERT INTO Dean VALUES ('45/2023', 'ID002', 'ФКНК'); 

ALTER TABLE Teacher 
ADD COLUMN SupervisorID VARCHAR(20),
ADD CONSTRAINT fk_teacher_self 
    FOREIGN KEY (SupervisorID) REFERENCES Teacher(PassportID);
 
UPDATE Teacher 
SET SupervisorID = 'ID004' WHERE PassportID = 'ID002';

CREATE TABLE Teacher_Discipline_Group (
    TeacherID VARCHAR(20),
    DeptName VARCHAR(100),
    DiscName VARCHAR(100),
    GroupName VARCHAR(20),
    PRIMARY KEY (TeacherID, DeptName, DiscName, GroupName),
    FOREIGN KEY (TeacherID) REFERENCES Teacher(PassportID),
    FOREIGN KEY (DeptName, DiscName) REFERENCES Discipline(DeptName, Name),
    FOREIGN KEY (GroupName) REFERENCES StudentGroup(Name)
);

INSERT INTO Teacher_Discipline_Group VALUES ('ID002', 'ТК', 'Бази даних', 'ТК-31'); 

 


 

 
