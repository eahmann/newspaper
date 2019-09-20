# Based on torchbox implementation

from django.shortcuts import render

from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                         MultiFieldPanel, PageChooserPanel)
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.core.signals import page_published
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from core.models import Author # CustomImage

@register_snippet
class YearsActive(models.Model):
    year_string = models.CharField(max_length=20)

    def __str__(self):
        return self.year_string

    search_fields = [
        index.SearchField('year_string'),
    ]

    class Meta:
        verbose_name = 'Years active'
        verbose_name_plural = 'Years active'
        ordering = ['-year_string']

        
class StaffPage(RoutablePageMixin, Page):
    max_count = 1
    subpage_types = [
        'people.PersonPage'
    ]
    parent_page_type = [
        'home.HomePage'
    ]

    current_year = models.ForeignKey('YearsActive', null=True, on_delete=models.SET_NULL, related_name='year')

    content_panels = Page.content_panels + [
        SnippetChooserPanel('current_year'),
    ]

    def get_people(self):
        return PersonPage.objects.all()

    def get_year(self):
        year = YearsActive.objects.all()
        latest = year[0].year_string
        return latest

    @property
    def staff_page(self):
        return self.specific()

    #def get_role(self):
        #role = RoleAssignment.objects.filter(page=self)
        #return role

    @route(r'^year/(?P<year>[-\w]+)/$', name='year')
    def staff_by_year(self, request, year, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        self.search_type = 'year'
        self.search_term = year
        context['year'] = year
        context['people'] = PersonPage.objects.filter(role_assignment__year__year_string=year)
        return render(request, "people/staff_page.html", context)

    def get_context(self, request):
        context = super().get_context(request)
        # context['staff_page'] = self,staff_page
        context['year'] = self.get_year()
        context['years'] = YearsActive.objects.all()
        context['people'] = self.get_people().filter(role_assignment__year__year_string=self.get_year()).distinct()
        return context


@register_snippet
class Roles(models.Model):
    role = models.CharField(max_length=75)

    def __str__(self):
        return self.role

    search_fields = [
        index.SearchField('role'),
    ]

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'





# Allow different role for different year
class RoleAssignment(Orderable):
    page = ParentalKey('PersonPage', related_name='role_assignment')
    role = models.ForeignKey(
        'people.Roles',
        on_delete=models.CASCADE,
        related_name='+',
    )
    year = models.ForeignKey(
        'people.YearsActive',
        on_delete=models.CASCADE,
        related_name='+',
    )

    panels = [
        SnippetChooserPanel('role'),
        SnippetChooserPanel('year'),
    ]

    def __str__(self):
        return self.role.role

class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


class PersonPage(Page, ContactFields):
    parent_page_type = [
        'staff.StaffPage'
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    is_senior = models.BooleanField(default=False)
    years_active = ParentalManyToManyField("YearsActive", blank=True)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    short_biography = models.CharField(
        max_length=255, blank=True,
        help_text='A shorter summary biography for including in other pages'
    )
    profile_image = models.ForeignKey(
        'core.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    template = 'people/person_page.html'

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('intro'),
        index.SearchField('biography'),
    ]

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        InlinePanel('role_assignment', label='My roles'),
        FieldPanel('is_senior'),
        FieldPanel("years_active", widget=forms.SelectMultiple),
        FieldPanel('intro', classname="full"),
        FieldPanel('biography', classname="full"),
        FieldPanel('short_biography', classname="full"),
        ImageChooserPanel('profile_image'),
        MultiFieldPanel(ContactFields.panels, "Contact"),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
    ]


    def staff_page(self):
        return StaffPage.objects.get(slug='staff')


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        posts = Author.objects.filter(author__person_page__slug=self.slug)
        roles = RoleAssignment.objects.filter(page=self)
        context['parent'] = self.staff_page()
        context['roles'] = roles
        context['posts'] = posts
        return context

@register_snippet
class Person(index.Indexed, models.Model):
    person_page = models.OneToOneField(
        'people.PersonPage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=255, blank=True)
    image = models.ForeignKey(
        'core.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    def update_manual_fields(self, person_page):
        self.name = person_page.title
        self.role = person_page.role
        self.image = person_page.profile_image

    def clean(self):
        if not self.person_page and not self.name:
            raise ValidationError({'person_page': "You must set either 'Person page' or 'Name'"})
        if self.person_page:
            self.update_manual_fields(self.person_page)

    def __str__(self):
        return self.name

    search_fields = [
        index.SearchField('name'),
    ]

    panels = [
        PageChooserPanel('person_page'),
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('role'),
        #     ImageChooserPanel('image'),
         ], "Manual fields (Automatically overridden if you have a page!)"),
    ]

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name']





