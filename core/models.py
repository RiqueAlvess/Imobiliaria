import uuid
from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _


class Proprietario(models.Model):
    owner_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_completo = models.CharField(max_length=150, validators=[MinLengthValidator(3)])
    email = models.EmailField(validators=[EmailValidator()])
    telefone = models.CharField(max_length=20, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Proprietário'
        verbose_name_plural = 'Proprietários'
        ordering = ['nome_completo']
    
    def __str__(self):
        return self.nome_completo


class InfraCondominio(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    icone = models.CharField(max_length=50, blank=True, help_text="Classe do ícone Font Awesome")
    
    class Meta:
        verbose_name = 'Infraestrutura do Condomínio'
        verbose_name_plural = 'Infraestruturas do Condomínio'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Imovel(models.Model):
    class TipoImovel(models.TextChoices):
        APARTAMENTO = 'apartamento', 'Apartamento'
        CASA = 'casa', 'Casa'
        SOBRADO = 'sobrado', 'Sobrado'
        KITNET = 'kitnet', 'Kitnet'
        LOFT = 'loft', 'Loft'
        SALA_COMERCIAL = 'sala_comercial', 'Sala Comercial'
        TERRENO = 'terreno', 'Terreno'
        CHACARA = 'chacara', 'Chácara'
        GALPAO = 'galpao', 'Galpão'
    
    class StatusImovel(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        VENDIDO = 'vendido', 'Vendido'
        ALUGADO = 'alugado', 'Alugado'
        RESERVADO = 'reservado', 'Reservado'
        INATIVO = 'inativo', 'Inativo'
    
    class Mobilia(models.TextChoices):
        MOBILIADO = 'mobiliado', 'Mobiliado'
        SEMIMOBILIADO = 'semimobiliado', 'Semimobiliado'
        VAZIO = 'vazio', 'Vazio'
    
    # Identificação
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE, related_name='imoveis')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TipoImovel.choices)
    status = models.CharField(max_length=20, choices=StatusImovel.choices, default=StatusImovel.ATIVO)
    
    # Localização
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='SP')
    cep = models.CharField(max_length=9)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Características físicas
    area_util = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    area_total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    quartos = models.PositiveIntegerField(default=0)
    suites = models.PositiveIntegerField(default=0)
    banheiros = models.PositiveIntegerField(default=0)
    vagas_garagem = models.PositiveIntegerField(default=0)
    andar = models.CharField(max_length=10, blank=True)
    ano_construcao = models.PositiveIntegerField(null=True, blank=True)
    
    # Características extras
    mobilia = models.CharField(max_length=20, choices=Mobilia.choices, default=Mobilia.VAZIO)
    pet_friendly = models.BooleanField(default=False)
    aceita_financiamento = models.BooleanField(default=True)
    
    # Valores
    valor_condominio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_iptu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Infraestrutura
    infraestrutura = models.ManyToManyField(InfraCondominio, blank=True)
    
    # Controle
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status', 'tipo']),
            models.Index(fields=['cidade', 'bairro']),
            models.Index(fields=['quartos', 'banheiros']),
            models.Index(fields=['criado_em']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.bairro}, {self.cidade}"
    
    @property
    def tem_fotos(self):
        return self.fotos.exists()
    
    @property
    def foto_capa(self):
        return self.fotos.filter(eh_capa=True).first() or self.fotos.first()
    
    @property
    def recem_publicado(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.criado_em >= timezone.now() - timedelta(days=7)


class PrecoPorFinalidade(models.Model):
    class Finalidade(models.TextChoices):
        VENDA = 'venda', 'Venda'
        ALUGUEL = 'aluguel', 'Aluguel'
        TEMPORADA = 'temporada', 'Temporada'
    
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='precos')
    finalidade = models.CharField(max_length=20, choices=Finalidade.choices)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Campos específicos para temporada
    diaria_minima = models.PositiveIntegerField(null=True, blank=True, help_text="Mínimo de diárias")
    taxa_limpeza = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capacidade_hospedes = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Preço por Finalidade'
        verbose_name_plural = 'Preços por Finalidade'
        unique_together = ['imovel', 'finalidade']
        indexes = [
            models.Index(fields=['finalidade', 'valor']),
        ]
    
    def __str__(self):
        if self.finalidade == self.Finalidade.TEMPORADA:
            return f"{self.imovel} - {self.get_finalidade_display()}: R$ {self.valor}/dia"
        return f"{self.imovel} - {self.get_finalidade_display()}: R$ {self.valor}"


class FotoImovel(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='fotos')
    imagem = models.ImageField(upload_to='imoveis/')
    legenda = models.CharField(max_length=200, blank=True)
    eh_capa = models.BooleanField(default=False)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Foto do Imóvel'
        verbose_name_plural = 'Fotos do Imóvel'
        ordering = ['ordem', 'criado_em']
        indexes = [
            models.Index(fields=['imovel', 'ordem']),
        ]
    
    def __str__(self):
        return f"Foto {self.ordem} - {self.imovel}"
    
    def save(self, *args, **kwargs):
        # Garantir que apenas uma foto seja capa por imóvel
        if self.eh_capa:
            FotoImovel.objects.filter(imovel=self.imovel).update(eh_capa=False)
        super().save(*args, **kwargs)