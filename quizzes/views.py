from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def index(request):
    cur = connection.cursor()
    cur.execute('SELECT id, created_at, description, title FROM quizzes;')
    quizz_list = dict_fetchall(cur)

    for quiz in quizz_list:
        cur.execute('''
        SELECT qr.student_id
        FROM quizzes q
        JOIN quiz_questions qq ON qq.quiz_id = q.id
        JOIN quiz_responses qr ON qr.question_id = qq.id
        WHERE q.id = %s
        GROUP BY qr.student_id;
        ''', [quiz['id']])
        responses = dict_fetchall(cur)
        quiz['responses'] = responses

    context = {"quizz_list": quizz_list}
    return render(request, "quizzes/index.html", context)


def detail(request, quiz_id, student_id):
    cur = connection.cursor()
    cur.execute('SELECT id, question FROM quiz_questions WHERE quiz_id = %s;', [quiz_id])
    questions = dict_fetchall(cur)

    for question in questions:
        cur.execute('''
        SELECT r.answer_text, r.answer_id
        FROM quiz_responses r WHERE r.question_id = %s AND r.student_id = %s;
        ''', [question['id'], student_id])
        response = dict_fetchone(cur)
        question['response'] = response

    context = {'quiz_id': quiz_id, 'student_id': student_id, 'questions': questions}
    return render(request, "quizzes/detail.html", context)

# --- helpers

def dict_fetchall(cursor):
    """Return all rows from a cursor as a list of dicts"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dict_fetchone(cursor):
    """Return one row from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row))