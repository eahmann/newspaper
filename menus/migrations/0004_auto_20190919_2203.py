# Generated by Django 2.2.5 on 2019-09-20 03:03

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_subitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropdownItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('menu_item', models.CharField(blank=True, max_length=250)),
                ('internal_url', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Submenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('subsite_url', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubmenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('menu_item', models.CharField(blank=True, max_length=250)),
                ('internal_url', models.CharField(blank=True, max_length=250)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenu_items', to='menus.Submenu')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='page',
        ),
        migrations.RemoveField(
            model_name='subitem',
            name='link_page',
        ),
        migrations.RemoveField(
            model_name='subitem',
            name='page',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
        migrations.DeleteModel(
            name='SubItem',
        ),
        migrations.AddField(
            model_name='dropdownitem',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='dropdown_items', to='menus.SubmenuItem'),
        ),
    ]
