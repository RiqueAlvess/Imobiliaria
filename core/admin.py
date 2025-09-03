from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from django.utils import timezone
from .models import Proprietario, Imovel, Cliente, PrecoPorFinalidade, FotoImovel, InfraCondominio


@admin.register(Proprietario)
class ProprietarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'telefone', 'total_imoveis', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['nome_completo', 'email', 'telefone']
    readonly_fields = ['owner_id', 'criado_em']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'email', 'telefone')
        }),
        ('Controle do Sistema', {
            'fields': ('owner_id', 'criado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def total_imoveis(self, obj):
        count = obj.imoveis.count()
        if count > 0:
            return format_html(
                '<span style="color: #C8A866; font-weight: bold;">{}</span>',
                count
            )
        return format_html('<span style="color: #7A7A7A;">0</span>')
    total_imoveis.short_description = 'Total de Imóveis'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome_completo', 'telefone', 'status_badge', 'origem_badge', 
        'finalidade_interesse', 'orcamento_formatado', 'total_imoveis_interesse', 
        'ultimo_contato_formatado', 'criado_em'
    ]
    list_filter = [
        'status', 'origem', 'finalidade_interesse', 'criado_em', 
        'ultimo_contato'
    ]
    search_fields = ['nome_completo', 'email', 'telefone']
    readonly_fields = ['criado_em', 'atualizado_em', 'total_imoveis_interesse']
    filter_horizontal = ['imoveis_interesse']
    date_hierarchy = 'criado_em'
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'email', 'telefone')
        }),
        ('Gestão Comercial', {
            'fields': ('status', 'origem', 'ultimo_contato'),
            'classes': ('wide',)
        }),
        ('Preferências do Cliente', {
            'fields': ('finalidade_interesse', 'orcamento_max', 'observacoes'),
            'classes': ('wide',)
        }),
        ('Imóveis de Interesse', {
            'fields': ('imoveis_interesse',),
            'classes': ('wide',)
        }),
        ('Controle do Sistema', {
            'fields': ('total_imoveis_interesse', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 80})},
    }
    
    def status_badge(self, obj):
        colors = {
            'lead_frio': '#7A7A7A',
            'lead_morno': '#C8A866', 
            'lead_quente': '#D4AF37',
            'cliente_ativo': '#1E3A5F',
            'cliente_perdido': '#dc3545',
            'cliente_finalizado': '#28a745'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#7A7A7A'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def origem_badge(self, obj):
        icons = {
            'site': 'fas fa-globe',
            'whatsapp': 'fas fa-phone', 
            'telefone': 'fas fa-phone',
            'email': 'fas fa-envelope',
            'indicacao': 'fas fa-user-friends',
            'facebook': 'fas fa-share-alt',
            'instagram': 'fas fa-share-alt',
            'placa': 'fas fa-sign',
            'outro': 'fas fa-question'
        }
        return format_html(
            '<span style="color: #C8A866;"><i class="{} me-1"></i>{}</span>',
            icons.get(obj.origem, 'fas fa-question'),
            obj.get_origem_display()
        )
    origem_badge.short_description = 'Origem'
    
    def orcamento_formatado(self, obj):
        if obj.orcamento_max:
            try:
                # Converter explicitamente para float e formatar
                valor = float(obj.orcamento_max)
                valor_formatado = f"R$ {valor:,.0f}"
                return format_html(
                    '<span style="color: #1E3A5F; font-weight: bold;">{}</span>',
                    valor_formatado
                )
            except (ValueError, TypeError):
                return format_html('<span style="color: #dc3545;">Valor inválido</span>')
        return format_html('<span style="color: #7A7A7A;">-</span>')
    orcamento_formatado.short_description = 'Orçamento'
    
    def ultimo_contato_formatado(self, obj):
        if obj.ultimo_contato:
            dias = (timezone.now().date() - obj.ultimo_contato.date()).days
            if dias == 0:
                return format_html('<span style="color: #28a745;">Hoje</span>')
            elif dias == 1:
                return format_html('<span style="color: #C8A866;">Ontem</span>')
            elif dias <= 7:
                return format_html('<span style="color: #ffc107;">{} dias</span>', dias)
            else:
                return format_html('<span style="color: #dc3545;">{} dias</span>', dias)
        return format_html('<span style="color: #7A7A7A;">Nunca</span>')
    ultimo_contato_formatado.short_description = 'Último Contato'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('imoveis_interesse')
    
    actions = ['marcar_como_lead_quente', 'marcar_como_cliente_ativo', 'atualizar_ultimo_contato']
    
    def marcar_como_lead_quente(self, request, queryset):
        count = queryset.update(status='lead_quente')
        self.message_user(request, f'{count} cliente(s) marcado(s) como Lead Quente.')
    marcar_como_lead_quente.short_description = 'Marcar como Lead Quente'
    
    def marcar_como_cliente_ativo(self, request, queryset):
        count = queryset.update(status='cliente_ativo')
        self.message_user(request, f'{count} cliente(s) marcado(s) como Cliente Ativo.')
    marcar_como_cliente_ativo.short_description = 'Marcar como Cliente Ativo'
    
    def atualizar_ultimo_contato(self, request, queryset):
        count = queryset.update(ultimo_contato=timezone.now())
        self.message_user(request, f'Último contato atualizado para {count} cliente(s).')
    atualizar_ultimo_contato.short_description = 'Atualizar último contato para hoje'


class PrecoPorFinalidadeInline(admin.TabularInline):
    model = PrecoPorFinalidade
    extra = 1
    fields = ['finalidade', 'valor', 'diaria_minima', 'taxa_limpeza', 'capacidade_hospedes']
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['valor'].widget.attrs.update({'style': 'width: 150px;'})
        return formset


class FotoImovelInline(admin.TabularInline):
    model = FotoImovel
    extra = 1
    fields = ['imagem', 'legenda', 'eh_capa', 'ordem', 'preview']
    readonly_fields = ['preview']
    ordering = ['ordem']
    
    def preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px; border: 2px solid #C8A866;" />',
                obj.imagem.url
            )
        return '-'
    preview.short_description = 'Preview'


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = [
        'titulo_resumido', 'proprietario', 'tipo_badge', 'cidade', 'bairro', 
        'status_badge', 'preco_resumo', 'quartos', 'tem_fotos_badge', 'criado_em'
    ]
    list_filter = [
        'status', 'tipo', 'cidade', 'bairro', 'quartos', 'pet_friendly', 
        'aceita_financiamento', 'mobilia', 'criado_em'
    ]
    search_fields = ['titulo', 'endereco', 'bairro', 'cidade', 'proprietario__nome_completo']
    readonly_fields = ['criado_em', 'atualizado_em']
    filter_horizontal = ['infraestrutura']
    inlines = [PrecoPorFinalidadeInline, FotoImovelInline]
    date_hierarchy = 'criado_em'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('proprietario', 'titulo', 'descricao', 'tipo', 'status')
        }),
        ('Localização', {
            'fields': (
                'endereco', 'bairro', 'cidade', 'estado', 'cep',
                ('latitude', 'longitude')
            )
        }),
        ('Características', {
            'fields': (
                ('area_util', 'area_total'),
                ('quartos', 'suites', 'banheiros'),
                ('vagas_garagem', 'andar', 'ano_construcao'),
                ('mobilia', 'pet_friendly', 'aceita_financiamento')
            )
        }),
        ('Valores Adicionais', {
            'fields': ('valor_condominio', 'valor_iptu'),
            'classes': ('collapse',)
        }),
        ('Infraestrutura do Condomínio', {
            'fields': ('infraestrutura',),
            'classes': ('collapse',)
        }),
        ('Controle do Sistema', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
    }
    
    def titulo_resumido(self, obj):
        titulo = obj.titulo[:50] + '...' if len(obj.titulo) > 50 else obj.titulo
        return format_html('<span style="color: #0D0D0D; font-weight: 500;">{}</span>', titulo)
    titulo_resumido.short_description = 'Título'
    
    def tipo_badge(self, obj):
        return format_html(
            '<span style="background-color: #1E3A5F; color: white; padding: 3px 8px; border-radius: 8px; font-size: 0.8rem;">{}</span>',
            obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'
    
    def status_badge(self, obj):
        colors = {
            'ativo': '#28a745',
            'vendido': '#dc3545',
            'alugado': '#ffc107',
            'reservado': '#17a2b8',
            'inativo': '#6c757d'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def preco_resumo(self, obj):
        precos = obj.precos.all()
        if not precos:
            return format_html('<span style="color: #7A7A7A;">-</span>')
        
        resumo = []
        for preco in precos[:2]:  # Mostrar no máximo 2 preços
            try:
                valor = float(preco.valor)
                if preco.finalidade == 'temporada':
                    resumo.append(f"R$ {valor:,.0f}/dia")
                else:
                    resumo.append(f"R$ {valor:,.0f}")
            except (ValueError, TypeError):
                resumo.append("Valor inválido")
        
        result = ' | '.join(resumo)
        if precos.count() > 2:
            result += '...'
        
        return format_html('<span style="color: #C8A866; font-weight: bold;">{}</span>', result)
    preco_resumo.short_description = 'Preços'
    
    def tem_fotos_badge(self, obj):
        if obj.tem_fotos:
            count = obj.fotos.count()
            return format_html(
                '<span style="background-color: #D4AF37; color: #0D0D0D; padding: 3px 8px; border-radius: 8px; font-size: 0.8rem; font-weight: bold;"><i class="fas fa-camera"></i> {}</span>',
                count
            )
        return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 8px; font-size: 0.8rem;">Sem fotos</span>')
    tem_fotos_badge.short_description = 'Fotos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('proprietario').prefetch_related('precos', 'fotos')
    
    actions = ['marcar_como_vendido', 'marcar_como_alugado', 'marcar_como_ativo']
    
    def marcar_como_vendido(self, request, queryset):
        count = queryset.update(status='vendido')
        self.message_user(request, f'{count} imóvel(is) marcado(s) como vendido(s).')
    marcar_como_vendido.short_description = 'Marcar como vendido'
    
    def marcar_como_alugado(self, request, queryset):
        count = queryset.update(status='alugado')
        self.message_user(request, f'{count} imóvel(is) marcado(s) como alugado(s).')
    marcar_como_alugado.short_description = 'Marcar como alugado'
    
    def marcar_como_ativo(self, request, queryset):
        count = queryset.update(status='ativo')
        self.message_user(request, f'{count} imóvel(is) marcado(s) como ativo(s).')
    marcar_como_ativo.short_description = 'Marcar como ativo'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


# Personalização global do Admin
admin.site.site_header = "DS Imóveis - Administração"
admin.site.site_title = "DS Imóveis Admin"
admin.site.index_title = "Painel de Controle"