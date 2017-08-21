from django import template
from django.template import loader
from django.utils.safestring import mark_safe

from interface.serializers import CharacterSerializer, StorySerializer, IssueSerializer, BrandgroupSerializer, \
    IndiciapublisherSerializer, PublisherSerializer, SeriesSerializer

register = template.Library()


@register.simple_tag
def character_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': CharacterSerializer(model_list, many=True).data,
        'field_list': ['id', 'name'],
        'table_name': 'Characters'
    })


@register.simple_tag
def story_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': StorySerializer(model_list, many=True).data,
        'field_list': ['id', 'title', 'genre', 'type', 'reprint', 'issue'],
        'foreign_field_list': [],
        'table_name': 'Story'
    })


@register.simple_tag
def issue_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': IssueSerializer(model_list, many=True).data,
        'field_list': ['id', 'isbn', 'title', 'series', 'valid_isbn', 'issue_number', 'publication_date', 'price',
                       'page_count', 'indicia_frequency', 'on_sale_date', 'rating', 'issue_number', 'reprint_of', 'indicia_publisher'],
        'foreign_field_list': [],
        'table_name': 'Issue'
    })


@register.simple_tag
def brand_group_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': BrandgroupSerializer(model_list, many=True).data,
        'field_list': ['id', 'name', 'publisher', 'year_began', 'year_ended', 'url'],
        'foreign_field_list': [],
        'table_name': 'Brand Group'
    })


@register.simple_tag
def indicia_publisher_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': IndiciapublisherSerializer(model_list, many=True).data,
        'field_list': ['id', 'name', 'publisher', 'country', 'year_began', 'year_ended', 'is_surrogate'],
        'foreign_field_list': [],
        'table_name': 'Indicia Publisher'
    })


@register.simple_tag
def publisher_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': PublisherSerializer(model_list, many=True).data,
        'field_list': ['id', 'name', 'country', 'year_began', 'year_ended'],
        'foreign_field_list': [],
        'table_name': 'Publisher'
    })


@register.simple_tag
def series_table(model_list):
    template = loader.get_template("table.html")
    return template.render({
        'model_list': SeriesSerializer(model_list, many=True).data,
        'field_list': ['id', 'name', 'format', 'year_began', 'year_ended', 'first_issue', 'last_issue', 'publisher',
                       'country', 'language', 'dimensions', 'paper_stock', 'publishing_format', 'publication_type'],
        'foreign_field_list': [],
        'table_name': 'Series'
    })


@register.simple_tag
def fill_table(model_list, field_list, foreign_field_list):
    """
    Simple utils function to fill the tables with data
    :param model_list: list[serialized_model]
    :param field_list: list[str]
    :param foreign_field_list: list[str]
    :return:
    """
    out = ''
    for model in model_list:
        out += '<tr>'
        for field in field_list:
            out += '<td>' + str(model[field]) + '</td>'
        # for field in foreign_field_list:
        #     attr = model[field]
        #     if attr is not None:
        #         out += '<td>' + '<a href=" + attr + "><div style="height:100%;width:100%">' + ', '.join([str(i.pk) for i in attr.all()]) + '</td>'
        out += '</tr>'
    return mark_safe(out)
