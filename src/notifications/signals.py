from django.dispatch import Signal

# creating signal to notify user
notify = Signal(providing_args=["recipient", "verb", "action", "target", "affected_users"])
