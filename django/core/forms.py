from django import forms
from core.apis import make_transaction, get_accounts


class TransactionForm(forms.Form):
    issuer = forms.IntegerField()
    receiver = forms.IntegerField()
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.user_core_id = args[len(args)-1]['user'].profile.core_id
        super(TransactionForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(TransactionForm, self).is_valid()
        if not valid:
            return valid

        issuer = self.cleaned_data['issuer']
        transaction_data = {
            'issuer': issuer,
            'receiver': self.cleaned_data['receiver'],
            'amount': self.cleaned_data['amount'],
        }

        # Check if issuer account belongs to user
        accounts_data = get_accounts(self.user_core_id)
        accounts_id = [account['NumeroCuenta']
                       for account in accounts_data
                       if 'NumeroCuenta' in account]

        if(issuer not in accounts_id):
            self.add_error('issuer', 'Cuenta no le pertenece')
            return False

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