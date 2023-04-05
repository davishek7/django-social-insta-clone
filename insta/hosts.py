from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns('',
    host('', settings.ROOT_URLCONF, name=' '),
    host(r'dashboard', 'dashboard.urls', name='dashboard'),
)