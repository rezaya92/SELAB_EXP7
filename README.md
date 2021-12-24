# SELAB EXP 7&8

## gateway (port 8080):
```
pip install -r requirements.txt
python server.py
```

## authentication service (port 8000):
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## profile service (port 9000):

```
pip install -r requirements.txt
```

to create db do:
```
$$ python
from prescription import *
db.create_all()
exit()
```

then just:
```
python prescription.py
```
