Cahier des charges — Application de gestion d’une église

Technologie recommandée : Django
Langue : Français/Anglais
Style:  Tailwindcss
Mode : Light/Night
Git: Mettre le projet sur Github

⸻

1. Contexte & objectif

Construire une application web de gestion d’une église permettant d’automatiser et centraliser :
	•	la gestion des membres et de leurs relations (familles, statuts);
	•	l’organisation des départements, des responsables et des mandats (dates de prise/fin de fonction);
	•	la gestion comptable liée aux collectes (dîmes, offrandes, autres recettes) ;
	•	un module d’accueil/formation des nouveaux membres (école, promotions, sessions, modules, devoirs, examens, relevés de notes) ;
	•	la gestion des audiences / programmes (hommes, femmes, jeunes, enfants) et la planification des réunions ;
	•	les rappels (anniversaires, prise de fonction qui arrive à terme, devoirs/examens) ;
	•	la production de rapports et l’impression des documents (relevés, listes, reçus).

Cible : pasteurs, responsables, secrétariat, trésorerie, enseignants de l’école de formation.

⸻

2. Périmètre fonctionnel

2.1 Gestion des membres
	•	CRUD membres (nom, prénom, sexe, date de naissance, téléphone, email, adresse, photo, état civil, profession).
	•	Catégories / statuts : Pasteur, Ancien, Diacre, Responsable, Membre, Aspirant, Nothing.
	•	Historique des statuts et appartenance aux départements.
	•	Groupes familiaux et personnes à contacter.
	•	Import / export CSV/Excel des membres.

2.2 Départements & responsables
	•	CRUD départements (nom, description, église locale si multi-sites).
	•	Affectation de 0..n responsables à un département, idem pour leurs membres.
	•	Pour chaque responsabilité : date de prise de fonction, date de fin (optionnelle), statut (actif, en vacance), rôle (leader, adj-leader, secretaire, adj-secretaire, tresorier, adj-tresorier, membre).
    •	Règles : une personne peut cumuler plusieurs responsabilités et apprtenir à plusieurs départements.
	•	Tableau de bord des mandats arrivant à terme.

2.3 Hiérarchie / rôles église
	•	Gestion hiérarchique : Pasteurs > Anciens > Diacres > Responsables.
	•	Attribution des permissions (voir section Sécurité).
	•	Rôle « Responsable » peut être attribué à n’importe quel membre (y compris Past/Ancien/Diacre).

2.4 Comptabilité des collectes
	•	Comptes de recette : Dîmes, Offrandes, Projets, Autres.
	•	Enregistrement des entrées : montant, date, mode (espèces, mobile money, chèque, virement), donateur (membre / invité), département associé, reçu / reçu imprimable.
	•	Remontée par collecte (par réunion/programme) et par période.
	•	Rapports : total par type, par département, par membre, balance journalière/mensuelle/annuelle.
	•	Export PDF/Excel des rapports et reçus fiscaux (si nécessaire).
	•	Suivi des entrées en caisse et journal comptable (simplifié) – possibilité d’export vers un logiciel comptable.

2.5 École de formation (nouveaux membres)
	•	Gestion des promotions (ex : Promotion 2025), sessions unitaires (une session par promotion).
	•	Modules (cours) liés à une session : titre, description, enseignant, resources (pdf/video), coefficient.
	•	Inscription des étudiants (automatique via statut candidat -> élève).
	•	Devoirs programmables : titre, date de remise, barème, note maximale, consignes, fichier joint.
	•	Examens finaux par module : date, durée, barème.
	•	Saisie des notes par enseignant ; calcul automatique (moyennes pondérées, mentions si applicable).
	•	Relevé de notes individuel imprimable et exportable.
	•	Règles d’évaluation : seuil de réussite, récalage (échec) si moyenne insuffisante.

2.6 Gestion des audiences et programmes
	•	Création d’événements/réunions récurrents et exceptionnels : type (hommes, femmes, jeunes, enfants, culte général), date/heure, lieu, ordre du jour.
	•	Liste de types de réunions (Culte d'adoration, Réunion de prière, Etude biblique)
	•	Planification des intervenants et des responsables pour chaque programme.
	•	Statistiques d’audience (taux de fréquentation par groupe, évolution).

2.7 Notifications & rappels
	•	Rappels automatiques par email / SMS / notifications push (si configuré) : anniversaires, devoirs à rendre, examens à venir, mandats arrivant à terme, échéances de paiements (offrandes projetées si applicable).
	•	Paramétrage de templates d’email / SMS.

2.8 Rapports & impressions
	•	Relevés de notes par étudiant (PDF imprimable).
	•	Reçus de paiement (PDF) pour dîmes/offrandes.
	•	Rapports financiers (par période, par type de collecte).
	•	Liste des responsables et leurs mandats.
	•	Export en CSV/Excel pour analyses externes.

2.9 Audit & journalisation
	•	Journal des actions critiques : création/suppression de membre, enregistrement de paiement, modification de note, connexion admin.
	•	Logs pour la trésorerie avec preuve (qui a validé/encodé l’opération).

⸻

3. Acteurs et permissions (RBAC)
	•	Super Admin : gestion globale, paramètres, utilisateurs, accès à tous les modules.
	•	Secrétariat : gestion des membres, départements, événements, impressions.
	•	Trésorier : encodage et validation des collectes, rapports financiers.
	•	Enseignant : création devoirs, saisie des notes, consultation des étudiants de sa promotion.
	•	Responsable de département : gestion d’événements du département, consultation des membres du département.
	•	Membre : consultation de son profil, relevé de notes (si élève), reçus de paiement, inscription aux événements.

Permissions granulaires : CRUD sur entités, export, validation financière, accès aux rapports sensibles.

⸻

4. Modèle de données (extrait — tables principales)
	•	users (id, name, email, password, phone, role_id, photo, created_at…)
	•	members (id, user_id nullable, first_name, last_name, dob, gender, address, status, profession, family_id, created_at…)
	•	families (id, name, address, head_member_id)
	•	departments (id, name, description)
	•	department_responsibilities (id, member_id, department_id, title, start_date, end_date, status)
	•	roles (id, name, permissions json)
	•	events (id, title, type, start_datetime, end_datetime, department_id, description)
	•	attendances (id, event_id, member_id, present boolean, note)
	•	collections (id, date, amount, type, payer_member_id nullable, method, department_id, receipt_no, recorded_by)
	•	sessions (id, promotion_name, start_date, end_date)
	•	modules (id, session_id, title, coefficient, teacher_id)
	•	assignments (id, module_id, title, due_date, max_score)
	•	assignment_submissions (id, assignment_id, student_id, file_path, score, graded_by)
	•	exams (id, module_id, date, max_score)
	•	exam_results (id, exam_id, student_id, score)
	•	grades (id, student_id, session_id, total_score, status)
	•	audit_logs (id, user_id, action, entity, before json, after json, created_at)

Ce modèle est un extrait ; il faudra le détailler lors de la phase de conception (noms de champs, contraintes, index, FK).

⸻

5. Wireframes & écrans clés (liste)
	1.	Tableau de bord (vue globale) : synthèse membres, collectes récentes, prochaines réunions, mandats arrivant à terme, messages.
	2.	Liste des membres (recherche, filtres : statut, département, âge, ville).
	3.	Fiche membre détaillée (historique, photos, documents, paiements, responsabilités).
	4.	Gestion départements / mandats.
	5.	Module Trésorerie : saisie collecte, validation, rapports, reçus.
	6.	École : création promotion/session, modules, devoirs, saisie notes, bulletin.
	7.	Événements & présences.
	8.	Paramètres & gestion utilisateurs / rôles.
	9.	Rapports & exports.

⸻

6. Règles métier importantes
	•	Une personne peut avoir plusieurs statuts historiques mais un seul statut actif.
	•	Les collectes peuvent être liées (ou non) à un membre ; les dons anonymes sont autorisés.
	•	Un étudiant dont la moyenne est inférieure au seuil paramétrable est recalé (statut échec) ; l’enseignant peut encoder des rattrapages.
	•	Les responsables doivent avoir une date de prise et (optionnellement) de fin de fonction; notification X jours avant fin (paramétrable).

⸻

7. Non-fonctionnel
	•	Performance : application responsive, pages principales chargent rapidement (cache Redis pour tableaux intensifs).
	•	Sécurité : HTTPS, stockage des mots de passe par bcrypt/argon2, protections CSRF/XSS, protections des endpoints financiers.
	•	Scalabilité : architecture monolithique Laravel évolutive (queues, jobs pour envoi d’emails/SMS).
	•	Sauvegardes : backups automatisés de la base (daily), export manuel.
	•	Localisation : support FR (par défaut), possibilité d’ajouter d’autres langues.
	•	Accessibilité : conformité basique (contraste, navigation au clavier).

⸻

8. Intégrations & choices techniques
	•	DB : MySQL / MariaDB
	•	Cache & queues : Redis
	•	File storage : local / S3 (selon déploiement)
	•	Envoi d’emails : SMTP / Mailgun / SendGrid
	•	SMS : intégration provider (Africa: Orange Money / MTN SMS gateways selon disponibilité)
	•	Auth : Laravel Breeze / Fortify + Livewire components
	•	Tests : PHPUnit + Pest (optionnel)
	•	CI/CD : GitHub Actions / GitLab CI

⸻

9. API & points d’accès (exemples)
	•	GET /api/members — liste
	•	GET /api/members/{id} — détail
	•	POST /api/collections — enregistrer collecte
	•	GET /api/sessions/{id}/grades — relevé de notes
	•	POST /api/events/{id}/attendance — marquer présence

API protégée par token (sanctum) pour intégration mobile si nécessaire.

⸻

10. Tests & critères d’acceptation (exemples)
	•	Création d’un membre => visible dans la liste + possibilité d’import.
	•	Enregistrement d’une collecte => reçu généré + montant dans rapport mensuel.
	•	Création d’une promotion => étudiants inscrits, devoirs créés, notes saisies, relevé généré.
	•	Mandat de responsable => notification programmée X jours avant fin.

⸻

11. Déploiement & maintenance
	•	Environnements : dev, staging, production.
	•	Procédure de déploiement via CI/CD.
	•	Monitoring des erreurs (Sentry) et des performances.
	•	Plan de sauvegarde et restauration.

⸻

12. Livrables
	•	Cahier des charges technique et fonctionnel finalisé.
	•	Base de données (script de migration Laravel).
	•	Application web (code source), Dockerfile / docker-compose (optionnel).
	•	Documentation d’installation et d’exploitation.
	•	Guide utilisateur (chemin critique : secrétariat, trésorier, enseignants).
	•	Jeux de tests et rapports d’acceptation.

⸻

13. Phases - ordre d’exécution (sans estimation temporelle)
	1.	Analyse détaillée & validation du cahier des charges.
	2.	Modélisation de la BD et wireframes UI.
	3.	Développement back-end (API, modèle, migrations).
	4.	Développement UI (Livewire components) et intégration.
	5.	Module comptabilité et génération de reçus.
	6.	Module école (inscriptions, devoirs, notes, bulletins).
	7.	Tests unitaires & d’intégration, tests utilisateurs.
	8.	Déploiement et formation des utilisateurs.
	9.	Maintenance corrective et évolutive.

⸻

14. Options & améliorations futures (extension)
	•	Application mobile (API + front natif ou PWA).
	•	Intégration paiement en ligne (mobile money, cartes) pour collectes.
	•	OCR pour numérisation de documents d’inscription.
	•	Tableau de bord métier avancé (KPIs, graphiques interactifs).

⸻

15. Annexes / éléments utiles à fournir par le client
	•	Charte graphique (logo, couleurs) si disponible.
	•	Liste initiale des membres (CSV) pour import.
	•	Règles internes (seuils d’évaluation, politique de collecte).
	•	Accès aux prestataires email/SMS si préférence.

⸻

Fin du cahier des charges — version initiale.

(Ce document est un modèle complet. Il sera affiné après réunion de cadrage et retours sur les priorités.)