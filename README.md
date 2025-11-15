# Gmail Epasta Adrešu Meklēšanas Rīks

Šis rīks ļauj meklēt epasta adreses jūsu Gmail kontā un ģenerēt pārskatu par adresēm, kurām nav nosūtīti epasti.

## Funkcionalitāte

- 📧 Nolasa epasta adreses no faila
- 🔍 Meklē katru adresi Gmail kontā (TO laukā)
- 📊 Ģenerē CSV pārskatu ar:
  - Neatrastajām adresēm (galvenais)
  - Atrastajām adresēm + ziņojumu skaits
  - Statistiku
- 🔐 Drošs OAuth 2.0 autentifikācija (bez parolēm)

## Prasības

- Python 3.7 vai jaunāks
- Gmail konts
- Google Cloud projekts ar Gmail API

## Instalēšana

### 1. Instalējiet Python bibliotēkas

```bash
pip install -r requirements.txt
```

### 2. Izveidojiet Google Cloud projektu un ieslēdziet Gmail API

1. Dodieties uz [Google Cloud Console](https://console.cloud.google.com/)
2. Izveidojiet jaunu projektu vai izvēlieties esošu
3. Ieslēdziet Gmail API:
   - Dodieties uz "APIs & Services" > "Library"
   - Meklējiet "Gmail API"
   - Klikšķiniet "Enable"

### 3. Izveidojiet OAuth 2.0 credentials

1. Dodieties uz "APIs & Services" > "Credentials"
2. Klikšķiniet "Create Credentials" > "OAuth client ID"
3. Ja nepieciešams, konfigurējiet OAuth consent screen:
   - User Type: External (ja jums nav Google Workspace)
   - App name: "Gmail Email Search Tool" (vai cits nosaukums)
   - User support email: jūsu email
   - Developer contact: jūsu email
   - Saglabājiet un turpiniet
   - Scopes: nav jāpievieno (izmantosim tikai lasīšanu)
   - Test users: pievienojiet savu Gmail adresi
4. Application type: Desktop app
5. Name: "Gmail Search Desktop"
6. Klikšķiniet "Create"
7. **Lejupielādējiet JSON failu** un pārdēvējiet to par `credentials.json`
8. Ievietojiet `credentials.json` šajā direktorijā

### 4. Sagatavojiet epasta adrešu failu

Izveidojiet failu `nosutiti.txt` ar epasta adresēm. Formāts var būt:

```
"alise.kanepa@gmail.com",
"ilzevipule@gmail.com",
"80bojdi@gmail.com"
```

Vai vienkārši:

```
alise.kanepa@gmail.com
ilzevipule@gmail.com
80bojdi@gmail.com
```

Skatiet `nosutiti.txt.example` piemēru.

## Lietošana

Palaidiet skriptu:

```bash
python gmail_search.py
```

### Pirmā palaišana

Pirmajā palaišanā:
1. Atvērsies pārlūkprogramma
2. Pierakstieties ar savu Gmail kontu
3. Atļaujiet piekļuvi (klikšķiniet "Allow")
4. Pēc tam varat aizvērt pārlūkprogrammu

Nākamajās reizēs autentifikācija notiks automātiski!

### Rezultāts

Pēc izpildes tiks izveidots fails `rezultats.csv` ar:

- **Neatrastajām adresēm** - tās, kurām nav nosūtīti epasti
- **Atrastajām adresēm** - ar ziņojumu skaitu
- Statistiku

## Failu struktūra

```
gmail_count/
├── gmail_search.py          # Galvenais skripts
├── requirements.txt         # Python bibliotēkas
├── credentials.json         # OAuth credentials (nav repo)
├── token.json              # Saglabāts auth token (nav repo)
├── nosutiti.txt            # Jūsu epasta adreses (nav repo)
├── nosutiti.txt.example    # Piemērs
├── rezultats.csv           # Rezultāti (nav repo)
└── README.md               # Šis fails
```

## Drošība

- `credentials.json` un `token.json` **nekad** netiek augšupielādēti Git
- Rīks izmanto **tikai lasīšanas** piekļuvi Gmail
- OAuth 2.0 - droša autentifikācija bez paroļu glabāšanas
- Varat jebkurā laikā atsaukt piekļuvi Google kontu iestatījumos

## Problēmu risināšana

### "No module named 'google'"
Instalējiet bibliotēkas: `pip install -r requirements.txt`

### "credentials.json not found"
Jums nepieciešams izveidot OAuth credentials (skatiet 3. soli)

### "Access denied" vai "403 error"
- Pārbaudiet vai Gmail API ir ieslēgts jūsu projektā
- Pārbaudiet vai jūsu email ir pievienots kā test user

### Meklēšana ir lēna
Tas ir normāli! Gmail API apstrādā 540 adreses, kas var aizņemt 5-10 minūtes.

## Autors

Izveidots ar Claude AI

## Licence

MIT
