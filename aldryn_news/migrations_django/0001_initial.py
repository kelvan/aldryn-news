# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djangocms_text_ckeditor.fields
import cms.models.fields
import filer.fields.image
import taggit.managers
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('contenttypes', '0001_initial'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('ordering', models.IntegerField(default=0, verbose_name='Ordering')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['ordering'],
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug', blank=True, help_text='Auto-generated. Clean it to have it re-created. WARNING! Used in the URL. If changed, the URL will change. ')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(related_name='translations', editable=False, null=True, to='aldryn_news.Category')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_tablespace': '',
                'db_table': 'aldryn_news_category_translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestNewsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, auto_created=True, to='cms.CMSPlugin')),
                ('latest_entries', models.PositiveSmallIntegerField(help_text='The number of latests entries to be displayed.', default=5)),
                ('type_list', models.CharField(max_length=255, choices=[('full', 'Full list'), ('simple', 'Simple list')], default='full', verbose_name='Type of list')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('publication_start', models.DateTimeField(help_text='Used in the URL. If changed, the URL will change.', default=datetime.datetime.now, verbose_name='Published Since')),
                ('publication_end', models.DateTimeField(null=True, verbose_name='Published Until', blank=True)),
                ('category', models.ForeignKey(blank=True, help_text='WARNING! Used in the URL. If changed, the URL will change.', null=True, to='aldryn_news.Category', verbose_name='Category')),
                ('content', cms.models.fields.PlaceholderField(slotname='blog_post_content', editable=False, null=True, to='cms.Placeholder')),
                ('key_visual', filer.fields.image.FilerImageField(blank=True, null=True, to='filer.Image', verbose_name='Key Visual')),
            ],
            options={
                'verbose_name_plural': 'News',
                'ordering': ['-publication_start'],
                'verbose_name': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsLinksPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, auto_created=True, to='cms.CMSPlugin')),
                ('news', models.ManyToManyField(to='aldryn_news.News', verbose_name='News')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NewsTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.CharField(max_length=255, verbose_name='Slug', blank=True, help_text='Auto-generated. Clean it to have it re-created. WARNING! Used in the URL. If changed, the URL will change. ')),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(help_text='Will be displayed in lists, and at the start of the detail page', verbose_name='Lead-in')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(related_name='translations', editable=False, null=True, to='aldryn_news.News')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_tablespace': '',
                'db_table': 'aldryn_news_news_translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('content_type', models.ForeignKey(related_name='aldryn_news_taggeditem_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(to='aldryn_news.Tag', related_name='aldryn_news_taggeditem_items')),
            ],
            options={
                'verbose_name_plural': 'Tagged Items',
                'verbose_name': 'Tagged Item',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(related_name='translations', editable=False, null=True, to='aldryn_news.Tag')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_tablespace': '',
                'db_table': 'aldryn_news_tag_translation',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tagtranslation',
            unique_together=set([('slug', 'language_code'), ('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='newstranslation',
            unique_together=set([('slug', 'language_code'), ('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='aldryn_news.TaggedItem', to='aldryn_news.Tag', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='latestnewsplugin',
            name='tags',
            field=models.ManyToManyField(help_text='Show only the news tagged with chosen tags.', to='taggit.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('slug', 'language_code'), ('language_code', 'master')]),
        ),
    ]
