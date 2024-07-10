from django.core.management.base import BaseCommand, CommandError
from django.dispatch import receiver
from main.mine_genesis import BlockCreator
from main.models import Block, LillyUser, Transaction
from django.conf import settings
import hashlib
import json
import rsa

class Command(BaseCommand):
    help = 'Initialize the first block in the blockchain'

    def handle(self, *args, **kwargs):
        if Block.objects.exists():
            self.stdout.write(self.style.WARNING('Blockchain already initialized. Aborting command.'))
            return
        
        admin_username = 'admin'
        admin_password = '*'*10 
        
        if LillyUser.objects.filter(username=admin_username).exists():
            self.stdout.write(self.style.WARNING('Admin user already exists. Aborting command.'))
            return
        
        try:
            admin_user = LillyUser.objects.create_user(username=admin_username, password=admin_password)
            admin_user.is_staff = True  
            admin_user.is_superuser = True 
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin_username}" created successfully.'))
        
        except Exception as e:
            raise CommandError(f'Error creating admin user: {str(e)}')

        try:
            from django.contrib.auth.models import AnonymousUser
            tranaction = Transaction(
                sender = AnonymousUser(), 
                receiver = admin_user, 
                amount = 10000
            )
            tranaction.save()
            first_block = BlockCreator()
            first_block.save()
            self.stdout.write(self.style.SUCCESS('First block initialized successfully.'))
        
        except Exception as e:
            raise CommandError(f'Error initializing first block: {str(e)}')
