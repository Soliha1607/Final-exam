from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductRating, Product, ProductComment
from django.db.models import Avg


@receiver(post_save, sender=ProductRating)
@receiver(post_delete, sender=ProductRating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.product
    avg_rating = ProductRating.objects.filter(product=product).aggregate(avg=Avg('rating'))['avg'] or 0
    product.average_rating = round(avg_rating, 1)
    product.save()


@receiver(post_save, sender=ProductComment)
def notify_about_new_comment(sender, instance, created, **kwargs):
    if created:
        print(f"Yangi komment: {instance.product.name} uchun '{instance.comment}'")


@receiver(post_save, sender=Product)
def product_saved_log(sender, instance, created, **kwargs):
    if created:
        print(f"Yangi mahsulot yaratildi: {instance.name}")
    else:
        print(f"Mahsulot yangilandi: {instance.name}")
