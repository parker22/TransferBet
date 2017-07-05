from rest_framework import serializers

from betapp.models import BetOdds


class BetOddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetOdds
        fields = ('t_created', 'odds')


class ClubRumorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetOdds
        fields = ('t_created', 'club_rumors')
