from django.dispatch import Signal

# creating signal to track page_views
page_view = Signal(providing_args=["page_path","primary_object","secondary_object"])
