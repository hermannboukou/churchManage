from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from members.models import Member
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Sends email reminders for upcoming member birthdays to administrators.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days in advance to check for birthdays (default: 7 days).',
        )

    def handle(self, *args, **options):
        days = options['days']
        upcoming_birthdays = Member.objects.birthdays_in_next_days(days=days)

        if not upcoming_birthdays:
            self.stdout.write(self.style.SUCCESS(f'No upcoming birthdays found in the next {days} days.'))
            return

        # Build email content
        subject = f"Rappel Anniversaires Membres - Prochains {days} jours"
        message_lines = [f"Bonjour Administrateur(trice),",
                         f"Voici la liste des membres dont l'anniversaire est dans les {days} prochains jours :",
                         ""]

        for member in upcoming_birthdays:
            # Calculate the exact birthday for the current/next year
            today = date.today()
            member_birthday_this_year = member.date_of_birth.replace(year=today.year)
            if member_birthday_this_year < today:
                member_birthday_this_year = member_birthday_this_year.replace(year=today.year + 1)
            
            days_left = (member_birthday_this_year - today).days
            
            message_lines.append(f"- {member.first_name} {member.last_name} ({member.date_of_birth.strftime('%d/%m')}) - dans {days_left} jours.")
        
        message_lines.append("\nCordialement,\nVotre application de gestion d'église.")
        message = "\n".join(message_lines)

        # Get administrators' email addresses
        # We'll send to all staff users for simplicity
        admin_emails = list(User.objects.filter(is_staff=True, email__isnull=False).values_list('email', flat=True))

        if not admin_emails:
            self.stdout.write(self.style.WARNING('No staff users with email addresses found to send reminders.'))
            return

        # Send email
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                admin_emails,
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent birthday reminders to {len(admin_emails)} administrators.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending birthday reminders: {e}'))
