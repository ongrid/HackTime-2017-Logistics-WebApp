from binascii import Error

from django.http import HttpResponse
from django.shortcuts import render, redirect
from web3 import Web3, HTTPProvider, RPCProvider
from logistapp.forms import ItemForm
from .models import *
import json
import time
from django.views.decorators.csrf import csrf_exempt


class ContractHandler:
    def __init__(self):
        self.web3 = Web3(RPCProvider(host='testnet', port='8545'))
        with open('contract_abi.json', 'r') as abi_definision:
            self.abi = json.load(abi_definision)

        self.account = '0x1d963c56f257c23c0f6fc5abbb9b51bfb0f1cf57'
        self.contract_address = '0x22c0b2b96067023a25d2ff342aeca0dc3f70c3a4'
        self.password = 'password'
        self.contract = self.web3.eth.contract(self.abi, self.contract_address)

    def unlock_account(self):
        self.web3.personal.unlockAccount(self.account, self.password)

    def wait_mined(self, tx_hash):
        tx = self.web3.eth.getTransaction(tx_hash)
        while tx['blockNumber'] is None:
            time.sleep(1)
            tx = self.web3.eth.getTransaction(tx_hash)

        value = self.web3.eth.getTransactionReceipt(tx_hash).logs[0].data
        return Web3.toDecimal(value)

    def trim(self, text):
        return text.rstrip('\x00')

    def get_stock_count(self):
        return self.contract.call().stockCount()

    def add_stock(self, name, address):
        self.unlock_account()
        new_post_index = self.contract.transact({'from': self.account}).add_stock(Web3.toHex(text=name), address)
        return self.wait_mined(new_post_index)

    def get_stock_name(self, index):
        stock_name = self.contract.call().get_stock_name(index)
        try:
            name = Web3.toText(self.trim(stock_name))
        except Error:
            name = stock_name
        if name != '':
            return name
        return False

    def get_stock_address(self, index):
        address = self.contract.call().get_stock_address(index)
        if Web3.isChecksumAddress(address):
            return address
        return False

    def add_item(self, name, address_from, address_to, weight, name_from, name_to):
        stock_from = self.get_stock_name(address_from)
        stock_to = self.get_stock_name(address_to)
        if stock_from and stock_to:
            # print('Всё ок')
            self.unlock_account()
            new_item_id = self.contract.transact({'from': self.account}).add_item(Web3.toHex(text=name),
                                                                                  address_from,
                                                                                  address_to,
                                                                                  Web3.toHex(weight),
                                                                                  Web3.toHex(text=name_from),
                                                                                  Web3.toHex(text=name_to))
            return self.wait_mined(new_item_id)
        return False

    def get_item(self, index):
        item = {}
        item_object = self.contract.call().get_item(index)
        item['name'] = Web3.toText(self.trim(item_object[0]))
        if item['name'] == '':
            return False
        item['address_from'] = item_object[1]
        item['address_to'] = item_object[2]
        item['weight'] = Web3.toText(self.trim(item_object[3]))
        item['name_from'] = Web3.toText(self.trim(item_object[4]))
        item['name_to'] = Web3.toText(self.trim(item_object[5]))
        item['current_stock'] = item_object[6]
        return item

    def get_item_path(self, index):
        path = self.contract.call().get_path(index)
        return path

    def get_item_path_times(self, index):
        path_times = self.contract.call().get_path_times(index)
        return path_times

    def transfer(self, item_id, address_from, address_to):
        stock_from = self.get_stock_name(address_from)
        stock_to = self.get_stock_name(address_to)
        address = self.get_stock_address(address_from)
        path = self.get_item_path(item_id)
        if len(path) > 0 and self.account.lower() == address.lower():
            if stock_from and stock_to and path[-1] == address_from:
                self.unlock_account()
                self.contract.transact({'from': self.account}).transfer(item_id, address_from, address_to)
                return True
        return False

    def get_all_items(self):
        return self.contract.call().get_all_items()


def index(request):
    return render(request, 'logistapp/index.html', {})


@csrf_exempt
def search_item(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('id'))
        args = get_item(int(item_id))
        return render(request, 'logistapp/search.html', args)
    return render(request, 'logistapp/search.html', {})


@csrf_exempt
def search_item_api(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('id'))
        args = get_item(item_id)
        if not args:
            return HttpResponse({}, status=404)
        else:
            return HttpResponse(json.dumps(args), status=200)
    else:
        return HttpResponse('You must use POST', status=404)


def get_item(id):
    cont = ContractHandler()
    args = {'item_pk': id, 'item': cont.get_item(id), 'post_offices': get_stocks()}
    if args['item']:
        path = cont.get_item_path(id)
        times = cont.get_item_path_times(id)
        args['path'] = []
        time_iter = 0
        for i in path:
            name = cont.get_stock_name(i)
            address = cont.get_stock_address(i)
            args['path'].append({'name': name, 'address': address, 'time': times[time_iter]})
            time_iter += 1
    else:
        return False
    return args


@csrf_exempt
def post_office(request):
    args = {}
    if request.method == 'POST':
        stock_id = int(request.POST.get('id'))
        args = get_post_office(stock_id)
        if not args:
            return render(request, 'logistapp/postoffice.html', {'error': 'Post Office #{} not found'.format(stock_id)})
    return render(request, 'logistapp/postoffice.html', args)


@csrf_exempt
def post_office_api(request):
    if request.method == 'POST':
        stock_id = int(request.POST.get('id'))
        args = get_post_office(stock_id)
        if not args:
            return HttpResponse({}, status=404)
        return HttpResponse(json.dumps(args), status=200)
    return HttpResponse('You must use POST', status=404)


def get_post_office(id):
    cont = ContractHandler()
    args = {'name': cont.get_stock_name(id)}
    if not args['name']:
        return False
    args['address'] = cont.get_stock_address(id)
    args['items'] = []
    all_items = cont.get_all_items()
    for item_i in all_items:
        item = cont.get_item(item_i)
        if item['current_stock'] == id:
            item['id'] = item_i
            args['items'].append(item)
    return args


@csrf_exempt
def registration_post_item(request):
    type_r = request.POST.get('type')
    args = {}
    if request.method == "POST":
        name = request.POST.get('name')
        name_from = request.POST.get('sender')
        address_from = int(request.POST.get('post_office_from'))
        name_to = request.POST.get('recipient')
        address_to = int(request.POST.get('post_office_to'))
        weight = request.POST.get('weight')
        if address_from != address_to:
            cont = ContractHandler()
            args['added_item'] = cont.add_item(name, address_from, address_to, weight, name_from, name_to)
        else:
            args['error'] = 'You cant send to similar post office!'
    else:
        args['stock_names'] = get_stocks()
    if type_r == 'api':
        return HttpResponse(json.dumps(args), status=200)
    return render(request, 'logistapp/register_item.html', args)


def get_stocks():
    cont = ContractHandler()
    stocks = []
    count = cont.get_stock_count()
    for i in range(count):
        name = cont.get_stock_name(i)
        if name:
            address = cont.get_stock_address(i)
            stocks.append({'name': name, 'index': i, 'address': address})
    return stocks


@csrf_exempt
def set_arr_dep(request):
    if request.method == 'POST':
        item = int(request.POST.get('item'))
        from_address = int(request.POST.get('from'))
        to_address = int(request.POST.get('to'))
        cont = ContractHandler()
        tr = cont.transfer(item, from_address, to_address)
        if not tr:
            return HttpResponse('Transfer can\'t be accepted', status=200)
        return HttpResponse('Your transfer will be confirmed soon', status=200)
    else:
        return HttpResponse('You must use POST', status=404)
