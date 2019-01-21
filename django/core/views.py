from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.apis import get_client, get_accounts, get_account_movements, id_card_exists
from django.views.generic import FormView
from core.forms import TransactionForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.contrib.auth.decorators import login_required

from django.utils import timezone

#PARA GENERAR LOS REPORTES PDF

class GeneratePdfHistorial(View):

    def get(self, request, *args, **kwargs):
        ctx = {}
        User = request.user
        nombre_usuario = User.first_name
        apellidos_usuario = User.last_name
        cedula = User.profile.id_card
        fecha = (timezone.now)
        cedula1 = id_card_exists(cedula)
        id_core = cedula1['mensaje']
        accounts = get_accounts(id_core)
        ctx['accounts'] = {}
        totalmovs = 0
        for account in accounts:
            # print(account)
            account_mov = get_account_movements(account['NumeroCuenta'])
            ctx['accounts'].update({account['NumeroCuenta']: account_mov})
            totalmovs = totalmovs + 1
            ctx['totalmovs'] = totalmovs
            ctx['Fecha'] = fecha
            ctx['nombre'] = nombre_usuario
            ctx['apellido'] = apellidos_usuario
            print(ctx['accounts'])
        #haremos todos los request para conseguir las cuentas del cliente denuevo x
        pdf = render_to_pdf('core/pdf_historial.html', ctx)
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
        User = request.user
        nombre_usuario = User.first_name
        apellidos_usuario = User.last_name
        cedula = User.profile.id_card
        fecha = (timezone.now)
        cedula1 = id_card_exists(cedula)
        id_core = cedula1['mensaje']
        accounts = get_accounts(id_core)
        total_balance = 0
        for cuenta in accounts:
            total_balance = total_balance + cuenta['Saldo']
        ctx = {
            'accounts': accounts,
            'total_balances': total_balance,
            'Fecha': fecha,
            'nombre': nombre_usuario,
            'apellido': apellidos_usuario,
        }
        #haremos todos los request para conseguir las cuentas del cliente denuevo x
        pdf = render_to_pdf('core/pdf_consultas.html', ctx)
        return HttpResponse(pdf, content_type='application/pdf')


class CheckAccounts(LoginRequiredMixin, TemplateView):
    template_name = 'core/accounts.html'

    def get_context_data(self):
        ctx = super(CheckAccounts, self).get_context_data()
        core_id = self.request.user.profile.core_id
        ctx['client'] = get_client(self.request.user.profile.core_id)
        accounts = get_accounts(core_id)
        ctx['accounts'] = accounts
        total_balance = 0
        for cuenta in accounts:
            total_balance = total_balance + cuenta['Saldo']
        ctx['total_balances'] = total_balance
        return ctx

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

    def get_form(self):
        if self.request.method == "POST":
            user_data = {'user': self.request.user}
            return TransactionForm(self.request.POST, user_data)
        return TransactionForm

    def form_valid(self, form):
        message = "Transferencia realizada con exito"
        ctx = self.get_context_data()
        ctx['message'] = message
        return render(self.request, self.template_name, context=ctx)
