import datetime
import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
 
 
logger = logging.getLogger(__name__)
 
 
def my_job():
    today = datetime.datetime.now()
    # last_week = today - datetime.timedelta(days = 7)
    # posts = Post.objects.filter(datetime_in__gte = last_week).distinct()
    # categories = set(posts.values_list('category__name', flat = True))
    # subscribers = set(Category.objects.filter(name__in = categories).values_list('subscribers__email', flat = True))
    # html_content = render_to_string(
    #    'week_posts.html',
    #    {
    #        'link': settings.SITE_URL,
    #        'posts': posts,    
    #    } 
    # )
    
    # msg = EmailMultiAlternatives(
    #     subject = 'Все статьи за неделю',
    #     body = '',
    #     from_email = settings.DEFAULT_FROM_EMAIL,
    #     to = subscribers,
    
    # )
    
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()
 
# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="sun", hour="22", minute="01"), 
            id="my_job", 
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")