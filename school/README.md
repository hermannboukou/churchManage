# Module École - Inscription des Étudiants

## Vue d'ensemble

Le module école permet de gérer l'inscription des étudiants, leurs sessions de formation, les devoirs, les examens et les notes.

## Modèles de données

### 1. Student (Étudiant)
Représente un étudiant lié à un membre de l'église.

**Champs principaux :**
- `member` : Lien vers le membre (OneToOne)
- `student_number` : Numéro d'étudiant unique
- `enrollment_date` : Date d'inscription initiale
- `status` : Statut (candidat, actif, diplômé, abandonné, suspendu)
- `notes` : Notes supplémentaires

### 2. Enrollment (Inscription)
Représente l'inscription d'un étudiant dans une session spécifique.

**Champs principaux :**
- `student` : L'étudiant inscrit
- `session` : La session d'inscription
- `status` : Statut de l'inscription (inscrit, en cours, complété, échoué, abandonné)
- `final_grade` : Note finale
- `remarks` : Remarques

### 3. Assignment (Devoir)
Représente un devoir à faire pour un module.

**Champs principaux :**
- `module` : Module concerné
- `title` : Titre du devoir
- `description` : Consignes détaillées
- `due_date` : Date limite de remise
- `max_score` : Note maximale
- `file` : Fichier joint (optionnel)

### 4. AssignmentSubmission (Soumission de devoir)
Représente la soumission d'un devoir par un étudiant.

**Champs principaux :**
- `assignment` : Le devoir concerné
- `student` : L'étudiant qui soumet
- `file` : Fichier soumis
- `comments` : Commentaires de l'étudiant
- `score` : Note obtenue
- `feedback` : Feedback de l'enseignant
- `graded_by` : Enseignant qui a noté
- `is_late` : Propriété calculée indiquant si la soumission est en retard

### 5. Exam (Examen)
Représente un examen final pour un module.

**Champs principaux :**
- `module` : Module concerné
- `title` : Titre de l'examen
- `exam_date` : Date de l'examen
- `duration` : Durée de l'examen
- `max_score` : Note maximale
- `location` : Lieu de l'examen

### 6. ExamResult (Résultat d'examen)
Représente le résultat d'un étudiant à un examen.

**Champs principaux :**
- `exam` : L'examen concerné
- `student` : L'étudiant
- `score` : Note obtenue
- `remarks` : Remarques
- `graded_by` : Enseignant qui a noté
- `percentage` : Propriété calculée du pourcentage obtenu

## Fonctionnalités

### Administration Django

Tous les modèles sont disponibles dans l'administration Django avec :
- Affichage optimisé des listes
- Filtres par session, statut, dates
- Recherche par nom, numéro d'étudiant
- Inlines pour gérer les relations (inscriptions, soumissions, résultats)

### Vues disponibles

#### Étudiants
- **Liste des étudiants** : `/school/students/`
  - Recherche par nom ou numéro
  - Filtrage par statut
  
- **Détail étudiant** : `/school/students/<id>/`
  - Affiche les informations complètes
  - Liste des inscriptions
  - Historique des devoirs soumis
  - Résultats d'examens

- **Créer un étudiant** : `/school/students/create/`
  - Formulaire de création
  - Sélection d'un membre non encore étudiant
  - Attribution automatique du numéro d'étudiant

- **Modifier un étudiant** : `/school/students/<id>/update/`

#### Inscriptions
- **Liste des inscriptions** : `/school/enrollments/`
  - Filtrage par session et statut
  
- **Créer une inscription** : `/school/enrollments/create/`
  - Inscription d'un étudiant dans une session
  - Peut être pré-rempli avec l'ID de l'étudiant

#### Devoirs
- **Liste des devoirs** : `/school/assignments/`
  - Filtrage par module
  
- **Détail du devoir** : `/school/assignments/<id>/`
  - Affiche les soumissions des étudiants

#### Examens
- **Liste des examens** : `/school/exams/`
  - Filtrage par module
  
- **Détail de l'examen** : `/school/exams/<id>/`
  - Affiche les résultats
  - Calcul automatique de la moyenne

## Utilisation

### 1. Créer un étudiant

1. Accéder à l'admin Django ou à `/school/students/create/`
2. Sélectionner un membre (seuls les membres non étudiants sont disponibles)
3. Attribuer un numéro d'étudiant unique
4. Définir la date d'inscription et le statut initial (candidat par défaut)
5. Enregistrer

### 2. Inscrire un étudiant dans une session

1. Accéder à `/school/enrollments/create/` ou via l'admin
2. Sélectionner l'étudiant
3. Sélectionner la session (qui appartient à une promotion)
4. Définir le statut initial (inscrit par défaut)
5. Enregistrer

**Note** : Un étudiant ne peut être inscrit qu'une seule fois dans une session (contrainte `unique_together`).

### 3. Créer des devoirs

1. Accéder à l'admin Django -> Devoirs
2. Sélectionner le module concerné
3. Définir le titre, les consignes et la date limite
4. Attribuer une note maximale
5. Optionnel : joindre un fichier
6. Enregistrer

### 4. Saisir les notes

Via l'admin Django :
- **Soumissions de devoirs** : Accéder à la soumission, entrer le score et le feedback
- **Résultats d'examens** : Créer un résultat pour chaque étudiant avec le score obtenu

### 5. Consulter les relevés

1. Accéder à la fiche de l'étudiant (`/school/students/<id>/`)
2. Voir toutes les inscriptions, soumissions et résultats d'examens
3. Les notes finales sont calculables par session

## Règles métier

1. **Un membre = un étudiant** : Relation OneToOne entre Member et Student
2. **Unicité des inscriptions** : Un étudiant ne peut être inscrit qu'une fois par session
3. **Soumissions uniques** : Un étudiant ne peut soumettre qu'une fois par devoir
4. **Résultats uniques** : Un étudiant ne peut avoir qu'un résultat par examen
5. **Retard automatique** : La propriété `is_late` vérifie automatiquement si la soumission est tardive

## Prochaines étapes (à implémenter)

1. **Templates HTML** : Créer les templates pour les vues
2. **Calcul automatique des moyennes** : Ajouter une méthode pour calculer la moyenne pondérée par les coefficients
3. **Relevés de notes PDF** : Génération automatique de bulletins imprimables
4. **Notifications** : Rappels automatiques pour les devoirs et examens à venir
5. **Validation des notes** : Système de validation des résultats par module
6. **Statistiques** : Tableaux de bord avec statistiques de réussite par session

## Tests

Pour tester le module :

```bash
# Vérifier que tout est en ordre
python manage.py check

# Lancer le serveur de développement
python manage.py runserver

# Accéder à l'admin
# URL : http://localhost:8000/admin/
```

## Support

Pour toute question ou problème, consulter le cahier des charges dans `ProjectChurch.md` ou contacter l'équipe de développement.
