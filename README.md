<h1 align="center">Projekt vytvořený pro maturitu</h1> 

**<p><ins>Obsah</ins></p>**

1. [O projektu](#about)
2. [Instalace a spouštění](#install)
3. [Dokumentace](#docs)
    
    *  [Endpointy](#endpoints)
    *  [Funkce](#functions)
    * [Frontend](#frontend)
    * [Desktop](#desktop)
    * [Databáze](#database)
  
4. [Použité technologie](#technologies)

<a name="about"></a>
# O projektu
Projekt je určený pro  **praktickou maturitní zkoušku** z programování. **Backendová** část je vytvořena pomocí pythonovské WSGI knihovny Flask pro propojení s databází aplikace využívá MySQL Connector. 
Hashování hesel má na starosti hashovací algoritmus **Argon2**. K autentizaci a k autorizaci aplikace používá **JSON Web Token**.
<br>
**Desktopová aplikace** je vytvořena přes open source herní engine **Godot**, jedná se o jednoduchou hru, kde registrovaní uživatelé bojují o co největší počet bodů. Hra spočívá v pinkání míčku a směrování míčku na target, který když hráč trefí získá bod. 
<br>
**Frontend** je vytvořen pomocí HTML, CSS a JavaScriptu, což umožňuje jednoduché, ale efektivní uživatelské rozhraní. Slouží především k registraci a přihlášení uživatelů, zobrazování výsledků a interakci s backendovou částí přes API.

<a name="install"></a>
# Instalace a spouštění


## 1️⃣ Naklonujte si projekt  
```sh
git clone https://github.com/DemsterCZE/Maturita.git
```
## 2️⃣ Nastavte svůj pracovní adresář
```sh
cd {Cesta_k_repozitari}/backend/
```
## 3️⃣ Nainstalujte si všechny dependencies k backendu
```sh
pip install -r requirements.txt
```
## 4️⃣ Spusťte Python aplikaci
```sh
py .\main.py
```
## 5️⃣ Otevřete si aplikaci v prohlížeči
Do URL ve vyhledávači zadejte:
localhost:5000
> [!IMPORTANT]
> Nepoužívejte 127.0.0.1, jinak nebudou fungovat cookies.

## 6️⃣ Přihlášení  
V databázi jsou již dva uživatelé, které můžete použít pro přihlášení:

| **Username** | **Heslo** | **Role** |
|--------------|-----------|----------|
| admin        | admin     | Admin   |
| player       | player    | Hráč    |

Pro přihlášení použijte jedno z těchto jmen a hesel. Po přihlášení budete mít přístup k odpovídajícím funkcím aplikace na základě role. <br>
Nebo se na stránkách můžete registrovat, avšak role Vám bude automaticky přidělena jako Player.

## 7️⃣ Otevřete hru v Godot engine  
1. Spusťte **Godot**.  
2. Ve správě projektů klikněte na **Importovat projekt**.  
3. Vyberte složku, která obsahuje projekt hry: {Cesta_k_repozitari}/hra
4. **Godot se postará o zbytek** a načte projekt.  
5. Po úspěšném importu můžete začít hrát. 🎮

## 8️⃣ Přihlášení ve hře  
- Po spuštění hry se přihlaste jako **hráč** (uživatel s `roleID 2`), protože **admini nejsou zobrazováni v žebříčku**.  
- Nepřihlášený hráč nemůže hrát.

## 9️⃣ Užijte si hru! 🎉

<a name="docs"></a>
# Dokumentace
<a name="endpoints"></a>
## Endpointy


> [!NOTE]
> Né všechny endpointy jsou volně přístupné pro některé je třeba autorizační token **JWT**.
<br>


- **URL:** `/get_users`
- **Metoda:** `GET`

Tento endpoint vrátí jméno, id a nejvyšší skór všech hráčů. Ve frontendu taky bude přidán filter, aby si uživatel mohl vybrat, kolik uživatelů se mu vypíše.
### JSON odpověď

```json
{
    "data": [
        {
            "highest_score": 451,
            "id": 1,
            "username": "Jirka"
        },
        {
            "highest_score": 350,
            "id": 2,
            "username": "Jakub"
        },
        {
            "highest_score": 275,
            "id": 3,
            "username": "Ondra"
        },
        {
            "highest_score": 120,
            "id": 4,
            "username": "Mates"
        },
        {
            "highest_score": 150,
            "id": 5,
            "username": "Jan"
        }
    ]
}
```
<hr>

- **URL:** `/get_me`
- **Metoda:** `GET`
- **Headers:** 
  - `Authorization: Bearer <token>`
  
  Tento endpoint vrátí konkretního uživatele na základě jeho tokenu (uživatel musí být přihlášen).

  ### JSON odpověď

  ```json
  [
    {
        "highest_score": 451,
        "id": 1,
        "username": "Jirka"
    }
  ]
  ```
  <hr>

- **URL:** `/register`
- **Metoda:** `POST`
- **Body:**
  ```json
  {
    "username" : "Emil",
    "email": "emil.zatopek@maraton.cz",
    "password" : "KdyzN3muz3sTakPrid3j"
  }
  ```
  ### JSON odpověď
 ```json
  {"Success": "Uživatel registrován"}
  ```
<hr>

- **URL:** `/login`
- **Metoda:** `POST`
- **Body:**
  
  ```json
  {
    "login" : "Emil",
    "password" : "KdyzN3muz3sTakPrid3j"
  }
  ```

### JSON odpověď

 ```json
{
    "Success": "Uživatel Emil úspěšně přihlášen",
    "Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkVtaWwifQ.25LQ0YT6fkkW7GWqJdy_G5_COf9aH8iSCLubCu0L8u4"
}
 ```
<hr>


- **URL:** `/update_score`
- **Metoda:** `PATCH`
- **Headers:** 
  - `Authorization: Bearer <token>`
- **Body:**
```json
  {
    "score": 450
  }
```
### JSON odpověď
```json
  {
  "Success":"Skóre úspěšně změněno"
  }
```
<hr>
<a name="functions"></a>

## Funkce


> [!NOTE]
> Nejsou zde všechny funkce

## `validate_email`

Funkce zkontroluje zdali je zadán správný formát emailu

### Argumenty
| Název       | Typ   | Popis               |
|------------|--------|-----------------------------|
| `email`        | `str`  |  Email co se bude kontrolovat  |


### Vrací
`bool`: Email je validní `True` , není validní `False`.

### Použití
```python
def validate_email(email:str):
    """
    Kontrola emailu
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    Argument:
        email (str): Email ke zkontrolování.
        

    Vrací:
        bool: kontrola emailu
    """
    return re.match(email_regex,email)

# Příklad
result1 = validate_email("john@email.cz")
print(result1)  # Output: True

result2 = validate_email("john@email")
print(result2)  # Output: False
```

## `create_hash`

Funkce vytvoří ze zadaného argumentu hash společně se saltem, který se pak uloží do databáze

### Argumenty
| Název       | Typ   | Popis               |
|------------|--------|-----------------------------|
| `passwd`        | `str`  |  heslo co se bude hashovat |


### Vrací
`str`: Zahashovane heslo.

### Použití
```python
def create_hash(password:str):
    """
    hashovani
    hash_builder : argon2.PasswordHasher = argon2.PasswordHasher()

  Argument:
        passwd (str): Heslo, co se bude hashovat.
        

    Vrací:
        str: Hash
    """
    return hash_builder.hash(passwd)

# Příklad
hash = create_hash("1234")
print(hash)  # Output: (Například: $argon2d$v=19$m=1024,t=16,p=4$c2FsdDEyM3NhbHQxMjM$2dVtFVPCezhvjtyu2PaeXOeBR+RUZ6SqhtD/+QF4F1o)

```

<a name="frontend"></a>
## Frontend
Frontend je vytvořen pomocí HTML, CSS a JavaScriptu, což umožňuje jednoduché, ale efektivní uživatelské rozhraní. Slouží především k registraci a přihlášení uživatelů, zobrazování výsledků a interakci s backendovou částí přes API. Je zde taky rozdílný obsah pro adminy a pro normální hráče, kde admini mají přístup 
na stránku admin panel, kde mohou smazat ostatní uživatele.
Ke smazání a přístupu je potřeba mít v cookině uložený autorizační token JWT
O renderování stránek se stará backend. Na stránku se lze dostat zadáním localhost:5000 do webového prohlížeče automaticky nás to přesměruje na hlavní stránku.
> [!IMPORTANT]
> Pro správné fungování cookies je potřeba používat frontend na doméně localhost. Né na 127.0.0.1

<a name="desktop"></a>
## Desktop
K zapnutí hry je třeba herního enginu Godot. Po zapnutí Godotu se nám otevře okno - Správa projektů. <br>
Je zde třeba projekt importovat. Cesta k projektu : Cesta_k_repozitari\hra\ Godot už si sám vše zařídí.

<a name="database"></a>
## Databáze

Databáze běží na školním serveru. Moje se nachází na Student27. K fungování jsou třeba 2 tabulky users a roles. Pokud se tam tabulky nenachází backend je automaticky vytvoří. <br>
V databázi jsou hesla zahashovaná. Databáze využívá 1:N vztahu Tj. Libovolný počet uživatelů může mít přiřazenou roli "player" nebo "admin". Ty to rozdíly se pak projevují ve frontendu.

### ER diagram

```mermaid
erDiagram
    USERS {
        int id PK
        string username "UNIQUE"
        string email
        string password_hash
        int highest_score "DEFAULT 0"
        int RoleID FK
    }
    ROLES {
        int RoleID PK
        string RoleName
    }
    USERS }o--|| ROLES : "has role"
```
<a name="technologies"></a>
#  🛠️ Použité technologie

### 🎮 Herní Engine:
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/godot/godot-original.svg" alt="Godot" width="50"/>
</p>

### 🖥️ Backend:
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" alt="Flask" width="50"/>
</p>

### 🗄️ Databáze:
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" alt="MySQL" width="50"/>
</p>

### 🌐 Frontend:
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" alt="HTML5" width="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" alt="CSS3" width="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" alt="JavaScript" width="50"/>
</p>

### 🔧 Ostatní:
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" alt="Git" width="50"/>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" alt="GitHub" width="50"/>
</p>
