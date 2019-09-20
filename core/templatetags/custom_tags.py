from django.template import Library, loader
from django.urls import resolve
from core.models import ArticleIndexPage, ArticlePage
from people.models import RoleAssignment, YearsActive, StaffPage
from home.models import HomePage

register = Library()


@register.simple_tag()
def articles(self):
    return ArticleIndexPage.objects.get(id=1)


@register.simple_tag()
def post_date_url(post, article_page):
    post_date = post.date
    url = article_page.url + article_page.reverse_subpage(
        'post_by_date_slug',
        args=(
            post_date.year,
            '{0:02}'.format(post_date.month),
            '{0:02}'.format(post_date.day),
            post.slug,
        )
    )
    return url


@register.simple_tag()
def post_cat_url(cat, blog_page):
    post_cat = cat
    url = blog_page.url + blog_page.reverse_subpage(
        'post_by_category',
        args=(
            post_cat,
        )
    )
    return url


@register.simple_tag()
def get_role(person, year):
    role = RoleAssignment.objects.filter(page=person, year=YearsActive.objects.get(year_string=year))
    return role

@register.simple_tag()
def get_posts_by_category(category):
    posts = ArticlePage.objects.filter(article_categories__article_category__slug=category)
    return posts

@register.simple_tag()
def tagline():
    home = HomePage.objects.get(slug='home')
    return home.tagline