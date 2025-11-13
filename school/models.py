from django.db import models
from members.models import Member # For teacher in Module

class Promotion(models.Model):
    """Represents a group of students starting together (e.g., 'Promotion 2025')."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la promotion")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-start_date']

class Session(models.Model):
    """Represents a specific period of study within a promotion."""
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name="sessions", verbose_name="Promotion")
    name = models.CharField(max_length=100, verbose_name="Nom de la session")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.promotion.name})"

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
        unique_together = ('promotion', 'name') # Session name unique within a promotion
        ordering = ['-start_date']

class Module(models.Model):
    """Represents a course within a session."""
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="modules", verbose_name="Session")
    title = models.CharField(max_length=200, verbose_name="Titre du module")
    description = models.TextField(blank=True, verbose_name="Description")
    teacher = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="taught_modules", verbose_name="Enseignant")
    resources = models.FileField(upload_to='school_resources/', null=True, blank=True, verbose_name="Ressources (PDF/Vidéo)")
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, default=1.0, verbose_name="Coefficient")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.session.name})"

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        unique_together = ('session', 'title') # Module title unique within a session
        ordering = ['title']

class Student(models.Model):
    """Represents a student (linked to a Member)."""
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="student_profile", verbose_name="Membre")
    student_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro d'étudiant")
    enrollment_date = models.DateField(verbose_name="Date d'inscription")
    status_choices = [
        ('candidat', 'Candidat'),
        ('actif', 'Actif'),
        ('diplome', 'Diplômé'),
        ('abandonne', 'Abandonné'),
        ('suspendu', 'Suspendu')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='candidat', verbose_name="Statut")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student_number} - {self.member.first_name} {self.member.last_name}"
    
    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['student_number']

class Enrollment(models.Model):
    """Represents a student's enrollment in a session."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments", verbose_name="Étudiant")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="enrollments", verbose_name="Session")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Date d'inscription")
    status_choices = [
        ('inscrit', 'Inscrit'),
        ('en_cours', 'En cours'),
        ('complete', 'Complété'),
        ('echoue', 'Échoué'),
        ('abandonne', 'Abandonné')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='inscrit', verbose_name="Statut")
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note finale")
    remarks = models.TextField(blank=True, verbose_name="Remarques")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.session}"
    
    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together = ('student', 'session')
        ordering = ['-enrollment_date']

class Assignment(models.Model):
    """Represents a homework assignment for a module."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="assignments", verbose_name="Module")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Consignes")
    due_date = models.DateTimeField(verbose_name="Date de remise")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note maximale")
    file = models.FileField(upload_to='assignments/', null=True, blank=True, verbose_name="Fichier joint")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.module.title})"
    
    class Meta:
        verbose_name = "Devoir"
        verbose_name_plural = "Devoirs"
        ordering = ['-due_date']

class AssignmentSubmission(models.Model):
    """Represents a student's submission for an assignment."""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions", verbose_name="Devoir")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions", verbose_name="Étudiant")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de soumission")
    file = models.FileField(upload_to='submissions/', null=True, blank=True, verbose_name="Fichier soumis")
    comments = models.TextField(blank=True, verbose_name="Commentaires de l'étudiant")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Note obtenue")
    feedback = models.TextField(blank=True, verbose_name="Feedback de l'enseignant")
    graded_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_submissions", verbose_name="Noté par")
    graded_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de notation")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.assignment.title}"
    
    @property
    def is_late(self):
        """Check if submission was late."""
        return self.submitted_at > self.assignment.due_date
    
    class Meta:
        verbose_name = "Soumission de devoir"
        verbose_name_plural = "Soumissions de devoirs"
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

class Exam(models.Model):
    """Represents a final exam for a module."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="exams", verbose_name="Module")
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    exam_date = models.DateTimeField(verbose_name="Date de l'examen")
    duration = models.DurationField(verbose_name="Durée")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note maximale")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.module.title}"
    
    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Examens"
        ordering = ['-exam_date']

class ExamResult(models.Model):
    """Represents a student's result for an exam."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results", verbose_name="Examen")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="exam_results", verbose_name="Étudiant")
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Note obtenue")
    remarks = models.TextField(blank=True, verbose_name="Remarques")
    graded_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="graded_exams", verbose_name="Noté par")
    graded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de notation")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student} - {self.exam.title}: {self.score}/{self.exam.max_score}"
    
    @property
    def percentage(self):
        """Calculate percentage score."""
        if self.exam.max_score > 0:
            return (self.score / self.exam.max_score) * 100
        return 0
    
    class Meta:
        verbose_name = "Résultat d'examen"
        verbose_name_plural = "Résultats d'examens"
        unique_together = ('exam', 'student')
        ordering = ['-graded_at']
