"""
Management command para inicializar dados de pets
Popula tipos de animais e raças
"""

from django.core.management.base import BaseCommand
from pets.models import TipoAnimal, Raca


class Command(BaseCommand):
    help = 'Inicializa dados de pets: tipos de animais e raças'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('� Inicializando dados de pets...'))
        
        # 1. Criar tipos de animais
        tipos = self.create_tipos_animais()
        
        # 2. Criar raças
        self.create_racas(tipos)
        
        self.stdout.write(self.style.SUCCESS('✅ Pets configurados!'))

    def create_tipos_animais(self):
        """Cria tipos de animais padrão"""
        self.stdout.write('  📦 Criando tipos de animais...')
        
        tipos_data = [
            {'nome': 'Cachorro', 'icone': '🐕'},
            {'nome': 'Gato', 'icone': '🐈'},
            {'nome': 'Pássaro', 'icone': '🐦'},
            {'nome': 'Coelho', 'icone': '🐰'},
            {'nome': 'Hamster', 'icone': '🐹'},
            {'nome': 'Peixe', 'icone': '🐠'},
        ]
        
        tipos = {}
        for tipo_data in tipos_data:
            tipo, created = TipoAnimal.objects.get_or_create(
                nome=tipo_data['nome'],
                defaults={'icone': tipo_data['icone']}
            )
            tipos[tipo_data['nome']] = tipo
            
            if created:
                self.stdout.write(f'     ✅ {tipo_data["icone"]} {tipo_data["nome"]}')
            else:
                self.stdout.write(f'     ⚠️  {tipo_data["icone"]} {tipo_data["nome"]} (já existe)')
        
        return tipos

    def create_racas(self, tipos):
        """Cria raças padrão para cada tipo de animal"""
        self.stdout.write('  📦 Criando raças...')
        
        racas_data = {
            'Cachorro': [
                'Labrador',
                'Poodle',
                'Golden Retriever',
                'Bulldog',
                'Pastor Alemão',
                'Beagle',
                'Pug',
                'Chihuahua',
                'Shih Tzu',
                'Vira-lata',
            ],
            'Gato': [
                'Persa',
                'Siamês',
                'Maine Coon',
                'Bengal',
                'Sphynx',
                'British Shorthair',
                'Ragdoll',
                'Angorá',
                'Vira-lata',
            ],
            'Pássaro': [
                'Calopsita',
                'Papagaio',
                'Periquito',
                'Canário',
                'Agapornis',
                'Cacatua',
                'Arara',
            ],
            'Coelho': [
                'Anão',
                'Mini Rex',
                'Lion Head',
                'Californiano',
                'Fuzzy Lop',
                'Holandês',
            ],
            'Hamster': [
                'Sírio',
                'Chinês',
                'Anão Russo',
                'Roborovski',
            ],
            'Peixe': [
                'Betta',
                'Guppy',
                'Neon',
                'Molinésia',
                'Platy',
                'Kinguio',
            ],
        }
        
        total_created = 0
        total_existing = 0
        
        for tipo_nome, racas_list in racas_data.items():
            if tipo_nome not in tipos:
                continue
                
            tipo = tipos[tipo_nome]
            
            for raca_nome in racas_list:
                _, created = Raca.objects.get_or_create(
                    nome=raca_nome,
                    tipo_animal=tipo
                )
                
                if created:
                    total_created += 1
                else:
                    total_existing += 1
        
        self.stdout.write(f'     ✅ {total_created} raças criadas')
        if total_existing > 0:
            self.stdout.write(f'     ⚠️  {total_existing} raças já existiam')
