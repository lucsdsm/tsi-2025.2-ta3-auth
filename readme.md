### Iniciar os Containers

```bash
cd django 
docker-compose up -d
```

### Configurar o Site no Django

Execute o seguinte comando para configurar o domínio correto:

```bash
docker-compose exec web python manage.py shell -c "
from django.contrib.sites.models import Site

# Configurar o site
site = Site.objects.get(id=1)
site.domain = 'localhost:8000'  # ou seu domínio do Codespaces
site.name = 'PetShop'
site.save()
print(f'✓ Site configurado: {site.domain}')
"
```

**Se estiver usando GitHub Codespaces**, substitua `localhost:8000` pela URL do seu Codespace (sem `http://` ou `https://`):

```bash
docker-compose exec web python manage.py shell -c "
from django.contrib.sites.models import Site

site = Site.objects.get(id=1)
site.domain = 'seu-codespace-xxx.app.github.dev'
site.name = 'PetShop'
site.save()
print(f'✓ Site configurado: {site.domain}')
"
```

### (Opcional) Criar Superusuário

Para acessar o Django Admin:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 🌐 Acessar a Aplicação

### Localmente:
```
http://localhost:8000
```

### GitHub Codespaces:
```
https://<seu-codespace>.app.github.dev
```