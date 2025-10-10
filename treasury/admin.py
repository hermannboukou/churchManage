from django.contrib import admin
from .models import CollectionType, PaymentMethod, Collection
# from simple_history.admin import HistoricalModelAdmin # New import

@admin.register(CollectionType)
class CollectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'church', 'collection_type', 'amount', 'payment_method', 'donor_member', 'donor_guest_name', 'department', 'receipt_number', 'recorded_by')
    list_filter = ('collection_type', 'payment_method', 'church', 'department', 'date')
    search_fields = ('receipt_number', 'donor_guest_name', 'donor_member__first_name', 'donor_member__last_name', 'notes')
    date_hierarchy = 'date'
   # readonly_fields = ('created_at', 'updated_at')

# @admin.register(Collection.history.model) # Register the historical model
# class HistoricalCollectionAdmin(HistoricalModelAdmin):
#     list_display = ('history_date', 'history_type', 'history_user', 'collection_type', 'amount', 'date')
#     list_filter = ('history_type', 'history_date', 'history_user', 'collection_type')
#     search_fields = ('collection_type__name', 'amount')