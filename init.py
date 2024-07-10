import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


django.setup()



from django.contrib.auth.models import User

from main.models import LillyUser, Transaction


user = LillyUser.objects.get(username = "admin")

user.is_superuser  = True

user.save()