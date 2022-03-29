from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Create(models.Model):
    TITLE = models.CharField(max_length=100)
    DESCRIPTION =  models.CharField(max_length=1000)
    CATEGORY =  models.CharField( max_length=50)
    BID =  models.IntegerField()
    IMAGE =  models.ImageField(upload_to='images',height_field=None,width_field=None,max_length=100,blank=True,null=True)
    TIME = models.CharField( max_length=20)
    OWNER = models.CharField(max_length =20,null=True)
    BIDGATE = models.CharField(max_length =10,null=True)
    def __str__(self):
        return f"{self.TITLE}" 


class Comment(models.Model):
    COMMENT = models.CharField(max_length=50)
    USER = models.CharField(max_length=20,null=True)
    ITEM = models.IntegerField(null=True)

class BIDDING(models.Model):
    BIDS = models.IntegerField(null=True)
    NAME =  models.CharField(max_length =20)
    ITEM = models.IntegerField(null=True)

class CATEGORY(models.Model):
    CARTEGORYNAME =  models.CharField(max_length = 50)
    def __str__(self):
        return f"{self.CARTEGORYNAME}" 


class mywatchlist(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, related_name="userwatchlists")
    auctionitem = models.ManyToManyField("Create", related_name="auctionitem_userwatchlists",null=True,blank=True)

    def __str__(self):
        return f"{self.user}" 

