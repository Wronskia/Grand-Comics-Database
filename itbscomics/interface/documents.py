from django_elasticsearch_dsl import DocType, Index
from interface.models import Characters, Story, Issue, Brandgroup, Indiciapublisher, Publisher, Series

comics_index = Index('comics')

comics_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@comics_index.doc_type
class CharactersDocument(DocType):
    class Meta:
        model = Characters
        fields = [
            'name',
        ]


@comics_index.doc_type
class StoryDocument(DocType):
    class Meta:
        model = Story
        fields = [
            'title',
        ]

@comics_index.doc_type
class IssueDocument(DocType):
    class Meta:
        model = Issue
        fields = [
            'title'
        ]

@comics_index.doc_type
class BrandgroupDocument(DocType):
    class Meta:
        model = Brandgroup
        fields = [
            'name'
        ]

@comics_index.doc_type
class IndiciapublisherDocument(DocType):
    class Meta:
        model = Indiciapublisher
        fields = [
            'name'
        ]

@comics_index.doc_type
class PublisherDocument(DocType):
    class Meta:
        model = Publisher
        fields = [
            'name'
        ]

@comics_index.doc_type
class SeriesDocument(DocType):
    class Meta:
        model = Series
        fields = [
            'name'
        ]