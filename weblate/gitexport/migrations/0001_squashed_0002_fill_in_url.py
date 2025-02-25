# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Generated by Django 1.11.13 on 2018-06-21 13:26

from django.db import migrations

from weblate.gitexport.models import SUPPORTED_VCS, get_export_url


def set_export_url(apps, schema_editor):
    Component = apps.get_model("trans", "Component")
    db_alias = schema_editor.connection.alias
    matching = (
        Component.objects.using(db_alias)
        .filter(vcs__in=SUPPORTED_VCS)
        .exclude(repo__startswith="weblate:/")
    )
    for component in matching:
        new_url = get_export_url(component)
        if component.git_export != new_url:
            component.git_export = new_url
            component.save()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("trans", "0001_squashed_0074_fix_broken_browser_alert"),
    ]

    operations = [
        migrations.RunPython(code=set_export_url, reverse_code=set_export_url)
    ]
