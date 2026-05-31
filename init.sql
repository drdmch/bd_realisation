CREATE TABLE University (
    Name VARCHAR(100) PRIMARY KEY
);

INSERT INTO University VALUES ('Київський національний універсиет');

CREATE TABLE Faculty (
    Name VARCHAR(100) PRIMARY KEY,
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Email VARCHAR(100),
    FoundationDate DATE,
    UniName VARCHAR(100),
    FOREIGN KEY (UniName) REFERENCES University(Name) ON DELETE CASCADE
);

INSERT INTO Faculty VALUES ('ФКНК', 'пр. Академіка Глушкова, 4д', '044-204-91-13', 'csc@knu.ua', '1969-09-01', 'Київський національний універсиет');

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
('ID002', 'Петренко Петро Петрович', '1975-10-20', 'petrenko@kpi.ua', '0504445566');

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

INSERT INTO Teacher VALUES ('ID002', 'Доцент', 'Кандидат техн. наук', 'ТК');

CREATE TABLE Student_Discipline (
    StudentPassport VARCHAR(20),
    DeptName VARCHAR(100),
    DiscName VARCHAR(100),
    PRIMARY KEY (StudentPassport, DeptName, DiscName),
    FOREIGN KEY (StudentPassport) REFERENCES Student(PassportID),
    FOREIGN KEY (DeptName, DiscName) REFERENCES Discipline(DeptName, Name)
);

INSERT INTO Student_Discipline VALUES 
('ID001', 'ТК', 'Бази даних'),
('ID001', 'ТК', 'Python');

CREATE TABLE Dean (
    OrderNumber VARCHAR(50) PRIMARY KEY,
    PassportID VARCHAR(20),
    FacultyName VARCHAR(100) UNIQUE,
    FOREIGN KEY (PassportID) REFERENCES Person(PassportID),
    FOREIGN KEY (FacultyName) REFERENCES Faculty(Name)
);

INSERT INTO Dean VALUES ('45/2023', 'ID002', 'ФКНК');