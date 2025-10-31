"""
Management command para inicializar usuários do sistema
Cria superusuário admin e configura o Site do Django
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site


User = get_user_model()


class Command(BaseCommand):
    help = 'Inicializa usuário admin e configurações do site'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('👥 Inicializando usuários...'))
        
        # 1. Criar superusuário admin
        self.create_admin_user()
        
        # 2. Configurar Site do Django
        self.configure_site()
        
        self.stdout.write(self.style.SUCCESS('✅ Usuários configurados!'))

    def create_admin_user(self):
        """Cria usuário admin se não existir"""
        username = 'admin'
        email = 'admin@petshop.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'  ⚠️  Usuário "{username}" já existe'))
            return
        
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write(self.style.SUCCESS(f'  ✅ Superusuário criado:'))
            self.stdout.write(f'     Username: {username}')
            self.stdout.write(f'     Email: {email}')
            self.stdout.write(f'     Password: {password}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro ao criar admin: {e}'))

    def configure_site(self):
        """Configura o Site do Django para OAuth"""
        try:
            site = Site.objects.get(id=1)
            
            # Verifica se já está configurado
            if site.domain != 'example.com' and site.name != 'example.com':
                self.stdout.write(self.style.WARNING(f'  ⚠️  Site já configurado: {site.domain}'))
                return
            
            # Configuração padrão para localhost
            site.domain = 'localhost:8000'
            site.name = 'PetShop'
            site.save()
            
            self.stdout.write(self.style.SUCCESS(f'  ✅ Site configurado: {site.domain}'))
            self.stdout.write(self.style.WARNING(f'     💡 Para Codespaces, atualize manualmente!'))
        except Site.DoesNotExist:
            self.stdout.write(self.style.ERROR('  ❌ Site com ID 1 não existe'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Erro ao configurar site: {e}'))
