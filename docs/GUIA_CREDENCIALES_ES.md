# Guía Completa para Obtener Credenciales de IBM Cloud

**LexConductor - IBM Dev Day AI Demystified Hackathon 2026**  
**Equipo: AI Kings 👑**

Esta guía te ayudará paso a paso a obtener cada variable de entorno necesaria para el proyecto LexConductor.

---

## 📋 Índice de Variables

1. [watsonx Orchestrate](#1-watsonx-orchestrate)
2. [watsonx.ai](#2-watsonxai)
3. [IBM Cloudant](#3-ibm-cloudant)
4. [IBM Cloud Object Storage (COS)](#4-ibm-cloud-object-storage-cos)
5. [IBM Code Engine](#5-ibm-code-engine)
6. [Resumen de Variables](#resumen-de-variables)

---

## 1. watsonx Orchestrate

### Variables Necesarias:
```bash
WO_INSTANCE=https://your-instance.watson-orchestrate.ibm.com
WO_API_KEY=your_watsonx_orchestrate_api_key_here
```

### 📖 Documentación Oficial:
- [Getting credentials for your environments](https://developer.watson-orchestrate.ibm.com/environment/production_import)
- [Getting the API endpoint](https://www.ibm.com/docs/en/watsonx/watson-orchestrate/current?topic=api-getting-endpoint)

### 🔧 Pasos Detallados:

#### Paso 1: Acceder a watsonx Orchestrate
1. Inicia sesión en [IBM Cloud Console](https://cloud.ibm.com/)
2. En el menú de navegación, ve a **Resource list** (Lista de recursos)
3. Bajo la sección **AI / Machine Learning**, busca **watsonx Orchestrate**
4. Haz clic en tu instancia de watsonx Orchestrate

#### Paso 2: Obtener el Service Instance URL (WO_INSTANCE)
1. Una vez dentro de watsonx Orchestrate, haz clic en el ícono de **Settings** (⚙️ engranaje) en la esquina superior derecha
2. Selecciona **Settings** del menú desplegable
3. Ve a la pestaña **API details**
4. Copia el **Service Instance URL**
   - Formato: `https://api.<region>.watson.cloud.ibm.com/instances/<instance-id>`
   - Ejemplo: `https://api.us-south.watson.cloud.ibm.com/instances/abc123-def456`

#### Paso 3: Generar API Key (WO_API_KEY)
1. En la misma página de **API details**
2. Busca la sección de **API Key**
3. Haz clic en **Generate API Key** o **Create API Key**
4. Copia la clave generada inmediatamente (no podrás verla después)
5. Guárdala en un lugar seguro

### ⚠️ Notas Importantes:
- La API key solo se muestra una vez al generarla
- Si pierdes la clave, deberás generar una nueva
- Cada clave tiene permisos específicos para tu instancia

### ✅ Verificación:
```bash
# Configurar el ADK
orchestrate env add prod --instance $WO_INSTANCE --api-key $WO_API_KEY
orchestrate env activate prod
orchestrate auth login
```

---

## 2. watsonx.ai

### Variables Necesarias:
```bash
WATSONX_API_KEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### 📖 Documentación Oficial:
- [IBM watsonx.ai for IBM Cloud](https://ibm.github.io/watsonx-ai-python-sdk/v1.5.0/setup_cloud.html)
- [Managing task credentials](https://www.ibm.com/docs/en/watsonx/wdi/saas?topic=projects-managing-task-credentials)

### 🔧 Pasos Detallados:

#### Paso 1: Acceder al Sandbox Project (Automático)

**¡IMPORTANTE!** Cuando te registras en watsonx.ai, se crea automáticamente un **Sandbox Project**. No necesitas crear un proyecto nuevo.

1. Ve a [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Inicia sesión con tu cuenta de IBM Cloud
3. **El Sandbox Project ya está creado automáticamente**
4. Verás el proyecto en tu dashboard

#### Paso 1b: Usar el Sandbox Project (Recomendado para Hackathon)

Si ya tienes el Sandbox Project:
1. En watsonx.ai, ve a **Projects** → **View all projects**
2. Busca el proyecto llamado **"Sandbox"** o similar
3. Haz clic en el proyecto
4. Ve a la pestaña **Manage**
5. En la sección **General** → **Details**, encontrarás el **Project ID**
6. Copia el Project ID (formato UUID)

#### Paso 1c: Crear un Proyecto Nuevo (Opcional)

Solo si prefieres crear un proyecto específico para el hackathon:
1. Haz clic en **Projects** en el menú de navegación
2. Haz clic en **New project**
3. Selecciona **Create an empty project**
4. Nombre: `lexconductor-hackathon`
5. Descripción: "LexConductor - IBM Dev Day Hackathon 2026"
6. Haz clic en **Create**

#### Paso 2: Obtener el Project ID (WATSONX_PROJECT_ID)
1. Dentro de tu proyecto, haz clic en la pestaña **Manage**
2. En la sección **General**, encontrarás el **Project ID**
3. Copia el ID completo
   - Formato: UUID de 36 caracteres
   - Ejemplo: `12345678-1234-1234-1234-123456789abc`

#### Paso 3: Generar IBM Cloud API Key (WATSONX_API_KEY)
1. Ve a [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Haz clic en **Create** (o **Create an IBM Cloud API key**)
3. Completa el formulario:
   - **Name**: `lexconductor-watsonx-key`
   - **Description**: "API key for LexConductor hackathon project"
4. Haz clic en **Create**
5. **¡IMPORTANTE!** Copia la API key inmediatamente
   - Solo se muestra una vez
   - Haz clic en **Copy** o **Download**
   - Guárdala en un lugar seguro

#### Paso 4: Determinar la URL (WATSONX_URL)
Según la región de tu instancia, usa una de estas URLs:

| Región | URL |
|--------|-----|
| **US South (Dallas)** | `https://us-south.ml.cloud.ibm.com` |
| **EU Germany (Frankfurt)** | `https://eu-de.ml.cloud.ibm.com` |
| **Japan (Tokyo)** | `https://jp-tok.ml.cloud.ibm.com` |
| **Australia (Sydney)** | `https://au-syd.ml.cloud.ibm.com` |

**Recomendado para el hackathon**: `https://us-south.ml.cloud.ibm.com`

#### Paso 5: Verificar Acceso al Modelo Granite
1. En watsonx.ai, ve a **Prompt Lab**
2. En el selector de modelos, busca: `ibm/granite-3-8b-instruct`
3. Verifica que el modelo esté disponible
4. Si no lo ves, contacta al soporte del hackathon

### ⚠️ Notas Importantes:
- **Sandbox Project**: Se crea automáticamente al registrarte en watsonx.ai
- **Para el hackathon**: Puedes usar el Sandbox Project o crear uno nuevo
- **Recomendación**: Usa el Sandbox Project para ahorrar tiempo
- La API key de IBM Cloud funciona para todos los servicios de IBM Cloud
- Puedes usar la misma API key para watsonx.ai, Cloudant y COS
- El Project ID es específico de cada proyecto en watsonx.ai

### ✅ Verificación:
```python
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key="tu_api_key_aqui"
)

client = APIClient(credentials, project_id="tu_project_id_aqui")
print("✓ Conexión exitosa a watsonx.ai")
```

---

## 3. IBM Cloudant

### Variables Necesarias:
```bash
CLOUDANT_URL=https://your-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=your_cloudant_api_key_here
CLOUDANT_USERNAME=your_cloudant_username
CLOUDANT_PASSWORD=your_cloudant_password
```

### 📖 Documentación Oficial:
- [Creating an IBM Cloudant instance](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-creating-an-ibm-cloudant-instance-on-ibm-cloud-by-using-the-ibm-cloud-cli)
- [Connecting to IBM Cloudant](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-connecting)
- [Managing access for Cloudant](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-managing-access-for-cloudant)

### 🔧 Pasos Detallados:

#### Paso 1: Crear Instancia de Cloudant
1. Ve a [IBM Cloud Console](https://cloud.ibm.com/)
2. Haz clic en **Create resource** (Crear recurso)
3. Busca "Cloudant" en el catálogo
4. Haz clic en **Cloudant**
5. Configura la instancia:
   - **Plan**: Lite (Gratis)
   - **Region**: US South (Dallas)
   - **Service name**: `lexconductor-cloudant`
   - **Resource group**: Default
   - **Authentication method**: IAM and legacy credentials
6. Haz clic en **Create**

#### Paso 2: Crear Service Credentials
1. Ve a tu instancia de Cloudant en la Resource List
2. En el menú lateral, haz clic en **Service credentials**
3. Haz clic en **New credential**
4. Completa el formulario:
   - **Name**: `lexconductor-credentials`
   - **Role**: Manager (para permisos completos)
5. Haz clic en **Add**

#### Paso 3: Obtener las Credenciales
1. Haz clic en **View credentials** junto a la credencial creada
2. Se abrirá un JSON con todas las credenciales
3. Copia los siguientes valores:

```json
{
  "apikey": "tu_api_key_aqui",           // → CLOUDANT_API_KEY
  "host": "xxx-bluemix.cloudant.com",    // → parte de CLOUDANT_URL
  "url": "https://xxx.cloudantnosqldb.appdomain.cloud",  // → CLOUDANT_URL
  "username": "xxx-bluemix",             // → CLOUDANT_USERNAME
  "password": "xxx"                      // → CLOUDANT_PASSWORD
}
```

#### Paso 4: Crear las Bases de Datos
1. Haz clic en **Launch Dashboard** (botón azul en la parte superior)
2. Se abrirá el Cloudant Dashboard
3. Haz clic en **Create Database** (esquina superior derecha)
4. Crea estas tres bases de datos:

**Base de datos 1: golden_clauses**
- Database name: `golden_clauses`
- Partitioning: Non-partitioned
- Clic en **Create**

**Base de datos 2: historical_decisions**
- Database name: `historical_decisions`
- Partitioning: Non-partitioned
- Clic en **Create**

**Base de datos 3: regulatory_mappings**
- Database name: `regulatory_mappings`
- Partitioning: Non-partitioned
- Clic en **Create**

### ⚠️ Notas Importantes:
- El plan Lite es gratuito pero tiene límites:
  - 1 GB de almacenamiento
  - 20 consultas por segundo
  - Suficiente para el hackathon
- Usa IAM authentication (API key) en lugar de legacy credentials cuando sea posible

### ✅ Verificación:
```python
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('tu_api_key_aqui')
client = CloudantV1(authenticator=authenticator)
client.set_service_url('tu_cloudant_url_aqui')

# Listar bases de datos
response = client.get_all_dbs().get_result()
print(f"✓ Bases de datos: {response}")
```

---

## 4. IBM Cloud Object Storage (COS)

### Variables Necesarias:
```bash
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=your_cos_api_key_here
COS_INSTANCE_ID=your_cos_instance_id_here
COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token
COS_BUCKET_NAME=watsonx-hackathon-regulations
```

### 📖 Documentación Oficial:
- [Service credentials](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-service-credentials)
- [Using Python](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-python)
- [HMAC credentials](https://cloud.ibm.com/docs/cloud-object-storage/hmac?topic=cloud-object-storage-uhc-hmac-credentials-main)

### 🔧 Pasos Detallados:

#### Paso 1: Crear Instancia de Cloud Object Storage
1. Ve a [IBM Cloud Console](https://cloud.ibm.com/)
2. Haz clic en **Create resource**
3. Busca "Object Storage" en el catálogo
4. Haz clic en **Cloud Object Storage**
5. Configura la instancia:
   - **Plan**: Lite (Gratis - 25GB)
   - **Service name**: `lexconductor-cos`
   - **Resource group**: Default
6. Haz clic en **Create**

#### Paso 2: Crear Service Credentials con HMAC
1. Ve a tu instancia de COS en la Resource List
2. En el menú lateral, haz clic en **Service credentials**
3. Haz clic en **New credential**
4. **¡IMPORTANTE!** Configura así:
   - **Name**: `lexconductor-cos-credentials`
   - **Role**: Writer
   - **Include HMAC Credential**: **ON** (¡Muy importante!)
   - **Service ID**: (dejar automático)
5. Haz clic en **Add**

#### Paso 3: Obtener las Credenciales
1. Haz clic en **View credentials** junto a la credencial creada
2. Se abrirá un JSON extenso
3. Copia los siguientes valores:

```json
{
  "apikey": "tu_api_key_aqui",                    // → COS_API_KEY
  "iam_serviceid_crn": "crn:v1:bluemix:...",     // → COS_INSTANCE_ID
  "endpoints": "https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints",
  "cos_hmac_keys": {
    "access_key_id": "xxx",                       // Para HMAC (opcional)
    "secret_access_key": "xxx"                    // Para HMAC (opcional)
  }
}
```

#### Paso 4: Determinar el Endpoint (COS_ENDPOINT)
Según tu región, usa uno de estos endpoints:

| Región | Endpoint Público |
|--------|------------------|
| **US South** | `s3.us-south.cloud-object-storage.appdomain.cloud` |
| **US East** | `s3.us-east.cloud-object-storage.appdomain.cloud` |
| **EU Germany** | `s3.eu-de.cloud-object-storage.appdomain.cloud` |
| **EU Great Britain** | `s3.eu-gb.cloud-object-storage.appdomain.cloud` |
| **Japan Tokyo** | `s3.jp-tok.cloud-object-storage.appdomain.cloud` |

**Recomendado para el hackathon**: `s3.us-south.cloud-object-storage.appdomain.cloud`

#### Paso 5: Crear el Bucket
1. En tu instancia de COS, haz clic en **Buckets** (menú lateral)
2. Haz clic en **Create bucket**
3. Selecciona **Customize your bucket**
4. Configura el bucket:
   - **Unique bucket name**: `watsonx-hackathon-regulations-[tu-nombre]`
     - Debe ser globalmente único
     - Solo minúsculas, números y guiones
     - Ejemplo: `watsonx-hackathon-regulations-aikings`
   - **Resiliency**: Regional
   - **Location**: us-south
   - **Storage class**: Standard
5. Haz clic en **Create bucket**

#### Paso 6: Crear Estructura de Carpetas
1. Abre tu bucket recién creado
2. Haz clic en **Upload** → **Folder**
3. Crea estas carpetas:
   - `EU/` (para regulaciones europeas)
   - `UK/` (para regulaciones del Reino Unido)
   - `US/` (para regulaciones de Estados Unidos)
   - `templates/` (para plantillas de contratos)

### ⚠️ Notas Importantes:
- El plan Lite incluye 25GB gratis
- Los nombres de buckets deben ser únicos globalmente
- HMAC credentials son necesarias para compatibilidad S3
- Usa endpoints públicos para desarrollo

### ✅ Verificación:
```python
import ibm_boto3
from ibm_botocore.client import Config

cos_client = ibm_boto3.client(
    "s3",
    ibm_api_key_id="tu_api_key_aqui",
    ibm_service_instance_id="tu_instance_id_aqui",
    config=Config(signature_version="oauth"),
    endpoint_url="https://s3.us-south.cloud-object-storage.appdomain.cloud"
)

# Listar buckets
response = cos_client.list_buckets()
print(f"✓ Buckets: {[b['Name'] for b in response['Buckets']]}")
```

---

## 5. IBM Code Engine

### Variables Necesarias:
```bash
CODE_ENGINE_PROJECT=lexconductor-agents
CODE_ENGINE_REGION=jp-osa
```

### 📖 Documentación Oficial:
- [Code Engine regions](https://cloud.ibm.com/docs/codeengine?topic=codeengine-regions)
- [Getting started with CLI](https://cloud.ibm.com/docs/codeengine?topic=codeengine-cecli-getstart)

### 🔧 Pasos Detallados:

#### Paso 1: Crear Proyecto de Code Engine
1. Ve a [IBM Cloud Console](https://cloud.ibm.com/)
2. Haz clic en **Create resource**
3. Busca "Code Engine" en el catálogo
4. Haz clic en **Code Engine**
5. Haz clic en **Start creating** o **Create project**

#### Paso 2: Configurar el Proyecto
1. Completa el formulario:
   - **Location**: Osaka (jp-osa) - **¡Requerido por el hackathon!**
   - **Project name**: `lexconductor-agents`
   - **Resource group**: Default
2. Haz clic en **Create**

#### Paso 3: Anotar Detalles del Proyecto
1. Una vez creado, ve a tu proyecto
2. Anota:
   - **Project ID**: Se muestra en la página del proyecto
   - **Region**: jp-osa (Osaka)
   - **Project name**: lexconductor-agents

### ⚠️ Notas Importantes:
- **IMPORTANTE**: Debes usar la región Osaka (jp-osa) según los requisitos del hackathon
- Code Engine es serverless - solo pagas por uso
- Las URLs de las aplicaciones se generarán después del despliegue
- Formato de URL: `https://{app-name}.jp-osa.codeengine.appdomain.cloud`

### 📝 URLs de Aplicaciones (se configurarán después)
Estas variables se agregarán después de desplegar las aplicaciones:
```bash
FUSION_AGENT_URL=https://fusion-agent.jp-osa.codeengine.appdomain.cloud
ROUTING_AGENT_URL=https://routing-agent.jp-osa.codeengine.appdomain.cloud
MEMORY_AGENT_URL=https://memory-agent.jp-osa.codeengine.appdomain.cloud
TRACEABILITY_AGENT_URL=https://traceability-agent.jp-osa.codeengine.appdomain.cloud
```

### ✅ Verificación:
```bash
# Instalar CLI de Code Engine (si no está instalado)
ibmcloud plugin install code-engine

# Listar proyectos
ibmcloud ce project list

# Seleccionar proyecto
ibmcloud ce project select --name lexconductor-agents
```

---

## Resumen de Variables

### Archivo .env Completo

Copia este template y reemplaza los valores:

```bash
# ============================================================================
# IBM watsonx Orchestrate
# ============================================================================
WO_INSTANCE=https://api.us-south.watson.cloud.ibm.com/instances/tu-instance-id
WO_API_KEY=tu_watsonx_orchestrate_api_key

# ============================================================================
# IBM watsonx.ai
# ============================================================================
WATSONX_API_KEY=tu_ibm_cloud_api_key
WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789abc
WATSONX_URL=https://us-south.ml.cloud.ibm.com

WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
WATSONX_TEMPERATURE=0.1
WATSONX_MAX_TOKENS=2000

# ============================================================================
# IBM Cloudant (NoSQL Database)
# ============================================================================
CLOUDANT_URL=https://tu-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=tu_cloudant_api_key
CLOUDANT_USERNAME=tu_cloudant_username
CLOUDANT_PASSWORD=tu_cloudant_password

CLOUDANT_DB_GOLDEN_CLAUSES=golden_clauses
CLOUDANT_DB_HISTORICAL_DECISIONS=historical_decisions
CLOUDANT_DB_REGULATORY_MAPPINGS=regulatory_mappings

# ============================================================================
# IBM Cloud Object Storage (COS)
# ============================================================================
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=tu_cos_api_key
COS_INSTANCE_ID=crn:v1:bluemix:public:cloud-object-storage:...
COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token

COS_BUCKET_NAME=watsonx-hackathon-regulations-aikings
COS_REGION=us-south

# ============================================================================
# IBM Code Engine
# ============================================================================
CODE_ENGINE_PROJECT=lexconductor-agents
CODE_ENGINE_REGION=jp-osa

# URLs de agentes (se configurarán después del despliegue)
FUSION_AGENT_URL=https://fusion-agent.jp-osa.codeengine.appdomain.cloud
ROUTING_AGENT_URL=https://routing-agent.jp-osa.codeengine.appdomain.cloud
MEMORY_AGENT_URL=https://memory-agent.jp-osa.codeengine.appdomain.cloud
TRACEABILITY_AGENT_URL=https://traceability-agent.jp-osa.codeengine.appdomain.cloud
```

---

## 🔍 Verificación Final

### Script de Verificación
```bash
# Activar entorno virtual
source .venv/bin/activate

# Verificar configuración
python scripts/verify_setup.py

# Probar conexiones
python scripts/test_connections.py
```

### Checklist de Verificación

- [ ] **watsonx Orchestrate**
  - [ ] WO_INSTANCE configurado
  - [ ] WO_API_KEY configurado
  - [ ] ADK puede conectarse

- [ ] **watsonx.ai**
  - [ ] WATSONX_API_KEY configurado
  - [ ] WATSONX_PROJECT_ID configurado
  - [ ] Modelo Granite 3 8B accesible

- [ ] **Cloudant**
  - [ ] CLOUDANT_URL configurado
  - [ ] CLOUDANT_API_KEY configurado
  - [ ] 3 bases de datos creadas

- [ ] **Cloud Object Storage**
  - [ ] COS_API_KEY configurado
  - [ ] COS_INSTANCE_ID configurado
  - [ ] Bucket creado
  - [ ] 4 carpetas creadas

- [ ] **Code Engine**
  - [ ] Proyecto creado en Osaka
  - [ ] CODE_ENGINE_PROJECT configurado

---

## 🆘 Solución de Problemas

### Error: "Invalid API key"
- Verifica que copiaste la clave completa
- Asegúrate de no tener espacios al inicio o final
- Regenera la clave si es necesario

### Error: "Project not found"
- Verifica el Project ID en watsonx.ai
- Asegúrate de tener acceso al proyecto
- Verifica que el proyecto esté en la región correcta

### Error: "Database not found"
- Verifica que creaste las 3 bases de datos en Cloudant
- Los nombres deben ser exactos (minúsculas, guiones bajos)

### Error: "Bucket does not exist"
- Verifica el nombre del bucket (debe ser único globalmente)
- Asegúrate de que el bucket esté en la región correcta
- Verifica permisos de acceso

---

## 📚 Referencias Adicionales

### Documentación Oficial IBM Cloud
- [IBM Cloud Console](https://cloud.ibm.com/)
- [IBM Cloud Docs](https://cloud.ibm.com/docs)
- [watsonx Orchestrate Docs](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)
- [watsonx.ai Docs](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [Cloudant Docs](https://cloud.ibm.com/docs/Cloudant)
- [Cloud Object Storage Docs](https://cloud.ibm.com/docs/cloud-object-storage)
- [Code Engine Docs](https://cloud.ibm.com/docs/codeengine)

### Soporte
- IBM Cloud Support: https://cloud.ibm.com/unifiedsupport/supportcenter
- Hackathon Slack: Canal #watsonx-orchestrate
- BeMyApp Support: support@bemyapp.com

---

## ⏰ Tiempo Estimado

| Servicio | Tiempo Estimado |
|----------|----------------|
| watsonx Orchestrate | 5 minutos |
| watsonx.ai | 5 minutos |
| Cloudant | 10 minutos |
| Cloud Object Storage | 10 minutos |
| Code Engine | 5 minutos |
| **TOTAL** | **35 minutos** |

---

## 💰 Monitoreo de Costos

### Configurar Alertas
1. Ve a [IBM Cloud Console](https://cloud.ibm.com/)
2. Menú → **Manage** → **Billing and usage**
3. **Spending notifications**
4. Configura alertas en:
   - 25% ($25)
   - 50% ($50)
   - 80% ($80)

### Presupuesto del Hackathon
- **Límite total**: $100 USD
- **Objetivo**: <$5 USD
- **Servicios**: Todos en plan Lite/Gratis

---

**¡Listo!** Ahora tienes todas las credenciales necesarias para comenzar el desarrollo de LexConductor.

**Fecha límite del hackathon**: 1 de febrero de 2026 - 10:00 AM ET

---

*Última actualización: 30 de enero de 2026*  
*Equipo: AI Kings 👑*
