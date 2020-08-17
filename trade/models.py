from django.db import models
from user.models import User

CRITERIA_CHOICES_CATEGORY = (
    (0, 'Clothes'),
    (1, 'Technology'),
    (2, 'Cars'),
    (3, 'Games'),
    (4, 'Software'),
    (5, 'Food'),
    (6, 'Service'),
)


class Item(models.Model):
    user = models.ForeignKey(User, related_name='item', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    category = models.IntegerField(verbose_name='Category',
                                   choices=CRITERIA_CHOICES_CATEGORY,
                                   blank=True,
                                   null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']

    def get_category(self):
        return CRITERIA_CHOICES_CATEGORY[self.category][1]
    

    def __str__(self):
        return ('%s owned by %s' % (self.name, self.user.get_full_name())).strip()


class Request(models.Model):
    user = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    requested_item = models.ForeignKey(Item, related_name='item_request', on_delete=models.CASCADE)
    offered_item = models.ForeignKey(Item, related_name='item_offer', on_delete=models.CASCADE)
    note = models.TextField(null=True)
    status = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('%s request item %s' % (self.user.get_full_name(), self.requested_item.name)).strip()

    class Meta:
        ordering = ['-create_at']


class Review(models.Model):
    user = models.ForeignKey(User, related_name='review', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='review', on_delete=models.CASCADE)
    review = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_at']


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notified', on_delete=models.CASCADE)
    user_req = models.ForeignKey(User, related_name='notifier', on_delete=models.CASCADE)
    request = models.ForeignKey(Request, related_name='request', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ('%s Notified %s' % (self.user_req.get_full_name(), self.user.get_full_name())).strip()

    class Meta:
        ordering = ['-create_at']

