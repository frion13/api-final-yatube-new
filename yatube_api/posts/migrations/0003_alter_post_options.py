from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_group_follow_post_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-pub_date',)},
        ),
    ]
