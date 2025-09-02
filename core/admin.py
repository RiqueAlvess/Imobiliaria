from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import Textarea
from .models import Proprietario, Imovel, PrecoPorFinalidade, FotoImovel, InfraCondominio


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
        return obj.imoveis.count()
    total_imoveis.short_description = 'Total de Imóveis'


@admin.register(InfraCondominio)
class InfraCondominioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone_preview', 'total_imoveis']
    search_fields = ['nome']
    
    def icone_preview(self, obj):
        if obj.icone:
            return format_html('<i class="{}"></i> {}', obj.icone, obj.icone)
        return '-'
    icone_preview.short_description = 'Ícone'
    
    def total_imoveis(self, obj):
        return obj.imovel_set.count()
    total_imoveis.short_description = 'Imóveis com esta infraestrutura'


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
                '<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px;" />',
                obj.imagem.url
            )
        return '-'
    preview.short_description = 'Preview'


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = [
        'titulo_resumido', 'proprietario', 'tipo', 'cidade', 'bairro', 
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
        return obj.titulo[:50] + '...' if len(obj.titulo) > 50 else obj.titulo
    titulo_resumido.short_description = 'Título'
    
    def status_badge(self, obj):
        colors = {
            'ativo': 'success',
            'vendido': 'danger',
            'alugado': 'warning',
            'reservado': 'info',
            'inativo': 'secondary'
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def preco_resumo(self, obj):
        precos = obj.precos.all()
        if not precos:
            return '-'
        
        resumo = []
        for preco in precos[:2]:  # Mostrar no máximo 2 preços
            if preco.finalidade == 'temporada':
                resumo.append(f"R$ {preco.valor}/dia")
            else:
                resumo.append(f"R$ {preco.valor}")
        
        result = ' | '.join(resumo)
        if precos.count() > 2:
            result += '...'
        return result
    preco_resumo.short_description = 'Preços'
    
    def tem_fotos_badge(self, obj):
        if obj.tem_fotos:
            count = obj.fotos.count()
            return format_html(
                '<span class="badge badge-success"><i class="fas fa-camera"></i> {}</span>',
                count
            )
        return format_html('<span class="badge badge-danger">Sem fotos</span>')
    tem_fotos_badge.short_description = 'Fotos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('proprietario').prefetch_related('precos', 'fotos')
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)


@admin.register(PrecoPorFinalidade)
class PrecoPorFinalidadeAdmin(admin.ModelAdmin):
    list_display = ['imovel', 'finalidade', 'valor_formatado', 'detalhes_temporada']
    list_filter = ['finalidade', 'imovel__tipo', 'imovel__cidade']
    search_fields = ['imovel__titulo', 'imovel__endereco']
    
    def valor_formatado(self, obj):
        if obj.finalidade == 'temporada':
            return f"R$ {obj.valor}/dia"
        return f"R$ {obj.valor}"
    valor_formatado.short_description = 'Valor'
    
    def detalhes_temporada(self, obj):
        if obj.finalidade == 'temporada':
            detalhes = []
            if obj.diaria_minima:
                detalhes.append(f"Mín: {obj.diaria_minima} dias")
            if obj.capacidade_hospedes:
                detalhes.append(f"Cap: {obj.capacidade_hospedes} pessoas")
            if obj.taxa_limpeza:
                detalhes.append(f"Limpeza: R$ {obj.taxa_limpeza}")
            return ' | '.join(detalhes)
        return '-'
    detalhes_temporada.short_description = 'Detalhes Temporada'


@admin.register(FotoImovel)
class FotoImovelAdmin(admin.ModelAdmin):
    list_display = ['preview_thumb', 'imovel', 'legenda', 'eh_capa', 'ordem', 'criado_em']
    list_filter = ['eh_capa', 'criado_em', 'imovel__tipo']
    search_fields = ['imovel__titulo', 'legenda']
    list_editable = ['eh_capa', 'ordem']
    ordering = ['imovel', 'ordem']
    
    def preview_thumb(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 60px; border-radius: 4px;" />',
                obj.imagem.url
            )
        return '-'
    preview_thumb.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('imovel')


# Personalizações globais do Admin
admin.site.site_header = "Imobiliária - Administração"
admin.site.site_title = "Imobiliária Admin"
admin.site.index_title = "Painel de Controle"