# Fitness Watch - System IoT z Azure

Kompletny system fitness watch wykorzystujący Azure IoT Hub, CosmosDB i Azure Functions.

## 🚀 Szybkie uruchomienie za pomocą Azure CLI

### Wymagania wstępne

- Azure CLI
- Terraform
- Azure Functions Core Tools
- Python 3.9+

### 1. **Logowanie i konfiguracja**

```bash
# Logowanie do Azure
az login

# Sprawdzenie aktualnej subskrypcji
az account show

# Lista dostępnych subskrypcji (jeśli masz więcej)
az account list --output table

# Ustawienie konkretnej subskrypcji (jeśli potrzebne)
az account set --subscription "nazwa-subskrypcji"
```

### 2. **Wdrożenie infrastruktury przez Terraform**

```bash
# Przejdź do folderu infrastruktury
cd infrastructure

# Inicjalizacja Terraform
terraform init

# Planowanie wdrożenia
terraform plan

# Wdrożenie infrastruktury
terraform apply
```

### 3. **Pobranie danych wyjściowych**

```bash
# Wyświetl wszystkie outputy
terraform output

# Pobierz konkretne wartości
FUNCTION_APP_NAME=$(terraform output -raw function_app_name)
IOT_HUB_NAME=$(terraform output -raw iot_hub_name)
COSMOS_ACCOUNT_NAME=$(terraform output -raw cosmos_db_account_name)
```

### 4. **Wdrożenie Azure Functions**

```bash
# Przejdź do folderu backend
cd ../backend

# Zainstaluj Azure Functions Core Tools (jeśli nie masz)
npm install -g azure-functions-core-tools@4

# Wdróż funkcje
func azure functionapp publish "$FUNCTION_APP_NAME" --python
```

### 5. **Konfiguracja zmiennych środowiskowych**

```bash
# Pobierz klucz CosmosDB
COSMOS_KEY=$(az cosmosdb keys list --name "$COSMOS_ACCOUNT_NAME" --resource-group "iot-terraform-rg" --query primaryMasterKey -o tsv)

# Ustaw zmienne środowiskowe dla Function App
az functionapp config appsettings set \
  --name "$FUNCTION_APP_NAME" \
  --resource-group "iot-terraform-rg" \
  --settings \
    COSMOS_ENDPOINT="https://$COSMOS_ACCOUNT_NAME.documents.azure.com:443/" \
    COSMOS_KEY="$COSMOS_KEY" \
    COSMOS_DATABASE_NAME="fitness-data" \
    COSMOS_CONTAINER_NAME="telemetry"
```

### 6. **Pobranie connection string dla IoT Hub**

```bash
# Pobierz connection string dla urządzenia
IOT_HUB_CONNECTION_STRING=$(az iot hub device-identity connection-string show \
  --hub-name "$IOT_HUB_NAME" \
  --resource-group "iot-terraform-rg" \
  --device-id "fitness-watch-001" \
  --query connectionString -o tsv)

echo "IoT Hub Connection String: $IOT_HUB_CONNECTION_STRING"
```

### 7. **Uruchomienie symulatora urządzeń**

```bash
# Przejdź do folderu symulatora
cd ../device-simulator

# Zainstaluj zależności
pip install azure-iot-device

# Zaktualizuj connection string w main.py (z kroku 6)
# Następnie uruchom symulator
python main.py
```

### 8. **Testowanie API**

```bash
# Pobierz URL Function App
FUNCTION_URL=$(az functionapp show \
  --name "$FUNCTION_APP_NAME" \
  --resource-group "iot-terraform-rg" \
  --query defaultHostName -o tsv)

# Test health check
curl "https://$FUNCTION_URL/health"

# Test pobierania danych
curl "https://$FUNCTION_URL/fitness-data"

# Test statystyk
curl "https://$FUNCTION_URL/fitness-stats"
```

### 9. **Dodatkowe komendy diagnostyczne**

```bash
# Sprawdź status Function App
az functionapp show --name "$FUNCTION_APP_NAME" --resource-group "iot-terraform-rg"

# Sprawdź logi Function App
az functionapp logs tail --name "$FUNCTION_APP_NAME" --resource-group "iot-terraform-rg"

# Sprawdź status IoT Hub
az iot hub show --name "$IOT_HUB_NAME" --resource-group "iot-terraform-rg"

# Sprawdź status CosmosDB
az cosmosdb show --name "$COSMOS_ACCOUNT_NAME" --resource-group "iot-terraform-rg"
```

### 10. **Czyszczenie (jeśli potrzebne)**

```bash
# Usuń całą infrastrukturę
cd infrastructure
terraform destroy
```

## 📝 Ważne uwagi:

1. **Przed uruchomieniem** upewnij się, że masz zainstalowane wszystkie wymagane narzędzia
2. **Kolejność wykonywania** jest ważna - najpierw infrastruktura, potem aplikacja
3. **Zmienne środowiskowe** muszą być ustawione po wdrożeniu infrastruktury
4. **Connection string** dla symulatora musi być zaktualizowany w pliku `device-simulator/main.py`

## 📁 Struktura projektu

```
fitness-watch/
├── backend/                 # Azure Functions API
├── device-simulator/        # Symulator urządzenia IoT
├── infrastructure/          # Terraform konfiguracja
├── cloud-deploy/           # Alternatywne wdrożenie
└── docs/                   # Dokumentacja
```

## 🔗 Dodatkowe zasoby

- [Dokumentacja API](backend/README.md)
- [Instrukcje Postman](POSTMAN_INSTRUCTIONS.md)
- [Wdrażanie przez Cloud Shell](infrastructure/cloud_shell_deploy.md)

README add
