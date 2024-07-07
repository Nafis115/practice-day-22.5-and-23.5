from django.db import models
from .constants import ACCOUNT_TYPE,GENDER_TYPE
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.

class UserBankAccount(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='account')
    account_type=models.CharField(max_length=10,choices=ACCOUNT_TYPE)
    account_no=models.IntegerField(unique=True)
    birth_date=models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=10,choices=GENDER_TYPE)
    initial_deposit_date=models.DateField(auto_now_add=True)
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    
    
    def __str__(self):
        return str(self.account_no)
    
    def transfer_funds(self,receiver_account_no,amount):
        try:
            receiver_account=UserBankAccount.objects.get(account_no=receiver_account_no)
        except UserBankAccount.DoesNotExist:
            raise ValidationError("Recipient account not found.")
        
        if self.balance>=amount:
            self.balance-=amount
            receiver_account.balance+=amount
            self.save()
            receiver_account.save()
            return "Transfer successful."
        else:
            return "Insufficient balance for transfer."
            
        
    

    
class UserAddress(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='address')
    street_address=models.CharField(max_length=120)
    city=models.CharField(max_length=120)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=20)
    
    def __str__(self):
        return (self.user.email)
    
    
    

