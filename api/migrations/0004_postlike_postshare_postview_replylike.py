# Generated manually for like, share, view tracking models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_newslettersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('link', 'Copy Link'), ('whatsapp', 'WhatsApp'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('email', 'Email')], max_length=20)),
                ('shared_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='api.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_shares', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-shared_at'],
            },
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='api.communitypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_views', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
            },
        ),
        migrations.CreateModel(
            name='ReplyLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='api.communityreply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='postlike',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_post_like'),
        ),
        migrations.AddConstraint(
            model_name='postview',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_post_view'),
        ),
        migrations.AddConstraint(
            model_name='replylike',
            constraint=models.UniqueConstraint(fields=('user', 'reply'), name='unique_reply_like'),
        ),
    ]