from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from baptisma_core.models import CourseModule, Lesson, Pathway, Question


class Command(BaseCommand):
    help = "Charge le contenu MVP BAPTISMA-CORE (7 modules de base)."

    def handle(self, *args, **options):
        pathway, _ = Pathway.objects.get_or_create(
            slug="parcours-bapteme-adg-mp",
            defaults={
                "title": "Parcours Baptême ADG MP",
                "description": "Parcours initial de formation pour les candidats au baptême.",
                "is_active": True,
            },
        )
        if not pathway.title:
            pathway.title = "Parcours Baptême ADG MP"
            pathway.save(update_fields=["title", "updated_at"])

        module_titles = [
            "Le Salut en Jésus-Christ",
            "La Bible",
            "Dieu : Père, Fils et Saint-Esprit",
            "La Vie de Prière",
            "Le Baptême d'Eau",
            "Le Baptême du Saint-Esprit",
            "La Dîme et les Offrandes",
        ]

        for order, title in enumerate(module_titles, start=1):
            module, _ = CourseModule.objects.get_or_create(
                pathway=pathway,
                order=order,
                defaults={
                    "title": title,
                    "description": f"Module {order} : {title}",
                    "badge_name": f"Badge {slugify(title)}",
                },
            )
            if not module.title:
                module.title = title
                module.save(update_fields=["title", "updated_at"])

            lesson, _ = Lesson.objects.get_or_create(
                module=module,
                order=1,
                defaults={
                    "title": f"{title} - Introduction",
                    "content": (
                        f"Contenu initial du module « {title} ».\n"
                        "Ce bloc est éditable depuis l'administration."
                    ),
                    "key_verse_reference": "Jean 3:16",
                    "key_verse_text": "Car Dieu a tant aimé le monde...",
                    "requires_manual_validation": False,
                    "passing_score": 70,
                },
            )

            Question.objects.get_or_create(
                lesson=lesson,
                order=1,
                defaults={
                    "statement": "Cette leçon vous semble-t-elle comprise ?",
                    "options": ["Oui", "Non", "En cours"],
                    "correct_answer": "Oui",
                    "explanation": "Cette question est un exemple initial, modifiable en admin.",
                },
            )

        for group_name in ("Candidat", "Instructeur", "Administrateur"):
            Group.objects.get_or_create(name=group_name)

        self.stdout.write(self.style.SUCCESS("Contenu MVP BAPTISMA-CORE chargé avec succès."))
