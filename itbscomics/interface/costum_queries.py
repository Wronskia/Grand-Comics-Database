from django.db import connections
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from pygments import highlight
from pygments.lexers.sql import SqlLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
import time
import math

QUERY_LIST = [
    (
        """
SELECT B.name
FROM
    (
    SELECT B.name AS name, rank() OVER (ORDER BY COUNT(I.id) desc) AS rank
    FROM BrandGroup B, IndiciaPublisher I, Country C
    WHERE B.publisher_id = I.publisher_id AND I.country_id = C.id AND C.name = '{0}'
    GROUP BY B.id, B.name
    ) B
WHERE B.rank = 1
            """,
        ['name'], ['str'], 'Q-1.a',
        [('country_name', 'Belgium')],
        "Print the brand group names with the highest number of Belgian indicia publishers."
    ),
    (
        """
        SELECT DISTINCT P.id, P.name
        FROM Publisher P, Series S, Country C
        WHERE P.id = S.publisher_id AND S.country_id = C.id AND C.name = '{0}' AND S.publication_type = '{1}'
        """,
        ['id', 'name'], ['int', 'str'], 'Q-1.b',
        [('country_name', 'Denmark'), ('publication_type', 'book')],
        "Print the ids and names of publishers of Danish book series."
    ),
    (
        """
        SELECT S.name
        FROM Series S, Country C
        WHERE S.publication_type = '{1}' AND S.country_id = C.id AND C.name = '{0}'
        """,
        ['name'], ['str'], 'Q-1.c',
        [('country_name', 'Switzerland'), ('publication_type', 'magazine')],
        "Print the names of all Swiss series that have been published in magazines."
    ),
    (
        """
        SELECT I.publication_date, COUNT(I.id)
        FROM Issue I
        WHERE I.publication_date >= {0}
        GROUP BY I.publication_date
        """,
        ['date', 'count'], ['int', 'int'], 'Q-1.d',
        [('publication_date', 1990)],
        "Starting from 1990, print the number of issues published each year."
    ),
    (
        """
        SELECT P.name, COUNT(DISTINCT I.series_id)
        FROM IndiciaPublisher P, Issue I
        WHERE P.id = I.indicia_publisher_id AND UTL_MATCH.jaro_winkler_similarity(P.name, '{0}') > {1}
        GROUP BY P.id, P.name
        """,
        ['name', 'count'], ['str', 'int'], 'Q-1.e',
        [('name', 'DC comics'), ('similarity', 65)],
        "Print the number of series for each indicia publisher whose name resembles ‘DC comics’."
    ),
    (
        """
        SELECT S.title
        FROM Story S
        WHERE S.id IN
            (
            SELECT S.reprint_id AS id
            FROM Story S
            WHERE S.reprint_id IS NOT NULL
            GROUP BY S.reprint_id
            ORDER BY COUNT(S.id) DESC
            OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
            )
        """,
        ['title'], ['str'], 'Q-1.f',
        [('top', 10)],
        "Print the titles of the 10 most reprinted stories"
    ),
    (
        """
        SELECT DISTINCT A.name
        FROM PersonAndStudio A, Scripts S, Pencils P, Colors C
        WHERE A.id = S.person_and_studio_id AND A.id = P.person_and_studio_id AND A.id = C.person_and_studio AND S.story_id = P.story_id AND S.story_id = C.story_id
        """,
        ['name'], ['str'], 'Q-1.g',
        [],
        "Print the artists that have scripted, drawn, and colored at least one of the stories they were involved in."
    ),
    (
        """
        SELECT DISTINCT S.title
        FROM Story S, Appearsin C, Characters X
        WHERE S.id NOT IN
            (
            SELECT S.reprint_id
            FROM Story S
            WHERE S.reprint_id IS NOT NULL
            )
        AND
        C.story_id = S.id
        AND
        C.character_id = X.id
        AND
        X.name = '{0}'
        AND
        X.id NOT IN
            (
            SELECT F.character_id
            FROM Features F
            WHERE F.story_id = S.id
            )
        """,
        ['title'], ['str'], 'Q-1.h',
        [('character', 'Batman')],
        "Print all non-reprinted stories involving Batman as a non-featured character."
    ),
    (
        """
        SELECT S.name
        FROM
        (
            SELECT S.name AS name, rank() OVER (ORDER BY COUNT(I.id) desc) AS rank
            FROM Series S, Issue I
            WHERE I.series_id = S.id AND I.id IN
            (
                SELECT S.issue_id
                FROM Story S
                WHERE S.id IN
                (
                    SELECT S.id AS id
                    FROM Story S
                    WHERE S.type <>
                    (
                        SELECT S.type
                        FROM Story S
                        GROUP BY S.type
                        ORDER BY COUNT(S.id) DESC
                        OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
                    )
                )
            )
            GROUP BY S.id, S.name
        ) S
        WHERE S.rank = 1

        """,
        ['name'], ['str'], 'Q-2.a',
        [],
        "Print the series names that have the highest number of issues which contain a story whose type (e.g., cartoon) is not the one occurring most frequently in the database (e.g, illustration)."
    ),
    (
        """
        SELECT P.name
        FROM Publisher P INNER JOIN
             Series S
             ON P.id = S.publisher_id
        GROUP BY P.id, P.name
        HAVING COUNT(DISTINCT S.publication_type)=3
        """,
        ['name'], ['str'], 'Q-2.b',
        [],
        "Print the names of publishers who have series with all series types."
    ),
    (
        """
        SELECT C.name, COUNT(ST.id)
        FROM Characters C, Appearsin A, Scripts S, Personandstudio P, Story ST
        WHERE C.id = A.character_id AND S.person_and_studio_id = P.id AND P.name = '{0}' AND ST.id = A.story_id AND A.story_id = S.story_id AND ST.reprint_id IS NOT NULL
        GROUP BY C.id, C.name
        ORDER BY COUNT(ST.id) DESC
        OFFSET 0 ROWS FETCH NEXT {1} ROWS ONLY
        """,
        ['name', 'count'], ['str', 'int'], 'Q-2.c',
        [('Persone_or_studio', 'Alan Moore'), ('top', 10)],
        "Print the 10 most-reprinted characters from Alan Moore's stories."
    ),
    (
        """
        SELECT DISTINCT X.name
        FROM PersonAndStudio X, Pencils P, Scripts S, Genre G, Story T
        WHERE X.id = P.person_and_studio_id AND X.id = S.person_and_studio_id AND P.story_id = T.id AND S.story_id = T.id AND G.story_id = T.id AND G.genre = '{0}'
        """,
        ['name'], ['str'], 'Q-2.d',
        [('genre', 'nature')],
        "Print the writers of nature-related stories that have also done the pencilwork in all their nature-related stories."
    ),
    (
        """
        SELECT L.name
        FROM
        (
            SELECT L.name AS name
            FROM
            (
                SELECT P.id AS publisher_id
                FROM Publisher P, Series S
                WHERE P.id = S.publisher_id
                GROUP BY P.id
                ORDER BY COUNT(S.id) DESC
                OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
            ) P, Series S, Language L
            WHERE P.publisher_id = S.publisher_id AND S.language_id = L.id
            GROUP BY L.id, L.name
            ORDER BY COUNT(DISTINCT L.id) DESC
            OFFSET 0 ROWS FETCH NEXT {1} ROWS ONLY
        ) L
        """,
        ['name'], ['str'], 'Q-2.e',
        [('top_publisher', 10), ('most_popular_language', 3)],
        "For each of the top-10 publishers in terms of published series, print the 3 most popular languages of their series."
    ),
    (
        """
        SELECT L.name, COUNT(ST.id)
        FROM Story ST, Issue I, Series SE, Language L
        WHERE ST.issue_id = I.id AND ST.reprint_id IS NULL AND I.series_id = SE.id AND SE.publication_type = '{1}' AND SE.language_id = L.id
        HAVING COUNT(ST.id) >= {0}
        GROUP BY L.id, L.name
        """,
        ['name', 'count'], ['str', 'int'], 'Q-2.f',
        [('original_stories', 10000), ('publication_type', 'magazine')],
        "Print the languages that have more than 10000 original stories published in magazines, along with the number of those stories."
    ),
    (
        """
        SELECT DISTINCT S.type
        FROM Story S
        WHERE S.type NOT IN
        (
            SELECT DISTINCT ST.type
            FROM Story ST, Issue I, Series SE, Country C
            WHERE ST.issue_id = I.id AND I.series_id = SE.id AND SE.publication_type = '{0}' AND SE.country_id = C.id AND C.name = '{1}'
        )
        """,
        ['type'], ['str'], 'Q-2.g',
        [('publication_type', 'magazine'), ('country', 'Italy')],
        "Print all story types that have not been published as a part of Italian magazine series."
    ),
    (
        """
        SELECT W.name
        FROM
        (
            SELECT DISTINCT P.id AS id, P.name AS name, I.id AS indicia_publisher_id
            FROM Story S, Personandstudio P, Scripts W, Issue I
            WHERE S.id = W.story_id AND P.id = W.person_and_studio_id AND S.issue_id = I.id AND P.id IN
            (
                SELECT P.id
                FROM Story S, Personandstudio P, Scripts W
                WHERE S.issue_id = I.id AND W.person_and_studio_id = P.id AND W.story_id = S.id AND S.type = '{0}'
            )
        ) W
        HAVING COUNT(DISTINCT W.indicia_publisher_id) > {1}
        GROUP BY W.id, W.name
        """,
        ['name'], ['str'], 'Q-2.h',
        [('story_type', 'cartoon'), ('indicia_publisher', 1)],
        "Print the writers of cartoon stories who have worked as writers for more than one indicia publisher."
    ),
    (
        """
        SELECT B.name
        FROM
        (
        SELECT DISTINCT P.id AS id, COUNT(DISTINCT I.id) AS count
        FROM Publisher P, IndiciaPublisher I
        WHERE I.publisher_id = P.id
        GROUP BY P.id
        ) P, BrandGroup B
        WHERE B.publisher_id = P.id
        ORDER BY P.count DESC
        OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
        """,
        ['name'], ['str'], 'Q-2.i',
        [('top', 10)],
        "Print the 10 brand groups with the highest number of indicia publishers."
    ),
    (
        """
        SELECT S.indicia_publisher_name, AVG(S.year_ended - S.year_began)
        FROM
        (
        SELECT DISTINCT S.id AS id, IP.id AS indicia_publisher, IP.name AS indicia_publisher_name, S.year_ended AS year_ended, S.year_began AS year_began
        FROM IndiciaPublisher IP, Series S, Issue I
        WHERE S.id = I.series_id AND I.indicia_publisher_id = IP.id AND S.year_ended IS NOT NULL AND S.year_began IS NOT NULL
        ) S
        GROUP BY S.indicia_publisher, S.indicia_publisher_name
        """,
        ['name', 'average year'], ['str', 'float'], 'Q-2.j',
        [],
        "Print the average series length (in terms of years) per indicia publisher."
    ),
    (
        """
        SELECT IP.name
        FROM Issue I, IndiciaPublisher IP
        WHERE I.id IN
        (
        SELECT I.id
        FROM Issue I
        HAVING COUNT(DISTINCT I.id) = 1
        GROUP BY I.series_id, I.id
        ) AND IP.id = I.indicia_publisher_id
        GROUP BY I.indicia_publisher_id, IP.name
        ORDER BY COUNT(DISTINCT I.id) DESC
        OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
        """,
        ['name'], ['str'], 'Q-2.k',
        [('top', 10)],
        "Print the top 10 indicia publishers that have published the most single-issue series."
    ),
    (
        """
        SELECT IP.name, MAX(S.count)
        FROM
        (
        SELECT S.id AS id, IP.id AS indicia_publisher_id, COUNT(DISTINCT W.person_and_studio_id) AS count
        FROM Story S, Scripts W, Issue I, IndiciaPublisher IP
        WHERE S.id = W.story_id AND I.id = S.issue_id AND IP.id = I.indicia_publisher_id
        GROUP BY S.id, IP.id
        ) S, IndiciaPublisher IP
        WHERE IP.id = S.indicia_publisher_id
        GROUP BY IP.id, IP.name
        ORDER BY MAX(S.count) DESC
        OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
        """,
        ['name', 'max count'], ['str', 'int'], 'Q-2.l',
        [('top', 10)],
        "Print the 10 indicia publishers with the highest number of script writers in a single story."
    ),
    (
        """
        SELECT C.name
        FROM Characters C
        WHERE C.id IN
        (
        SELECT C.cid
        FROM
        (
        SELECT C.id AS cid, P.id AS pid
        FROM Publisher P, Series S, Issue I, Story ST, Appearsin A, Characters C
        WHERE P.id = S.publisher_id AND I.series_id = S.id AND ST.issue_id = I.id AND A.story_id = ST.id AND C.id = A.character_id AND (P.name = 'Marvel' OR P.name = 'DC')
        UNION
        SELECT C.id AS cid, P.id AS pid
        FROM Publisher P, Series S, Issue I, Story ST, Features A, Characters C
        WHERE P.id = S.publisher_id AND I.series_id = S.id AND ST.issue_id = I.id AND A.story_id = ST.id AND C.id = A.character_id AND (P.name = 'Marvel' OR P.name = 'DC')
        ) C
        HAVING COUNT(DISTINCT pid)=2
        GROUP BY C.cid
        )
        AND C.id IN
        (
        SELECT C.id AS cid
        FROM Publisher P, Series S, Issue I, Story ST, Appearsin A, Characters C
        WHERE P.id = S.publisher_id AND I.series_id = S.id AND ST.issue_id = I.id AND A.story_id = ST.id AND C.id = A.character_id AND (P.name = 'Marvel')
        UNION
        SELECT C.id AS cid
        FROM Publisher P, Series S, Issue I, Story ST, Features A, Characters C
        WHERE P.id = S.publisher_id AND I.series_id = S.id AND ST.issue_id = I.id AND A.story_id = ST.id AND C.id = A.character_id AND (P.name = 'Marvel')
        )
        """,
        ['name'], ['str'], 'Q-2.m',
        [],
        "Print all Marvel heroes that appear in Marvel-DC story crossovers."
    ),
    (
        """
        SELECT S.name
        FROM Series S
        WHERE S.ID in(
        SELECT ISS.SERIES_ID
        FROM ISSUE ISS
        GROUP BY ISS.SERIES_ID
        ORDER BY COUNT(DISTINCT ISS.ID) DESC
        OFFSET 0 ROWS FETCH NEXT {0} ROWS ONLY
        )
        """,
        ['name'], ['str'], 'Q-2.n',
        [('top', 5)],
        "Print the top 5 series with most issues."
    ),
    (
        """
        SELECT S.title
        FROM Story S, Story S2
        WHERE S2.reprint_id IS NOT NULL AND S2.reprint_id = S.id AND S.issue_id = {0}
        GROUP BY S2.reprint_id, S.title, S.issue_id
        ORDER BY COUNT(DISTINCT S2.id)
        OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
        """,
        ['title'], ['str'], 'Q-2.o',
        [('issue_id', 154)],
        "Given an issue, print its most reprinted story."
    ),
]

QUESTION_TO_INDEX_MAPPING = {QUERY_LIST[i][3]: i for i in range(len(QUERY_LIST))}

SERIALIZER = {
    'int': lambda x: str(x),
    'str': lambda x: x,
    'float': lambda x: str(round(x, 2))
}


def serializer(rows, fields, fields_type):
    out = []
    for r in rows:
        obj = {}
        for i in range(len(fields)):
            obj[fields[i]] = SERIALIZER[fields_type[i]](r[i])
        out.append(obj)
    return out


def execute_query(sql_query_str):
    with connections['oracle'].cursor() as cursor:
        cursor.execute(sql_query_str)
        rows = cursor.fetchall()
    return rows


def general_view(request, question):
    try:
        query_tuple = QUERY_LIST[QUESTION_TO_INDEX_MAPPING[question]]
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if len(query_tuple) > 4:
        parameter_names = [var[0] for var in query_tuple[4]]
        default_values = [var[1] for var in query_tuple[4]]
    else:
        parameter_names = []
        default_values = []

    parameter_values = default_values

    for i in range(len(parameter_names)):
        if request.GET.get(parameter_names[i]) is not None:
            parameter_values[i] = request.GET.get(parameter_names[i])

    parameters = [(parameter_names[i], parameter_values[i]) for i in range(len(parameter_names))]

    sql_query = query_tuple[0].format(*parameter_values)

    start_time = time.time()
    tuples = execute_query(sql_query)
    execution_time = time.time() - start_time
    serialized_objs = serializer(tuples, query_tuple[1], query_tuple[2])
    template = loader.get_template("costum_query.html")

    return HttpResponse(template.render({
        'serialized_data': serialized_objs,
        'field_list': query_tuple[1],
        # 'sql_query': mark_safe(highlight(sql_query, SqlLexer(), HtmlFormatter(full=True))),
        'sql_execution_time': '% .2E' % execution_time,
        'foreign_field_list': [],
        'parameters': parameters,
        'parameters_present': len(parameters) > 0,
        'query_description': query_tuple[-1]
    }), request)
