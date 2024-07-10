from django.http import  HttpRequest, JsonResponse
from django.urls import reverse
from main.api import get_blockchain_data, serialize_blockchain
from main.firebase import sync_blockchain_to_firebase
from main.mine import MineBlock
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from main.forms import MintUserCreationForm
from django.contrib.auth import login
from django.db.models import Sum
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from main.mine_genesis import BlockCreator, ValidateBlock, block_json
from main.models import Block, Transaction, MintUser
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = "main/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("account"))
        return super().get(request, *args, **kwargs)


@login_required
def transaction(request:HttpRequest, recv_address:str):
    context = dict()
    if request.method == "POST":
        reciever_address = request.POST.get("address")
        amount = int(request.POST.get("amount"))
        sender_obj = request.user
        if MintUser.objects.filter(address = reciever_address).exists():
            reciever_obj = MintUser.objects.get(address = reciever_address)
            if reciever_obj == sender_obj:
                messages.error(request, "sender is same as reciever")
            elif sender_obj.amount < amount:
                messages.error(request, "Low Balance!")
            else:
                Transaction.objects.create(
                    sender = sender_obj,
                    reciever = reciever_obj,
                    amount = amount
                )
                messages.success(request, "Transactions successfull")
        else:
            messages.error(request, "User does not exist")
    context["transactions"] = Transaction.objects.filter(sender = request.user)

    context["recv_address"] = recv_address if recv_address != "default" else None
    return render(request, "main/menu/transaction.html", context)

@login_required
def account(request:HttpRequest):
    context = {
        "user_transaction_url": request.build_absolute_uri("transaction/"+request.user.address),
        "pending_coins":Transaction.objects.filter(confirmed = False, reciever = request.user).aggregate(Sum("amount")).get("amount__sum")
    }
    return render(request, "main/menu/account.html", context)

@login_required
def add_block(request:HttpRequest):
    if request.method == "POST":
        block_hash = request.POST.get("block_hash")
        nonce = int(request.POST.get("nonce"))
        transaction_hashes = request.POST.getlist("transaction_hash")
        if ValidateBlock(request, transaction_hashes, block_hash, nonce).validate():
            BlockCreator(request, block_hash, nonce, transaction_hashes).create_block()
            return redirect(reverse("blockchain"))
        else:
            return redirect(reverse("mining"))

@login_required
def mining(request:HttpRequest):
    if Transaction.objects.count() == 0:
        main_user = MintUser.objects.get(username = "admin")
        Transaction.objects.create(sender = main_user, reciever= request.user, amount=0)
    context = dict()
    if request.method == "POST":
        transaction_hashes = request.POST.getlist("transactions")
        if transaction_hashes:    
            json_data = block_json(request, transaction_hashes)
            context["transaction_hashes"] = transaction_hashes
            context["json_data"] = json_data
            block_hash, nonce = MineBlock(json_data).get_block_hash()
            context["block_hash"] = block_hash
            context["nonce"] = nonce
            context["block_json_data"] = {
                "nonce":nonce,
                "block_hash":block_hash
            }
    context["block_reward"] = settings.MINING_REWARD
    context["transactions"] = Transaction.objects.filter(confirmed = False)
    return render(request, "main/menu/mining.html", context)

def blockchain(request:HttpRequest):
    if Block.objects.count() == 0:
        return redirect(reverse("mining"))
    context = {
        "block_list":Block.objects.all()
    }
    return render(request, "main/menu/blockchain.html", context)

def blockview(request:HttpRequest, block_hash):
    context = {
        "Block": Block.objects.get(hash = block_hash)
    }
    return render(request, "main/menu/block.html", context)


class RegisterView(FormView):
    template_name = "registration/signup.html"
    form_class = MintUserCreationForm
    success_url = reverse_lazy("account")

    def form_valid(self, form:MintUserCreationForm):
        user = form.save(commit=False)
        user.amount = 0
        user.save()
        login(self.request, user)
        return super().form_valid(form)
    
# JSON RESPONSE FUNCTIONS

def get_blockchain(request):
    return JsonResponse(sync_blockchain_to_firebase(), safe=False)