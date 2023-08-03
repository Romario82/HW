SELECT students.students, AVG(grades.grade) AS avg_grade FROM students INNER JOIN grades ON students.id = grades.student_id GROUP BY students.id, students.students ORDER BY avg_grade DESC LIMIT 5
