# -*- coding: utf-8 -*-

from flask import current_app
from iota import Iota, Transaction
from werkzeug.security import generate_password_hash, check_password_hash
from iota.crypto.addresses import AddressGenerator
from .extensions import db
from utils.iota import address_balance, address_checksum, make_transfer
from utils.hash import get_checksum, verify_checksum
from datetime import datetime


class IOTAAddress(db.Document):
    """
    IOTA Address model
    """
    created_at = db.DateTimeField(default=datetime.now(), required=True)
    index = db.IntField(required=True)
    address = db.StringField(required=True)
    balance = db.IntField(required=True, default=0)
    checksum = db.StringField(required=True)

    def update_balance(self):
        """
        Update address balance
        """
        self.balance = address_balance(current_app.config['IOTA_HOST'], self.address)
        self.save()


class IOTAAccount(db.Document):
    """
    IOTA Account model
    """
    meta = {
        'abstract': True,
    }
    created_at = db.DateTimeField(default=datetime.now(), required=True)
    seed = db.StringField(required=True, default='')
    addresses = db.ListField(db.ReferenceField(IOTAAddress))
    f_index = db.IntField(required=True, default=0)
    l_index = db.IntField(required=True, default=0)

    @property
    def balance(self):
        """
        Return account balance
        """
        t = 0
        for a in self.addresses:
            a.update_balance()
            t += a.balance

        return t

    def _save_fal_balance(self, f_index=0, l_index=0):
        """
        Update f_index and l_index

        :param f_index:
        :param l_index:
        :return:
        """
        if f_index > 0 and l_index > 0:
            self.f_index = f_index
            self.l_index = l_index

        elif f_index > 0:
            self.f_index = f_index
        elif l_index > 0:
            self.l_index = l_index

    def _update_fal_balance(self):
        """
        Update fal balance

        :return:
        """
        index_with_value = []
        for a in self.addresses:
            if a.balance > 0:
                index_with_value.append(a.index)

        if len(index_with_value) > 0:
            f_index = min(index_with_value)
            l_index = max(index_with_value)
            self._save_fal_balance(f_index, l_index)

    def _generate_addresses(self, count):
        """
        Generate addresses for user

        :param count:
        """
        index_list = [-1]
        for i in range(0, len(self.addresses)):
            index_list.append(self.addresses[i].index)

        if max(index_list) == -1:
            start_index = 0
        else:
            start_index = max(index_list) + 1

        generator = AddressGenerator(self.seed)
        generated = generator.get_addresses(start_index, count)
        i = 0

        while i < count:
            index = start_index + i
            address = address_checksum(str(generated[i]))
            balance = address_balance(current_app.config['IOTA_HOST'], address)
            addr = IOTAAddress(
                index=index,
                address=str(address),
                balance=balance,
                checksum=str(get_checksum(address, self.seed))
            )
            addr.save()
            self.addresses.append(addr)
            i += 1
        self.save()

    @property
    def deposit_address(self):
        """
        Return deposit address of account
        :return:
        """
        if self.l_index == 0:
            if len(self.addresses) > 0:
                return self.addresses[0]

            for a in self.addresses:
                integrity = verify_checksum(a.checksum, a.address, self.seed)
                if a.index > self.l_index and integrity:
                    return a
                elif not integrity:
                    raise Exception('Integrity error')

            self._generate_addresses(1)
            for a in self.addresses:
                integrity = verify_checksum(a.checksum, a.address, self.seed)
                if a.index > self.l_index and integrity:
                    return a

    def get_transfers(self):
        """
        Get transactions

        :return:
        """
        api = Iota(current_app.config['IOTA_HOST'], self.seed)
        result = []

        for a in self.addresses:
            t = api.find_transactions(addresses=[a.address])
            for th in t['hashes']:
                gt = api.get_trytes([th])
                txn = Transaction.from_tryte_string(gt['trytes'][0])
                result.append(txn)

        return result


class Campus(IOTAAccount):
    """
    Campus model
    """
    name = db.StringField(required=True, unique=True)


class Section(db.Document):
    """
    Section model
    """
    created_at = db.DateTimeField(default=datetime.now())
    campus = db.ReferenceField(Campus, required=True)
    year = db.IntField(required=True)
    name = db.StringField(required=True)


class Project(db.Document):
    """
    Project model
    """
    created_at = db.DateTimeField(default=datetime.now())
    campus = db.ReferenceField(Campus, required=True)
    name = db.StringField(required=True)


class User(db.Document):
    """
    User model
    """
    meta = {'allow_inheritance': True}

    created_at = db.DateTimeField(default=datetime.now())
    type = db.StringField(default='user')
    img_uri = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    username = db.StringField(required=True, unique=True)
    secret_hash = db.StringField()
    scopes = db.ListField(db.StringField())

    @property
    def secret(self):
        return self.secret_hash

    @secret.setter
    def secret(self, pwd):
        self.secret_hash = generate_password_hash(pwd)

    def check_secret(self, pwd):
        if not self.secret_hash:
            return False
        return check_password_hash(self.secret_hash, pwd)


class Facilitator(User, IOTAAccount):
    """
    Facilitator model
    """


class Student(User):
    """
    Student model
    """
    campus = db.ReferenceField(Campus, required=True)
    section = db.ReferenceField(Section, required=True)


class Group(IOTAAccount):
    """
    Group model
    """
    project = db.ReferenceField(Project, required=True)
    name = db.StringField(required=True)
    students = db.ListField(db.ReferenceField(Student))
    reserved = db.IntField(required=True, default=0)

    def delete(self):
        b = self.balance
        if b > 0:
            make_transfer(current_app.config['IOTA_HOST'], {
                'recipient_address': self.campus.deposit_address.address,
                'message': 'From EPSI',
                'tag': 'WITHDRAWGROUP',
                'value': b,
                'seed': self.seed,
                'deposit_address': self.deposit_address.address
            })

        super().delete()


class Offer(db.Document):
    """
    Offer model
    """
    created_at = db.DateTimeField(default=datetime.now())
    facilitator = db.ReferenceField(Facilitator)
    name = db.StringField(required=True, unique=True)
    tags = db.ListField(db.StringField())
    price = db.IntField(required=True, default=0)
    description = db.StringField()


class Claim(db.Document):
    """
    Claim model
    """
    created_at = db.DateTimeField(default=datetime.now())
    offer = db.ReferenceField(Offer, required=True)
    group = db.ReferenceField(Group)
    status = db.StringField(required=True)
