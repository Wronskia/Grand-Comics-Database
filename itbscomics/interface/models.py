from __future__ import unicode_literals

from django.db import models


def return_if_no_none(value):
    if value is not None:
        return str(value)
    else:
        return ""


class Brandgroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING, blank=True, null=True)
    year_began = models.BigIntegerField(blank=True, null=True)
    year_ended = models.BigIntegerField(blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'brandgroup'


class Characters(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    #appearsin = models.ManyToManyField('Story', through='Appearsin')

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'characters'


class Country(models.Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.CharField(max_length=4, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'country'


class Indiciapublisher(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    year_began = models.BigIntegerField(blank=True, null=True)
    year_ended = models.BigIntegerField(blank=True, null=True)
    is_surrogate = models.NullBooleanField()
    notes = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'indiciapublisher'


class Issue(models.Model):
    id = models.BigIntegerField(primary_key=True)
    issue_number = models.CharField(max_length=100, blank=True, null=True)
    publication_date = models.BigIntegerField(blank=True, null=True)
    series = models.ForeignKey('Series', models.DO_NOTHING, blank=True, null=True)
    indicia_publisher = models.ForeignKey(Indiciapublisher, models.DO_NOTHING, blank=True, null=True)
    price = models.CharField(max_length=1000, blank=True, null=True)
    page_count = models.BigIntegerField(blank=True, null=True)
    indicia_frequency = models.CharField(max_length=1000, blank=True, null=True)
    editing = models.CharField(max_length=2000, blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    isbn = models.CharField(max_length=100, blank=True, null=True)
    valid_isbn = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    on_sale_date = models.BigIntegerField(blank=True, null=True)
    rating = models.CharField(max_length=100, blank=True, null=True)
    reprint_of = models.ForeignKey('self', models.DO_NOTHING, db_column='reprint_of', blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.title)

    class Meta:
        managed = False
        db_table = 'issue'


class Language(models.Model):
    id = models.BigIntegerField(primary_key=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'language'


class Personandstudio(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'personandstudio'


class Publisher(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    year_began = models.BigIntegerField(blank=True, null=True)
    year_ended = models.BigIntegerField(blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'publisher'


class Series(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    format = models.CharField(max_length=500, blank=True, null=True)
    year_began = models.BigIntegerField(blank=True, null=True)
    year_ended = models.BigIntegerField(blank=True, null=True)
    first_issue = models.ForeignKey(Issue, models.DO_NOTHING, blank=True, null=True, related_name='first_issue')
    last_issue = models.ForeignKey(Issue, models.DO_NOTHING, blank=True, null=True, related_name='last_issue')
    publisher = models.ForeignKey(Publisher, models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    language = models.ForeignKey(Language, models.DO_NOTHING, blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    dimensions = models.CharField(max_length=1000, blank=True, null=True)
    paper_stock = models.CharField(max_length=500, blank=True, null=True)
    binding = models.CharField(max_length=1000, blank=True, null=True)
    publishing_format = models.CharField(max_length=100, blank=True, null=True)
    publication_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.name)

    class Meta:
        managed = False
        db_table = 'series'


class Story(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    synopsis = models.CharField(max_length=2000, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=2000, blank=True, null=True)
    reprint_notes = models.CharField(max_length=2000, blank=True, null=True)
    reprint = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    issue = models.ForeignKey(Issue, models.DO_NOTHING, blank=True, null=True)
    characters = models.ManyToManyField(Characters, through='Appearsin')

    def __str__(self):
        return str(self.id) + '-' + return_if_no_none(self.title)

    class Meta:
        managed = False
        db_table = 'story'


class Genre(models.Model):
    story = models.ForeignKey(Story, models.DO_NOTHING, primary_key=True, related_name='genre')
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return return_if_no_none(self.genre)

    class Meta:
        managed = False
        db_table = 'genre'


### Character Story relations
class Appearsin(models.Model):
    character = models.ForeignKey('Characters', models.DO_NOTHING, primary_key=True, related_name='appearsin')
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'appearsin'
        unique_together = (('character', 'story'),)


class Features(models.Model):
    character = models.ForeignKey(Characters, models.DO_NOTHING, primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'features'
        unique_together = (('character', 'story'),)


### PersoneAndStudio Story relations
class Colors(models.Model):
    person_and_studio = models.ForeignKey('Personandstudio', models.DO_NOTHING, db_column='person_and_studio',
                                          primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'colors'
        unique_together = (('person_and_studio', 'story'),)


class Inks(models.Model):
    person_and_studio = models.ForeignKey('Personandstudio', models.DO_NOTHING, primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'inks'
        unique_together = (('person_and_studio', 'story'),)


class Letters(models.Model):
    person_and_studio = models.ForeignKey('Personandstudio', models.DO_NOTHING, primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'letters'
        unique_together = (('person_and_studio', 'story'),)


class Pencils(models.Model):
    person_and_studio = models.ForeignKey('Personandstudio', models.DO_NOTHING, primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pencils'
        unique_together = (('person_and_studio', 'story'),)


class Scripts(models.Model):
    person_and_studio = models.ForeignKey(Personandstudio, models.DO_NOTHING, primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'scripts'
        unique_together = (('person_and_studio', 'story'),)


class EditingStory(models.Model):
    person_and_studio = models.ForeignKey('Personandstudio', models.DO_NOTHING, db_column='person_and_studio',
                                          primary_key=True)
    story = models.ForeignKey('Story', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'editing_story'
        unique_together = (('person_and_studio', 'story'),)
