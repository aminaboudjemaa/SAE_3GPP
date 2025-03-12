# SAE_3GPP

## Instalation 
```bash
pip install -r requirements
```
## Run Server
```bash
cd web/sae_3gpp_web
python manage.py makemigrations
python manage.py migrate
python manage.py qcluster &
python manage.py runserver

```
Access Web server at 127.0.0.0:8000

## Populate database (without AI data)
Manually start database population by accessing 127.0.0.0:8000/tdoc/collect

## Configuration
See web/sae_3gpp_web/sae_3gpp_web/settings.py for configuration