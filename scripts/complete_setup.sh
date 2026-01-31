#!/bin/bash

# LexConductor - Complete Setup (solo variables faltantes)
# IBM Dev Day AI Demystified Hackathon 2026

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Header
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                                                                ║"
echo "║        LexConductor - Completar Configuración                  ║"
echo "║        IBM Dev Day AI Demystified Hackathon 2026               ║"
echo "║                                                                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}✗ Archivo .env no encontrado${NC}"
    echo "Ejecuta primero: cat .env.setup >> .env"
    exit 1
fi

# Load current .env
source .env 2>/dev/null || true

echo "Detectando qué credenciales ya tienes configuradas..."
echo ""

# Check what's already configured
HAS_API_KEY=false
HAS_WO=false
HAS_PROJECT=false
HAS_CLOUDANT=false
HAS_COS=false

if [ ! -z "$WATSONX_API_KEY" ] && [ "$WATSONX_API_KEY" != "your_ibm_cloud_api_key_here" ]; then
    HAS_API_KEY=true
    echo -e "${GREEN}✓${NC} IBM Cloud API Key configurada"
fi

if [ ! -z "$WO_INSTANCE" ] && [ "$WO_INSTANCE" != "https://your-instance.watson-orchestrate.ibm.com" ]; then
    HAS_WO=true
    echo -e "${GREEN}✓${NC} watsonx Orchestrate configurado"
fi

if [ ! -z "$WATSONX_PROJECT_ID" ] && [ "$WATSONX_PROJECT_ID" != "your_watsonx_project_id_here" ]; then
    HAS_PROJECT=true
    echo -e "${GREEN}✓${NC} watsonx.ai Project ID configurado"
fi

if [ ! -z "$CLOUDANT_URL" ] && [ "$CLOUDANT_URL" != "https://your-cloudant-instance.cloudantnosqldb.appdomain.cloud" ]; then
    HAS_CLOUDANT=true
    echo -e "${GREEN}✓${NC} Cloudant configurado"
fi

if [ ! -z "$COS_INSTANCE_ID" ] && [ "$COS_INSTANCE_ID" != "your_cos_instance_id_here" ]; then
    HAS_COS=true
    echo -e "${GREEN}✓${NC} Cloud Object Storage configurado"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Temporary file for new credentials
TEMP_FILE=".env.new_credentials"
> $TEMP_FILE

# watsonx Orchestrate (MANDATORY)
if [ "$HAS_WO" = false ]; then
    echo -e "${YELLOW}⚠ watsonx Orchestrate NO configurado (OBLIGATORIO)${NC}"
    echo ""
    echo "Instrucciones:"
    echo "1. Abre: ${BLUE}https://cloud.ibm.com/resources${NC}"
    echo "2. Busca 'watsonx Orchestrate' en AI/Machine Learning"
    echo "3. Click 'Launch watsonx Orchestrate'"
    echo "4. Ve a Settings → API Details"
    echo "5. Copia 'Service Instance URL' y 'API Key'"
    echo ""
    read -p "Presiona Enter cuando estés listo..."
    echo ""
    
    read -p "Pega el Service Instance URL: " WO_INSTANCE
    if [ ! -z "$WO_INSTANCE" ]; then
        echo "WO_INSTANCE=$WO_INSTANCE" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} WO_INSTANCE guardado"
    fi
    
    read -p "Pega el API Key de Orchestrate: " WO_API_KEY
    if [ ! -z "$WO_API_KEY" ]; then
        echo "WO_API_KEY=$WO_API_KEY" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} WO_API_KEY guardado"
    fi
    echo ""
fi

# watsonx.ai Project ID
if [ "$HAS_PROJECT" = false ]; then
    echo -e "${YELLOW}⚠ watsonx.ai Project ID NO configurado${NC}"
    echo ""
    echo "Instrucciones:"
    echo "1. Abre: ${BLUE}https://dataplatform.cloud.ibm.com/wx/home${NC}"
    echo "2. Click en 'Sandbox' (ya existe automáticamente)"
    echo "3. Ve a la pestaña 'Manage'"
    echo "4. Copia el 'Project ID' (formato UUID)"
    echo ""
    read -p "Presiona Enter cuando estés listo..."
    echo ""
    
    read -p "Pega el Project ID: " WATSONX_PROJECT_ID
    if [ ! -z "$WATSONX_PROJECT_ID" ]; then
        echo "WATSONX_PROJECT_ID=$WATSONX_PROJECT_ID" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} WATSONX_PROJECT_ID guardado"
    fi
    echo ""
fi

# Cloudant
if [ "$HAS_CLOUDANT" = false ]; then
    echo -e "${YELLOW}⚠ Cloudant NO configurado${NC}"
    echo ""
    echo "Instrucciones:"
    echo "1. Abre: ${BLUE}https://cloud.ibm.com/resources${NC}"
    echo "2. Busca tu instancia de Cloudant"
    echo "3. Click en la instancia → Service credentials"
    echo "4. Si no hay credenciales, click 'New credential'"
    echo "5. Copia: url, username, password"
    echo ""
    read -p "Presiona Enter cuando estés listo..."
    echo ""
    
    read -p "Pega el Cloudant URL: " CLOUDANT_URL
    if [ ! -z "$CLOUDANT_URL" ]; then
        echo "CLOUDANT_URL=$CLOUDANT_URL" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} CLOUDANT_URL guardado"
    fi
    
    read -p "Pega el Cloudant Username: " CLOUDANT_USERNAME
    if [ ! -z "$CLOUDANT_USERNAME" ]; then
        echo "CLOUDANT_USERNAME=$CLOUDANT_USERNAME" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} CLOUDANT_USERNAME guardado"
    fi
    
    read -p "Pega el Cloudant Password: " CLOUDANT_PASSWORD
    if [ ! -z "$CLOUDANT_PASSWORD" ]; then
        echo "CLOUDANT_PASSWORD=$CLOUDANT_PASSWORD" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} CLOUDANT_PASSWORD guardado"
    fi
    echo ""
fi

# Cloud Object Storage
if [ "$HAS_COS" = false ]; then
    echo -e "${YELLOW}⚠ Cloud Object Storage NO configurado${NC}"
    echo ""
    echo "Instrucciones:"
    echo "1. Abre: ${BLUE}https://cloud.ibm.com/resources${NC}"
    echo "2. Busca tu instancia de Cloud Object Storage"
    echo "3. Click en la instancia → Service credentials"
    echo "4. Si no hay credenciales, click 'New credential'"
    echo "5. Copia: resource_instance_id"
    echo ""
    read -p "Presiona Enter cuando estés listo..."
    echo ""
    
    read -p "Pega el COS Instance ID (resource_instance_id): " COS_INSTANCE_ID
    if [ ! -z "$COS_INSTANCE_ID" ]; then
        echo "COS_INSTANCE_ID=$COS_INSTANCE_ID" >> $TEMP_FILE
        echo -e "${GREEN}✓${NC} COS_INSTANCE_ID guardado"
    fi
    echo ""
fi

# Check if any new credentials were added
if [ -s $TEMP_FILE ]; then
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "Nuevas credenciales recopiladas:"
    echo ""
    cat $TEMP_FILE
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo ""
    echo "¿Qué deseas hacer con estas credenciales?"
    echo ""
    echo "1) Agregar al archivo .env (recomendado)"
    echo "2) Guardar en .env.new_credentials (manual)"
    echo "3) Descartar (cancelar)"
    echo ""
    read -p "Selecciona una opción [1-3]: " choice
    
    case $choice in
        1)
            cat $TEMP_FILE >> .env
            echo ""
            echo -e "${GREEN}✓ Credenciales agregadas a .env${NC}"
            rm $TEMP_FILE
            ;;
        2)
            mv $TEMP_FILE .env.new_credentials
            echo ""
            echo -e "${GREEN}✓ Credenciales guardadas en .env.new_credentials${NC}"
            echo "Para agregarlas manualmente: cat .env.new_credentials >> .env"
            ;;
        3)
            rm $TEMP_FILE
            echo ""
            echo -e "${YELLOW}⚠ Credenciales descartadas${NC}"
            ;;
        *)
            rm $TEMP_FILE
            echo ""
            echo -e "${RED}✗ Opción inválida. Credenciales descartadas.${NC}"
            ;;
    esac
else
    echo -e "${GREEN}✓ Todas las credenciales ya están configuradas!${NC}"
    rm $TEMP_FILE
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Próximo paso: Verificar la configuración"
echo "Ejecuta: ${BLUE}python3 scripts/verify_setup.py${NC}"
echo ""
