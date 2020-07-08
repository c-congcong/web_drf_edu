from rest_framework import serializers

from home.models import Banner


class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("img", 'link')


class FooterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("title", "link")


class HeaderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("title", "link")
