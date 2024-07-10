from django.contrib import admin
from main.models import Block, MintUser, Transaction
from django.contrib.auth.admin import UserAdmin

from .forms import MintUserCreationForm, MintUserChangeForm

@admin.register(MintUser)
class MintUserAdmin(UserAdmin):
    add_form = MintUserCreationForm
    form = MintUserChangeForm
    model = MintUser
    list_display = ['username','address', 'amount']
    fieldsets = UserAdmin.fieldsets + (
            ("Mint Coins", {
                'fields': ('private_key', 'public_key', 'amount')
                    }),
                ) 


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('sender','reciever', 'amount')



@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("hash", "miner", "timestamp")


