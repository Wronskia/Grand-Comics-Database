import interface.models as models
import pandas
from datetime import date

CSV_ROOT = '/home/marc/Documents/uni/introduction_to_databases/project/milestone_2/cleaned_data/'


class Logger():
    def __init__(self, file):
        self.file = open(file, 'w')

    def log(self, *args):
        out = " ".join([str(a) for a in args])
        self.file.write(out + '\n')
        print(out)

    def close(self):
        self.file.close()


def loader(loader_class, ignore_first_rows=0):
    dataframe = pandas.read_csv(CSV_ROOT + loader_class.file_name + '.csv')
    logger = Logger(CSV_ROOT + loader_class.file_name + '.log')
    for index, data in dataframe.iterrows():
        if index < ignore_first_rows: continue
        if index % 100 == 0: print(index)
        dictionary = loader_class.iter(index, data, logger)
        try:
            loader_class.model_class(**dictionary).save()
        except Exception as e:
            logger.log(*[str(key) + ': ' + str(dictionary[key]) for key in dictionary])
            logger.log(e)
    logger.close()


### Loader Classes
class CharacterLoader:
    file_name = 'characters'
    model_class = models.Characters

    def iter(self, index, data, logger):
        return {'id': int(data['id']), 'name': data['name']}


class PersonAndStudioLoader:
    file_name = 'personsandstudios'
    model_class = models.Personandstudio

    def iter(self, index, data, logger):
        return {'id': int(data['id']), 'name': data['name']}


class CountryLoader:
    file_name = 'country'
    model_class = models.Country

    def iter(self, index, data, logger):
        return {'id': int(data['id']), 'code': data['code'], 'name': data['name']}


class LanguageLoader:
    file_name = 'language'
    model_class = models.Language

    def iter(self, index, data, logger):
        return {'id': int(data['id']), 'code': data['code'], 'name': data['name']}


class PublisherLoader:
    file_name = 'publisher'
    model_class = models.Publisher

    def iter(self, index, data, logger):
        return {
            'id': int(data['id']),
            'name': data['name'],
            'country': models.Country.objects.get(id=int(data['country_id'])),
            'year_began': toInt(data['year_began']),
            'year_ended': toInt(data['year_ended']),
            'notes': data['notes'],
            'url': data['url']
        }


class IndicaPublisherLoader:
    file_name = 'indicia_publisher'
    model_class = models.Indiciapublisher

    def __init__(self):
        self.get_publisher = TryGetObject(models.Publisher)
        self.get_country = TryGetObject(models.Country)

    def iter(self, index, data, logger):
        return {
            'id': int(data['id']),
            'name': data['name'],
            'country': self.get_country.try_get(int(data['country_id']), logger),
            'publisher': self.get_publisher.try_get(int(data['publisher_id']), logger),
            'year_began': toInt(data['year_began']),
            'year_ended': toInt(data['year_ended']),
            'is_surrogate': toBool(data['is_surrogate']),
            'notes': data['notes'],
            'url': data['url']
        }


class BrandGroupLoader:
    file_name = 'band_group'
    model_class = models.Brandgroup

    def __init__(self):
        self.get_publisher = TryGetObject(models.Publisher)

    def iter(self, index, data, logger):
        return {
            'id': int(data['id']),
            'name': data['name'],
            'publisher': self.get_publisher.try_get(data['publisher_id'], logger),
            'year_began': toInt(data['year_began']),
            'year_ended': toInt(data['year_ended']),
            'notes': data['notes'],
            'url': data['url']
        }


# reload issue with get reprint
class IssueLoader:
    file_name = 'issue'
    model_class = models.Issue

    def __init__(self, get_series_and_reprint_of):
        self.get_series_and_reprint_of = get_series_and_reprint_of
        self.try_series = TryGetObject(models.Series)
        self.try_reprint_of = TryGetObject(models.Issue)
        self.try_indica_publisher = TryGetObject(models.Indiciapublisher)

    def iter(self, index, data, logger):
        if self.get_series_and_reprint_of:
            series = self.try_series.try_get(data['series_id'], logger)
            reprint = self.try_reprint_of.try_get(data['reprint_of'], logger)
        else:
            series = None
            reprint = None

        return {
            'id': int(data['id']),
            'issue_number': toInt(data['number']),
            'publication_date': toDateYear(data['publication_date']),
            'series': series,
            'indicia_publisher': self.try_indica_publisher.try_get(data['indicia_publisher_id'], logger),
            'price': data['price'],
            'page_count': toInt(data['page_count']),
            'indicia_frequency': data['indicia_frequency'],
            'editing': toString(data['editing']),
            'notes': toString(data['notes']),
            'isbn': toInt(data['isbn']),
            'valid_isbn': toInt(data['valid_isbn']),
            'barcode': toInt(data['barcode']),
            'title': toString(data['title']),
            'on_sale_date': toDateYear(data['on_sale_date']),
            'rating': toString(data['rating']),
            'reprint_of': reprint
        }


class SeriesLoader:
    file_name = 'series'
    model_class = models.Series

    def __init__(self):
        self.try_last_issue = TryGetObject(models.Issue)
        self.try_first_issue = TryGetObject(models.Issue)
        self.try_country = TryGetObject(models.Country)
        self.try_publisher = TryGetObject(models.Publisher)
        self.try_language = TryGetObject(models.Language)

    def iter(self, index, data, logger):
        return {
            'id': int(data['id']),
            'name': toString(data['name']),
            'format': toString(data['format']),
            'year_began': toDateYear(data['year_began']),
            'year_ended': toDateYear(data['year_ended']),
            'first_issue': self.try_first_issue.try_get(data['first_issue_id'], logger),
            'last_issue': self.try_last_issue.try_get(data['last_issue_id'], logger),
            'publisher': self.try_publisher.try_get(data['publisher_id'], logger),
            'country': self.try_country.try_get(data['country_id'], logger),
            'language': self.try_language.try_get(data['language_id'], logger),
            'notes': toString(data['notes']),
            'dimensions': toString(data['dimensions']),
            'paper_stock': toInt(data['paper_stock']),
            'binding': toString(data['binding']),
            'publishing_format': toString(data['publishing_format']),
            'publication_type': toString(data['publication_type'])
        }


class StoryLoader:
    file_name = 'story'
    model_class = models.Story

    def __init__(self, get_reprint):
        self.get_reprint = False
        self.try_reprint = TryGetObject(models.Story)
        self.try_issue = TryGetObject(models.Issue)

    def iter(self, index, data, logger):
        if self.get_reprint:
            reprint = self.try_reprint.try_get(data['reprint_id'], logger)
        else:
            reprint = None

        return {
            'id': int(data['id']),
            'title': toString(data['title']),
            'genre': toString(data['genre']),
            'synopsis': toString(data['synopsis']),
            'type': toString(data['type']),
            'notes': toString(data['notes']),
            'reprint_notes': toString(data['reprint_notes']),
            'reprint': reprint,
            'issue': self.try_issue.try_get(data['issue_id'], logger)
        }


class ScriptsLoader:
    file_name = 'scripts_stories'
    model_class = models.Scripts

    def __init__(self):
        self.try_get_person_and_studio = TryGetObject(models.Personandstudio)
        self.try_get_story = TryGetObject(models.Story)

    def iter(self, index, data, logger):
        person = self.try_get_person_and_studio.try_get(data['person_or_studio_id'], logger)
        story = self.try_get_story.try_get(data['story_id'], logger)

        if person is None or story is None:
            raise Exception('No link exists')
        else:
            return {
                'person_and_studio': person,
                'story': story
            }


class FeaturesLoader:
    file_name = 'features_stories'
    model_class = models.Features

    def __init__(self):
        self.try_get_story = TryGetObject(models.Story)
        self.try_get_character = TryGetObject(models.Characters)

    def iter(self, index, data, logger):
        story = self.try_get_story.try_get(data['story_id'], logger)
        character = self.try_get_character.try_get(data['character_id'], logger)

        if story is None or character is None:
            raise Exception('No linkk exists')
        else:
            return {
                'story': story,
                'character': character
            }


class AppearsinLoader:
    file_name = 'characters_stories'
    model_class = models.Appearsin

    def __init__(self):
        self.try_get_story = TryGetObject(models.Story)
        self.try_get_character = TryGetObject(models.Characters)

    def iter(self, index, data, logger):
        story = self.try_get_story.try_get(data['story_id'], logger)
        character = self.try_get_character.try_get(data['character_id'], logger)

        if story is None or character is None:
            raise Exception('No linkk exists')
        else:
            return {
                'story': story,
                'character': character
            }


### Utils
def toInt(value):
    try:
        value = float(value)
    except ValueError:
        return None

    if value.is_integer():
        return int(value)
    else:
        return None


def toBool(value):
    return bool(value)


def toDateYear(value):
    value = toInt(value)
    if value != None:
        pub_date = date(value, 1, 1)
    else:
        pub_date = None
    return pub_date


def toString(value):
    val = str(value)
    if val != 'nan':
        return val
    else:
        return None


class TryGetObject:
    max_buffer_size = 5000

    def __init__(self, class_model, buffer=None):
        self.class_model = class_model
        if buffer == None:
            self.buffer = dict()
        else:
            self.buffer = buffer

    def try_get(self, id, logger):
        id = toInt(id)
        if id == None:
            return None
        if id in self.buffer:
            return self.buffer[id]
        else:
            if len(self.buffer) > self.max_buffer_size:
                self.buffer.popitem()
            try:
                obj = self.class_model.objects.get(id=id)
            except Exception as e:
                logger.log('id:', id, 'exception:', e)
                return None
            self.buffer[id] = obj
            return obj


def load_all():
    loader(IssueLoader(False), 1008200)
    loader(SeriesLoader())
    loader(StoryLoader(False))
    for class_loader in [ScriptsLoader(), FeaturesLoader(), AppearsinLoader()]:
        print(class_loader.file_name)
        loader(class_loader)
    loader(IssueLoader(True))
    loader(StoryLoader(True))
