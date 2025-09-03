import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-sua-chave-secreta-aqui-mude-em-producao'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'imobiliaria.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'imobiliaria.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===============================
# 🎨 CONFIGURAÇÕES JAZZMIN DS IMÓVEIS
# ===============================

JAZZMIN_SETTINGS = {
    # Identidade da Empresa
    "site_title": "DS Imóveis - Admin",
    "site_header": "DS Imóveis",
    "site_brand": "DS Admin",
    "site_logo": None,
    "login_logo": None,
    "welcome_sign": "Bem-vindo ao Painel DS Imóveis",
    "copyright": "DS Imóveis © 2025 - Todos os direitos reservados",
    
    # Busca
    "search_model": ["core.Imovel", "core.Proprietario", "core.Cliente"],
    "user_avatar": None,
    
    # Menu Superior
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Ver Site", "url": "/", "new_window": True},
        {"name": "Relatórios", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
    
    # Menu do Usuário
    "usermenu_links": [
        {"name": "👤 Meu Perfil", "url": "admin:auth_user_change", "icon": "fas fa-user"},
        {"model": "auth.user"}
    ],
    
    # =====================================
    # 🎨 ÍCONES POR MODELO
    # =====================================
    "icons": {
        # Sistema de Autenticação
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        
        # Modelos Principais
        "core.imovel": "fas fa-home",
        "core.proprietario": "fas fa-user-tie", 
        "core.cliente": "fas fa-handshake",
        
        # Modelos Auxiliares
        "core.fotoimovel": "fas fa-camera",
        "core.precoporfinalidade": "fas fa-dollar-sign",
        "core.infracondominio": "fas fa-building",
    },
    
    # Ícones padrão
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # =====================================
    # 🎨 CONFIGURAÇÕES DE LAYOUT
    # =====================================
    
    # Modais e Customizações
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    
    # Layout dos Formulários
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs",
        "core.imovel": "horizontal_tabs",
        "core.cliente": "horizontal_tabs"
    },
    
    # =====================================
    # 🎨 TEMA E CORES
    # =====================================
    
    # Tema Principal
    "theme": "default",
    
    # Navegação e Layout
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark bg-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    
    # =====================================
    # 🎨 CONFIGURAÇÕES AVANÇADAS
    # =====================================
    
    # Ordem dos aplicativos no menu
    "order_with_respect_to": ["core", "auth"],
    
    # Ocultar aplicativos
    "hide_apps": [],
    
    # Ocultar modelos específicos
    "hide_models": [
        "core.fotoimovel",          # Gerenciado via inline
        "core.precoporfinalidade",  # Gerenciado via inline
        "core.infracondominio",     # Modelo auxiliar
    ],
    
    # Customizar labels dos aplicativos
    "custom_links": {
        "core": [{
            "name": "Dashboard", 
            "url": "admin:index", 
            "icon": "fas fa-chart-line",
            "permissions": ["core.view_imovel"]
        }]
    },
    
    # Language chooser
    "language_chooser": False,
}

# =========================================
# 🎨 JAZZMIN UI TWEAKS (CORES CORPORATIVAS)
# =========================================

JAZZMIN_UI_TWEAKS = {
    # Texto
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    
    # Cores de acento
    "accent": "accent-warning",
    
    # Navbar
    "navbar": "navbar-dark bg-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    
    # Layout
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    
    # Sidebar
    "sidebar": "sidebar-dark-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    
    # Tema
    "theme": "default",
    "dark_mode_theme": None,
    
    # =====================================
    # 🎨 BOTÕES CORPORATIVOS
    # =====================================
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    
    # =====================================
    # 🎨 CUSTOM CSS CORPORATIVO
    # =====================================
    "custom_css": """
        /* Paleta de cores corporativa */
        :root {
            --ds-gold: #C8A866;
            --ds-gold-light: #D4AF37;
            --ds-dark: #0D0D0D;
            --ds-blue: #1E3A5F;
        }
        
        /* Header corporativo */
        .main-header {
            background-color: var(--ds-blue) !important;
            border-bottom: 3px solid var(--ds-gold) !important;
        }
        
        /* Brand corporativo */
        .navbar-brand {
            color: var(--ds-gold-light) !important;
            font-weight: bold !important;
        }
        
        /* Sidebar corporativo */
        .main-sidebar {
            background-color: var(--ds-dark) !important;
        }
        
        /* Botões corporativos */
        .btn-warning {
            background-color: var(--ds-gold) !important;
            border-color: var(--ds-gold) !important;
            color: var(--ds-dark) !important;
            font-weight: 600 !important;
        }
        
        .btn-warning:hover {
            background-color: var(--ds-gold-light) !important;
            border-color: var(--ds-gold-light) !important;
            color: var(--ds-dark) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(200, 168, 102, 0.3) !important;
        }
        
        /* Cards corporativos */
        .card {
            border: 1px solid rgba(200, 168, 102, 0.2) !important;
            border-radius: 8px !important;
        }
        
        .card-header {
            background-color: #f8f9fa !important;
            border-bottom: 2px solid var(--ds-gold) !important;
            color: var(--ds-blue) !important;
            font-weight: bold !important;
        }
        
        /* Links corporativos */
        a {
            color: var(--ds-blue) !important;
        }
        
        a:hover {
            color: var(--ds-gold) !important;
        }
        
        /* Tabelas corporativas */
        .table th {
            background-color: #f8f9fa !important;
            color: var(--ds-blue) !important;
            font-weight: 600 !important;
            border-bottom: 2px solid var(--ds-gold) !important;
        }
        
        /* Badges corporativos */
        .badge-success {
            background-color: #28a745 !important;
        }
        
        .badge-warning {
            background-color: var(--ds-gold) !important;
            color: var(--ds-dark) !important;
        }
        
        /* Formulários corporativos */
        .form-control:focus {
            border-color: var(--ds-gold) !important;
            box-shadow: 0 0 0 0.2rem rgba(200, 168, 102, 0.25) !important;
        }
        
        /* Menu sidebar corporativo */
        .nav-sidebar .nav-link {
            color: rgba(255, 255, 255, 0.9) !important;
        }
        
        .nav-sidebar .nav-link:hover {
            background-color: rgba(200, 168, 102, 0.2) !important;
            color: var(--ds-gold-light) !important;
        }
        
        .nav-sidebar .nav-link.active {
            background-color: var(--ds-gold) !important;
            color: var(--ds-dark) !important;
            font-weight: bold !important;
        }
        
        /* Footer corporativo */
        .main-footer {
            background-color: var(--ds-dark) !important;
            color: var(--ds-gold) !important;
            border-top: 2px solid var(--ds-gold) !important;
        }
        
        /* Animations corporativas */
        .btn, .card, .form-control {
            transition: all 0.3s ease !important;
        }
        
        /* Dashboard cards corporativo */
        .info-box {
            border-radius: 8px !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
            border: 1px solid rgba(200, 168, 102, 0.2) !important;
        }
        
        .info-box-icon {
            background-color: var(--ds-gold) !important;
            color: var(--ds-dark) !important;
        }
    """,
    
    # JavaScript corporativo
    "custom_js": """
        // Adicionar efeitos corporativos
        document.addEventListener('DOMContentLoaded', function() {
            // Adicionar ícone no título
            const brandElement = document.querySelector('.navbar-brand');
            if (brandElement && !brandElement.querySelector('.fas')) {
                brandElement.innerHTML = '<i class="fas fa-home me-2"></i>' + brandElement.innerHTML;
            }
            
            // Smooth animations para botões
            document.querySelectorAll('.btn').forEach(btn => {
                btn.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-1px)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0)';
                });
            });
            
            // Console log corporativo
            console.log('🏠 DS Imóveis Admin carregado com sucesso!');
        });
    """
}

# ===============================
# 🔧 CONFIGURAÇÕES ADICIONAIS
# ===============================

# Configurações de e-mail (para produção)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Para desenvolvimento

# Configurações de cache (para produção)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Configurações de logging corporativo
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'corporativo': {
            'format': '🏠 [{levelname}] {asctime} - {name}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'corporativo',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Configurações de segurança (para produção)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True