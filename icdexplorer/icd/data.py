"""
ICDexplorer

(c) 2011 Jan Poeschko
jan@poeschko.com
"""

from django.conf import settings
from django.db.models import Min, Max
from django.contrib.auth.models import User

from icdexplorer.icd.models import Category, Change, Annotation, CategoryMetrics, Author, Group, AuthorCategoryMetrics, Property
from icdexplorer.storage.models import PickledData

print "Load data"

GRAPH = PickledData.objects.get(settings.INSTANCE, 'graph')
CATEGORIES = dict((category.name, category) for category in Category.objects.filter(instance=settings.INSTANCE))

print "Categories loaded"

"""GRAPH_POSITIONS = {}
GRAPH_POSITIONS_TREE = {}
for layout, dot_prog in settings.LAYOUTS:
    GRAPH_POSITIONS[dot_prog] = PickledData.objects.get(settings.INSTANCE,
        'graph_positions_%s' % dot_prog)
    GRAPH_POSITIONS_TREE[dot_prog] = PickledData.objects.get(settings.INSTANCE,
        'graph_positions_tree_%s_' % dot_prog)
WEIGHTS = PickledData.objects.get(settings.INSTANCE, 'weights')
#WEIGHTS = {}
"""

AUTHORS = dict((author.instance_name, author) for author in Author.objects.filter(instance=settings.INSTANCE))
for author in AUTHORS.values():
    author.groups_list = list(author.groups.order_by('name'))
GROUPS = Group.objects.order_by('name')
for group in GROUPS:
    group.authors_list = list(group.authors.all())
    group.authors_list.sort(key=lambda author: author.changes_count + author.annotations_count, reverse=True)
print "Authors loaded"

GRAPH_AUTHORS = PickledData.objects.get(settings.INSTANCE, 'author_graph')
GRAPH_AUTHORS_DIRECTED = PickledData.objects.get(settings.INSTANCE, 'author_graph_directed')
GRAPH_AUTHORS_POSITIONS = PickledData.objects.get(settings.INSTANCE, 'author_graph_positions')

print "Author Graphs loaded"

FEATURES = [(name, description) for name, value, description in CategoryMetrics.objects.all()[0].get_metrics()]
AUTHOR_FEATURES = [(name, description) for name, value, description in AuthorCategoryMetrics.objects.all()[0].get_metrics()]

print "Features loaded"

MINMAX_CHANGES_DATE = Change.objects.filter(_instance=settings.INSTANCE).aggregate(min=Min('timestamp'), max=Max('timestamp'))
print MINMAX_CHANGES_DATE

#if MINMAX_CHANGES_DATE['min'] == None:
#    MIN_CHANGES_DATE = MINMAX_CHANGES_DATE['max'].date()
#else:
MIN_CHANGES_DATE = MINMAX_CHANGES_DATE['min'].date()
MAX_CHANGES_DATE = MINMAX_CHANGES_DATE['max'].date()

print "Change dates loaded"

CHANGES_COUNT = sum(author.changes_count for author in AUTHORS.values())
ANNOTATIONS_COUNT = sum(author.annotations_count for author in AUTHORS.values())

print "Annotations loaded"

PROPERTIES = dict((property.name, property) for property in Property.objects.filter(instance=settings.INSTANCE))
GRAPH_PROPERTIES_POSITIONS = PickledData.objects.get(settings.INSTANCE, 'properties_graph_positions')
FOLLOW_UPS = PickledData.objects.get(settings.INSTANCE, 'follow_ups')

print "Properties loaded"
    
print "Data loaded"
