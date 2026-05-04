from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pathway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=220, unique=True, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Parcours',
                'verbose_name_plural': 'Parcours',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='CourseModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Ordre')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('illustration', models.ImageField(blank=True, null=True, upload_to='baptisma/modules/', verbose_name='Image')),
                ('badge_name', models.CharField(blank=True, max_length=100, verbose_name='Nom du badge')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pathway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='baptisma_core.pathway', verbose_name='Parcours')),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
                'ordering': ['pathway', 'order', 'title'],
                'unique_together': {('pathway', 'order'), ('pathway', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Titre')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Ordre')),
                ('content', models.TextField(blank=True, verbose_name='Contenu')),
                ('key_verse_reference', models.CharField(blank=True, max_length=150, verbose_name='Référence du verset clé')),
                ('key_verse_text', models.TextField(blank=True, verbose_name='Texte du verset clé')),
                ('requires_manual_validation', models.BooleanField(default=False, verbose_name='Validation manuelle requise (instructeur)')),
                ('passing_score', models.PositiveSmallIntegerField(default=70, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Score minimal (%)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='baptisma_core.coursemodule', verbose_name='Module')),
            ],
            options={
                'verbose_name': 'Leçon',
                'verbose_name_plural': 'Leçons',
                'ordering': ['module__order', 'order', 'title'],
                'unique_together': {('module', 'order'), ('module', 'title')},
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(verbose_name='Énoncé')),
                ('options', models.JSONField(default=list, verbose_name='Options')),
                ('correct_answer', models.CharField(max_length=255, verbose_name='Bonne réponse')),
                ('explanation', models.TextField(blank=True, verbose_name='Explication')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Ordre')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='baptisma_core.lesson', verbose_name='Leçon')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['lesson', 'order'],
                'unique_together': {('lesson', 'order')},
            },
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('LOCKED', 'Locked'), ('CURRENT', 'Current'), ('COMPLETED', 'Completed')], default='LOCKED', max_length=20, verbose_name='Statut')),
                ('score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Score')),
                ('quiz_passed', models.BooleanField(default=False, verbose_name='Quiz validé')),
                ('instructor_validated', models.BooleanField(default=False, verbose_name='Validation instructeur')),
                ('validated_at', models.DateTimeField(blank=True, null=True, verbose_name='Validé le')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Terminé le')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_entries', to='baptisma_core.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_progress', to=settings.AUTH_USER_MODEL)),
                ('validated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='validated_learning_steps', to=settings.AUTH_USER_MODEL, verbose_name='Validé par')),
            ],
            options={
                'verbose_name': 'Progression',
                'verbose_name_plural': 'Progressions',
                'ordering': ['lesson__module__order', 'lesson__order', 'lesson__title'],
                'unique_together': {('user', 'lesson')},
            },
        ),
        migrations.CreateModel(
            name='ModuleBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('awarded_at', models.DateTimeField(auto_now_add=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='badges', to='baptisma_core.coursemodule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='module_badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Badge module',
                'verbose_name_plural': 'Badges modules',
                'ordering': ['-awarded_at'],
                'unique_together': {('user', 'module')},
            },
        ),
    ]
