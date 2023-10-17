from rest_framework import serializers
from .models import Anbieter
from .models import Einzelteil
from .models import Einzelteilmarktpreis
from .models import EinzelteilLegoset
from .models import Legoset
from .models import Setmarktpreis


class EinzelteilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Einzelteil
        fields = 'id'


class AnbieterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anbieter
        fields = ('url',
                  'name')


class LegosetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legoset
        fields = ('set_id',
                  'name')


class EinzelteilmarktpreisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Einzelteilmarktpreis
        fields = ('einzelteil',
                  'anbieter_url',
                  'preis',
                  'url')


class SetmarktpreisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setmarktpreis
        fields = ('set',
                  'anbieter_url',
                  'preis',
                  'url')


class EinzelteilLegosetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EinzelteilLegoset
        fields = ('einzelteil',
                  'legoset',
                  'anzahl')


