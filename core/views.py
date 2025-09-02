from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.http import Http404
from .models import Imovel, InfraCondominio, PrecoPorFinalidade


def home(request):
    """Página inicial com busca rápida e destaques"""
    # Imóveis em destaque (recentes e com fotos)
    imoveis_destaque = Imovel.objects.filter(
        status=Imovel.StatusImovel.ATIVO
    ).prefetch_related('fotos', 'precos').order_by('-criado_em')[:6]
    
    # Cidades disponíveis para o filtro
    cidades = Imovel.objects.filter(
        status=Imovel.StatusImovel.ATIVO
    ).values_list('cidade', flat=True).distinct().order_by('cidade')
    
    # Tipos de imóveis disponíveis
    tipos = Imovel.TipoImovel.choices
    
    context = {
        'imoveis_destaque': imoveis_destaque,
        'cidades': cidades,
        'tipos': tipos,
    }
    return render(request, 'core/home.html', context)


def lista_imoveis(request):
    """Lista de imóveis com filtros"""
    imoveis = Imovel.objects.filter(
        status=Imovel.StatusImovel.ATIVO
    ).select_related('proprietario').prefetch_related(
        'fotos',
        Prefetch('precos', queryset=PrecoPorFinalidade.objects.all()),
        'infraestrutura'
    )
    
    # Função helper para verificar se um valor é válido
    def is_valid_value(value):
        return value and value.strip() and value.strip().lower() not in ['none', '']
    
    # Aplicar filtros
    # Busca por texto
    busca = request.GET.get('busca', '').strip()
    if is_valid_value(busca):
        imoveis = imoveis.filter(
            Q(titulo__icontains=busca) |
            Q(endereco__icontains=busca) |
            Q(bairro__icontains=busca) |
            Q(cidade__icontains=busca) |
            Q(descricao__icontains=busca)
        )
    
    # Finalidade (venda, aluguel, temporada)
    finalidade = request.GET.get('finalidade', '').strip()
    if is_valid_value(finalidade):
        imoveis = imoveis.filter(precos__finalidade=finalidade)
    
    # Tipo de imóvel
    tipo = request.GET.get('tipo', '').strip()
    if is_valid_value(tipo):
        imoveis = imoveis.filter(tipo=tipo)
    
    # Cidade
    cidade = request.GET.get('cidade', '').strip()
    if is_valid_value(cidade):
        imoveis = imoveis.filter(cidade__iexact=cidade)
    
    # Bairro
    bairro = request.GET.get('bairro', '').strip()
    if is_valid_value(bairro):
        imoveis = imoveis.filter(bairro__icontains=bairro)
    
    # Quartos mínimos
    quartos = request.GET.get('quartos', '').strip()
    if is_valid_value(quartos):
        try:
            quartos_int = int(quartos)
            if quartos_int > 0:
                imoveis = imoveis.filter(quartos__gte=quartos_int)
        except (ValueError, TypeError):
            pass
    
    # Banheiros mínimos
    banheiros = request.GET.get('banheiros', '').strip()
    if is_valid_value(banheiros):
        try:
            banheiros_int = int(banheiros)
            if banheiros_int > 0:
                imoveis = imoveis.filter(banheiros__gte=banheiros_int)
        except (ValueError, TypeError):
            pass
    
    # Vagas de garagem mínimas
    vagas = request.GET.get('vagas', '').strip()
    if is_valid_value(vagas):
        try:
            vagas_int = int(vagas)
            if vagas_int > 0:
                imoveis = imoveis.filter(vagas_garagem__gte=vagas_int)
        except (ValueError, TypeError):
            pass
    
    # Área mínima
    area_min = request.GET.get('area_min', '').strip()
    if is_valid_value(area_min):
        try:
            area_min_float = float(area_min)
            if area_min_float > 0:
                imoveis = imoveis.filter(area_util__gte=area_min_float)
        except (ValueError, TypeError):
            pass
    
    # Preço mínimo e máximo
    preco_min = request.GET.get('preco_min', '').strip()
    preco_max = request.GET.get('preco_max', '').strip()
    
    if is_valid_value(preco_min):
        try:
            preco_min_float = float(preco_min)
            if preco_min_float > 0:
                imoveis = imoveis.filter(precos__valor__gte=preco_min_float)
        except (ValueError, TypeError):
            pass
    
    if is_valid_value(preco_max):
        try:
            preco_max_float = float(preco_max)
            if preco_max_float > 0:
                imoveis = imoveis.filter(precos__valor__lte=preco_max_float)
        except (ValueError, TypeError):
            pass
    
    # Mobília
    mobilia = request.GET.get('mobilia', '').strip()
    if is_valid_value(mobilia):
        imoveis = imoveis.filter(mobilia=mobilia)
    
    # Pet friendly
    pet_friendly = request.GET.get('pet_friendly', '').strip()
    if pet_friendly == 'true':
        imoveis = imoveis.filter(pet_friendly=True)
    
    # Aceita financiamento
    financiamento = request.GET.get('financiamento', '').strip()
    if financiamento == 'true':
        imoveis = imoveis.filter(aceita_financiamento=True)
    
    # Somente com fotos
    com_fotos = request.GET.get('com_fotos', '').strip()
    if com_fotos == 'true':
        imoveis = imoveis.filter(fotos__isnull=False)
    
    # Infraestrutura do condomínio
    infraestrutura_ids = request.GET.getlist('infraestrutura')
    if infraestrutura_ids:
        for infra_id in infraestrutura_ids:
            try:
                infra_id_int = int(infra_id)
                imoveis = imoveis.filter(infraestrutura=infra_id_int)
            except (ValueError, TypeError):
                pass
    
    # Ordenação
    ordenacao = request.GET.get('ordenacao', '').strip()
    if ordenacao == 'preco_menor':
        imoveis = imoveis.order_by('precos__valor')
    elif ordenacao == 'preco_maior':
        imoveis = imoveis.order_by('-precos__valor')
    elif ordenacao == 'mais_recentes':
        imoveis = imoveis.order_by('-criado_em')
    elif ordenacao == 'maior_area':
        imoveis = imoveis.order_by('-area_util')
    else:  # relevancia (padrão)
        imoveis = imoveis.order_by('-criado_em', '-atualizado_em')
        ordenacao = 'relevancia'
    
    # Remover duplicatas (devido aos joins com preços)
    imoveis = imoveis.distinct()
    
    # Paginação
    paginator = Paginator(imoveis, 12)  # 12 imóveis por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para os filtros
    cidades = Imovel.objects.filter(
        status=Imovel.StatusImovel.ATIVO
    ).values_list('cidade', flat=True).distinct().order_by('cidade')
    
    infraestruturas = InfraCondominio.objects.all().order_by('nome')
    
    tipos = Imovel.TipoImovel.choices
    finalidades = PrecoPorFinalidade.Finalidade.choices
    mobilias = Imovel.Mobilia.choices
    
    # Filtros aplicados - limpar valores None/vazios para o template
    filtros_aplicados = {}
    for key, value in request.GET.items():
        if key != 'page' and is_valid_value(value):
            filtros_aplicados[key] = value
    
    # Adicionar listas múltiplas
    if infraestrutura_ids:
        filtros_aplicados['infraestrutura'] = infraestrutura_ids
    
    context = {
        'page_obj': page_obj,
        'total_imoveis': paginator.count,
        'cidades': cidades,
        'infraestruturas': infraestruturas,
        'tipos': tipos,
        'finalidades': finalidades,
        'mobilias': mobilias,
        'filtros_aplicados': filtros_aplicados,
    }
    
    return render(request, 'core/lista_imoveis.html', context)


def detalhe_imovel(request, pk):
    """Página de detalhes do imóvel"""
    imovel = get_object_or_404(
        Imovel.objects.select_related('proprietario').prefetch_related(
            'fotos', 'precos', 'infraestrutura'
        ),
        pk=pk,
        status=Imovel.StatusImovel.ATIVO
    )
    
    # Imóveis similares (mesmo tipo e cidade)
    imoveis_similares = Imovel.objects.filter(
        tipo=imovel.tipo,
        cidade=imovel.cidade,
        status=Imovel.StatusImovel.ATIVO
    ).exclude(pk=imovel.pk).prefetch_related('fotos', 'precos')[:4]
    
    # Montar mensagem para WhatsApp
    whatsapp_msg = f"Olá! Tenho interesse no imóvel: {imovel.titulo} - {imovel.endereco}, {imovel.bairro}, {imovel.cidade}"
    
    context = {
        'imovel': imovel,
        'imoveis_similares': imoveis_similares,
        'whatsapp_msg': whatsapp_msg,
    }
    
    return render(request, 'core/detalhe_imovel.html', context)