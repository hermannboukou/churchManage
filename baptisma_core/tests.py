from django.contrib.auth.models import User
from django.test import TestCase

from .models import CourseModule, Lesson, ModuleBadge, Pathway, Progress, Question, initialize_user_progress


class BaptismaCoreProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="candidat", password="secret123")
        self.pathway = Pathway.objects.create(
            title="Parcours Baptême",
            slug="parcours-bapteme",
            description="Parcours test"
        )
        self.module_1 = CourseModule.objects.create(pathway=self.pathway, title="Module 1", order=1)
        self.module_2 = CourseModule.objects.create(pathway=self.pathway, title="Module 2", order=2)

        self.lesson_1 = Lesson.objects.create(module=self.module_1, title="Leçon 1", order=1, passing_score=70)
        self.lesson_2 = Lesson.objects.create(module=self.module_2, title="Leçon 2", order=1, passing_score=70)

        Question.objects.create(
            lesson=self.lesson_1,
            statement="Question 1",
            options=["A", "B", "C"],
            correct_answer="A",
            order=1,
        )
        Question.objects.create(
            lesson=self.lesson_2,
            statement="Question 2",
            options=["Oui", "Non"],
            correct_answer="Oui",
            order=1,
        )

    def test_initialize_progress_unlocks_first_lesson(self):
        initialize_user_progress(self.user, self.pathway)
        p1 = Progress.objects.get(user=self.user, lesson=self.lesson_1)
        p2 = Progress.objects.get(user=self.user, lesson=self.lesson_2)
        self.assertEqual(p1.status, Progress.Status.CURRENT)
        self.assertEqual(p2.status, Progress.Status.LOCKED)

    def test_quiz_success_unlocks_next_lesson_and_awards_badge(self):
        initialize_user_progress(self.user, self.pathway)
        progress_lesson_1 = Progress.objects.get(user=self.user, lesson=self.lesson_1)
        progress_lesson_1.mark_quiz_result(90)

        progress_lesson_1.refresh_from_db()
        progress_lesson_2 = Progress.objects.get(user=self.user, lesson=self.lesson_2)

        self.assertEqual(progress_lesson_1.status, Progress.Status.COMPLETED)
        self.assertEqual(progress_lesson_2.status, Progress.Status.CURRENT)
        self.assertTrue(ModuleBadge.objects.filter(user=self.user, module=self.module_1).exists())
