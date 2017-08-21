from django.contrib import admin
from interface.models import Characters, Story, Issue, Brandgroup, Indiciapublisher, Publisher, Series, Appearsin
from django_extensions.admin import ForeignKeyAutocompleteAdmin


class MultiDBModelAdmin(ForeignKeyAutocompleteAdmin):
    # A handy constant for the name of the alternate database.
    using = 'oracle'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


@admin.register(Characters)
class CharactersModelAdmin(MultiDBModelAdmin):
    search_fields = ['id', 'name']


@admin.register(Story)
class StoryModelAdmin(MultiDBModelAdmin):
    related_search_fields = {
        'reprint': ('id', 'title'),
        'issue': ('id', 'title'),
        'characters': ('id', 'name')
    }

    search_fields = ['id', 'title', 'type']


@admin.register(Issue)
class IssueModelAdmin(MultiDBModelAdmin):
    related_search_fields = {
        'series': ('id', 'title'),
        'indicia_publisher': ('id', 'name'),
        'reprint_of': ('id', 'title')
    }

    search_fields = ['id', 'title']


@admin.register(Brandgroup)
class BrandgroupModelAdmin(MultiDBModelAdmin):
    related_search_fields = {
        'publisher': ('id', 'name'),
    }

    search_fields = ['id', 'name']


@admin.register(Indiciapublisher)
class IndiciapublisherModelAdmin(MultiDBModelAdmin):
    related_search_fields = {
        'publisher': ('id', 'name')
    }

    search_fields = ['id', 'name']


@admin.register(Publisher)
class PublisherModelAdmin(MultiDBModelAdmin):
    search_fields = ['id', 'name', 'country']


@admin.register(Series)
class SeriesModelAdmin(MultiDBModelAdmin):
    related_search_fields = {
        'first_issue': ('id', 'title'),
        'last_issue': ('id', 'title'),
        'publisher': ('id', 'name'),
    }

    search_fields = ['id', 'name', 'country', 'language']
