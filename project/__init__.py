from django.db import connections

# TODO
cursor = connections['default'].cursor()
cursor.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
