# OpenShift Image Album with Django

Ez a projekt egy konténerizált fényképalbum alkalmazás, amely a Django web frameworköt, PostgreSQL adatbázist és OpenShift felhőalapú környezetet használ. A cél egy skálázható és biztonságos rendszer, amely lehetővé teszi regisztrált felhasználók számára fényképek feltöltését, megtekintését és kezelését.

---

## Funkciók

- Felhasználó regisztráció, bejelentkezés, kilépés
- Képek feltöltése és törlése (csak bejelentkezett felhasználók számára)
- Képek listázása név és dátum szerint rendezve
- Kattintható listaelem, ami megnyitja a képet teljes nézetben
- Csak bejelentkezett felhasználó végezhet módosításokat

---

## Projekt struktúra

```
/
├── gallery/                        # A fő alkalmazás a képek kezelésére
│   ├── __init__.py
│   ├── apps.py
│   ├── forms.py                   # Feltöltési űrlap (PhotoForm)
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py       # A Photo modell migrációja
│   ├── models.py                 # Photo modell: név, kép, dátum, user
│   ├── tests.py                  # Egyszerű unit tesztek (pl. login tesztelés)
│   ├── urls.py                   # `gallery/` app URL-jei (index, feltöltés, törlés)
│   └── views.py                  # A képekhez tartozó view-k (listázás, feltöltés, törlés)
├── photoalbum/                    # A teljes Django projekt konfigurációs mappája
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Beállítások: DB, statikus fájlok, auth, stb.
│   ├── urls.py                  # Globális URL-ek (admin, login, logout, signup)
│   ├── wsgi.py
│   └──templates/                     # Globális HTML sablonok
│       ├── base.html         # Alap layout (navbar, blokkok)
│       ├── home.html         # Bejelentkezés utáni főoldal, kép lista
│       ├── upload.html       # Kép feltöltő oldal
│       └── detail.html       # Teljes méretben mutat egy képet

├── registration/                  # Egyedi regisztrációs logika
│   ├── __init__.py
│   └── views.py                 # `signup` view 
├── templates/                     
│   ├── registration/           # Django auth rendszer sablonjai
│   │   ├── login.html         # Bejelentkezési oldal
│   │   └── signup.html        # Regisztrációs oldal
│
├── manage.py                     # Django CLI belépési pont
├── entrypoint.sh                 # Django CLI belépési pont
└── requirements.txt              # Python függőségek listája

```

---

## Adatmodell (SQL szinten)

A `PostgreSQL` adatbázis a következő táblákat tartalmazza:

### auth_user (Django beépített táblája)
- username, password (hash), last_login, stb.

photoalbumdb=> \d auth_user    
                                     Table "public.auth_user"
    Column    |           Type           | Collation | Nullable |   
--------------+--------------------------+-----------+----------+
 id           | integer                  |           | not null |
 password     | character varying(128)   |           | not null | 
 last_login   | timestamp with time zone |           |          | 
 is_superuser | boolean                  |           | not null | 
 username     | character varying(150)   |           | not null | 
 first_name   | character varying(150)   |           | not null | 
 last_name    | character varying(150)   |           | not null | 
 email        | character varying(254)   |           | not null | 
 is_staff     | boolean                  |           | not null | 
 is_active    | boolean                  |           | not null | 
 date_joined  | timestamp with time zone |           | not null | 

### gallery_photo
- id (PK)
- name (max. 40 karakter)
- image (fájl elérési útvonal a media mappában)
- uploaded_at (datetime)
- user_id (FK → auth_user.id)

photoalbumdb=> \d gallery_photo
                                   Table "public.gallery_photo"
   Column    |           Type           | Collation | Nullable | 
-------------+--------------------------+-----------+----------+
 id          | bigint                   |           | not null | 
 name        | character varying(40)    |           | not null | 
 image       | character varying(100)   |           | not null | 
 uploaded_at | timestamp with time zone |           | not null | 
 owner_id    | integer                  |           | not null | 


### django_session
- session_key, session_data, expire_date
- A felhasználók session állapotát tárolja

---

## Tesztelés

```bash
python manage.py test
```

- `test_login_required_for_upload`: ellenőrzi, hogy bejelentkezés nélkül redirect történik-e
- `test_logged_in_user_can_access_index`: ellenőrzi, hogy belépés után a főoldal elérhető-e

---

## OpenShift deploy workflow

1. **Build + Push**: GitHub webhook trigger (buildconfig)
2. **ImageStream**: új image verzió detektálása
3. **DeploymentConfig**: új pod rollout, PVC mountolása
4. **Route**: publikus endpoint elérhető pl. [`https://open-shift-image...`](https://open-shift-image-album-with-django-git-somodibme-dev.apps.rm1.0a51.p1.openshiftapps.com/login/)

---

##  PersistentVolumeClaim (PVC)

- A `/media` mappa a podban PVC-re van mountolva
- A képek nem vesznek el pod újraindításkor

---

## Auth és session kezelés

- A `SESSION_ENGINE = 'django.contrib.sessions.backends.db'`
- A session adatok az adatbázisban tárolódnak
- Kilépéskor a session törlődik vagy inaktívvá válik

---
