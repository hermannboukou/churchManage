
import locale
import json
from collections import defaultdict
from django.utils import translation
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from church.models import Church
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import datetime
from django.utils.translation import gettext as _
from .forms import MeetingForm, EventForm, AudienceForm, AttendanceForm
from meetings.models import Meeting, Audiences, Event, Attendance

class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'meetings/meeting_list.html'
    context_object_name = 'meetings'

class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/meeting_form.html'
    success_url = reverse_lazy('meetings:meeting_list')

class MeetingUpdateView(LoginRequiredMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/meeting_form.html'
    success_url = reverse_lazy('meetings:meeting_list')

class MeetingDeleteView(LoginRequiredMixin, DeleteView):
    model = Meeting
    template_name = 'meetings/meeting_confirm_delete.html'
    success_url = reverse_lazy('meetings:meeting_list')


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'meetings/event_list.html'
    context_object_name = 'events'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'meetings/event_form.html'
    success_url = reverse_lazy('meetings:event_list')

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'meetings/event_form.html'
    success_url = reverse_lazy('meetings:event_list')

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'meetings/event_confirm_delete.html'
    success_url = reverse_lazy('meetings:event_list')


class AudienceCreateView(LoginRequiredMixin, CreateView):
    model = Audiences
    form_class = AudienceForm
    template_name = 'meetings/audience_form.html'
    success_url = reverse_lazy('meetings:audiences_list')

class AudienceUpdateView(LoginRequiredMixin, UpdateView):
    model = Audiences
    form_class = AudienceForm
    template_name = 'meetings/audience_form.html'
    success_url = reverse_lazy('meetings:audiences_list')

class AudienceDeleteView(LoginRequiredMixin, DeleteView):
    model = Audiences
    template_name = 'meetings/audience_confirm_delete.html'
    success_url = reverse_lazy('meetings:audiences_list')


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'meetings/attendance_list.html'
    context_object_name = 'attendances'

class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'meetings/attendance_form.html'
    success_url = reverse_lazy('meetings:attendance_list')

class AttendanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'meetings/attendance_form.html'
    success_url = reverse_lazy('meetings:attendance_list')

class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'meetings/attendance_confirm_delete.html'
    success_url = reverse_lazy('meetings:attendance_list')


@login_required
def audiences_list(request):
    translation.activate('fr')
    # Optionnel mais utile si le serveur l'autorise
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    except locale.Error:
        pass  # fallback to Django translation

    meeting_filter = request.GET.get('meeting')
    church_filter = request.GET.get('church')

    meetings = Meeting.objects.all()
    churches = Church.objects.all()

    audiences = Audiences.objects.all().order_by('-day')

    if meeting_filter and meeting_filter != '':
        audiences = audiences.filter(meeting_id=meeting_filter)
    if church_filter and church_filter != '':
        audiences = audiences.filter(church_id=church_filter)

    # Grouping audiences by day
    grouped = defaultdict(list)
    for audience in audiences:
        grouped[audience.day].append(audience)

    # Sort dates in descending order
    sorted_dates = sorted(grouped.keys(), reverse=True)

    # Pagination on dates
    paginator = Paginator(sorted_dates, 15)  # 5 dates per page
    page = request.GET.get('page')

    try:
        paginated_dates = paginator.page(page)
    except PageNotAnInteger:
        paginated_dates = paginator.page(1)
    except EmptyPage:
        paginated_dates = paginator.page(paginator.num_pages)

    # Create final grouped data for display
    grouped_audiences = []
    for date in paginated_dates:
        audiences_for_day = grouped[date]
        total_for_day = sum(audience.total for audience in audiences_for_day)
        formatted_date = date.strftime("%A %d %B %Y")
        grouped_audiences.append({
            'date': formatted_date,
            'audiences': audiences_for_day,
            'total_for_day': total_for_day
        })

    total_audience = sum(audience.men_count + audience.women_count + audience.youth_count + audience.children_count for audience in audiences)

    return render(request, 'meetings/audiences_list.html', {
        'total': total_audience,
        'grouped_audiences': grouped_audiences,
        'meetings': meetings,
        'churches': churches,
        'meeting_filter': meeting_filter,
        'church_filter': church_filter,
        'page_obj': paginated_dates  # pour la pagination dans le template
    })


@login_required
def audiences_summary(request):
    # Récupérer tous les enregistrements de la table Audiences
    all_audiences = Audiences.objects.all()

    # Initialiser les compteurs
    total_men = 0
    total_women = 0
    total_youth = 0
    total_children = 0
    total_visitors = 0

    # Boucler sur tous les enregistrements pour agréger les données
    for audience in all_audiences:
        total_men += audience.men_count
        total_women += audience.women_count
        total_youth += audience.youth_count
        total_children += audience.children_count
        total_visitors += audience.visitors_count

    # Calculer le total général
    total_audience = total_men + total_women + total_youth + total_children

    # Préparer le contexte pour le template
    context = {
        'total_men': total_men,
        'total_women': total_women,
        'total_youth': total_youth,
        'total_children': total_children,
        'total_audience': total_audience,
        'total_visitors': total_visitors,
    }

    # Rendre le template avec les données
    return render(request, 'meetings/audiences_summary.html', context)


def audience_report(request):
    # Récupérer tous les filtres possibles
    churches = Church.objects.all()
    meetings = Meeting.objects.all()

    translation.activate('fr')
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    except locale.Error:
        pass

    # Récupérer les paramètres de filtre
    church_id = request.GET.get('church')
    meeting_id = request.GET.get('meeting')
    month = request.GET.get('month', timezone.now().month)
    year = request.GET.get('year', timezone.now().year)

    # Appliquer les filtres
    filters = Q()
    if church_id and church_id != '':
        filters &= Q(church_id=church_id)
    if meeting_id and meeting_id != '':
        filters &= Q(meeting_id=meeting_id)
    if month:
        filters &= Q(day__month=month)
    if year:
        filters &= Q(day__year=year)

    # Récupérer les données groupées par jour
    daily_data = Audiences.objects.filter(filters).values('day').annotate(
        total_men=Sum('men_count'),
        total_women=Sum('women_count'),
        total_youth=Sum('youth_count'),
        total_children=Sum('children_count'),
        total_visitors=Sum('visitors_count'),
    ).order_by('-day')

    # Initialiser les totaux globaux
    total_men = 0
    total_women = 0
    total_youth = 0
    total_children = 0
    total_visitors = 0
    total_audience = 0
    day_count = 0  # Compteur de jours

    # Calculer le total par jour et les totaux globaux
    for day in daily_data:
        day['total'] = (
                (day['total_men'] or 0) +
                (day['total_women'] or 0) +
                (day['total_youth'] or 0) +
                (day['total_children'] or 0)
        )
        day['formatted_date'] = datetime.strftime(day['day'], '%A %d %B %Y')

        total_men += day['total_men'] or 0
        total_women += day['total_women'] or 0
        total_youth += day['total_youth'] or 0
        total_children += day['total_children'] or 0
        total_visitors += day['total_visitors'] or 0
        total_audience += day['total'] or 0
        day_count += 1

    # Calcul des moyennes
    avg_men = total_men / day_count if day_count else 0
    avg_women = total_women / day_count if day_count else 0
    avg_youth = total_youth / day_count if day_count else 0
    avg_children = total_children / day_count if day_count else 0
    avg_visitors = total_visitors / day_count if day_count else 0
    avg_total = total_audience / day_count if day_count else 0

    # Préparer les années disponibles pour le filtre
    years = Audiences.objects.dates('day', 'year').values_list('day__year', flat=True).distinct()

    context = {
        'daily_data': daily_data,
        'churches': churches,
        'meetings': meetings,
        'selected_church': int(church_id) if church_id and str(church_id).isdigit() else None,
        'selected_meeting': int(meeting_id) if meeting_id and str(meeting_id).isdigit() else None,
        'selected_month': int(month) if month and str(month).isdigit() else timezone.now().month,
        'selected_year': int(year) if year and str(year).isdigit() else timezone.now().year,
        'months': [
            (1, _('Janvier')), (2, _('Février')), (3, _('Mars')),
            (4, _('Avril')), (5, _('Mai')), (6, _('Juin')),
            (7, _('Juillet')), (8, _('Août')), (9, _('Septembre')),
            (10, _('Octobre')), (11, _('Novembre')), (12, _('Décembre'))
        ],
        'years': sorted(years, reverse=True) if years else [timezone.now().year],
        'total_men': total_men,
        'total_women': total_women,
        'total_youth': total_youth,
        'total_children': total_children,
        'total_visitors': total_visitors,
        'total_audience': total_audience,
        'avg_men': round(avg_men, 2),
        'avg_women': round(avg_women, 2),
        'avg_youth': round(avg_youth, 2),
        'avg_children': round(avg_children, 2),
        'avg_visitors': round(avg_visitors, 2),
        'avg_total': round(avg_total, 2),
    }

    # Chart data
    chart_data = {
        'labels': [_('Janvier'), _('Février'), _('Mars'), _('Avril'), _('Mai'), _('Juin'), _('Juillet'), _('Août'), _('Septembre'), _('Octobre'), _('Novembre'), _('Décembre')],
        'datasets': []
    }

    if meeting_id and meeting_id != '':
        meetings_for_chart = Meeting.objects.filter(id=meeting_id)
    else:
        meetings_for_chart = Meeting.objects.all()

    colors = ['rgba(54, 162, 235, 0.5)', 'rgba(255, 99, 132, 0.5)', 'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)']
    categories = ['men_count', 'women_count', 'youth_count', 'children_count']
    category_labels = [_('Hommes'), _('Femmes'), _('Jeunes'), _('Enfants')]

    for meeting in meetings_for_chart:
        for i, category in enumerate(categories):
            dataset = {
                'label': f'{meeting.name} - {category_labels[i]}',
                'data': [],
                'backgroundColor': colors[i]
            }
            for month_num in range(1, 13):
                q_filter = Q(day__year=year, day__month=month_num, meeting_id=meeting.id)
                if church_id and church_id != '':
                    q_filter &= Q(church_id=church_id)

                monthly_total = Audiences.objects.filter(q_filter).aggregate(total=Sum(category))['total'] or 0
                dataset['data'].append(monthly_total)
            chart_data['datasets'].append(dataset)

    context['chart_data'] = json.dumps(chart_data)

    return render(request, 'meetings/audience_report.html', context)

