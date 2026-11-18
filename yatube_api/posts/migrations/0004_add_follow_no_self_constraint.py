from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='no_self_follow',
            ),
        ),
    ]
