from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

#TODO: Move to commons
BOOK_CATEGORY_CHOICES = (('F', 'Fiction'), ('S', 'Science'), ('A', 'AI & Code'), 
						('P', 'Philosophy'), ('B', 'Biography'))
class Book(models.Model):
	title = models.CharField(max_length=50)
	author = models.CharField(max_length=50)
	category = models.CharField(choices=BOOK_CATEGORY_CHOICES, max_length=1)
	slug = models.SlugField(blank=True, null=True)
	image = models.ImageField(upload_to='books/', blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	def __str__(self):
		return self.title

	def get_absoulte_url(self):
		# TODO: Look up django revese
		return reverse('books:book', kwargs={
			'slug': self.slug
	})

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Book, self).save(*args, **kwargs)

BOOK_CONDITION_CHOICES = (('O', 'Old'), ('G', 'Good'), ('N', 'Almost New'))
class BookAD(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	price = models.FloatField()
	amazon_price = models.FloatField()
	condition = models.CharField(choices=BOOK_CONDITION_CHOICES, max_length=1)
	sold = models.BooleanField(default=False)
	slug = models.SlugField(blank=True, null=True)
	ad_image = models.ImageField(upload_to='ads/', blank=True, null=True)
	votes = models.FloatField(default=0, blank=True, null=True)

	def __str__(self):
		return self.book.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.book.title + self.user.username)
		super(BookAD, self).save(*args, **kwargs)


# class BookPurchased(models.Model):

# class BookSold(models.Model):
	
class BookOrder(models.Model):
	buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	book_ad = models.ForeignKey(BookAD, on_delete=models.CASCADE)
	ordered = models.BooleanField(default=False)
	start_date = models.DateTimeField(auto_now_add = True)
	review = models.CharField(max_length=512, blank=True, null=True)

	def __str__(self):
		return self.book_ad.book.title

	def get_price(self):
		return self.book_ad.price * self.quantity

class BookRate(models.Model): 
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	rating = models.FloatField()
	rate_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.book.title


class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to='avatars/', blank=True, null=True)
	phone_num = models.FloatField(blank=True, null=True)
	
	def __str__(self):
		return str(self.user)

def create_profile(sender, instance, created, **kwargs):
	if created: 
		UserProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
def update_profile(sender, instance, created, **kwargs):
	if not created: 
		instance.profile.save()


class Blog(models.Model):
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	rating = models.FloatField()
	title = models.CharField(max_length=50)
	content = models.TextField()

	def __str__(self):
		return self.title

class BlogComment(models.Model):
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	comment = models.TextField()

class ImageBoi(models.Model):
	image = models.ImageField(upload_to='imageboi/', blank=True, null=True)