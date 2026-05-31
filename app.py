# На початку файлу додано імпорт об'єкта "g"
from flask import Flask, render_template, request, redirect, url_for, flash, g
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)
app.secret_key = 'university-db-secret-key'

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": "5434",
}


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=DictCursor)


def fetch_all(query, params=None):
    g.last_query = query  # Зберігаємо запит у глобальний контекст поточного сеансу сторінки
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def execute_commit(query, params=None, success_message='Операцію виконано'):
    g.last_query = query  # Зберігаємо зміну даних у глобальний контекст
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        conn.commit()
        flash(success_message, 'success')
    except psycopg2.Error as error:
        conn.rollback()
        flash(f'Помилка: {error.pgerror or error}', 'danger')
    finally:
        cur.close()
        conn.close()


@app.route('/')
def index():
    study_forms = [row[0] for row in fetch_all('SELECT DISTINCT studyform FROM student WHERE studyform IS NOT NULL ORDER BY studyform')]
    departments = [row[0] for row in fetch_all('SELECT name FROM department ORDER BY name')]
    faculties = [row[0] for row in fetch_all('SELECT name FROM faculty ORDER BY name')]
    degrees = [row[0] for row in fetch_all('SELECT DISTINCT academicdegree FROM teacher WHERE academicdegree IS NOT NULL ORDER BY academicdegree')]
    disciplines = [row[0] for row in fetch_all('SELECT DISTINCT name FROM discipline ORDER BY name')]
    return render_template('index.html', study_forms=study_forms, departments=departments, faculties=faculties, degrees=degrees, disciplines=disciplines)


@app.route('/universities', methods=['GET', 'POST'])
def universities():
    if request.method == 'POST':
        execute_commit('INSERT INTO university (name) VALUES (%s)', (request.form['name'],), 'Університет додано')
        return redirect(url_for('universities'))
    universities_list = fetch_all('SELECT name FROM university ORDER BY name')
    return render_template('universities.html', universities=universities_list)


@app.route('/universities/update', methods=['POST'])
def update_university():
    execute_commit('UPDATE university SET name = %s WHERE name = %s', (request.form['name'], request.form['old_name']), 'Університет оновлено')
    return redirect(url_for('universities'))


@app.route('/universities/delete', methods=['POST'])
def delete_university():
    execute_commit('DELETE FROM university WHERE name = %s', (request.form['name'],), 'Університет видалено')
    return redirect(url_for('universities'))


@app.route('/faculties', methods=['GET', 'POST'])
def faculties():
    if request.method == 'POST':
        execute_commit('INSERT INTO faculty (name, address, phone, email, foundationdate, uniname) VALUES (%s, %s, %s, %s, %s, %s)', (request.form['name'], request.form['address'], request.form['phone'], request.form['email'], request.form['foundation_date'], request.form['uni_name']), 'Факультет додано')
        return redirect(url_for('faculties'))
    universities_list = fetch_all('SELECT name FROM university ORDER BY name')
    faculties_list = fetch_all('SELECT name, address, phone, email, foundationdate, uniname FROM faculty ORDER BY name')
    return render_template('faculties.html', faculties=faculties_list, universities=universities_list)


@app.route('/faculties/update', methods=['POST'])
def update_faculty():
    execute_commit('UPDATE faculty SET name = %s, address = %s, phone = %s, email = %s, foundationdate = %s, uniname = %s WHERE name = %s', (request.form['name'], request.form['address'], request.form['phone'], request.form['email'], request.form['foundation_date'], request.form['uni_name'], request.form['old_name']), 'Факультет оновлено')
    return redirect(url_for('faculties'))


@app.route('/faculties/delete', methods=['POST'])
def delete_faculty():
    execute_commit('DELETE FROM faculty WHERE name = %s', (request.form['name'],), 'Факультет видалено')
    return redirect(url_for('faculties'))


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'POST':
        execute_commit('INSERT INTO department (name, headname, office, email, facultyname) VALUES (%s, %s, %s, %s, %s)', (request.form['name'], request.form['head_name'], request.form['office'], request.form['email'], request.form['faculty_name']), 'Кафедру додано')
        return redirect(url_for('departments'))
    faculties_list = fetch_all('SELECT name FROM faculty ORDER BY name')
    departments_list = fetch_all('SELECT name, headname, office, email, facultyname FROM department ORDER BY name')
    return render_template('departments.html', departments=departments_list, faculties=faculties_list)


@app.route('/departments/update', methods=['POST'])
def update_department():
    execute_commit('UPDATE department SET name = %s, headname = %s, office = %s, email = %s, facultyname = %s WHERE name = %s', (request.form['name'], request.form['head_name'], request.form['office'], request.form['email'], request.form['faculty_name'], request.form['old_name']), 'Кафедру оновлено')
    return redirect(url_for('departments'))


@app.route('/departments/delete', methods=['POST'])
def delete_department():
    execute_commit('DELETE FROM department WHERE name = %s', (request.form['name'],), 'Кафедру видалено')
    return redirect(url_for('departments'))


@app.route('/persons', methods=['GET', 'POST'])
def persons():
    if request.method == 'POST':
        execute_commit('INSERT INTO person (passportid, fullname, birthdate, email, phone) VALUES (%s, %s, %s, %s, %s)', (request.form['passport_id'], request.form['full_name'], request.form['birth_date'] or None, request.form['email'], request.form['phone']), 'Особу додано')
        return redirect(url_for('persons'))
    persons_list = fetch_all('SELECT passportid, fullname, birthdate, email, phone FROM person ORDER BY fullname')
    return render_template('persons.html', persons=persons_list)


@app.route('/persons/update', methods=['POST'])
def update_person():
    execute_commit('UPDATE person SET passportid = %s, fullname = %s, birthdate = %s, email = %s, phone = %s WHERE passportid = %s', (request.form['passport_id'], request.form['full_name'], request.form['birth_date'] or None, request.form['email'], request.form['phone'], request.form['old_passport_id']), 'Особу оновлено')
    return redirect(url_for('persons'))


@app.route('/persons/delete', methods=['POST'])
def delete_person():
    execute_commit('DELETE FROM person WHERE passportid = %s', (request.form['passport_id'],), 'Особу видалено')
    return redirect(url_for('persons'))


@app.route('/student-groups', methods=['GET', 'POST'])
def student_groups():
    if request.method == 'POST':
        execute_commit('INSERT INTO studentgroup (name, enrollmentyear, course, deptname) VALUES (%s, %s, %s, %s)', (request.form['name'], request.form['enrollment_year'], request.form['course'], request.form['dept_name']), 'Групу додано')
        return redirect(url_for('student_groups'))
    departments_list = fetch_all('SELECT name FROM department ORDER BY name')
    groups_list = fetch_all('SELECT name, enrollmentyear, course, deptname FROM studentgroup ORDER BY name')
    return render_template('student_groups.html', groups=groups_list, departments=departments_list)


@app.route('/student-groups/update', methods=['POST'])
def update_student_group():
    execute_commit('UPDATE studentgroup SET name = %s, enrollmentyear = %s, course = %s, deptname = %s WHERE name = %s', (request.form['name'], request.form['enrollment_year'], request.form['course'], request.form['dept_name'], request.form['old_name']), 'Групу оновлено')
    return redirect(url_for('student_groups'))


@app.route('/student-groups/delete', methods=['POST'])
def delete_student_group():
    execute_commit('DELETE FROM studentgroup WHERE name = %s', (request.form['name'],), 'Групу видалено')
    return redirect(url_for('student_groups'))


@app.route('/deans', methods=['GET', 'POST'])
def deans():
    if request.method == 'POST':
        execute_commit('INSERT INTO dean (ordernumber, passportid, facultyname) VALUES (%s, %s, %s)', (request.form['order_number'], request.form['passport_id'], request.form['faculty_name']), 'Декана додано')
        return redirect(url_for('deans'))
    persons_list = fetch_all('SELECT passportid, fullname FROM person ORDER BY fullname')
    faculties_list = fetch_all('SELECT name FROM faculty ORDER BY name')
    deans_list = fetch_all('SELECT d.ordernumber, d.passportid, p.fullname, d.facultyname FROM dean d JOIN person p ON d.passportid = p.passportid ORDER BY d.facultyname')
    return render_template('deans.html', deans=deans_list, persons=persons_list, faculties=faculties_list)


@app.route('/deans/update', methods=['POST'])
def update_dean():
    execute_commit('UPDATE dean SET ordernumber = %s, passportid = %s, facultyname = %s WHERE ordernumber = %s', (request.form['order_number'], request.form['passport_id'], request.form['faculty_name'], request.form['old_order_number']), 'Декана оновлено')
    return redirect(url_for('deans'))


@app.route('/deans/delete', methods=['POST'])
def delete_dean():
    execute_commit('DELETE FROM dean WHERE ordernumber = %s', (request.form['order_number'],), 'Декана видалено')
    return redirect(url_for('deans'))


@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        execute_commit('INSERT INTO student (passportid, recordbookid, admissionyear, studyform, groupname) VALUES (%s, %s, %s, %s, %s)', (request.form['passport_id'], request.form['record_book'], request.form['year'], request.form['study_form'], request.form['group_name']), 'Студента додано')
        return redirect(url_for('students'))
    persons_list = fetch_all('SELECT passportid, fullname FROM person ORDER BY fullname')
    groups_list = fetch_all('SELECT name FROM studentgroup ORDER BY name')
    students_list = fetch_all('SELECT s.passportid, p.fullname, s.recordbookid, s.admissionyear, s.studyform, s.groupname FROM student s JOIN person p ON s.passportid = p.passportid ORDER BY p.fullname')
    return render_template('students.html', students=students_list, persons=persons_list, groups=groups_list)


@app.route('/students/update', methods=['POST'])
def update_student():
    execute_commit('UPDATE student SET passportid = %s, recordbookid = %s, admissionyear = %s, studyform = %s, groupname = %s WHERE passportid = %s', (request.form['passport_id'], request.form['record_book'], request.form['year'], request.form['study_form'], request.form['group_name'], request.form['old_passport_id']), 'Студента оновлено')
    return redirect(url_for('students'))


@app.route('/students/delete', methods=['POST'])
def delete_student():
    execute_commit('DELETE FROM student WHERE passportid = %s', (request.form['passport_id'],), 'Студента видалено')
    return redirect(url_for('students'))


@app.route('/teachers', methods=['GET', 'POST'])
def teachers():
    if request.method == 'POST':
        supervisor = request.form['supervisor_id'] or None
        execute_commit('INSERT INTO teacher (passportid, position, academicdegree, deptname, supervisorid) VALUES (%s, %s, %s, %s, %s)', (request.form['passport_id'], request.form['position'], request.form['degree'], request.form['dept_name'], supervisor), 'Викладача додано')
        return redirect(url_for('teachers'))
    persons_list = fetch_all('SELECT passportid, fullname FROM person ORDER BY fullname')
    departments_list = fetch_all('SELECT name FROM department ORDER BY name')
    supervisors = fetch_all('SELECT t.passportid, p.fullname FROM teacher t JOIN person p ON t.passportid = p.passportid ORDER BY p.fullname')
    teachers_list = fetch_all('SELECT t.passportid, p.fullname, t.position, t.academicdegree, t.deptname, t.supervisorid, sp.fullname AS super_name FROM teacher t JOIN person p ON t.passportid = p.passportid LEFT JOIN person sp ON t.supervisorid = sp.passportid ORDER BY p.fullname')
    return render_template('teachers.html', teachers=teachers_list, persons=persons_list, departments=departments_list, supervisors=supervisors)


@app.route('/teachers/update', methods=['POST'])
def update_teacher():
    supervisor = request.form['supervisor_id'] or None
    execute_commit('UPDATE teacher SET passportid = %s, position = %s, academicdegree = %s, deptname = %s, supervisorid = %s WHERE passportid = %s', (request.form['passport_id'], request.form['position'], request.form['degree'], request.form['dept_name'], supervisor, request.form['old_passport_id']), 'Викладача оновлено')
    return redirect(url_for('teachers'))


@app.route('/teachers/delete', methods=['POST'])
def delete_teacher():
    execute_commit('DELETE FROM teacher WHERE passportid = %s', (request.form['passport_id'],), 'Викладача видалено')
    return redirect(url_for('teachers'))


@app.route('/disciplines', methods=['GET', 'POST'])
def disciplines():
    if request.method == 'POST':
        has_exam = request.form.get('has_exam') == 'TRUE'
        execute_commit('INSERT INTO discipline (deptname, name, credits, hasexam) VALUES (%s, %s, %s, %s)', (request.form['dept_name'], request.form['name'], request.form['credits'], has_exam), 'Дисципліну додано')
        return redirect(url_for('disciplines'))
    departments_list = fetch_all('SELECT name FROM department ORDER BY name')
    disciplines_list = fetch_all('SELECT deptname, name, credits, hasexam FROM discipline ORDER BY deptname, name')
    return render_template('disciplines.html', disciplines=disciplines_list, departments=departments_list)


@app.route('/disciplines/update', methods=['POST'])
def update_discipline():
    has_exam = request.form.get('has_exam') == 'TRUE'
    execute_commit('UPDATE discipline SET deptname = %s, name = %s, credits = %s, hasexam = %s WHERE deptname = %s AND name = %s', (request.form['dept_name'], request.form['name'], request.form['credits'], has_exam, request.form['old_dept_name'], request.form['old_name']), 'Дисципліну оновлено')
    return redirect(url_for('disciplines'))


@app.route('/disciplines/delete', methods=['POST'])
def delete_discipline():
    execute_commit('DELETE FROM discipline WHERE deptname = %s AND name = %s', (request.form['dept_name'], request.form['name']), 'Дисципліну видалено')
    return redirect(url_for('disciplines'))


@app.route('/teacher-discipline-groups', methods=['GET', 'POST'])
def teacher_discipline_groups():
    if request.method == 'POST':
        dept_name, disc_name = request.form['discipline_key'].split('|', 1)
        execute_commit('INSERT INTO teacher_discipline_group (teacherid, deptname, discname, groupname) VALUES (%s, %s, %s, %s)', (request.form['teacher_id'], dept_name, disc_name, request.form['group_name']), 'Призначення додано')
        return redirect(url_for('teacher_discipline_groups'))
    teachers_list = fetch_all('SELECT t.passportid, p.fullname FROM teacher t JOIN person p ON t.passportid = p.passportid ORDER BY p.fullname')
    disciplines_list = fetch_all('SELECT deptname, name FROM discipline ORDER BY deptname, name')
    groups_list = fetch_all('SELECT name FROM studentgroup ORDER BY name')
    assignments = fetch_all('SELECT tdg.teacherid, p.fullname AS teacher_name, tdg.deptname, tdg.discname, tdg.groupname FROM teacher_discipline_group tdg JOIN person p ON tdg.teacherid = p.passportid ORDER BY tdg.groupname, tdg.discname, p.fullname')
    return render_template('teacher_discipline_groups.html', assignments=assignments, teachers=teachers_list, disciplines=disciplines_list, groups=groups_list)


@app.route('/teacher-discipline-groups/update', methods=['POST'])
def update_teacher_discipline_group():
    dept_name, disc_name = request.form['discipline_key'].split('|', 1)
    execute_commit('UPDATE teacher_discipline_group SET teacherid = %s, deptname = %s, discname = %s, groupname = %s WHERE teacherid = %s AND deptname = %s AND discname = %s AND groupname = %s', (request.form['teacher_id'], dept_name, disc_name, request.form['group_name'], request.form['old_teacher_id'], request.form['old_dept_name'], request.form['old_disc_name'], request.form['old_group_name']), 'Призначення оновлено')
    return redirect(url_for('teacher_discipline_groups'))


@app.route('/teacher-discipline-groups/delete', methods=['POST'])
def delete_teacher_discipline_group():
    execute_commit('DELETE FROM teacher_discipline_group WHERE teacherid = %s AND deptname = %s AND discname = %s AND groupname = %s', (request.form['teacher_id'], request.form['dept_name'], request.form['disc_name'], request.form['group_name']), 'Призначення видалено')
    return redirect(url_for('teacher_discipline_groups'))


@app.route('/query1', methods=['POST'])
def query1():
    study_form = request.form['study_form']
    dept_name = request.form['dept_name']
    rows = fetch_all('SELECT p.fullname, s.recordbookid, g.name FROM student s JOIN person p ON s.passportid = p.passportid JOIN studentgroup g ON s.groupname = g.name WHERE s.studyform = %s AND g.deptname = %s ORDER BY p.fullname', (study_form, dept_name))
    return render_template('query_results.html', title='Запит 1', desc=f"Студенти форми навчання '{study_form}' на кафедрі {dept_name}", results=rows, columns=['ПІБ студента', 'Залікова книжка', 'Група'])


@app.route('/query2', methods=['POST'])
def query2():
    min_credits = request.form['min_credits']
    dept_name = request.form['dept_name']
    rows = fetch_all("SELECT d.name, d.credits, CASE WHEN d.hasexam THEN 'Екзамен' ELSE 'Залік' END, dep.headname FROM discipline d JOIN department dep ON d.deptname = dep.name WHERE d.credits > %s AND dep.name = %s ORDER BY d.credits DESC, d.name", (min_credits, dept_name))
    return render_template('query_results.html', title='Запит 2', desc=f'Дисципліни з кредитами > {min_credits} на кафедрі {dept_name}', results=rows, columns=['Назва дисципліни', 'Кредити', 'Форма контролю', 'Завідувач кафедри'])


@app.route('/query3', methods=['POST'])
def query3():
    faculty_name = request.form['faculty_name']
    degree = request.form['degree']
    rows = fetch_all('SELECT p.fullname, t.position, t.academicdegree, t.deptname FROM teacher t JOIN person p ON t.passportid = p.passportid JOIN department d ON t.deptname = d.name WHERE d.facultyname = %s AND t.academicdegree = %s ORDER BY p.fullname', (faculty_name, degree))
    return render_template('query_results.html', title='Запит 3', desc=f"Викладачі факультету {faculty_name} зі ступенем '{degree}'", results=rows, columns=['ПІБ', 'Посада', 'Ступінь', 'Кафедра'])


@app.route('/query4', methods=['POST'])
def query4():
    disc_name = request.form['disc_name']
    rows = fetch_all('SELECT sp.fullname, s.recordbookid, s.groupname, tp.fullname AS teacher_name FROM student s JOIN person sp ON s.passportid = sp.passportid JOIN teacher_discipline_group tdg ON s.groupname = tdg.groupname JOIN person tp ON tdg.teacherid = tp.passportid WHERE tdg.discname = %s ORDER BY s.groupname, sp.fullname', (disc_name,))
    return render_template('query_results.html', title='Запит 4', desc=f"Студенти, які слухають '{disc_name}', та їх викладачі", results=rows, columns=['Студент', 'Залікова книжка', 'Група', 'Викладач'])


@app.route('/query5', methods=['POST'])
def query5():
    year = request.form['year']
    rows = fetch_all('SELECT d.name, d.headname, f.name, f.foundationdate FROM department d JOIN faculty f ON d.facultyname = f.name WHERE EXTRACT(YEAR FROM f.foundationdate) > %s ORDER BY f.foundationdate', (year,))
    return render_template('query_results.html', title='Запит 5', desc=f'Кафедри факультетів, заснованих після {year} року', results=rows, columns=['Кафедра', 'Завідувач', 'Факультет', 'Засновано'])


@app.route('/query6', methods=['POST'])
def query6():
    rows = fetch_all('SELECT g1.name, g2.name FROM studentgroup g1 JOIN studentgroup g2 ON g1.name < g2.name WHERE NOT EXISTS (SELECT tdg1.discname FROM teacher_discipline_group tdg1 WHERE tdg1.groupname = g1.name EXCEPT SELECT tdg2.discname FROM teacher_discipline_group tdg2 WHERE tdg2.groupname = g2.name) AND NOT EXISTS (SELECT tdg2.discname FROM teacher_discipline_group tdg2 WHERE tdg2.groupname = g2.name EXCEPT SELECT tdg1.discname FROM teacher_discipline_group tdg1 WHERE tdg1.groupname = g1.name)')
    return render_template('query_results.html', title='Запит 6 (множинне порівняння)', desc='Пари студентських груп, що вивчають однакову множину дисциплін', results=rows, columns=['Група А', 'Група Б'])


@app.route('/query7', methods=['POST'])
def query7():
    rows = fetch_all('SELECT p.fullname, t.deptname, t.position FROM teacher t JOIN person p ON t.passportid = p.passportid WHERE NOT EXISTS (SELECT sg.name FROM studentgroup sg WHERE sg.deptname = t.deptname EXCEPT SELECT tdg.groupname FROM teacher_discipline_group tdg WHERE tdg.teacherid = t.passportid) ORDER BY p.fullname')
    return render_template('query_results.html', title='Запит 7 (множинне порівняння)', desc='Викладачі, які викладають у всіх групах своєї кафедри', results=rows, columns=['ПІБ викладача', 'Кафедра', 'Посада'])


@app.route('/report1')
def report1():
    rows = fetch_all('SELECT d.name, f.name AS faculty_name, COUNT(s.passportid) AS student_count, ROUND(COUNT(s.passportid) * 100.0 / NULLIF((SELECT COUNT(*) FROM student), 0), 2) AS percent_of_total FROM department d JOIN faculty f ON d.facultyname = f.name LEFT JOIN studentgroup sg ON sg.deptname = d.name LEFT JOIN student s ON s.groupname = sg.name GROUP BY d.name, f.name ORDER BY d.name')
    return render_template('query_results.html', title='Звіт 1', desc='Процентний розподіл студентів за кафедрами', results=rows, columns=['Кафедра', 'Факультет', 'Кількість студентів', '% від загальної кількості'])


@app.route('/report2')
def report2():
    rows = fetch_all('SELECT d.name, f.name AS faculty_name, COUNT(DISTINCT tdg.teacherid) AS teachers_count, COUNT(DISTINCT tdg.discname) AS disciplines_count, ROUND(COUNT(DISTINCT tdg.discname)::NUMERIC / NULLIF(COUNT(DISTINCT tdg.teacherid), 0), 2) AS avg_disciplines_per_teacher FROM department d JOIN faculty f ON d.facultyname = f.name LEFT JOIN teacher_discipline_group tdg ON tdg.deptname = d.name GROUP BY d.name, f.name ORDER BY d.name')
    return render_template('query_results.html', title='Звіт 2', desc='Середнє навчальне навантаження викладачів за кафедрами', results=rows, columns=['Кафедра', 'Факультет', 'Активних викладачів', 'Дисциплін', 'Дисциплін на викладача'])


@app.route('/report3')
def report3():
    rows = fetch_all('SELECT dep.name, fac.name AS faculty_name, COUNT(d.name) AS disciplines_count, COALESCE(SUM(d.credits), 0) AS total_credits, COALESCE(SUM(d.credits), 0) * 30 AS academic_hours FROM department dep JOIN faculty fac ON dep.facultyname = fac.name LEFT JOIN discipline d ON d.deptname = dep.name GROUP BY dep.name, fac.name ORDER BY dep.name')
    return render_template('query_results.html', title='Звіт 3', desc='Сумарний облік навчальних годин за кафедрами', results=rows, columns=['Кафедра', 'Факультет', 'Дисциплін', 'Всього кредитів', 'Академічні години'])


@app.route('/report4')
def report4():
    rows = fetch_all('SELECT dep.name, COUNT(DISTINCT s.passportid) AS students_count, COUNT(DISTINCT t.passportid) AS teachers_count, ROUND(COUNT(DISTINCT s.passportid)::NUMERIC / NULLIF(COUNT(DISTINCT t.passportid), 0), 2) AS students_per_teacher FROM department dep LEFT JOIN studentgroup sg ON sg.deptname = dep.name LEFT JOIN student s ON s.groupname = sg.name LEFT JOIN teacher t ON t.deptname = dep.name GROUP BY dep.name ORDER BY dep.name')
    return render_template('query_results.html', title='Звіт 4', desc='Співвідношення кількості студентів і викладачів за кафедрами', results=rows, columns=['Кафедра', 'Студентів', 'Викладачів', 'Студентів на викладача'])


if __name__ == '__main__':
    app.run(debug=True)