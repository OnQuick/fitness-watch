# 🚀 Fitness Watch - Wdrażanie w Azure Cloud Shell

## 📋 Wymagane pliki:

- `main.tf` - Konfiguracja Terraform
- `outputs.tf` - Dane wyjściowe
- `deploy.sh` - Skrypt wdrażania

## 🚀 Wdrażanie:

### Krok 1: Wgraj pliki do Cloud Shell

1. Otwórz [portal.azure.com](https://portal.azure.com)
2. Kliknij Cloud Shell (terminal)
3. Wybierz Bash
4. Wgraj pliki: `main.tf`, `outputs.tf`, `deploy.sh`

### Krok 2: Uruchom wdrożenie

```bash
chmod +x deploy.sh
./deploy.sh
```

### Krok 3: Wdróż API

W nowym terminalu Cloud Shell:

```bash
npm install -g azure-functions-core-tools@4
func azure functionapp publish <function-app-name> --python
```

### Krok 4: Testuj API

```bash
curl <api-url>/health
curl <api-url>/fitness-data
```

## 📊 Co zostanie wdrożone:

- Resource Group: `fitness-watch-rg`
- IoT Hub: `fitness-hub<random>`
- CosmosDB: `fitness-cosmos<random>`
- Stream Analytics: `fitness-stream<random>`
- Azure Functions: `fitness-api<random>`
- Storage Account: `fitness<random>`

## 🎯 Gotowe!

Twój system Fitness Watch działa w Azure!
