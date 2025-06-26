# 🌐 Wdrażanie przez Azure Cloud Shell

## Krok 1: Otwórz Azure Cloud Shell

1. Przejdź do [portal.azure.com](https://portal.azure.com)
2. Zaloguj się na swoje konto Azure
3. Kliknij ikonę **Cloud Shell** (terminal) w górnym pasku
4. Wybierz **Bash** (nie PowerShell)
5. Wybierz **Create storage** jeśli to pierwszy raz

## Krok 2: Wgraj pliki

### Opcja A: Przez Git (jeśli masz repo)

```bash
git clone https://github.com/your-username/fitness-watch.git
cd fitness-watch/infrastructure
```

### Opcja B: Przez upload

1. W Cloud Shell kliknij ikonę **Upload/Download files** (📁)
2. Wybierz **Upload**
3. Wgraj wszystkie pliki z folderu `infrastructure/`
4. W terminalu przejdź do folderu: `cd infrastructure`

## Krok 3: Wdrażanie

```bash
# Inicjalizacja Terraform
terraform init

# Planowanie wdrożenia
terraform plan

# Wdrożenie (potwierdź wpisując 'yes')
terraform apply
```

## Krok 4: Pobierz dane wyjściowe

```bash
# Wyświetl wszystkie outputy
terraform output

# Pobierz konkretne wartości
terraform output -raw function_app_name
terraform output -raw iot_hub_name
terraform output -raw cosmos_db_account_name
```

## Krok 5: Wdróż API

W nowym terminalu Cloud Shell:

```bash
# Wgraj pliki backend
cd fitness-watch/backend

# Zainstaluj Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Pobierz nazwę Function App
FUNCTION_APP_NAME=$(cd ../infrastructure && terraform output -raw function_app_name)

# Wdróż API
func azure functionapp publish "$FUNCTION_APP_NAME" --python
```

## Krok 6: Testowanie

```bash
# Pobierz URL API
API_URL=$(cd infrastructure && terraform output -raw function_app_url)

# Test health check
curl "$API_URL/health"

# Test pobierania danych
curl "$API_URL/fitness-data"

# Test statystyk
curl "$API_URL/fitness-stats"
```

## Krok 7: Konfiguracja symulatora

Pobierz dane IoT Hub:

```bash
cd infrastructure
terraform output -raw iot_hub_name
terraform output -raw iot_hub_connection_string
```

Zaktualizuj `device-simulator/main.py` z tymi danymi.

## Krok 8: Uruchom symulator

W lokalnym terminalu:

```bash
cd device-simulator
pip install azure-iot-device
python main.py
```

## 🎉 Gotowe!

Twój system jest teraz w pełni wdrożony i działa w chmurze Azure!
