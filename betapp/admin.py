from django.contrib import admin

# Register your models here.
from betapp.models import Player, Club, BetOdds

admin.site.register([Player, Club,BetOdds])
