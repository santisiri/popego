# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
import os
from datetime import datetime
from time import mktime
from popserver.agents import twitter_agent
from popserver.tests import *
from popserver.tests.nodb_model import *
import popserver.tests.mock as p
from unittest import TestCase

class TestTwitterAgent(TestCase):
    def setUp(self):
        super(self.__class__, self).setUp()
        # initialize here ...
        import popserver.tests as t
        self.samplepath = '%s/samples/twitter/' % t.__path__[0]
        self.oldValue = twitter_agent.BASE_URL
        twitter_agent.BASE_URL = self.samplepath 

    def tearDown(self):
        twitter_agent.BASE_URL = self.oldValue
        # ... finalize here
        super(self.__class__, self).tearDown()

    def test_userExists(self):
        exists = twitter_agent.userExists('manuelaristaran')
        self.assertEqual(exists, True)

    def test_userExists_expectingFalse(self):
        exists = twitter_agent.userExists('inexistent_user')
        self.assertEqual(exists, False)

    def test_updateAccount(self):
        a = Account(username='manuelaristaran', last_updated=None)
        cacheApiMock = p.Mock()
        cacheApiMock.expects(p.once()).addGroup(p.eq(None), \
                                                    name=p.eq('Twitter'), is_null_group=p.eq(True))
        cacheApiMock.expects(p.once()).method('itemExists') \
            .will(p.return_value(True))
        twitter_agent.updateAccount(a, cacheApiMock)
        cacheApiMock.verify()
        # NOTE: When itemExists returns True, _parseEntry is
        # no longer called. Then itemExists is called just once.

    def test_updateAccount_withExistentDefaultGroup(self):
        a = Account(username='manuelaristaran')
        a.last_updated = datetime.now()
        cacheApiMock = p.Mock()
        cacheApiMock.expects(p.once()).method('itemExists') \
            .will(p.return_value(True))
        twitter_agent.updateAccount(a, cacheApiMock)
        cacheApiMock.verify()

    def test_getFeed(self):
        titles = [u'manuelaristaran: Primer d\xeda en los nuevos HQ de Popego. Classy.',
                  u'manuelaristaran: musica.jazzido.com: Rolling Stone Cover to Cover: The First 40 Years http://tinyurl.com/2aven5',
                  u'manuelaristaran: @amartino: otro que no tuvo demasiada difusi\xf3n (ser\xe1 porque es medio incendiario?): http://snurl.com/1uer3',
                  u'manuelaristaran: @dfgonzalez: a veces soy sysadmin :)',
                  u'manuelaristaran: "Sab\xe9s qu\xe9 hay en una chica que despu\xe9s de un tiempo agarra una guitarra y se pone a tocar? Mucho m\xe1s que eso" http://snurl.com/1uemz',
                  u'manuelaristaran: Todav\xeda sysadmineando para designdeadline.com',
                  u'manuelaristaran: @amartino: Genial!',
                  u'manuelaristaran: Sincronicidad: Empec\xe9 a leer Rainbows End hace unos d\xedas. Hoy, el autor public\xf3 el texto completo en su site; http://snurl.com/1udco',
                  u'manuelaristaran: In the meantime, un roommate contamina el ambiente con un disco de Andrea Boccelli. ANDREA BOCCELLI!!',
                  u'manuelaristaran: @earlkman: encima, los m\xe9todos m\xe1s jugosos necesitan autenticaci\xf3n. Y eso que son m\xe9todos read-only...',
                  u'manuelaristaran: @earlkman: dif\xedcil implementar un buen sync minimizando los API calls. Me hace pensar que algunos sitios tienen API solo para ser 2.0...',
                  u'manuelaristaran: Me cago en el API de Flickr',
                  u'manuelaristaran: xkcd no para: http://xkcd.com/350/',
                  u'manuelaristaran: musica.jazzido.com: \u201cMusic and Life\u201d, sobre una grabaci\xf3n de\xa0Alan Watts,\xa0por l.. http://tinyurl.com/2uwprh',
                  u'manuelaristaran: "It\'s not the documents, it is the things they are about which are important". Obvious, really. http://snurl.com/1u9vh',
                  u'manuelaristaran: descubrimiento musical: Stan Kenton. Adelantado para su \xe9poca.',
                  u'manuelaristaran: musica.jazzido.com: Tom Z\xe9 - A Felicidade http://tinyurl.com/2hvofc',
                  u'manuelaristaran: musica.jazzido.com: \u201cRequiem pour un con\u201d (R\xe9quiem para un gil) \nde\xa0Serge... http://tinyurl.com/yom7pm',
                  u'manuelaristaran: @amartino: definitivamente! Y no tuvo mucha repercusi\xf3n, no?',
                  u'manuelaristaran: Seteando hosting en slicehost.com para designdeadline.com. Sysadmining, fun stuff.']
        feedUrl = twitter_agent._getFeedUrl('manuelaristaran')
        f = twitter_agent._getFeed(feedUrl)
        self.assertEqual([i.get('title') for i in f.entries], titles)

    def test_parseEntry(self):
        entry = {'id': u'http://twitter.com/manuelaristaran/statuses/465479172',
                 'link': u'http://twitter.com/manuelaristaran/statuses/465479172',
                 'summary': u'manuelaristaran: Primer d\xeda en los nuevos HQ de Popego. Classy.',
                 'title': u'manuelaristaran: Primer d\xeda en los nuevos HQ de Popego. Classy.',
                 'updated': u'Mon, 03 Dec 2007 14:24:28 +0000',
                 'updated_parsed': (2007, 12, 3, 14, 24, 28, 0, 337, 0)}
        ext_id = entry['id']
        cacheApiMock = p.Mock()
        cacheApiMock.expects(p.once()).itemExists(p.eq(ext_id)) \
            .will(p.return_value(False))
        cacheApiMock.expects(p.once()).method('addItem')
        cacheApiMock.expects(p.once()).method('bindItem2Group')
        quote = twitter_agent._parseEntry(entry, cacheApiMock)
        cacheApiMock.verify()
        # non-happy paths are validated in other tests

    def test_entryToQuote(self):
        entry = {'id': u'http://twitter.com/manuelaristaran/statuses/465479172',
                 'link': u'http://twitter.com/manuelaristaran/statuses/465479172',
                 'summary': u'manuelaristaran: Primer d\xeda en los nuevos HQ de Popego. Classy.',
                 'title': u'manuelaristaran: Primer d\xeda en los nuevos HQ de Popego. Classy.',
                 'updated': u'Mon, 03 Dec 2007 14:24:28 +0000',
                 'updated_parsed': (2007, 12, 3, 14, 24, 28, 0, 337, 0)}
        expected_title = u'Primer d\xeda en los nuevos HQ de Popego. Classy.'
        quote = twitter_agent._entryToQuote(entry)
        self.assertEqual(quote['title'], expected_title)
        self.assertEqual(quote['description'], expected_title)
        self.assertEqual(quote['external_url'], entry['link'])
        self.assertEqual(quote['creation_date'], \
                             datetime(2007, 12, 3, 17, 24, 28))

