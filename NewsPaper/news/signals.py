from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import email_after_create_new

    
@receiver(m2m_changed, sender = PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        category = instance.category.all()
        subscribes_emails = []
        
        for cat in category:
            subscribes = cat.subscribers.all()
            subscribes_emails += [s.email for s in subscribes]
    
        email_after_create_new.delay(instance.preview(), instance.pk, instance.name, subscribes_emails)
            
            
        
            
      