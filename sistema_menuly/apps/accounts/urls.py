from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # AJAX Views para checkout inteligente
    path('ajax/buscar-cliente/', views.BuscarClienteAjaxView.as_view(), name='buscar_cliente_ajax'),
    path('ajax/salvar-endereco/', views.SalvarEnderecoAjaxView.as_view(), name='salvar_endereco_ajax'),
    path('ajax/marcar-endereco-utilizado/', views.MarcarEnderecoUtilizadoAjaxView.as_view(), name='marcar_endereco_utilizado'),
    path('ajax/formatar-celular/', views.FormatarCelularAjaxView.as_view(), name='formatar_celular_ajax'),
    path('ajax/validar-cep/', views.ValidarCepAjaxView.as_view(), name='validar_cep_ajax'),
    path('ajax/historico-completo/', views.HistoricoCompletoAjaxView.as_view(), name='historico_completo_ajax'),
    path('ajax/criar-cliente-guest/', views.CriarClienteGuestView.as_view(), name='criar_cliente_guest'),
]
