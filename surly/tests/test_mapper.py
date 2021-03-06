from nose.tools import *

import unittest

from surly.mapper import Mapper, url, MapperError, include

class MapperTestCase(unittest.TestCase):
    m = Mapper([
        url(r'^/$', None, name='home'),
        url(r'^/home$', None),
        url(r'^/foo$', None, name='foos'),
        url(r'^/foo/(?P<foo>\d+)$', None, name='foo'),
    ])
    
    def test_mapper_simple(self):

        assert self.m.reverse('home') == '/'
        assert self.m.reverse('foos') == '/foo'
        assert self.m.reverse('foo', foo=5) == '/foo/5'
    
    @raises(MapperError)
    def test_double_name_error(self):
        m = Mapper([
            url(r'^/$', None, name='home'),
            url(r'^/home$', None, name='home'),
        ])

    def test_prefix(self):
        app_urls = [ url(r'/home', None),
                     url(r'/foo', None, name='foo')]
        mapper = Mapper([
                        url(r'^/$', None),
                        include('/app', app_urls),
                        url('help', None),
                        ])
        assert mapper.reverse('foo') == '/app/foo', mapper.reverse('foo')
    
    @raises(MapperError)
    def test_no_pattern(self):
        self.m.reverse('DOES_NOT_EXIST')

    def test_js_mapper(self):
        m = Mapper([
            url(r'^/$', None, name='home'),
            url(r'^/home$', None),
            url(r'^/foo$', None, name='foos'),
            url(r'^/foo/(?P<foo>\d+)$', None, name='foo'),
        ])

        expected = '''Mapper = function(name, args){var mapping = {"home":function(fields){return ""+"/";},"foo":function(fields){return ""+"/foo/"+fields["foo"];},"foos":function(fields){return ""+"/foo";}};return mapping[name](args);};'''
        assert expected == m.js_mapper('Mapper'), m.js_mapper('Mapper')
    def test_replacements(self):
        m = Mapper([
            url(r'^/{home}$', None, name='home1'),
        ], replacements={'home' : 'foo'})
        m.urls[0].apply_replacements(**{'home':'bar'})
        expected = '/foo'
        assert expected == m.reverse('home1')
