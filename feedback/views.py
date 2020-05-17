from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Avg, Q
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
import csv, io, re, datetime

# Create your views here.
@require_http_methods(["GET"])
@login_required(login_url="student_login")
def index(request):
    if request.user.is_superuser: return HttpResponseRedirect(reverse("sfsadmin_index"))
    if request.user.is_staff: return HttpResponseRedirect(reverse("teacher_index"))
    student = Student.objects.get(user=request.user)
    department = student.department
    semester = student.semester
    batch = student.batch
    subjects = Subject.objects.all().filter(
        department=department, semester=semester, practical=False)
    complete = []
    for subject in subjects:
        try:
            feedback = Feedback.objects.get(student=student, subject=subject)
            flag = 1
        except:
            flag = 0
        complete.append(flag)
    b = []
    for t in complete:
        if t == 0:
            b.append(t)
    length = len(b)
    # Practical Subjects
    practicals = Batches.objects.all().filter(
        subject__department=department, subject__semester=semester, subject__practical=True, batch=batch)
    complete1 = []
    for practical in practicals:
        try:
            feedback1 = Feedback.objects.get(student=student, subject=practical.subject)
            flag1 = 1
        except:
            flag1 = 0
        complete1.append(flag1)
    b1 = []
    for t1 in complete1:
        if t1 == 0:
            b1.append(t1)
    length1 = len(b1)
    if length == 0 and length1 == 0:
        return HttpResponseRedirect(reverse("student_logout"))
    context = {
        'student': student,
        'subjects': subjects,
        'practicals': practicals,
        'complete': complete,
        'complete1': complete1,
    }
    return render(request, "feedback/student/index.html", context)

@require_http_methods(["GET", "POST"])
def student_login(request):
    if request.method == 'POST':
        form = StudentLogin(request.POST)
        # Getting Form Fields
        username = request.POST["username"]
        if not username:
            messages.success(request, "Must Provide Username!")
            return render(request, "feedback/student/student_login.html", {'form': form})
        password = request.POST["password"]
        if not password:
            messages.success(request, "Must Provide PassWord!!")
            return render(request, "feedback/student/student_login.html", {'form': form})
        user = authenticate(request, username=username,
                            password=password, is_staff=False)
        if not user:
            messages.success(request, "Username or Password did not Match!!!")
            return render(request, "feedback/student/student_login.html", {'form': form})
        if user.is_staff:
            messages.success(request, "You cannot access here")
            return render(request, "feedback/student/student_login.html", {'form': form})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = StudentLogin()
        return render(request, "feedback/student/student_login.html", {'form': form})

@require_http_methods(["GET"])
@login_required(login_url="student_login")
def student_logout(request):
    if request.user.is_staff: return HttpResponseForbidden
    # Sending Mail to the User
    subject = 'Thanks Giving'
    message = f"""
    Thank You for Your Valuable Feedback!
    We will look back to it and will try to improve accordingly.
    """
    email_from = settings.EMAIL_HOST_USER
    student_list = [request.user.email, ]
    send_mail(subject, message, email_from, student_list)
    logout(request)
    messages.success(
        request, "Thank you for completing your feedback. You have been logged out from the system.")
    return HttpResponseRedirect(reverse("student_login"))

# Feedback Page for Student
@require_http_methods(["GET", "POST"])
@login_required(login_url="student_login")
def student_feedback(request, teacher_id, subject_id):
    if request.user.is_staff: return HttpResponseForbidden
    if request.method == "POST":
        question1 = int(request.POST["option1"])
        question2 = int(request.POST["option2"])
        question3 = int(request.POST["option3"])
        question4 = int(request.POST["option4"])
        question5 = int(request.POST["option5"])
        question6 = int(request.POST["option6"])
        question7 = int(request.POST["option7"])
        suggestions = request.POST["suggestions"]
        try:
            question8 = int(request.POST["option8"])
            question9 = int(request.POST["option9"])
            question10 = int(request.POST["option10"])
            question11 = int(request.POST["option11"])
            question12 = int(request.POST["option12"])
        except:
            question8 = question9 = question10 = question11 = question12 = -1
        # save to db
        student = Student.objects.get(user=request.user)
        subject = Subject.objects.get(id=subject_id)
        teacher = Teacher.objects.get(id=teacher_id)

        if question8 == -1 or question9 == -1 or question10 == -1 or question11 == -1 or question12 == -1:
            feedback = Feedback(
                student=student,
                subject=subject,
                teacher=teacher,
                q1=question1,
                q2=question2,
                q3=question3,
                q4=question4,
                q5=question5,
                q6=question6,
                q7=question7,
                suggestions=suggestions,
            )
        else:
            feedback = Feedback(
                student=student,
                subject=subject,
                teacher=teacher,
                q1=question1,
                q2=question2,
                q3=question3,
                q4=question4,
                q5=question5,
                q6=question6,
                q7=question7,
                q8=question8,
                q9=question9,
                q10=question10,
                q11=question11,
                q12=question12,
                suggestions=suggestions,
            )
        feedback.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        try:
            student = Student.objects.get(user=request.user)
            teacher = Teacher.objects.get(id=teacher_id)
            subject = Subject.objects.filter(
                teacher=teacher,
                id=subject_id,
                semester=student.semester,
                department=student.department,
            )
            if not subject:
                raise Http404("Entry is False!")
        except:
            raise Http404("Entry doesn't exists!")
        context = {
            'subject': subject,
        }
        return render(request, "feedback/student/student_feedback.html", context)


# Teacher Operations
@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def teacher_index(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    i = 0
    teacher = Teacher.objects.get(user=request.user)
    # Get distinct subjects
    subjects = Feedback.objects.all().filter(
        teacher=teacher).order_by().values('subject__id', 'subject__subject_name', 'subject__practical').distinct()
    # Feedback of Regular Students
    temp1 = {}
    for subject in subjects:
        sub = subject['subject__subject_name']
        # Automation
        temp1[sub] = {}
        temp1[sub]['id'] = subject['subject__id']
        temp1[sub]['count1'] = 0
        for i in range(1, 13):
            temp1[sub]['status'] = subject['subject__practical']
            temp1[sub]['q'+str(i)+'E'] = 0
            temp1[sub]['q'+str(i)+'V'] = 0
            temp1[sub]['q'+str(i)+'G'] = 0
            temp1[sub]['q'+str(i)+'A'] = 0
            temp1[sub]['q'+str(i)+'P'] = 0
            temp1[sub]['q'+str(i)+'N'] = 0
            temp1[sub]['subE'] = 0
            temp1[sub]['subV'] = 0
            temp1[sub]['subG'] = 0
            temp1[sub]['subA'] = 0
            temp1[sub]['subP'] = 0
            temp1[sub]['subN'] = 0
            temp1[sub]['subT'] = 0
            temp1[sub]['subO'] = 0
            temp1[sub]['subPerc'] = 0
        try:
            feedbacks = Feedback.objects.all().filter(teacher=teacher, subject__subject_name=sub, student__attendance__gte=75)
            for feedback in feedbacks:
                temp1[sub]['count1'] += 1
                # Question 1
                if feedback.q1 == 5:
                    temp1[sub]['q1E'] += 1
                elif feedback.q1 == 4:
                    temp1[sub]['q1V'] += 1
                elif feedback.q1 == 3:
                    temp1[sub]['q1G'] += 1
                elif feedback.q1 == 2:
                    temp1[sub]['q1A'] += 1
                elif feedback.q1 == 1:
                    temp1[sub]['q1P'] += 1
                else:
                    temp1[sub]['q1N'] += 1
                # Question 2
                if feedback.q2 == 5:
                    temp1[sub]['q2E'] += 1
                elif feedback.q2 == 4:
                    temp1[sub]['q2V'] += 1
                elif feedback.q2 == 3:
                    temp1[sub]['q2G'] += 1
                elif feedback.q2 == 2:
                    temp1[sub]['q2A'] += 1
                elif feedback.q2 == 1:
                    temp1[sub]['q2P'] += 1
                else:
                    temp1[sub]['q2N'] += 1
                # Question 3
                if feedback.q3 == 5:
                    temp1[sub]['q3E'] += 1
                elif feedback.q3 == 4:
                    temp1[sub]['q3V'] += 1
                elif feedback.q3 == 3:
                    temp1[sub]['q3G'] += 1
                elif feedback.q3 == 2:
                    temp1[sub]['q3A'] += 1
                elif feedback.q3 == 1:
                    temp1[sub]['q3P'] += 1
                else:
                    temp1[sub]['q3N'] += 1
                # Question 4
                if feedback.q4 == 5:
                    temp1[sub]['q4E'] += 1
                elif feedback.q4 == 4:
                    temp1[sub]['q4V'] += 1
                elif feedback.q4 == 3:
                    temp1[sub]['q4G'] += 1
                elif feedback.q4 == 2:
                    temp1[sub]['q4A'] += 1
                elif feedback.q4 == 1:
                    temp1[sub]['q4P'] += 1
                else:
                    temp1[sub]['q4N'] += 1
                # Question 5
                if feedback.q5 == 5:
                    temp1[sub]['q5E'] += 1
                elif feedback.q5 == 4:
                    temp1[sub]['q5V'] += 1
                elif feedback.q5 == 3:
                    temp1[sub]['q5G'] += 1
                elif feedback.q5 == 2:
                    temp1[sub]['q5A'] += 1
                elif feedback.q5 == 1:
                    temp1[sub]['q5P'] += 1
                else:
                    temp1[sub]['q5N'] += 1
                # Question 6
                if feedback.q6 == 5:
                    temp1[sub]['q6E'] += 1
                elif feedback.q6 == 4:
                    temp1[sub]['q6V'] += 1
                elif feedback.q6 == 3:
                    temp1[sub]['q6G'] += 1
                elif feedback.q6 == 2:
                    temp1[sub]['q6A'] += 1
                elif feedback.q6 == 1:
                    temp1[sub]['q6P'] += 1
                else:
                    temp1[sub]['q6N'] += 1
                # Question 7
                if feedback.q7 == 5:
                    temp1[sub]['q7E'] += 1
                elif feedback.q7 == 4:
                    temp1[sub]['q7V'] += 1
                elif feedback.q7 == 3:
                    temp1[sub]['q7G'] += 1
                elif feedback.q7 == 2:
                    temp1[sub]['q7A'] += 1
                elif feedback.q7 == 1:
                    temp1[sub]['q7P'] += 1
                else:
                    temp1[sub]['q7N'] += 1
                # Question 8
                if feedback.q8 == 5:
                    temp1[sub]['q8E'] += 1
                elif feedback.q8 == 4:
                    temp1[sub]['q8V'] += 1
                elif feedback.q8 == 3:
                    temp1[sub]['q8G'] += 1
                elif feedback.q8 == 2:
                    temp1[sub]['q8A'] += 1
                elif feedback.q8 == 1:
                    temp1[sub]['q8P'] += 1
                else:
                    temp1[sub]['q8N'] += 1
                # Question 9
                if feedback.q9 == 5:
                    temp1[sub]['q9E'] += 1
                elif feedback.q9 == 4:
                    temp1[sub]['q9V'] += 1
                elif feedback.q9 == 3:
                    temp1[sub]['q9G'] += 1
                elif feedback.q9 == 2:
                    temp1[sub]['q9A'] += 1
                elif feedback.q9 == 1:
                    temp1[sub]['q9P'] += 1
                else:
                    temp1[sub]['q9N'] += 1
                # Question 10
                if feedback.q10 == 5:
                    temp1[sub]['q10E'] += 1
                elif feedback.q10 == 4:
                    temp1[sub]['q10V'] += 1
                elif feedback.q10 == 3:
                    temp1[sub]['q10G'] += 1
                elif feedback.q10 == 2:
                    temp1[sub]['q10A'] += 1
                elif feedback.q10 == 1:
                    temp1[sub]['q10P'] += 1
                else:
                    temp1[sub]['q10N'] += 1
                # Question 11
                if feedback.q11 == 5:
                    temp1[sub]['q11E'] += 1
                elif feedback.q11 == 4:
                    temp1[sub]['q11V'] += 1
                elif feedback.q11 == 3:
                    temp1[sub]['q11G'] += 1
                elif feedback.q11 == 2:
                    temp1[sub]['q11A'] += 1
                elif feedback.q11 == 1:
                    temp1[sub]['q11P'] += 1
                else:
                    temp1[sub]['q11N'] += 1
                # Question 12
                if feedback.q12 == 5:
                    temp1[sub]['q12E'] += 1
                elif feedback.q12 == 4:
                    temp1[sub]['q12V'] += 1
                elif feedback.q12 == 3:
                    temp1[sub]['q12G'] += 1
                elif feedback.q12 == 2:
                    temp1[sub]['q12A'] += 1
                elif feedback.q12 == 1:
                    temp1[sub]['q12P'] += 1
                else:
                    temp1[sub]['q12N'] += 1
            # Calc total, out of, percentage for Theory subjects
            if not temp1[sub]['status']:
                for i in range(1, 13):
                        temp1[sub]['q'+str(i)+'T'] = (temp1[sub]['q'+str(i)+'E'] * 5) + (temp1[sub]['q'+str(i)+'V'] * 4) + (temp1[sub]['q'+str(i)+'G'] * 3) + (temp1[sub]['q'+str(i)+'A'] * 2) + (temp1[sub]['q'+str(i)+'P'] * 1)
                        temp1[sub]['q'+str(i)+'O'] = (temp1[sub]['q'+str(i)+'E'] + temp1[sub]['q'+str(i)+'V'] + temp1[sub]['q'+str(i)+'G'] +
                            temp1[sub]['q'+str(i)+'A'] + temp1[sub]['q'+str(i)+'P'] + temp1[sub]['q'+str(i)+'N']) * 5
                        temp1[sub]['q'+str(i)+'Perc'] = (
                            "%.2f" % round(((temp1[sub]['q'+str(i)+'T'] * 100) / temp1[sub]['q'+str(i)+'O']), 2)
                            )
                        # Overall Calculation
                        temp1[sub]['subE'] += temp1[sub]['q'+str(i)+'E']
                        temp1[sub]['subV'] += temp1[sub]['q'+str(i)+'V']
                        temp1[sub]['subG'] += temp1[sub]['q'+str(i)+'G']
                        temp1[sub]['subA'] += temp1[sub]['q'+str(i)+'A']
                        temp1[sub]['subP'] += temp1[sub]['q'+str(i)+'P']
                        temp1[sub]['subN'] += temp1[sub]['q'+str(i)+'N']
                        temp1[sub]['subT'] += temp1[sub]['q'+str(i)+'T']
                        temp1[sub]['subO'] += temp1[sub]['q'+str(i)+'O']
                        temp1[sub]['subPerc'] = (
                            "%.2f" % round(((temp1[sub]['subT'] * 100) / temp1[sub]['subO']), 2)
                            )
            # Calc total, out of, percentage for Practical subjects
            else:
                for i in range(1, 8):
                    temp1[sub]['q'+str(i)+'T'] = (temp1[sub]['q'+str(i)+'E'] * 5) + (temp1[sub]['q'+str(i)+'V'] * 4) + (temp1[sub]['q'+str(i)+'G'] * 3) + (temp1[sub]['q'+str(i)+'A'] * 2) + (temp1[sub]['q'+str(i)+'P'] * 1)
                    temp1[sub]['q'+str(i)+'O'] = (temp1[sub]['q'+str(i)+'E'] + temp1[sub]['q'+str(i)+'V'] + temp1[sub]['q'+str(i)+'G'] +
                        temp1[sub]['q'+str(i)+'A'] + temp1[sub]['q'+str(i)+'P'] + temp1[sub]['q'+str(i)+'N']) * 5
                    temp1[sub]['q'+str(i)+'Perc'] = (
                        "%.2f" % round(((temp1[sub]['q'+str(i)+'T'] * 100) / temp1[sub]['q'+str(i)+'O']), 2)
                        )
                    # Overall Calculation
                    temp1[sub]['subE'] += temp1[sub]['q'+str(i)+'E']
                    temp1[sub]['subV'] += temp1[sub]['q'+str(i)+'V']
                    temp1[sub]['subG'] += temp1[sub]['q'+str(i)+'G']
                    temp1[sub]['subA'] += temp1[sub]['q'+str(i)+'A']
                    temp1[sub]['subP'] += temp1[sub]['q'+str(i)+'P']
                    temp1[sub]['subN'] += temp1[sub]['q'+str(i)+'N']
                    temp1[sub]['subT'] += temp1[sub]['q'+str(i)+'T']
                    temp1[sub]['subO'] += temp1[sub]['q'+str(i)+'O']
                    temp1[sub]['subPerc'] = (
                        "%.2f" % round(((temp1[sub]['subT'] * 100) / temp1[sub]['subO']), 2)
                        )
        except:
            for i in range(1, 13):
                temp1[sub]['q'+str(i)+'T'] = 0
                temp1[sub]['q'+str(i)+'O'] = 0
                temp1[sub]['q'+str(i)+'Perc'] = 0.0
    # Feedback of Dafaulters
    temp2 = {}
    for subject in subjects:
        sub = subject['subject__subject_name']
        # Automation
        temp2[sub] = {}
        temp2[sub]['id'] = subject['subject__id']
        temp2[sub]['count2'] = 0
        for i in range(1, 13):
            temp2[sub]['status'] = subject['subject__practical']
            temp2[sub]['q'+str(i)+'E'] = 0
            temp2[sub]['q'+str(i)+'V'] = 0
            temp2[sub]['q'+str(i)+'G'] = 0
            temp2[sub]['q'+str(i)+'A'] = 0
            temp2[sub]['q'+str(i)+'P'] = 0
            temp2[sub]['q'+str(i)+'N'] = 0
            temp2[sub]['subE'] = 0
            temp2[sub]['subV'] = 0
            temp2[sub]['subG'] = 0
            temp2[sub]['subA'] = 0
            temp2[sub]['subP'] = 0
            temp2[sub]['subN'] = 0
            temp2[sub]['subT'] = 0
            temp2[sub]['subO'] = 0
            temp2[sub]['subPerc'] = 0
        try:
            feedbacks = Feedback.objects.all().filter(teacher=teacher, subject__subject_name=sub, student__attendance__lt=75)
            for feedback in feedbacks:
                temp2[sub]['count2'] += 1
                # Question 1
                if feedback.q1 == 5:
                    temp2[sub]['q1E'] += 1
                elif feedback.q1 == 4:
                    temp2[sub]['q1V'] += 1
                elif feedback.q1 == 3:
                    temp2[sub]['q1G'] += 1
                elif feedback.q1 == 2:
                    temp2[sub]['q1A'] += 1
                elif feedback.q1 == 1:
                    temp2[sub]['q1P'] += 1
                else:
                    temp2[sub]['q1N'] += 1
                # Question 2
                if feedback.q2 == 5:
                    temp2[sub]['q2E'] += 1
                elif feedback.q2 == 4:
                    temp2[sub]['q2V'] += 1
                elif feedback.q2 == 3:
                    temp2[sub]['q2G'] += 1
                elif feedback.q2 == 2:
                    temp2[sub]['q2A'] += 1
                elif feedback.q2 == 1:
                    temp2[sub]['q2P'] += 1
                else:
                    temp2[sub]['q2N'] += 1
                # Question 3
                if feedback.q3 == 5:
                    temp2[sub]['q3E'] += 1
                elif feedback.q3 == 4:
                    temp2[sub]['q3V'] += 1
                elif feedback.q3 == 3:
                    temp2[sub]['q3G'] += 1
                elif feedback.q3 == 2:
                    temp2[sub]['q3A'] += 1
                elif feedback.q3 == 1:
                    temp2[sub]['q3P'] += 1
                else:
                    temp2[sub]['q3N'] += 1
                # Question 4
                if feedback.q4 == 5:
                    temp2[sub]['q4E'] += 1
                elif feedback.q4 == 4:
                    temp2[sub]['q4V'] += 1
                elif feedback.q4 == 3:
                    temp2[sub]['q4G'] += 1
                elif feedback.q4 == 2:
                    temp2[sub]['q4A'] += 1
                elif feedback.q4 == 1:
                    temp2[sub]['q4P'] += 1
                else:
                    temp2[sub]['q4N'] += 1
                # Question 5
                if feedback.q5 == 5:
                    temp2[sub]['q5E'] += 1
                elif feedback.q5 == 4:
                    temp2[sub]['q5V'] += 1
                elif feedback.q5 == 3:
                    temp2[sub]['q5G'] += 1
                elif feedback.q5 == 2:
                    temp2[sub]['q5A'] += 1
                elif feedback.q5 == 1:
                    temp2[sub]['q5P'] += 1
                else:
                    temp2[sub]['q5N'] += 1
                # Question 6
                if feedback.q6 == 5:
                    temp2[sub]['q6E'] += 1
                elif feedback.q6 == 4:
                    temp2[sub]['q6V'] += 1
                elif feedback.q6 == 3:
                    temp2[sub]['q6G'] += 1
                elif feedback.q6 == 2:
                    temp2[sub]['q6A'] += 1
                elif feedback.q6 == 1:
                    temp2[sub]['q6P'] += 1
                else:
                    temp2[sub]['q6N'] += 1
                # Question 7
                if feedback.q7 == 5:
                    temp2[sub]['q7E'] += 1
                elif feedback.q7 == 4:
                    temp2[sub]['q7V'] += 1
                elif feedback.q7 == 3:
                    temp2[sub]['q7G'] += 1
                elif feedback.q7 == 2:
                    temp2[sub]['q7A'] += 1
                elif feedback.q7 == 1:
                    temp2[sub]['q7P'] += 1
                else:
                    temp2[sub]['q7N'] += 1
                # Question 8
                if feedback.q8 == 5:
                    temp2[sub]['q8E'] += 1
                elif feedback.q8 == 4:
                    temp2[sub]['q8V'] += 1
                elif feedback.q8 == 3:
                    temp2[sub]['q8G'] += 1
                elif feedback.q8 == 2:
                    temp2[sub]['q8A'] += 1
                elif feedback.q8 == 1:
                    temp2[sub]['q8P'] += 1
                else:
                    temp2[sub]['q8N'] += 1
                # Question 9
                if feedback.q9 == 5:
                    temp2[sub]['q9E'] += 1
                elif feedback.q9 == 4:
                    temp2[sub]['q9V'] += 1
                elif feedback.q9 == 3:
                    temp2[sub]['q9G'] += 1
                elif feedback.q9 == 2:
                    temp2[sub]['q9A'] += 1
                elif feedback.q9 == 1:
                    temp2[sub]['q9P'] += 1
                else:
                    temp2[sub]['q9N'] += 1
                # Question 10
                if feedback.q10 == 5:
                    temp2[sub]['q10E'] += 1
                elif feedback.q10 == 4:
                    temp2[sub]['q10V'] += 1
                elif feedback.q10 == 3:
                    temp2[sub]['q10G'] += 1
                elif feedback.q10 == 2:
                    temp2[sub]['q10A'] += 1
                elif feedback.q10 == 1:
                    temp2[sub]['q10P'] += 1
                else:
                    temp2[sub]['q10N'] += 1
                # Question 11
                if feedback.q11 == 5:
                    temp2[sub]['q11E'] += 1
                elif feedback.q11 == 4:
                    temp2[sub]['q11V'] += 1
                elif feedback.q11 == 3:
                    temp2[sub]['q11G'] += 1
                elif feedback.q11 == 2:
                    temp2[sub]['q11A'] += 1
                elif feedback.q11 == 1:
                    temp2[sub]['q11P'] += 1
                else:
                    temp2[sub]['q11N'] += 1
                # Question 12
                if feedback.q12 == 5:
                    temp2[sub]['q12E'] += 1
                elif feedback.q12 == 4:
                    temp2[sub]['q12V'] += 1
                elif feedback.q12 == 3:
                    temp2[sub]['q12G'] += 1
                elif feedback.q12 == 2:
                    temp2[sub]['q12A'] += 1
                elif feedback.q12 == 1:
                    temp2[sub]['q12P'] += 1
                else:
                    temp2[sub]['q12N'] += 1
            # Calc total, out of, percentage for Thoery subjects
            if not temp2[sub]['status']:
                for i in range(1, 13):
                    temp2[sub]['q'+str(i)+'T'] = (temp2[sub]['q'+str(i)+'E'] * 5) + (temp2[sub]['q'+str(i)+'V'] * 4) + (temp2[sub]['q'+str(i)+'G'] * 3) + (temp2[sub]['q'+str(i)+'A'] * 2) + (temp2[sub]['q'+str(i)+'P'] * 1)
                    temp2[sub]['q'+str(i)+'O'] = (temp2[sub]['q'+str(i)+'E'] + temp2[sub]['q'+str(i)+'V'] + temp2[sub]['q'+str(i)+'G'] +
                        temp2[sub]['q'+str(i)+'A'] + temp2[sub]['q'+str(i)+'P'] + temp2[sub]['q'+str(i)+'N']) * 5
                    temp2[sub]['q'+str(i)+'Perc'] = (
                        "%.2f" % round(((temp2[sub]['q'+str(i)+'T'] * 100) / temp2[sub]['q'+str(i)+'O']), 2)
                        )
                    # Overall Calculation
                    temp2[sub]['subE'] += temp2[sub]['q'+str(i)+'E']
                    temp2[sub]['subV'] += temp2[sub]['q'+str(i)+'V']
                    temp2[sub]['subG'] += temp2[sub]['q'+str(i)+'G']
                    temp2[sub]['subA'] += temp2[sub]['q'+str(i)+'A']
                    temp2[sub]['subP'] += temp2[sub]['q'+str(i)+'P']
                    temp2[sub]['subN'] += temp2[sub]['q'+str(i)+'N']
                    temp2[sub]['subT'] += temp2[sub]['q'+str(i)+'T']
                    temp2[sub]['subO'] += temp2[sub]['q'+str(i)+'O']
                temp2[sub]['subPerc'] = (
                        "%.2f" % round(((temp2[sub]['subT'] * 100) / temp2[sub]['subO']), 2)
                        )
            # Calc total, out of, percentage for Practical subjects
            else:
                for i in range(1, 8):
                    temp2[sub]['q'+str(i)+'T'] = (temp2[sub]['q'+str(i)+'E'] * 5) + (temp2[sub]['q'+str(i)+'V'] * 4) + (temp2[sub]['q'+str(i)+'G'] * 3) + (temp2[sub]['q'+str(i)+'A'] * 2) + (temp2[sub]['q'+str(i)+'P'] * 1)
                    temp2[sub]['q'+str(i)+'O'] = (temp2[sub]['q'+str(i)+'E'] + temp2[sub]['q'+str(i)+'V'] + temp2[sub]['q'+str(i)+'G'] +
                        temp2[sub]['q'+str(i)+'A'] + temp2[sub]['q'+str(i)+'P'] + temp2[sub]['q'+str(i)+'N']) * 5
                    temp2[sub]['q'+str(i)+'Perc'] = (
                        "%.2f" % round(((temp2[sub]['q'+str(i)+'T'] * 100) / temp2[sub]['q'+str(i)+'O']), 2)
                        )
                    # Overall Calculation
                    temp2[sub]['subE'] += temp2[sub]['q'+str(i)+'E']
                    temp2[sub]['subV'] += temp2[sub]['q'+str(i)+'V']
                    temp2[sub]['subG'] += temp2[sub]['q'+str(i)+'G']
                    temp2[sub]['subA'] += temp2[sub]['q'+str(i)+'A']
                    temp2[sub]['subP'] += temp2[sub]['q'+str(i)+'P']
                    temp2[sub]['subN'] += temp2[sub]['q'+str(i)+'N']
                    temp2[sub]['subT'] += temp2[sub]['q'+str(i)+'T']
                    temp2[sub]['subO'] += temp2[sub]['q'+str(i)+'O']
                temp2[sub]['subPerc'] = (
                        "%.2f" % round(((temp2[sub]['subT'] * 100) / temp2[sub]['subO']), 2)
                        )
        except:
            for i in range(1, 13):
                temp2[sub]['q'+str(i)+'T'] = 0
                temp2[sub]['q'+str(i)+'O'] = 0
                temp2[sub]['q'+str(i)+'Perc'] = 0.0
    # When there is no feedback
    if len(subjects) > 0:
        i += 1
    context = {
        'teacher': teacher,
        'feedbacks': temp1,
        'feedbacks2': temp2,
        'i': i,
    }
    return render(request, "feedback/teacher/teacher_index.html", context)

@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def regular_suggestions(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(user=request.user)
        subject = Subject.objects.get(id=id, teacher=teacher)
    except:
        raise Http404("No Such Subject Found")
    feedback = Feedback.objects.filter(subject=subject)
    regular = Feedback.objects.filter(subject=subject, student__attendance__gte=75)
    context = {
        'regulars': regular,
        'feedback': feedback,
    }
    return render(request, "feedback/teacher/suggestions.html", context)

@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def defaulter_suggestions(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(user=request.user)
        subject = Subject.objects.get(id=id, teacher=teacher)
    except:
        raise Http404("No Such Subject Found")
    defaulter = Feedback.objects.filter(subject=subject, student__attendance__lt=75)
    feedback = Feedback.objects.filter(subject=subject)
    context = {
        'defaulters': defaulter,
        'feedback': feedback,
    }
    return render(request, "feedback/teacher/suggestions.html", context)

@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def all_suggestions(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(user=request.user, hod=True)
    except:
        return HttpResponseForbidden()
    feedbacks = Feedback.objects.filter(subject__department=teacher.department).exclude(teacher__user=request.user)
    length = len(feedbacks)
    context = {
        'feedbacks': feedbacks,
        'length': length,
    }
    return render(request, "feedback/teacher/all_suggestions.html", context)

@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def hod_suggestions(request, id, t_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    if not teacher.hod:
        return HttpResponseForbidden() 
    try:
        teacher = Teacher.objects.get(id=t_id)
        subject = Subject.objects.get(id=id, teacher=teacher)
    except:
        raise Http404("No Such Subject Found")
    feedback = Feedback.objects.filter(subject=subject)
    regular = Feedback.objects.filter(subject=subject, student__attendance__gte=75)
    defaulter = Feedback.objects.filter(subject=subject, student__attendance__lt=75)
    context = {
        'regulars': regular,
        'defaulters': defaulter,
        'feedback': feedback,
    }
    return render(request, "feedback/teacher/suggestions.html", context)

@require_http_methods(["GET", "POST"])
def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLogin(request.POST)
        # Getting Form Fields
        username = request.POST["username"]
        if not username:
            messages.success(request, "Must Provide Username!")
            return render(request, "feedback/teacher/teacher_login.html", {'form': form})
        password = request.POST["password"]
        if not password:
            messages.success(request, "Must Provide PassWord!!")
            return render(request, "feedback/teacher/teacher_login.html", {'form': form})
        user = authenticate(request, username=username,
                            password=password, is_staff=True)
        if not user:
            messages.success(request, "Username or Password did not Match!!!")
            return render(request, "feedback/teacher/teacher_login.html", {'form': form})
        try:
            teacher = Teacher.objects.get(user__username=user)
            if not teacher.user.is_staff:
                messages.success(request, "Waiting For approval from Admin!")
                return render(request, "feedback/teacher/teacher_login.html", {'form': form})
        except:
            messages.success(request, "You cannot access here!")
            return render(request, "feedback/teacher/teacher_login.html", {'form': form})
        login(request, user)
        return HttpResponseRedirect(reverse("teacher_index"))
    else:
        form = TeacherLogin()
        return render(request, "feedback/teacher/teacher_login.html", {'form': form})

@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def teacher_logout(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    logout(request)
    messages.success(request, "Logged Out")
    return HttpResponseRedirect(reverse("teacher_login"))


# Subject Managing Functions
@require_http_methods(["GET", "POST"])
@login_required(login_url="teacher_login")
def add_subject(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    user = Teacher.objects.get(user=request.user)
    if request.method == "POST":
        # subjects = Subject.objects.filter(department=user.department)
        subject = request.POST["subject"]
        if not subject:
            messages.success(request, "Must Provide Subject!")
            return HttpResponseRedirect(reverse("add_subject"))
        try:
            s = Subject.objects.get(subject_name=subject)
        except:
            pass
        teacher_id = request.POST["teacher"]
        if not teacher_id:
            messages.success(request, "Must Select Teacher!")
            return HttpResponseRedirect(reverse("add_subject"))
        teacher = Teacher.objects.get(id=teacher_id)
        semester = request.POST["semester"]
        if not semester:
            messages.success(request, "Must Select Semester!")
            return HttpResponseRedirect(reverse("add_subject"))
        practical = request.POST["practical"]
        if not practical:
            messages.success(request, "Must Select Subject Type!")
            return HttpResponseRedirect(reverse("add_subject"))
        assign_subject = Subject(
                subject_name=subject,
                teacher=teacher,
                department=user.department,
                semester=semester,
                practical=practical,
            )
        assign_subject.save()
        try:
            batch = request.POST.getlist('batch')
            for b in batch:
                batches = Batches(
                    subject=assign_subject,
                    teacher=teacher,
                    batch=b,
                )
                batches.save()
        except:
            pass
        messages.success(request, "Subject Assigned Successfully!")
        return HttpResponseRedirect(reverse("add_subject"))
    else:
        teachers = Teacher.objects.filter(user__is_staff=True).order_by('department')
        subjects = Subject.objects.filter(department=user.department, practical=False)
        batches = Batches.objects.filter(subject__department=user.department)
        i = j = 0
        if len(subjects) > 0:
            i += 1
        if len(batches) > 0:
            j += 1
        context = {
            'teachers': teachers,
            'subjects': subjects,
            'batches': batches,
            'i': i,
            'j': j
        }
        return render(request, "feedback/teacher/manage_subject.html", context)

# Theory Subjects 
@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def subject_details(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    try:
        subject = Subject.objects.get(id=id)
        context = {
            "subject": subject,
        }
    except:
        raise Http404("No Such Subject Found")
    return render(request,  "feedback/teacher/subject_details.html", context)

@require_http_methods(["POST"])
@login_required(login_url="teacher_login")
def subject_edit(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    subject_id = request.POST["id"]
    subject = Subject.objects.get(id=subject_id)
    subject.subject_name = request.POST["subjectName"]
    if not subject.subject_name:
        messages.success(request, "Please Provide Subject Name!")
        return HttpResponseRedirect(reverse("add_subject"))
    subject.semester = request.POST["semester"]
    if not subject.semester:
        messages.success(request, "Please Select a Semester!")
        return HttpResponseRedirect(reverse("add_subject"))
    subject.practical = "False"
    if not subject.practical:
        messages.success(request, "Please Select a Subject Type!")
        return HttpResponseRedirect(reverse("add_subject"))
    subject.save()
    messages.success(request, f"Subject {subject.subject_name} has been Updated Successfully!")
    return HttpResponseRedirect(reverse("add_subject"))

# Approval for delete
@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def subject_delete(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    try:
        subject = Subject.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request, "feedback/teacher/subject_delete.html", {"subject": subject})

# When action is Delete
@require_http_methods(["POST"])
@login_required(login_url="teacher_login")
def subject_deletion(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    subject_id = request.POST["id"]
    subject = Subject.objects.get(id=subject_id)
    subject.delete()
    messages.success(
        request, f"Subject {subject.subject_name} is deleted")
    return HttpResponseRedirect(reverse("add_subject"))

# Practical Subjects
@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def practical_details(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    try:
        batch = Batches.objects.get(id=id)
        context = {
            "batch": batch,
        }
    except:
        raise Http404("No Such Subject Found")
    return render(request,  "feedback/teacher/practical_details.html", context)

@require_http_methods(["POST"])
@login_required(login_url="teacher_login")
def practical_edit(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    batches_id = request.POST["id"]
    batches = Batches.objects.get(id=batches_id)
    batches.subject.subject_name = request.POST["subjectName"]
    if not batches.subject.subject_name:
        messages.success(request, "Please Provide Subject Name!")
        return HttpResponseRedirect(reverse("add_subject"))
    batches.subject.semester = request.POST["semester"]
    if not batches.subject.semester:
        messages.success(request, "Please Select a Semester!")
        return HttpResponseRedirect(reverse("add_subject"))
    batches.subject.practical = "True"
    if not batches.subject.practical:
        messages.success(request, "Please Select a Subject Type!")
        return HttpResponseRedirect(reverse("add_subject"))
    batches.save()
    messages.success(request, f"Subject {batches.subject.subject_name} has been Updated Successfully!")
    return HttpResponseRedirect(reverse("add_subject"))

# Approval for delete
@require_http_methods(["GET"])
@login_required(login_url="teacher_login")
def practical_delete(request, id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    try:
        batches = Batches.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request, "feedback/teacher/practical_delete.html", {"batches": batches})

# When action is Delete
@require_http_methods(["POST"])
@login_required(login_url="teacher_login")
def practical_deletion(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    elif request.user.is_superuser:
        return HttpResponseForbidden()
    teacher = Teacher.objects.get(user=request.user)
    batches_id = request.POST["id"]
    batches = Batches.objects.get(id=batches_id)
    batches.delete()
    messages.success(
        request, f"Subject {batches.subject.subject_name} is deleted")
    return HttpResponseRedirect(reverse("add_subject"))

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = TeacherRegister(request.POST)
        # Getting Form Fields
        first_name = request.POST["first_name"]
        if not first_name:
            messages.success(request, "Must provide first name")
            return render(request, "feedback/teacher/register.html", {'form': form})
        last_name = request.POST["last_name"]
        if not last_name:
            messages.success(request, "Must provide last name")
            return render(request, "feedback/teacher/register.html", {'form': form})
        email = request.POST["email"]
        if not email:
            messages.success(request, "Must provide Email")
            return render(request, "feedback/teacher/register.html", {'form': form})
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex, email)):
            pass
        else:
            messages.success(request, "Invalid Email")
            return render(request, "feedback/teacher/register.html", {'form': form})
        username = request.POST["username"]
        if not username:
            messages.success(request, "Must provide username")
            return render(request, "feedback/teacher/register.html", {'form': form})
        password = request.POST["password"]
        if not password:
            messages.success(request, "Must provide password")
            return render(request, "feedback/teacher/register.html", {'form': form})
        try:
            myuser = User.objects.get(username=username)
            messages.success(request, f"Username {myuser} Already Exist!!!")
            return render(request, "feedback/teacher/register.html", {'form': form})
        except:
            try:
                user = User.objects.get(email=email)
                messages.success(
                    request, f"Email {user.email} Already Exist!!!")
                return render(request, "feedback/teacher/register.html", {'form': form})
            except:
                department = request.POST["department"]
                if not department:
                    messages.success(request, "Must Select Department!")
                    return render(request, "feedback/teacher/register.html", {'form': form})
                departments = Department.objects.get(department_name=department)
                HOD = request.POST["HOD"]
                if not HOD:
                    messages.success(request, "Make a Choice for HOD")
                    return render(request, "feedback/teacher/register.html", {'form': form})
                coordinator = request.POST["coordinator"]
                if not coordinator:
                    messages.success(request, "Make a Choice for Feedback Co-ordinator")
                    return render(request, "feedback/teacher/register.html", {'form': form})
                try:
                    image = request.FILES['image']
                    my_suffixes = (".jpg", ".jpeg", ".png")
                    if not image.name.endswith(my_suffixes):
                        messages.success(request, 'THIS IS NOT A IMAGE FILE')
                        return render(request, "feedback/teacher/register.html", {'form': form})
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    teacher = Teacher(
                        user=user,
                        department=departments,
                        image=image,
                        hod=HOD,
                        coordinator=coordinator,
                    )
                    user.save()
                    teacher.save()
                except:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    teacher = Teacher(
                        user=user,
                        department=departments,
                        hod=HOD,
                        coordinator=coordinator,
                    )
                    user.save()
                    teacher.save()
                messages.success(
                    request, "Registration Completed! Wait for approval from Admin!!")
                return HttpResponseRedirect(reverse("teacher_login"))
    else:
        form = TeacherRegister()
        return render(request, "feedback/teacher/register.html", {'form': form})


# Admin Operations
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def sfsadmin_index(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher = Teacher.objects.filter(user__is_staff=False)
    length = len(teacher) # Total number of moderations
    form = csvFile()
    context = {
        "form": form,
        "length": length
    }
    return render(request, "feedback/admin/sfsadmin_index.html", context)

@require_http_methods(["GET", "POST"])
def sfsadmin_login(request):
    if request.method == 'POST':
        form = AdminLogin(request.POST)
        # Getting Form Fields
        username = request.POST["username"]
        if not username:
            messages.success(request, "Must Provide Username!")
            return render(request, "feedback/admin/sfsadmin_login.html", {'form': form})
        password = request.POST["password"]
        if not password:
            messages.success(request, "Must Provide Password!!")
            return render(request, "feedback/admin/sfsadmin_login.html", {'form': form})
        user = authenticate(request, username=username,
                            password=password, is_staff=True, is_superuser=True)                    
        if not user:
            messages.success(request, "Username and Password did not Match!!!")
            return render(request, "feedback/admin/sfsadmin_login.html", {'form': form})
        if not user.is_superuser:
            messages.success(request, "You cannot access here")
            return render(request, "feedback/admin/sfsadmin_login.html", {'form': form})
        login(request, user)
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    else:
        form = AdminLogin()
        return render(request, "feedback/admin/sfsadmin_login.html", {'form': form})

@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def sfsadmin_logout(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    logout(request)
    messages.success(request, "Logged Out")
    return HttpResponseRedirect(reverse("sfsadmin_login"))

@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def teacher_list(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher = Teacher.objects.filter(user__is_staff=False)
    length = len(teacher) # Total number of moderations
    teachers = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='First Year')
    t_chemicals = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='Chemical Engineering')
    t_civils = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='Civil Engineering')
    t_computers = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='Computer Engineering')
    t_extc = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='Extc Engineering')
    t_mechanicals = Teacher.objects.filter(user__is_staff=True, department__department_name__icontains='Mechanical Engineering')
    # Pagination - 5 Results Per Page
    # First Year
    fy_paginator = Paginator(teachers, 10)
    fy_page = request.GET.get("page1")
    fy_per_page = fy_paginator.get_page(fy_page)
    # Chemical
    chemicals_paginator = Paginator(t_chemicals, 10)
    chemicals_page = request.GET.get("page2")
    chemicals_per_page = chemicals_paginator.get_page(chemicals_page)
    # Civil
    civils_paginator = Paginator(t_civils, 10)
    civils_page = request.GET.get("page3")
    civils_per_page = civils_paginator.get_page(civils_page)
    # Computer
    computers_paginator = Paginator(t_computers, 10)
    computers_page = request.GET.get("page4")
    computers_per_page = computers_paginator.get_page(computers_page)
    # ExTC
    extc_paginator = Paginator(t_extc, 10)
    extc_page = request.GET.get("page5")
    extc_per_page = extc_paginator.get_page(extc_page)
    # Mechanical
    mechanicals_paginator = Paginator(t_mechanicals, 10)
    mechanicals_page = request.GET.get("page6")
    mechanicals_per_page = mechanicals_paginator.get_page(mechanicals_page)
    # Get Page Numbers
    try:
        page1 = request.GET["page1"]
    except:
        page1 = 1
    try:
        page2 = request.GET["page2"]
    except:
        page2 = 1
    try:
        page3 = request.GET["page3"]
    except:
        page3 = 1
    try:
        page4 = request.GET["page4"]
    except:
        page4 = 1
    try:
        page5 = request.GET["page5"]
    except:
        page5 = 1
    try:
        page6 = request.GET["page6"]
    except:
        page6 = 1
    context = {
        "length": length,
        "teachers": fy_per_page,
        "t_chemicals": chemicals_per_page,
        "t_civils": civils_per_page,
        "t_computers": computers_per_page,
        "t_extc": extc_per_page,
        "t_mechanicals": mechanicals_per_page,
        "page1": page1,
        "page2": page2,
        "page3": page3,
        "page4": page4,
        "page5": page5,
        "page6": page6,
        }
    return render(request, "feedback/teacher/teacher_list.html", context)

@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def teacher_details(request, id):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request,  "feedback/teacher/teacher_details.html", {"teacher": teacher})

@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def teacher_edit(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher_id = request.POST["id"]
    teacher = Teacher.objects.get(id=teacher_id)
    department = request.POST["department"]
    dept = Department.objects.get(department_name=department)
    teacher.department = dept
    if not dept:
        messages.success(request, "Please Select a Department!")
        return HttpResponseRedirect(reverse("teacher_list"))
    user = User.objects.get(username=teacher.user.username)
    user.username = request.POST["username"]
    if not user.username:
        messages.success(request, "Please Provide a Username!")
        return HttpResponseRedirect(reverse("teacher_list"))
    user.first_name = request.POST["first_name"]
    if not user.first_name:
        messages.success(request, "Please Provide a First Name!")
        return HttpResponseRedirect(reverse("teacher_list"))
    user.last_name = request.POST["last_name"]
    if not user.last_name:
        messages.success(request, "Please Provide a Last Name!")
        return HttpResponseRedirect(reverse("teacher_list"))
    user.email = request.POST["email"]
    if not user.email:
        messages.success(request, "Please Provide a Email!")
        return HttpResponseRedirect(reverse("teacher_list"))
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, user.email)):
        pass
    else:
        messages.success(
            request, f"Invalid Email for {teacher.user.first_name} {teacher.user.last_name}")
        return HttpResponseRedirect(reverse("teacher_list"))
    teacher.department.save()
    teacher.save()
    user.save()
    messages.success(
        request, f"Teacher {teacher.user.first_name} {teacher.user.last_name} has been Updated Successfully!")
    return HttpResponseRedirect(reverse("teacher_list"))

# Approval for delete
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def teacher_delete(request, id):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request, "feedback/teacher/teacher_delete.html", {"teacher": teacher})

# When action is Delete
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def teacher_deletion(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher_id = request.POST["id"]
    teacher = Teacher.objects.get(id=teacher_id)
    user = User.objects.get(username=teacher.user.username)
    user.delete()
    messages.success(
        request, f"Teacher {teacher.user.first_name} {teacher.user.last_name} is deleted")
    return HttpResponseRedirect(reverse("teacher_list"))

# Search for Teacher
# @require_http_methods(["POST"])
# @login_required(login_url="sfsadmin_login")
# def teacher_search(request):
#     search = request.POST["searchQuery"]
#     teacher_search = Teacher.objects.filter(
#         Q(user__first_name__startswith=search) | Q(user__last_name__startswith=search)
#         )
#     return render(request, "feedback/teacher/teacher_list.html", {"teachers": teacher_search})

# Displaying Student List
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def student_list(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher = Teacher.objects.filter(user__is_staff=False)
    length = len(teacher) # Total number of moderations
    students = Student.objects.filter(department__department_name__icontains='First Year')
    chemicals = Student.objects.filter(department__department_name__icontains='Chemical Engineering')
    civils = Student.objects.filter(department__department_name__icontains='Civil Engineering')
    computers = Student.objects.filter(department__department_name__icontains='Computer Engineering')
    extc = Student.objects.filter(department__department_name__icontains='Extc Engineering')
    mechanicals = Student.objects.filter(department__department_name__icontains='Mechanical Engineering')
    # Pagination - 5 Results Per Page
    # First Year
    fy_paginator = Paginator(students, 10)
    fy_page = request.GET.get("page1")
    fy_per_page = fy_paginator.get_page(fy_page)
    # Chemical
    chemicals_paginator = Paginator(chemicals, 10)
    chemicals_page = request.GET.get("page2")
    chemicals_per_page = chemicals_paginator.get_page(chemicals_page)
    # Civil
    civils_paginator = Paginator(civils, 10)
    civils_page = request.GET.get("page3")
    civils_per_page = civils_paginator.get_page(civils_page)
    # Computer
    computers_paginator = Paginator(computers, 10)
    computers_page = request.GET.get("page4")
    computers_per_page = computers_paginator.get_page(computers_page)
    # ExTC
    extc_paginator = Paginator(extc, 10)
    extc_page = request.GET.get("page5")
    extc_per_page = extc_paginator.get_page(extc_page)
    # Mechanical
    mechanicals_paginator = Paginator(mechanicals, 10)
    mechanicals_page = request.GET.get("page6")
    mechanicals_per_page = mechanicals_paginator.get_page(mechanicals_page)
    # Get Page Numbers
    try:
        page1 = request.GET["page1"]
    except:
        page1 = 1
    try:
        page2 = request.GET["page2"]
    except:
        page2 = 1
    try:
        page3 = request.GET["page3"]
    except:
        page3 = 1
    try:
        page4 = request.GET["page4"]
    except:
        page4 = 1
    try:
        page5 = request.GET["page5"]
    except:
        page5 = 1
    try:
        page6 = request.GET["page6"]
    except:
        page6 = 1
    context = {
        "length": length,
        "students": fy_per_page,
        "chemicals": chemicals_per_page,
        "civils": civils_per_page,
        "computers": computers_per_page,
        "extc": extc_per_page,
        "mechanicals": mechanicals_per_page,
        "page1": page1,
        "page2": page2,
        "page3": page3,
        "page4": page4,
        "page5": page5,
        "page6": page6,
    }
    return render(request, "feedback/student/student_list.html", context)

# Editing Student
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def student_details(request, id):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        student = Student.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request, "feedback/student/student_details.html", {"student": student})

# Saving the Edited Student
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def student_edit(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    student_id = request.POST["id"]
    student = Student.objects.get(id=student_id)
    department = request.POST["department"]
    dept = Department.objects.get(department_name=department)
    if not dept:
        messages.success(request, "Should Select Department")
        return HttpResponseRedirect(reverse("student_list"))
    student.department = dept
    student.semester = request.POST["semester"]
    if not student.semester:
        messages.success(request, "Should Select Semester")
        return HttpResponseRedirect(reverse("student_list"))
    student.attendance = float(request.POST["attendance"])
    if not student.attendance:
        messages.success(request, "Should Write Attendance")
        return HttpResponseRedirect(reverse("student_list"))
    if student.attendance > 100 or student.attendance < 0:
        messages.success(request, "Attendance is Out of Range")
        return HttpResponseRedirect(reverse("student_list"))
    user = User.objects.get(username=student.user.username)
    user.username = request.POST["username"]
    if not user.username:
        messages.success(request, "Should Provide Username")
        return HttpResponseRedirect(reverse("student_list"))
    user.first_name = request.POST["first_name"]
    if not user.first_name:
        messages.success(request, "Should Provide First Name")
        return HttpResponseRedirect(reverse("student_list"))
    user.last_name = request.POST["last_name"]
    if not user.last_name:
        messages.success(request, "Should Provide Last Name")
        return HttpResponseRedirect(reverse("student_list"))
    user.email = request.POST["email"]
    if not user.email:
        messages.success(request, "Should Provide Email")
        return HttpResponseRedirect(reverse("student_list"))
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex, user.email)):
        pass
    else:
        messages.success(
            request, f"Invalid Email for {user.first_name} {user.last_name}")
        return HttpResponseRedirect(reverse("student_list"))
    student.department.save()
    student.save()
    user.save()
    messages.success(
        request, f"Student {user.first_name} {user.last_name} has been Updated Successfully!")
    return HttpResponseRedirect(reverse("student_list"))

# Approval for delete
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def student_delete(request, id):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        student = Student.objects.get(id=id)
    except:
        raise Http404("No Such Student Found")
    return render(request, "feedback/student/student_delete.html", {"student": student})

# When action is Delete
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def student_deletion(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    student_id = request.POST["id"]
    student = Student.objects.get(id=student_id)
    user = User.objects.get(username=student.user.username)
    user.delete()
    messages.success(
        request, f"Student {student.user.first_name} {student.user.last_name} is deleted")
    return HttpResponseRedirect(reverse("student_list"))

# Uploading List of Student Using csv format
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def student_upload(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        csv_file = request.FILES['csv_file']
    except:
        messages.success(request, 'Must Select a FILE')
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if not csv_file.name.endswith('.csv'):
        messages.success(request, 'Wrong file format!!!')
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    data_set = csv_file.read().decode('UTF-8-SIG')
    io_string = io.StringIO(data_set)
    data = next(io_string).strip().split(',')
    data = [i.lower() for i in data]
    if "first name" in data:
        first_name = data.index("first name")
    else:
        messages.success(request, "Wrong format for First Name!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "last name" in data:
        last_name = data.index("last name")
    else:
        messages.success(request, "Wrong format for Last Name!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "registration number" in data:
        username = data.index("registration number")
    else:
        messages.success(request, "Wrong Format for Registration Number!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "dob" in data:
        password = data.index("dob")
    else:
        messages.success(request, "Wrong format for Date of Birth!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "batch" in data:
        batch = data.index("batch")
    else:
        messages.success(request, "Wrong format for Batch")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "attendance" in data:
        attendance = data.index("attendance")
    else:
        messages.success(request, "Wrong format for Attendance!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "department" in data:
        department = data.index("department")
    else:
        messages.success(request, "Wrong format for Department!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "semester" in data:
        semester = data.index("semester")
    else:
        messages.success(request, "Wrong format for Semester!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    if "email" in data:
        email = data.index("email")
    else:
        messages.success(request, "Wrong format for E-Mail Address!")
        return HttpResponseRedirect(reverse("sfsadmin_index"))
    count = 1
    for row in csv.reader(io_string):
        count += 1
        # Vaidations for blank Fields
        if not row[username]:
            messages.success(
                request, f"Please Provide a Registration Number! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[password]:
            messages.success(
                request, f"Please Provide a DOB! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[first_name]:
            messages.success(
                request, f"Please Provide a First Name! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[last_name]:
            messages.success(
                request, f"Please Provide a Last Name! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[attendance]:
            messages.success(
                request, f"Please Provide a Attendance! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[batch]:
            messages.success(
                request, f"Please Provide a Batch of student! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[email]:
            messages.success(
                request, f"Please Provide a Email Address! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[department]:
            messages.success(
                request, f"Please Provide a Department! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        if not row[semester]:
            messages.success(
                request, f"Please Provide a Semester! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # When Semester is Out of Range
        sem = int(row[semester])
        if sem > 8 or sem < 1:
            messages.success(
                request, f"Semester Should be in between 1 to 8 (Error on line {count}) for user {row[first_name]} {row[last_name]}")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # When Attendance is out of Range
        present = float(row[attendance])
        if present > 100 or present < 0:
            messages.success(
                request, f"Attendance Should be in between 0 to 100 (Error on line {count}) for user {row[first_name]} {row[last_name]}")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # When Batch is not valid
        if not row[batch] in ['b1', 'b2', 'b3', 'b4']:
            messages.success(
                request, f"Batch is not valid for user {row[first_name]} {row[last_name]}. It should only be (b1, b2, b3, b4) (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # when username length is small 
        if len(row[username]) < 3:
            messages.error(
                request, f"Length of Registration number should be greater than 3 (Error on line {count}")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # when password length is small
        if len(row[password]) < 8:
            messages.success(
                request, f"Length of Date of Birth should be greater than 8 (Error on line {count}")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        # Email Validation
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if(re.search(regex, row[email])):
            pass
        else:
            messages.error(
                request, f"Invalid Email for {row[first_name]} {row[last_name]} (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        try:
            dept = Department.objects.get(
                department_name__icontains=row[department])
        except:
            messages.success(
                request, f"Selected Department for {row[first_name]} {row[last_name]} is not Present! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        try:
            myuser = User.objects.get(username=row[username])
            messages.success(
                request, f"Username {myuser} Already Exist! (Error on line {count})")
            return HttpResponseRedirect(reverse("sfsadmin_index"))
        except:
            try:
                user = User.objects.get(email=row[email])
                messages.success(
                    request, f"Email {user.email} Already Exist! (Error on line {count})")
                return HttpResponseRedirect(reverse("sfsadmin_index"))
            except:
                pass
    # Saving 
    io_string = io.StringIO(data_set)
    data = next(io_string).strip().split(',')
    data = [i.lower() for i in data]
    all_data = []
    for row in csv.reader(io_string):
        row_data = {}
        for column in row:
            row_data[data[row.index(column)]] = column
        all_data.append(row_data)
    for data in all_data:
        user = User.objects.create_user(
                    first_name=data["first name"],
                    last_name=data["last name"],
                    username=data["registration number"],
                    password=data["dob"],
                    email=data["email"],
                )
        user = User.objects.get(username=data["registration number"])
        dept = Department.objects.get(
                department_name__icontains=data["department"])
        student = Student.objects.create(
            user=user,
            department=dept,
            semester=data["semester"],
            attendance=data["attendance"],
            batch=data["batch"],
        )
        user.save()
        student.save()
    messages.success(request, f"Student Data Added Successfully!")
    return HttpResponseRedirect(reverse("sfsadmin_index"))

# List of teacher approvals
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def moderate(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher = Teacher.objects.filter(user__is_staff=False)
    length = len(teacher)
    context = {
        "teacher": teacher,
        "length": length,
    }
    return render(request, "feedback/teacher/moderate.html", context)

# details of individual teacher request
@require_http_methods(["GET"])
@login_required(login_url="sfsadmin_login")
def moderate_details(request, id):
    if not request.user.is_superuser: return HttpResponseForbidden()
    try:
        teacher = Teacher.objects.get(id=id)
    except:
        raise Http404("Teacher Not Found")
    return render(request, "feedback/teacher/details.html", {"teacher": teacher})

@require_http_methods(["GET", "POST"])
@login_required(login_url="sfsadmin_login")
def details(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    if request.method == "POST":
        if request.POST == approve:
            return HttpResponseRedirect(reverse("approve"))
        else:
            return HttpResponseRedirect(reverse("decline"))
    else:
        teacher = Teacher.objects.filter(user__is_staff=False)
        return render(request, "feedback/teacher/details.html", {"teacher": teacher})

# Approval of Teacher Request
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def approve(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher_id = request.POST["id"]
    teacher = Teacher.objects.get(id=teacher_id)
    user = User.objects.get(username=teacher.user.username)
    user.is_staff = True
    user.save()
    hod = request.POST["HOD"]
    teacher.hod = hod
    coordinator = request.POST["coordinator"]
    teacher.coordinator = coordinator
    teacher.save()
    # Email after Approval
    subject = 'Registration Successfull'
    message = f"""
    You can now Login to Teacher Module of student feedback system with username {user.username}.
    click on link below to go to login page
    http://127.0.0.1:8000/teacher/
    """
    email_from = settings.EMAIL_HOST_USER
    teacher_list = [user.email, ]
    send_mail(subject, message, email_from, teacher_list)
    messages.success(request, f"User {user.first_name} {user.last_name} is Authorized Successfully!")
    return HttpResponseRedirect(reverse("moderate"))

# Declining teacher request
@require_http_methods(["POST"])
@login_required(login_url="sfsadmin_login")
def decline(request):
    if not request.user.is_superuser: return HttpResponseForbidden()
    teacher_id = request.POST["id"]
    teacher = Teacher.objects.get(id=teacher_id)
    user = User.objects.get(username=teacher.user.username)
    user.delete()
    messages.success(request, f"User {user.first_name} {user.last_name} is deleted")
    return HttpResponseRedirect(reverse("moderate"))
