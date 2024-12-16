# Návod pro implementaci a nasazení middleware aplikace s robotem NAO 🤖 a OpenAI API 

![Version](https://img.shields.io/badge/version-2.0-red) ![License](https://img.shields.io/badge/license-MIT-yellow) ![Last Commit](https://img.shields.io/github/last-commit/Dsa-jpg/BcThesis_CI-CD) ![Contributors](https://img.shields.io/github/contributors/Dsa-jpg/BcThesis_CI-CD) ![Languages](https://img.shields.io/github/languages/top/Dsa-jpg/BcThesis_CI-CD) 

Tento návod poskytuje detailní kroky pro nasazení middleware aplikace, která propojuje robota NAO s OpenAI API prostřednictvím platformy Google Cloud Run. Tento dokument zahrnuje všechny klíčové části procesu, od přípravy prostředí po zabezpečení komunikace mezi jednotlivými komponentami.

## Obsah

1. [Úvod](#1úvod)
2. [Příprava prostředí](#2příprava-prostředí)
    2.1 [Instalace potřebných nástrojů](#21instalace-potřebných-nástrojů)
    2.2 [Nastavení Google Cloud](#22nastavení-google-cloud)
3. [Nastavení Google Cloud](#3nastavení-google-cloud)
    3.1 [Vytvoření Docker repozitáře](#31vytvoření-docker-repozitáře)
    3.2 [Nastavení Dockeru pro komunikaci s Google Cloud](#32nastavení-dockeru-pro-komunikaci-s-google-cloud)
4. [Vytvoření a nasazení kontejneru](#vytvoření-a-nasazení-kontejneru)
    4.1 [Vytvoření Docker image](#41vytvoření-docker-image)
    4.2 [Nasazení aplikace na Google Cloud Run](#42nasazení-aplikace-na-google-cloud-run)
5. [Testování aplikace](#5testování-aplikace)
    5.1 [Postup](#61postup)
6. [Připojení robota NAO k aplikaci](#6připojení-robota-nao-k-aplikaci)
---

## 1.Úvod

Tento návod je součástí bakalářské práce, která se zaměřuje na integraci robota NAO s OpenAI API prostřednictvím middleware aplikace nasazené na Google Cloud Run. Cílem je ukázat, jak efektivně propojit roboty s velkými jazykovými modely pro přirozenou a plynulou interakci s uživateli.

## 2.Příprava prostředí

Pro nasazení aplikace na Google Cloud je třeba mít připravené následující nástroje:

### 2.1.Instalace potřebných nástrojů


- **Google Cloud SDK (CLI)**: Slouží pro autentifikaci a komunikaci s Google Cloud.
  - [Instalace Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

- **Python 3.x**: Tento jazyk je nutný pro běh aplikace.
  - [Instalace Pythonu](https://www.python.org/downloads/)

- **Docker (volitelné)**: Je volitelný nástroj pro vytvoření kontejneru aplikace.
  - [Instalace Dockeru](https://docs.docker.com/get-docker/)

- **IDE pro vývoj (volitelné)**: Usnadňuje vývoj aplikace, správu závislostí a debugging.
  - **PyCharm** (doporučeno pro větší projekty s Pythonem a Flaskem):  
    [Instalace PyCharm](https://www.jetbrains.com/pycharm/download/)
  - **VS Code** (lehčí a flexibilní IDE):  
    [Instalace VS Code](https://code.visualstudio.com/Download)

Poslední 3 body jsou pouze v případě, že je potřeba provést revizi kódu, či aktualizaci. Jinak stačí stáhnou celý projekt, který je přiložen v přílohách u mojí bakalařské práci a pokračovat dále v tomto návodu.


### 2.2.Nastavení Google Cloud

Předtím než se dostanete do Google Cloud tak musíte mít účet od Googlu a Billing účet. Pro správné fungování aplikace na Google Cloud musíte vytvořit projekt a nastavit potřebné API.

1. Vytvořte projekt na [Google Cloud Console](https://console.cloud.google.com/).
![Obrázek instalace nástrojů](CreateProject.jpg)
*Obrázek 1:  Klikněte na tlačítko vedle loga Google Cloud pro vytvoření projektu.*
![Obrázek instalace nástrojů](CreateProject2.jpg)
*Obrázek 2:  Klikněte na tlačítko create project.*
![Obrázek instalace nástrojů](GCP3.jpg)
*Obrázek 3:  Vytvořte projekt doporučuji si zapamatovat "id" Vašeho projektu.*

2. Aktivujte potřebná API (Cloud Run,Cloud Build API, Artifact Registry).
3. Potřebujete mít daný projekt v skupině platného billing účtu. Pokud ho nemáte tak ho vytvořte viz obrázky níže.
![Obrázek instalace nástrojů](CreateProject.jpg)
*Obrázek 4:  Znovu klikněte na tlačítko vedle loga Google Cloud pro vytvoření projektu.*
![Obrázek instalace nástrojů](GCP2.jpg)
*Obrázek 5:  Klikněte na modrou složku na obrázku.*
![Obrázek instalace nástrojů](billaccount.jpg)
*Obrázek 6:  Najděte Váš projekt, u kterému chcete přiřadit nebo vytvořit billing účet.*
![Obrázek instalace nástrojů](GCP5.jpg)
*Obrázek 7:  Zde máte na výběr na přiřazení billing účtu k Vašemu projektu nebo pokud ho nemáte tak klikněte na manage billing account, kde si ho můžete vytvořit.*
4. Pokud máte všechny předešlé kroky tak si otevřete Vaši Google Cloud SDK CLI u můžete začít s nastavení autentifikace pomocí příkazů:
```bash
gcloud auth login 
gcloud config set project YOUR_PROJECT_ID # projekt id je viditelné na obrázku 2 nebo na hlavní stránce console cloud
```
## 3.Nastavení Google Cloud
### 3.1.Vytvoření Docker repozitáře

Pokud ještě nemáte repozitář pro ukládání Docker image, vytvořte nový pomocí následujícího příkazu:
```bash
gcloud artifacts repositories create YOUR_REPO_NAME \
  --repository-format=docker \
  --location=europe-west4 \
  --description="" \
  --immutable-tags \
  --async
```

### 3.2.Nastavení Dockeru pro komunikaci s Google Cloud

Pro konfiguraci Dockeru pro práci s Google Cloud:

```bash
gcloud auth configure-docker europe-west4-docker.pkg.dev
```

## 4.Vytvoření a nasazení kontejneru
### 4.1.Vytvoření Docker image
Přejděte do adresáře, kde máte svůj Dockerfile, a spusťte následující příkaz pro vytvoření Docker image:

```bash
gcloud builds submit --tag europe-west4-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPO_NAME/openaiimg:latest
```
> ⚠️ **Varování:** Může se stát, že Vám neprojde nasazení proto je nutné jít do [IAM & Admin](https://console.cloud.google.com/iam-admin/). Zde budete mít dva účty Váš osobní a dále druhý účet. U každého účtu bude tužka, která umožní přidávat a odebírat práva. Tak mu přidejte práva na 'Storage Object Viewer'.



### 4.2.Nasazení aplikace na Google Cloud Run
Po vytvoření Docker image nasadíte aplikaci na Google Cloud Run. Jde to buď přes Google Cloud SDK CLI nebo přímo přes Google Cloud Run. V tomto případě můžete zavřít CLI a otevřít Google Cloud Run.

1. Zadejte do vyhledavacího okna na Google Cloud název Cloud Run a klikněte na něj.
![Obrázek instalace nástrojů](gcp8.jpg)
*Obrázek 8:  Klikněte na tlačítko Create Service.*
![Obrázek instalace nástrojů](gcp7+.jpg)
*Obrázek 9:  Klikněte na (Deploy one revision from an existing container image) a Zmáčkněte Select u Container Image URL.*
![Obrázek instalace nástrojů](gcp11.jpg)
*Obrázek 10: Zde vyberte img containeru, co jste tam nasadili předtím pomocí CLI.*
![Obrázek instalace nástrojů](gcp7.jpg)
*Obrázek 11: Zde vyberte stejný region, jako u Vašeho docker image. V tomto případě to bude europe-west4*
![Obrázek instalace nástrojů](gcp9.jpg)
*Obrázek 12: Zde zadejte minimalní počet instatncí 1, abychom zamezili cold startu serveru a kontajneru.*
![Obrázek instalace nástrojů](gcp10.jpg)
*Obrázek 13: U nastavení počtu instancí je to individuální. V mém případě stačilo <0-1>*
> ⚠️ **Varování:** Je důležité zde povolit (Allow unauthenticated invocations Check this if you are creating a public API or website), jinak robot nebude schopen komunikovat s WebServerem. 

> ⚠️ **Varování:** Dále je důležite zaškrtnout (CPU is only allocated during request processing You are charged per request and only when the container instance processes a request.) Toto způsobuje úsporu financí, jelikož platíte pouze, když je server aktivně dotazován.

## 5.Testování aplikace
Po nasazení aplikace na Google Cloud Run proveďte testovací požadavek na veřejnou URL aplikace na endpoint /stats:

```bash
curl https://YOUR_SERVICE_URL/stats
```

U endpointu pro komunikaci s robotem je curl dotaz nasledovný.

```bash
curl -X POST -F "file=@path/to/file.wav" https://YOUR_SERVICE_URL/upload-non-streamed
```
> 💡 **Info:** Odpověd bude v JSON formátu {"response": "Some text"}.


Pokud aplikace správně odpoví, znamená to, že nasazení bylo úspěšné.



## 6.Připojení robota NAO k aplikaci

Pro zajištění propojení robota NAO s middleware aplikací je nutné provést několik kroků. Pro usnadnění tohoto procesu je k dispozici připravený soubor ve formátu ZIP, který je součástí této bakalářské práce. Stačí jej stáhnout a provést úpravu jediné proměnné v modulu pro odesílání audia.

### 6.1.Postup:

1. **Stažení souboru ZIP**: Stáhněte si přiložený ZIP soubor, který obsahuje potřebné skripty a moduly pro integraci robota NAO s aplikací.
2. **Úprava URL**:
   - Otevřete soubor zodpovědný za odesílání audia z robota na middleware.
   - Vyhledejte řádek, který obsahuje proměnnou `self.api_url`.
   - Změňte hodnotu této proměnné z:
     ```python
     self.api_url = 'http://172.20.10.4:5000/upload'
     ```
     na novou URL adresu serveru, který hostuje middleware aplikaci.

3. **Uložení a nasazení**: Uložte provedené změny a nahrajte upravený modul zpět do robota NAO.

Tímto krokem je robot NAO propojen s middleware aplikací a je připraven na interakci s OpenAI API prostřednictvím serveru.


## Author
👤 Filip Nachtman

## 📝 License
Copyright © 2024 Dsa-jpg. This project is MIT licensed.
