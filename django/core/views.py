from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.apis import get_client, get_accounts, get_account_movements
from django.views.generic import FormView
from core.forms import TransactionForm
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self):
        ctx = super(HomeView, self).get_context_data()
        if self.request.user.is_authenticated:
            client_data = get_client(self.request.user.profile.core_id)
            ctx['client'] = client_data
        return ctx


class MovementHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'core/mov_history.html'

    def get_context_data(self):
        ctx = super(MovementHistoryView, self).get_context_data()
        core_id = self.request.user.profile.core_id
        client_data = get_client(core_id)
        ctx['client'] = client_data

        accounts_data = get_accounts(core_id)
        accounts_id = [account['NumeroCuenta']
                       for account in accounts_data
                       if 'NumeroCuenta' in account]

        ctx['accounts'] = {}
        for account in accounts_id:
            account_mov = get_account_movements(account)
            ctx['accounts'].update({account: account_mov})
        return ctx


class TransactionView(LoginRequiredMixin, FormView):
    form_class = TransactionForm
    template_name = 'core/transactions.html'

    def form_valid(self, form):
        message = "Transferencia realizada con exito"
        ctx = self.get_context_data()
        ctx['message'] = message
        return render(self.request, self.template_name, context=ctx)


class CheckAccounts(LoginRequiredMixin, TemplateView):
    template_name = 'core/accounts.html'

    def get_context_data(self):
        ctx = super(CheckAccounts, self).get_context_data()
        core_id = self.request.user.profile.core_id
        ctx['client'] = get_client(self.request.user.profile.core_id)
        ctx['accounts'] = get_accounts(core_id)

        return ctx
