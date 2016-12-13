from django.dispatch import Signal

# signal for our membership
membership_dates = Signal(providing_args=["new_date_start"])
