from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Lesson, ModuleBadge, Pathway, Progress, initialize_user_progress


def _is_instructor(user):
    return (
        user.is_superuser
        or user.groups.filter(name="Instructeur").exists()
        or user.groups.filter(name="Instructor").exists()
    )


@login_required
def candidate_dashboard(request):
    pathway = Pathway.objects.filter(is_active=True).prefetch_related("modules__lessons").first()
    if not pathway:
        return render(request, "baptisma_core/dashboard.html", {"pathway": None})

    initialize_user_progress(request.user, pathway)
    user_progress = Progress.objects.filter(
        user=request.user,
        lesson__module__pathway=pathway
    ).select_related("lesson", "lesson__module")

    progress_by_lesson = {progress.lesson_id: progress for progress in user_progress}

    total_lessons = user_progress.count()
    completed_lessons = user_progress.filter(status=Progress.Status.COMPLETED).count()
    progress_percent = round((completed_lessons / total_lessons) * 100, 2) if total_lessons else 0

    badges = ModuleBadge.objects.filter(
        user=request.user,
        module__pathway=pathway
    ).select_related("module")
    module_cards = []
    for module in pathway.modules.all().order_by("order", "id"):
        lesson_rows = []
        for lesson in module.lessons.all().order_by("order", "id"):
            lesson_rows.append(
                {
                    "lesson": lesson,
                    "progress": progress_by_lesson.get(lesson.id),
                }
            )
        module_cards.append({"module": module, "lessons": lesson_rows})

    context = {
        "pathway": pathway,
        "module_cards": module_cards,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percent": progress_percent,
        "badges": badges,
    }
    return render(request, "baptisma_core/dashboard.html", context)


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects.select_related("module", "module__pathway").prefetch_related("questions"),
        id=lesson_id
    )

    initialize_user_progress(request.user, lesson.module.pathway)
    progress = get_object_or_404(Progress, user=request.user, lesson=lesson)

    if progress.status == Progress.Status.LOCKED:
        messages.error(request, "Cette leçon est verrouillée. Terminez la leçon en cours d'abord.")
        return redirect("baptisma_core:dashboard")

    questions = lesson.questions.all().order_by("order")

    if request.method == "POST":
        total_questions = questions.count()
        correct_answers = 0

        for question in questions:
            answer = request.POST.get(f"question_{question.id}", "")
            if question.is_correct(answer):
                correct_answers += 1

        score = round((correct_answers / total_questions) * 100, 2) if total_questions else 0
        progress.mark_quiz_result(score)

        if progress.status == Progress.Status.COMPLETED:
            messages.success(request, f"Leçon validée avec succès ({score}%).")
        elif progress.lesson.requires_manual_validation:
            messages.info(
                request,
                f"Quiz réussi ({score}%). Cette leçon nécessite aussi une validation manuelle par un instructeur."
            )
        else:
            messages.warning(request, f"Quiz non validé ({score}%). Reprenez la leçon puis réessayez.")
        return redirect("baptisma_core:dashboard")

    return render(
        request,
        "baptisma_core/lesson_detail.html",
        {
            "lesson": lesson,
            "progress": progress,
            "questions": questions,
        },
    )


@login_required
@user_passes_test(_is_instructor)
def instructor_dashboard(request):
    pending_validation = Progress.objects.filter(
        status=Progress.Status.CURRENT,
        lesson__requires_manual_validation=True
    ).select_related("user", "lesson", "lesson__module", "lesson__module__pathway")

    return render(
        request,
        "baptisma_core/instructor_dashboard.html",
        {"pending_validation": pending_validation},
    )


@login_required
@user_passes_test(_is_instructor)
def validate_progress(request, progress_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    progress = get_object_or_404(Progress.objects.select_related("lesson"), id=progress_id)
    progress.validate_manually(request.user)
    messages.success(request, f"Validation manuelle enregistrée pour {progress.user.username}.")
    return redirect("baptisma_core:instructor_dashboard")


@login_required
def progress_snapshot(request):
    pathway = Pathway.objects.filter(is_active=True).first()
    if not pathway:
        return JsonResponse({"progress_percent": 0, "completed_lessons": 0, "total_lessons": 0})

    initialize_user_progress(request.user, pathway)
    user_progress = Progress.objects.filter(user=request.user, lesson__module__pathway=pathway)
    total_lessons = user_progress.count()
    completed_lessons = user_progress.filter(status=Progress.Status.COMPLETED).count()
    progress_percent = round((completed_lessons / total_lessons) * 100, 2) if total_lessons else 0

    return JsonResponse(
        {
            "progress_percent": progress_percent,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
        }
    )
