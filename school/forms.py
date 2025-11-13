from django import forms
from .models import Student, Enrollment, Assignment, AssignmentSubmission, Exam, ExamResult
from members.models import Member


class StudentForm(forms.ModelForm):
    """Form for creating/updating a student."""
    
    class Meta:
        model = Student
        fields = ['member', 'student_number', 'enrollment_date', 'status', 'notes']
        widgets = {
            'enrollment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'member': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter members who are not already students
        existing_student_members = Student.objects.values_list('member_id', flat=True)
        self.fields['member'].queryset = Member.objects.exclude(id__in=existing_student_members)


class EnrollmentForm(forms.ModelForm):
    """Form for enrolling a student in a session."""
    
    class Meta:
        model = Enrollment
        fields = ['student', 'session', 'status', 'final_grade', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'final_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AssignmentForm(forms.ModelForm):
    """Form for creating/updating an assignment."""
    
    class Meta:
        model = Assignment
        fields = ['module', 'title', 'description', 'due_date', 'max_score', 'file']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    """Form for submitting an assignment."""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['file', 'comments']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Commentaires optionnels...'}),
        }


class GradeSubmissionForm(forms.ModelForm):
    """Form for grading a submission."""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ExamForm(forms.ModelForm):
    """Form for creating/updating an exam."""
    
    class Meta:
        model = Exam
        fields = ['module', 'title', 'description', 'exam_date', 'duration', 'max_score', 'location']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'exam_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2:00:00 pour 2 heures'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ExamResultForm(forms.ModelForm):
    """Form for recording exam results."""
    
    class Meta:
        model = ExamResult
        fields = ['student', 'score', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
