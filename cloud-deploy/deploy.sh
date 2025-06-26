#!/bin/bash

echo "🚀 Wdrażanie Fitness Watch w Azure Cloud Shell"
echo "=============================================="

# Inicjalizacja Terraform
echo "📦 Inicjalizacja Terraform..."
terraform init

# Planowanie wdrożenia
echo "📋 Planowanie wdrożenia..."
terraform plan -out=tfplan

# Wdrożenie
echo "🚀 Wdrażanie (może potrwać 10-15 minut)..."
terraform apply tfplan

# Pobierz dane wyjściowe
echo ""
echo "📊 Dane wyjściowe:"
echo "=================="
terraform output

echo ""
echo "✅ Wdrożenie zakończone!"
echo ""
echo "🌐 API URL: $(terraform output -raw function_app_url)"
echo "📚 Dokumentacja: $(terraform output -raw function_app_url)/docs"
echo ""
echo "📋 Następne kroki:"
echo "1. Wdróż kod API (w nowym terminalu Cloud Shell):"
echo "   npm install -g azure-functions-core-tools@4"
echo "   func azure functionapp publish $(terraform output -raw function_app_name) --python"
echo ""
echo "2. Skopiuj dane IoT Hub do symulatora:"
echo "   IoT Hub: $(terraform output -raw iot_hub_name)"
echo "   Connection String: $(terraform output -raw iot_hub_connection_string)" 