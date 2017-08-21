from rest_framework.serializers import ModelSerializer, SerializerMethodField, DateField
from interface.models import Characters, Story, Issue, Brandgroup, Indiciapublisher, Publisher, Series


class CharacterSerializer(ModelSerializer):
    class Meta:
        model = Characters
        fields = ['id', 'name']


class StorySerializer(ModelSerializer):
    reprint = SerializerMethodField()
    issue = SerializerMethodField()
    genre = SerializerMethodField()

    def get_reprint(self, story):
        if story.reprint is not None:
            return story.reprint.title
        return ""

    def get_issue(self, story):
        if story.issue is not None:
            return story.issue.title
        return ""

    def get_genre(self, story):
        out = []
        if story.genre is not None:
            for genre in story.genre.all():
                out.append(genre.genre)
        return ', '.join(out)

    class Meta:
        model = Story
        fields = '__all__'


class IssueSerializer(ModelSerializer):
    series = SerializerMethodField()
    indicia_publisher = SerializerMethodField()
    reprint_of = SerializerMethodField()

    def get_series(self, issue):
        if issue.series is not None:
            return issue.series.name
        return ""

    def get_indicia_publisher(self, issue):
        if issue.indicia_publisher is not None:
            return issue.indicia_publisher.name
        return ""

    def get_reprint_of(self, issue):
        if issue.reprint_of is not None:
            return issue.reprint_of.title
        return ""

    class Meta:
        model = Issue
        fields = '__all__'


class BrandgroupSerializer(ModelSerializer):
    publisher = SerializerMethodField()

    def get_publisher(self, brand_group):
        if brand_group.publisher is not None:
            return brand_group.publisher.name
        return ''

    class Meta:
        model = Brandgroup
        fields = '__all__'


class IndiciapublisherSerializer(ModelSerializer):
    publisher = SerializerMethodField()
    country = SerializerMethodField()

    def get_publisher(self, indicia_publisher):
        if indicia_publisher.publisher is not None:
            return indicia_publisher.publisher.name
        return ""

    def get_country(self, indicia_publisher):
        if indicia_publisher.country is not None:
            return indicia_publisher.country.name
        return ""

    class Meta:
        model = Indiciapublisher
        fields = '__all__'


class PublisherSerializer(ModelSerializer):
    country = SerializerMethodField()

    def get_country(self, publisher):
        if publisher.country is not None:
            return publisher.country.name
        return ''

    class Meta:
        model = Publisher
        fields = '__all__'


class SeriesSerializer(ModelSerializer):
    country = SerializerMethodField()
    language = SerializerMethodField()
    first_issue = SerializerMethodField()
    last_issue = SerializerMethodField()
    publisher = SerializerMethodField()

    def get_country(self, serie):
        if serie.country is not None:
            return serie.country.name
        return ''

    def get_language(self, serie):
        if serie.language is not None:
            return serie.language.name
        return ''

    def get_publisher(self, serie):
        if serie.publisher is not None:
            return serie.publisher.name
        return ''

    def get_first_issue(self, serie):
        if serie.first_issue is not None:
            return serie.first_issue.title
        return ''

    def get_last_issue(self, serie):
        if serie.last_issue is not None:
            return serie.last_issue.title
        return ''

    class Meta:
        model = Series
        fields = '__all__'
