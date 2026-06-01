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

 

INSERT INTO person (passportid, fullname, birthdate, email, phone) VALUES 
('ID005', 'Рибаков Олексій Леонідович', '1965-03-14', 'rybakov@knu.ua', '0501112233'),
('ID006', 'Проценко Олена Володимирівна', '1978-11-22', 'protsenko@knu.ua', '0674445566'),
('ID007', 'Глибовець Микола Миколайович', '1957-08-19', 'glybovets@knu.ua', '0937778899'),
('ID008', 'Завадський Ігор Олександрович', '1972-04-05', 'zavadsky@knu.ua', '0509998877'),
('ID010', 'Коваленко Андрій Васильович', '2005-02-12', 'kovalenko.a@gmail.com', '0951112222'),
('ID011', 'Сидоренко Марія Ігорівна', '2006-09-30', 'sydorenko.m@outlook.com', '0633334444'),
('ID012', 'Ткаченко Богдан Олегович', '2005-07-15', 'tkach.b@meta.ua', '0675556666'),
('ID013', 'Романова Анна Сергіївна', '2004-12-01', 'romanova.a@gmail.com', '0508889999'),
('ID014', 'Павленко Віталій Юрійович', '2005-05-20', 'pavlenko.v@knu.ua', '0681119999'),
('ID015', 'Дмитренко Ольга Миколаївна', '2006-01-11', 'dmytrenko.o@gmail.com', '0732223333')
ON CONFLICT (passportid) DO NOTHING;


INSERT INTO department (name, headname, office, email, facultyname) VALUES 
('МС', 'Нікітченко М.С.', '302', 'kafedrams@unicyb.kiev.ua', 'ФКНК'),
('ОМ', 'Хіміч О.М.', '215', 'kafedraom@unicyb.kiev.ua', 'ФКНК'),
('ІС', 'Провотар О.І.', '408', 'kafedrais@unicyb.kiev.ua', 'ФКНК')
ON CONFLICT (name) DO NOTHING;

INSERT INTO discipline (deptname, name, credits, hasexam) VALUES 
('ТК', 'Об’єктно-орієнтоване програмування', 6, TRUE),
('ТК', 'Паралельні обчислення', 4, FALSE),
('МС', 'Математична логіка', 5, TRUE),
('МС', 'Теорія алгоритмів', 4, FALSE),
('ОМ', 'Чисельні методи', 5, TRUE),
('ОМ', 'Методи оптимізації', 5, TRUE),
('ІС', 'Штучний інтелект', 6, TRUE),
('ІС', 'Дискретна математика', 4, FALSE)
ON CONFLICT (deptname, name) DO NOTHING;

INSERT INTO studentgroup (name, enrollmentyear, course, deptname) VALUES 
('К-26', 2024, 2, 'ТК'),
('МІ-31', 2023, 3, 'МС'),
('ОМ-41', 2022, 4, 'ОМ'),
('ІС-11', 2025, 1, 'ІС'),
('К-16', 2025, 1, 'ТК')
ON CONFLICT (name) DO NOTHING;

INSERT INTO student (passportid, recordbookid, admissionyear, studyform, groupname) VALUES 
('ID011', 'КВ-123458', 2024, 'Денна', 'К-26'),
('ID013', 'КВ-123460', 2022, 'Заочна', 'ОМ-41'),
('ID014', 'КВ-123461', 2025, 'Денна', 'ІС-11'),
('ID015', 'КВ-123462', 2025, 'Заочна', 'К-16')
ON CONFLICT (passportid) DO NOTHING;

INSERT INTO teacher (passportid, position, academicdegree, deptname, supervisorid) VALUES 
('ID005', 'Професор', 'Доктор техн. наук', 'ТК', 'ID004'),
('ID006', 'Доцент', 'Кандидат фіз.-мат. наук', 'МС', 'ID004'),
('ID007', 'Професор', 'Доктор техн. наук', 'ІС', NULL),
('ID008', 'Доцент', 'Кандидат техн. наук', 'ТК', 'ID005')
ON CONFLICT (passportid) DO NOTHING;

INSERT INTO teacher_discipline_group (teacherid, deptname, discname, groupname) VALUES 
('ID002', 'ТК', 'Python', 'К-26'),
('ID005', 'ТК', 'Об’єктно-орієнтоване програмування', 'ТК-31'),
('ID005', 'ТК', 'Об’єктно-орієнтоване програмування', 'К-26'),
('ID008', 'ТК', 'Бази даних', 'К-16'),
('ID006', 'МС', 'Математична логіка', 'МІ-31'),
('ID007', 'ІС', 'Штучний інтелект', 'ІС-11')
ON CONFLICT (teacherid, deptname, discname, groupname) DO NOTHING;

DELETE FROM discipline d
WHERE NOT EXISTS (
    SELECT 1 
    FROM teacher_discipline_group tdg 
    WHERE tdg.deptname = d.deptname 
      AND tdg.discname = d.name
);
INSERT INTO Faculty VALUES ('ФІТ', 'вул. Шевченківська, 4', '045-567-91-13', 'fit@knu.ua', '2018-09-01', 'Київський національний університет');

INSERT INTO studentgroup
(name, enrollmentyear, course, deptname)
VALUES
('ТК-32', 2023, 2, 'ТК')
ON CONFLICT (name) DO NOTHING;

INSERT INTO teacher_discipline_group
(teacherid, deptname, discname, groupname)
VALUES
('ID002', 'ТК', 'Python', 'ТК-32'),
('ID005', 'ТК', 'Об’єктно-орієнтоване програмування', 'ТК-32')
ON CONFLICT (teacherid, deptname, discname, groupname) DO NOTHING;
 

 
