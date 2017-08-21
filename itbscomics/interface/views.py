from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import re

from interface.models import Characters, Story, Issue, Brandgroup, Indiciapublisher, Publisher, Series
from interface.documents import CharactersDocument, StoryDocument, IssueDocument, BrandgroupDocument, \
    IndiciapublisherDocument, PublisherDocument, SeriesDocument


def home(request):
    template = loader.get_template("home.html")
    return HttpResponse(template.render({}, request))


SPACE_RE = re.compile('\s+')


def globalsearch(request):
    template = loader.get_template("globalsearch.html")
    keywords = request.GET.get('query')

    page_size = 25

    return HttpResponse(template.render({
        'query_string': request.GET.get('query'),
        'character_list': Characters.objects.filter(
            id__in=get_id_list(CharactersDocument, 'name', keywords, page_size)).prefetch_related('appearsin').all(),
        'story_list': Story.objects.filter(id__in=get_id_list(StoryDocument, 'title', keywords, page_size))
            .prefetch_related('genre').prefetch_related('reprint').prefetch_related('issue')
            .prefetch_related('characters').all(),
        'issue_list': Issue.objects.filter(id__in=get_id_list(IssueDocument, 'title', keywords, page_size))
            .prefetch_related('series').prefetch_related('indicia_publisher').prefetch_related('reprint_of').all(),
        'brand_group_list': Brandgroup.objects.filter(
            id__in=get_id_list(BrandgroupDocument, 'name', keywords, page_size))
            .prefetch_related('publisher').all(),
        'indicia_publisher_list': Indiciapublisher.objects.filter(
            id__in=get_id_list(IndiciapublisherDocument, 'name', keywords, page_size))
            .prefetch_related('publisher').prefetch_related('country').all(),
        'publisher_list': Publisher.objects.filter(id__in=get_id_list(PublisherDocument, 'name', keywords, page_size))
            .prefetch_related('country').all(),
        'series_list': Series.objects.filter(id__in=get_id_list(SeriesDocument, 'name', keywords, page_size))
            .prefetch_related('country').prefetch_related('language').prefetch_related('first_issue')
            .prefetch_related('last_issue').prefetch_related('publisher').all(),
    }, request))


def get_id_list(elasticsearch_document, field, keywords, page_size):
    # result = model.objects.filter(generate_django_query(fields, keywords))[:page_size].all()
    # return result
    result_ids = [int(hit.meta.id) for hit in
                  elasticsearch_document.search().query("fuzzy", **{field: keywords})[:page_size].execute().hits]
    return result_ids
