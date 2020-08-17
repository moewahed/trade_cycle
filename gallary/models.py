from django.db import models
from django.core.validators import FileExtensionValidator

from user.model_addon import UploadToPathAndRename
from user.models import User

from blog.models import Blog, Comment
from trade.models import Item, Review

class Image(models.Model):
    user = models.ForeignKey(User, related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(
        verbose_name='Image',
        upload_to=UploadToPathAndRename('upload/img/gallery'),
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg', 'PNG', 'JPG']),
        ],
        help_text='Limits:<ul><li>Size 4MB</li><li>Dimensions Range: Width & height (400-2600)</li></ul>',
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class BlogImage(Image):
    blog = models.ForeignKey(Blog, related_name='blog_image', on_delete=models.CASCADE)


class CommentImage(Image):
    comment = models.ForeignKey(Comment, related_name='comment_image', on_delete=models.CASCADE)


class ItemImage(Image):
    item = models.ForeignKey(Item, related_name='item_image', on_delete=models.CASCADE)


class ReviewImage(Image):
    review = models.ForeignKey(Review, related_name='review_image', on_delete=models.CASCADE)
