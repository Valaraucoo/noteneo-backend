from rest_framework import serializers

from pages import models
from users.api import serializers as users_serializers


class PageAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageAnalytics
        fields = '__all__'


class MainPageAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainPageAnalytics
        fields = '__all__'


class PageSerializer(serializers.ModelSerializer):
    user = users_serializers.UserRetrieveSerializer(read_only=True)
    view_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Page
        fields = ('id', 'slug', 'user', 'is_created', 'main_color',
                  'name', 'page_type', 'contact_email', 'view_count',
                  'header_title', 'header_description',
                  'services_enable', 'services_title', 'services_description',
                  'services_1_type', 'services_1_title', 'services_1_description',
                  'services_2_type', 'services_2_title', 'services_2_description',
                  'services_3_type', 'services_3_title', 'services_3_description',
                  'about_enable', 'about_title', 'about_subtitle', 'about_description',
                  'created_at', 'updated_at')
