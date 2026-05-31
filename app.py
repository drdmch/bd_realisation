from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": "5434"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=DictCursor)

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Збираємо унікальні значення для випадаючих списків на головній сторінці
    cur.execute('SELECT DISTINCT StudyForm FROM Student WHERE StudyForm IS NOT NULL')
    study_forms = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT Name FROM Department')
    departments = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT Name FROM Faculty')
    faculties = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT DISTINCT AcademicDegree FROM Teacher WHERE AcademicDegree IS NOT NULL')
    degrees = [row[0] for row in cur.fetchall()]
    
    cur.execute('SELECT DISTINCT Name FROM Discipline')
    disciplines = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return render_template(
        'index.html',
        study_forms=study_forms,
        departments=departments,
        faculties=faculties,
        degrees=degrees,
        disciplines=disciplines
    )

# --- КЕРУВАННЯ СТУДЕНТАМИ ---
@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute(
            "INSERT INTO student (passportid, recordbookid, admissionyear, studyform, groupname) VALUES (%s, %s, %s, %s, %s)",
            (request.form['passport_id'], request.form['record_book'], request.form['year'], request.form['study_form'], request.form['group_name'])
        )
        conn.commit()
        return redirect(url_for('students'))
    
    cur.execute("SELECT passportid, fullname FROM person")
    persons = cur.fetchall()
    cur.execute("SELECT name FROM studentgroup")
    groups = cur.fetchall()
    cur.execute("SELECT s.passportid, p.fullname, s.recordbookid, s.studyform, s.groupname FROM student s JOIN person p ON s.passportid = p.passportid")
    students_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('students.html', students=students_list, persons=persons, groups=groups)

# --- КЕРУВАННЯ ВИКЛАДАЧАМИ ---
@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        supervisor = request.form['supervisor_id'] if request.form['supervisor_id'] != 'None' else None
        cur.execute(
            "INSERT INTO teacher (passportid, position, academicdegree, deptname, supervisorid) VALUES (%s, %s, %s, %s, %s)",
            (request.form['passport_id'], request.form['position'], request.form['degree'], request.form['dept_name'], supervisor)
        )
        conn.commit()
        return redirect(url_for('teachers'))
    
    cur.execute("SELECT passportid, fullname FROM person")
    persons = cur.fetchall()
    cur.execute("SELECT name FROM department")
    departments = cur.fetchall()
    cur.execute("SELECT t.passportid, p.fullname FROM teacher t JOIN person p ON t.passportid = p.passportid")
    supervisors = cur.fetchall()
    
    cur.execute("""
        SELECT t.passportid, p.fullname, t.position, t.academicdegree, t.deptname, s.fullname AS super_name 
        FROM teacher t 
        JOIN person p ON t.passportid = p.passportid
        LEFT JOIN person s ON t.supervisorid = s.passportid
    """)
    teachers_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('teachers.html', teachers=teachers_list, persons=persons, departments=departments, supervisors=supervisors)

# --- КЕРУВАННЯ ДИСЦИПЛІНАМИ ---
@app.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        has_exam = True if request.form.get('has_exam') == 'TRUE' else False
        cur.execute(
            "INSERT INTO discipline (deptname, name, credits, hasexam) VALUES (%s, %s, %s, %s)",
            (request.form['dept_name'], request.form['name'], request.form['credits'], has_exam)
        )
        conn.commit()
        return redirect(url_for('disciplines'))
    
    cur.execute("SELECT name FROM department")
    departments = cur.fetchall()
    cur.execute("SELECT deptname, name, credits, hasexam FROM discipline")
    disciplines_list = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('disciplines.html', disciplines=disciplines_list, departments=departments)

# --- 5 ПАРАМЕТРИЗОВАНИХ ЗАПИТІВ ---

@app.route('/query1', methods=['POST'])
def query1():
    study_form = request.form['study_form']
    dept_name = request.form['dept_name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.fullname, s.recordbookid, g.name
        FROM student s
        JOIN person p ON s.passportid = p.passportid
        JOIN studentgroup g ON s.groupname = g.name
        WHERE s.studyform = %s AND g.deptname = %s;
    """, (study_form, dept_name))
    return render_template('query_results.html', title="Запит 1", desc=f"Студенти форми навчання '{study_form}' на кафедрі {dept_name}", results=cur.fetchall(), columns=['ПІБ Студента', 'Заліковка', 'Група'])

@app.route('/query2', methods=['POST'])
def query2():
    min_credits = request.form['min_credits']
    dept_name = request.form['dept_name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, credits, hasexam FROM discipline WHERE credits > %s AND deptname = %s;
    """, (min_credits, dept_name))
    return render_template('query_results.html', title="Запит 2", desc=f"Дисципліни з кредитами > {min_credits} на кафедрі {dept_name}", results=cur.fetchall(), columns=['Назва курсу', 'Кредити', 'Іспит'])

@app.route('/query3', methods=['POST'])
def query3():
    faculty_name = request.form['faculty_name']
    degree = request.form['degree']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.fullname, t.position, t.academicdegree, t.deptname
        FROM teacher t
        JOIN person p ON t.passportid = p.passportid
        JOIN department d ON t.deptname = d.name
        WHERE d.facultyname = %s AND t.academicdegree = %s;
    """, (faculty_name, degree))
    return render_template('query_results.html', title="Запит 3", desc=f"Викладачі факультету {faculty_name} зі ступенем '{degree}'", results=cur.fetchall(), columns=['ПІБ', 'Посада', 'Ступінь', 'Кафедра'])

@app.route('/query4', methods=['POST'])
def query4():
    disc_name = request.form['disc_name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.fullname, s.recordbookid, s.groupname, tp.fullname AS teacher_name
        FROM student s
        JOIN person p ON s.passportid = p.passportid
        JOIN teacher_discipline_group tdg ON s.groupname = tdg.groupname
        JOIN person tp ON tdg.teacherid = tp.passportid
        WHERE tdg.discname = %s;
    """, (disc_name,))
    return render_template('query_results.html', title="Запит 4", desc=f"Студенти, які слухають '{disc_name}', та їх викладачі", results=cur.fetchall(), columns=['Студент', 'Заліковка', 'Група', 'Викладач'])

@app.route('/query5', methods=['POST'])
def query5():
    year = request.form['year']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.name, d.headname, f.name, f.foundationdate
        FROM department d
        JOIN faculty f ON d.facultyname = f.name
        WHERE EXTRACT(YEAR FROM f.foundationdate) > %s;
    """, (year,))
    return render_template('query_results.html', title="Запит 5", desc=f"Кафедри факультетів, заснованих після {year} року", results=cur.fetchall(), columns=['Кафедра', 'Завідувач', 'Факультет', 'Засновано'])

# --- 2 ЗАПИТИ З МНОЖИННИМ ПОРІВНЯННЯМ ---

@app.route('/query6', methods=['POST'])
def query6():
    conn = get_db_connection()
    cur = conn.cursor()
    # Пари груп, які слухають абсолютно однакову множину предметів
    cur.execute("""
        SELECT g1.groupname, g2.groupname
        FROM teacher_discipline_group g1
        JOIN teacher_discipline_group g2 ON g1.groupname < g2.groupname
        GROUP BY g1.groupname, g2.groupname
        HAVING COUNT(DISTINCT g1.discname) = (SELECT COUNT(DISTINCT discname) FROM teacher_discipline_group WHERE groupname = g1.groupname)
           AND COUNT(DISTINCT g2.discname) = (SELECT COUNT(DISTINCT discname) FROM teacher_discipline_group WHERE groupname = g2.groupname)
           AND NOT EXISTS (
                SELECT discname FROM teacher_discipline_group WHERE groupname = g1.groupname
                EXCEPT
                SELECT discname FROM teacher_discipline_group WHERE groupname = g2.groupname
           );
    """)
    return render_template('query_results.html', title="Запит 6 (Множинне)", desc="Пари студентських груп, що вивчають однакову множину дисциплін", results=cur.fetchall(), columns=['Група А', 'Група Б'])

@app.route('/query7', methods=['POST'])
def query7():
    conn = get_db_connection()
    cur = conn.cursor()
    # Викладачі, які викладають у ВСІХ існуючих групах своєї кафедри
    cur.execute("""
        SELECT p.fullname, t.deptname, t.position
        FROM teacher t
        JOIN person p ON t.passportid = p.passportid
        WHERE (
            SELECT COUNT(DISTINCT groupname) 
            FROM teacher_discipline_group 
            WHERE teacherid = t.passportid
        ) = (
            SELECT COUNT(*) 
            FROM studentgroup 
            WHERE deptname = t.deptname
        );
    """)
    return render_template('query_results.html', title="Запит 7 (Повне ділення)", desc="Викладачі, які викладають абсолютно у всіх групах своєї кафедри", results=cur.fetchall(), columns=['ПІБ Викладача', 'Кафедра', 'Посада'])

# --- 4 АРИФМЕТИЧНІ ЗВІТИ ---

@app.route('/report1')
def report1():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT sg.deptname, COUNT(s.passportid),
               ROUND(COUNT(s.passportid) * 100.0 / NULLIF((SELECT COUNT(*) FROM student), 0), 2)
        FROM studentgroup sg
        LEFT JOIN student s ON sg.name = s.groupname
        GROUP BY sg.deptname;
    """)
    return render_template('query_results.html', title="Звіт 1", desc="Процентний розподіл студентів за кафедрами", results=cur.fetchall(), columns=['Кафедра', 'Студентів', '% від загальної к-сті'])

@app.route('/report2')
def report2():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT deptname, COUNT(DISTINCT teacherid), COUNT(DISTINCT discname),
               ROUND(COUNT(DISTINCT discname)::NUMERIC / NULLIF(COUNT(DISTINCT teacherid), 0), 2)
        FROM teacher_discipline_group GROUP BY deptname;
    """)
    return render_template('query_results.html', title="Звіт 2", desc="Коефіцієнт навантаження викладачів предметів", results=cur.fetchall(), columns=['Кафедра', 'Активних викладачів', 'Курсів', 'Сер. кількість курсів на викладача'])

@app.route('/report3')
def report3():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT deptname, COUNT(name), SUM(credits), (SUM(credits) * 30) FROM discipline GROUP BY deptname;")
    return render_template('query_results.html', title="Звіт 3", desc="Сумарний облік навчальних годин за кафедрами", results=cur.fetchall(), columns=['Кафедра', 'Дисциплін', 'Всього кредитів', 'Академічні години (Кредити * 30)'])

@app.route('/report4')
def report4():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT (SELECT COUNT(*) FROM student), (SELECT COUNT(*) FROM teacher),
               ROUND((SELECT COUNT(*) FROM student)::NUMERIC / NULLIF((SELECT COUNT(*) FROM teacher), 0), 2);
    """)
    return render_template('query_results.html', title="Звіт 4", desc="Загальносистемний аудит пропорцій", results=cur.fetchall(), columns=['Всього студентів', 'Всього викладачів', 'Індекс завантаженості (Студ/Викл)'])

if __name__ == '__main__':
    app.run(debug=True)