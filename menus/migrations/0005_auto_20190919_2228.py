# Generated by Django 2.2.5 on 2019-09-20 03:28

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('menus', '0004_auto_20190919_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_title', models.CharField(blank=True, max_length=50, null=True)),
                ('link_url', models.CharField(blank=True, max_length=500)),
                ('fa_icon', models.CharField(blank=True, max_length=25, verbose_name='Font Awesome icon')),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='menus.Menu')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_title', models.CharField(blank=True, max_length=50, null=True)),
                ('link_url', models.CharField(blank=True, max_length=500)),
                ('fa_icon', models.CharField(blank=True, max_length=25, verbose_name='Font Awesome icon')),
                ('open_in_new_tab', models.BooleanField(blank=True, default=False)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_items', to='menus.MenuItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='submenuitem',
            name='page',
        ),
        migrations.DeleteModel(
            name='DropdownItem',
        ),
        migrations.DeleteModel(
            name='Submenu',
        ),
        migrations.DeleteModel(
            name='SubmenuItem',
        ),
    ]
