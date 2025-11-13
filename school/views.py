from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Sum
from django.utils import timezone
from .models import (
    Student, Enrollment, Session, Assignment, 
    AssignmentSubmission, Exam, ExamResult, Module
)
from .forms import (
    StudentForm, EnrollmentForm, AssignmentForm, 
    AssignmentSubmissionForm, GradeSubmissionForm, 
    ExamForm, ExamResultForm
)


@login_required
def student_list(request):
    """Display list of all students."""
    students = Student.objects.select_related('member').all()
    
    # Search functionality
    search = request.GET.get('search', '')
    if search:
        students = students.filter(
            Q(student_number__icontains=search) |
            Q(member__first_name__icontains=search) |
            Q(member__last_name__icontains=search)
        )
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        students = students.filter(status=status)
    
    context = {
        'students': students,
        'search': search,
        'status': status,
    }
    return render(request, 'school/student_list.html', context)


@login_required
def student_detail(request, pk):
    """Display student details with enrollments and grades."""
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('session').all()
    submissions = student.submissions.select_related('assignment__module').all()
    exam_results = student.exam_results.select_related('exam__module').all()
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'submissions': submissions,
        'exam_results': exam_results,
    }
    return render(request, 'school/student_detail.html', context)


@login_required
def student_create(request):
    """Create a new student."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Étudiant {student.student_number} créé avec succès.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    
    context = {'form': form, 'title': 'Nouvel étudiant'}
    return render(request, 'school/student_form.html', context)


@login_required
def student_update(request, pk):
    """Update an existing student."""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations de l\'étudiant mises à jour.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    
    context = {'form': form, 'student': student, 'title': 'Modifier étudiant'}
    return render(request, 'school/student_form.html', context)


@login_required
def enrollment_create(request):
    """Enroll a student in a session."""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f'Étudiant inscrit dans la session {enrollment.session.name}.')
            return redirect('student_detail', pk=enrollment.student.pk)
    else:
        # Pre-fill student if provided in URL
        student_id = request.GET.get('student')
        initial = {'student': student_id} if student_id else {}
        form = EnrollmentForm(initial=initial)
    
    context = {'form': form, 'title': 'Nouvelle inscription'}
    return render(request, 'school/enrollment_form.html', context)


@login_required
def enrollment_list(request):
    """Display list of all enrollments."""
    enrollments = Enrollment.objects.select_related('student__member', 'session').all()
    
    # Filter by session
    session_id = request.GET.get('session')
    if session_id:
        enrollments = enrollments.filter(session_id=session_id)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        enrollments = enrollments.filter(status=status)
    
    sessions = Session.objects.all()
    
    context = {
        'enrollments': enrollments,
        'sessions': sessions,
        'selected_session': session_id,
        'selected_status': status,
    }
    return render(request, 'school/enrollment_list.html', context)


@login_required
def assignment_list(request):
    """Display list of assignments."""
    assignments = Assignment.objects.select_related('module__session').all()
    
    # Filter by module
    module_id = request.GET.get('module')
    if module_id:
        assignments = assignments.filter(module_id=module_id)
    
    modules = Module.objects.select_related('session').all()
    
    context = {
        'assignments': assignments,
        'modules': modules,
        'selected_module': module_id,
    }
    return render(request, 'school/assignment_list.html', context)


@login_required
def assignment_detail(request, pk):
    """Display assignment details with submissions."""
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = assignment.submissions.select_related('student__member').all()
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'school/assignment_detail.html', context)


@login_required
def exam_list(request):
    """Display list of exams."""
    exams = Exam.objects.select_related('module__session').all()
    
    # Filter by module
    module_id = request.GET.get('module')
    if module_id:
        exams = exams.filter(module_id=module_id)
    
    modules = Module.objects.select_related('session').all()
    
    context = {
        'exams': exams,
        'modules': modules,
        'selected_module': module_id,
    }
    return render(request, 'school/exam_list.html', context)


@login_required
def exam_detail(request, pk):
    """Display exam details with results."""
    exam = get_object_or_404(Exam, pk=pk)
    results = exam.results.select_related('student__member').all()
    
    # Calculate statistics
    avg_score = results.aggregate(Avg('score'))['score__avg']
    
    context = {
        'exam': exam,
        'results': results,
        'avg_score': avg_score,
    }
    return render(request, 'school/exam_detail.html', context)
