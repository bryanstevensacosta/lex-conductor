# Guía Rápida - Obtener Credenciales IBM Cloud

**LexConductor - Hackathon IBM Dev Day 2026**

## 🚀 Inicio Rápido (35 minutos)

### 1. watsonx Orchestrate (5 min)

```bash
WO_INSTANCE=https://api.us-south.watson.cloud.ibm.com/instances/...
WO_API_KEY=...
```

**Pasos:**
1. [IBM Cloud](https://cloud.ibm.com/) → Resource list → watsonx Orchestrate
2. Settings ⚙️ → API details
3. Copiar **Service Instance URL** → `WO_INSTANCE`
4. **Generate API Key** → `WO_API_KEY`

---

### 2. watsonx.ai (5 min)

```bash
WATSONX_API_KEY=...
WATSONX_PROJECT_ID=...
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Pasos:**
1. [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home) → **Usa el Sandbox Project** (creado automáticamente)
2. Projects → View all projects → Selecciona "Sandbox"
3. Manage → General → Copiar **Project ID** → `WATSONX_PROJECT_ID`
4. [API Keys](https://cloud.ibm.com/iam/apikeys) → Create → Copiar → `WATSONX_API_KEY`

**💡 Tip**: El Sandbox Project se crea automáticamente al registrarte. ¡No necesitas crear uno nuevo!

---

### 3. Cloudant (10 min)

```bash
CLOUDANT_URL=https://xxx.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=...
```

**Pasos:**
1. [IBM Cloud](https://cloud.ibm.com/) → Create resource → Cloudant
2. Plan: **Lite**, Region: **US South**, Name: `lexconductor-cloudant`
3. Service credentials → New credential → Role: **Manager**
4. View credentials → Copiar `url` y `apikey`
5. Launch Dashboard → Create Database (3 veces):
   - `golden_clauses`
   - `historical_decisions`
   - `regulatory_mappings`

---

### 4. Cloud Object Storage (10 min)

```bash
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=...
COS_INSTANCE_ID=crn:v1:bluemix:...
```

**Pasos:**
1. [IBM Cloud](https://cloud.ibm.com/) → Create resource → Cloud Object Storage
2. Plan: **Lite**, Name: `lexconductor-cos`
3. Service credentials → New credential
   - **¡IMPORTANTE!** Include HMAC Credential: **ON**
   - Role: **Writer**
4. View credentials → Copiar `apikey` y `iam_serviceid_crn`
5. Buckets → Create bucket → Customize:
   - Name: `watsonx-hackathon-regulations-[tu-nombre]`
   - Resiliency: **Regional**, Location: **us-south**
6. Crear carpetas: `EU/`, `UK/`, `US/`, `templates/`

---

### 5. Code Engine (5 min)

```bash
CODE_ENGINE_PROJECT=lexconductor-agents
CODE_ENGINE_REGION=jp-osa
```

**Pasos:**
1. [IBM Cloud](https://cloud.ibm.com/) → Create resource → Code Engine
2. Location: **Osaka (jp-osa)** ← ¡Requerido!
3. Project name: `lexconductor-agents`

---

## ✅ Verificación

```bash
# Activar entorno
source .venv/bin/activate

# Verificar setup
python scripts/verify_setup.py

# Probar conexiones
python scripts/test_connections.py
```

---

## 📋 Template .env

```bash
# watsonx Orchestrate
WO_INSTANCE=https://api.us-south.watson.cloud.ibm.com/instances/tu-id
WO_API_KEY=tu_api_key

# watsonx.ai
WATSONX_API_KEY=tu_ibm_cloud_api_key
WATSONX_PROJECT_ID=12345678-1234-1234-1234-123456789abc
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Cloudant
CLOUDANT_URL=https://tu-instance.cloudantnosqldb.appdomain.cloud
CLOUDANT_API_KEY=tu_api_key
CLOUDANT_USERNAME=tu_username
CLOUDANT_PASSWORD=tu_password

# Cloud Object Storage
COS_ENDPOINT=s3.us-south.cloud-object-storage.appdomain.cloud
COS_API_KEY=tu_api_key
COS_INSTANCE_ID=crn:v1:bluemix:public:cloud-object-storage:...
COS_AUTH_ENDPOINT=https://iam.cloud.ibm.com/identity/token
COS_BUCKET_NAME=watsonx-hackathon-regulations-aikings

# Code Engine
CODE_ENGINE_PROJECT=lexconductor-agents
CODE_ENGINE_REGION=jp-osa
```

---

## 🆘 Problemas Comunes

| Error | Solución |
|-------|----------|
| "Invalid API key" | Regenerar la clave, copiar completa |
| "Project not found" | Verificar Project ID en watsonx.ai |
| "Database not found" | Crear las 3 bases de datos en Cloudant |
| "Bucket does not exist" | Verificar nombre único del bucket |

---

## 📚 Documentación Completa

Ver: `docs/GUIA_CREDENCIALES_ES.md`

---

**Tiempo total**: ~35 minutos  
**Costo**: <$5 (todos en plan Lite/Gratis)  
**Deadline**: 1 de febrero de 2026 - 10:00 AM ET

---

*Equipo: AI Kings 👑*
