from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from composer.models import Slot, Row, Column, Tile
from composer.tests.models import DummyModel1, DummyModel2


HOME_REGEX = "^" + reverse("home") + "$"


class TemplateTagsATestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsATestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name="content", url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()

    def test_default_slot(self):
        # Home renders the custom composer/inclusion_tags/content.html
        response = self.client.get(reverse("home"))
        self.assertHTMLEqual("""
        <div id="header">
            Header slot
        </div>
        <div id="content">
            This is the default content
        </div>
        <div id="footer">
            Footer slot
        </div>""", response.content)


class TemplateTagsBTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsBTestCase, cls).setUpTestData()
        cls.dm_one = DummyModel1.objects.create(title="One")
        cls.slot = Slot.objects.create(slot_name="content", url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(
            column=Column.objects.create(row=Row.objects.create(slot=cls.slot))
        )
        cls.tile.target = cls.dm_one
        cls.tile.save()

    def test_target(self):

        # DummyModel1 has its own detail page, no templates for the tile style
        response = self.client.get(reverse("home"))
        self.assertHTMLEqual("""
        <div id="header">
            Header slot
        </div>
        <div id="content">
            <div class="composer-row None">
                <div class="composer-column composer-column-8 None">
                    <div class="composer-tile None">
                        I am DummyModel1 One
                    </div>
                </div>
            </div>
        </div>
        <div id="footer">
            Footer slot
        </div>""", response.content)


class TemplateTagsCTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsCTestCase, cls).setUpTestData()
        cls.dm_one = DummyModel2.objects.create(title="One")
        cls.slot = Slot.objects.create(slot_name="content", url=HOME_REGEX)
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(
            column=Column.objects.create(row=Row.objects.create(slot=cls.slot))
        )
        cls.tile.target = cls.dm_one
        cls.tile.save()

    def test_target(self):

        # DummyModel2 has a tile style template
        # tests/inclusion_tags/dummymodel2_tile.html
        response = self.client.get(reverse("home"))
        self.assertHTMLEqual("""
        <div id="header">
            Header slot
        </div>
        <div id="content">
            <div class="composer-row None">
                <div class="composer-column composer-column-8 None">
                    <div class="composer-tile None">
                        I am a tile for DummyModel2 One
                    </div>
                </div>
            </div>
        </div>
        <div id="footer">
            Footer slot
        </div>""", response.content)


class TemplateTagsDTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsDTestCase, cls).setUpTestData()
        cls.slot = Slot.objects.create(slot_name="header", url="^" + reverse("aaa"))
        cls.slot.sites = Site.objects.all()
        cls.slot.save()
        cls.tile = Tile.objects.create(
            column=Column.objects.create(row=Row.objects.create(slot=cls.slot))
        )
        cls.tile.view_name = "header"
        cls.tile.save()

    def test_header(self):

        # aaa gets the header slot
        response = self.client.get(reverse("aaa"))
        self.assertHTMLEqual("""
        <div id="header">
        	<div class="composer-row None">
            	<div class="composer-column composer-column-8 None">
                	<div class="composer-tile None">
                    	I am the header
                    </div>
                </div>
	        </div>
        </div>
        <div id="content">
            I am aaa. I live at /aaa/.
        </div>
        <div id="footer">
            Footer slot
        </div>""", response.content)

		# bbb also gets the header slot because the regex does not end with a dollar
        response = self.client.get(reverse("bbb"))
        self.assertHTMLEqual("""
        <div id="header">
        	<div class="composer-row None">
            	<div class="composer-column composer-column-8 None">
                	<div class="composer-tile None">
                    	I am the header
                    </div>
                </div>
	        </div>
        </div>
        <div id="content">
            I am bbb. I live at /aaa/bbb/.
        </div>
        <div id="footer">
            Footer slot
        </div>""", response.content)
