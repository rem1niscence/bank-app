from django import forms
from core.apis import make_transaction


class TransactionForm(forms.Form):
    issuer = forms.IntegerField()
    receiver = forms.IntegerField()
    amount = forms.FloatField()

    def is_valid(self):
        valid = super(TransactionForm, self).is_valid()
        if not valid:
            return valid

        transaction_data = {
            'issuer': self.cleaned_data['issuer'],
            'receiver': self.cleaned_data['receiver'],
            'amount': self.cleaned_data['amount'],
        }

        transaction = make_transaction(transaction_data)
        if transaction['exito']:
            return valid
        else:
            if transaction['codigo'] == -1:
                self.add_error('issuer', transaction['mensaje'])
            if transaction['codigo'] == -2:
                self.add_error('receiver', transaction['mensaje'])
            if transaction['codigo'] == -3:
                self.add_error('amount', transaction['mensaje'])
            return False
