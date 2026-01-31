# watsonx.ai Sandbox Project - Información Importante

**LexConductor - IBM Dev Day AI Demystified Hackathon 2026**

## 🎯 ¡Descubrimiento Importante!

Cuando te registras en **watsonx.ai**, se crea automáticamente un **Sandbox Project**. **No necesitas crear un proyecto nuevo** para el hackathon.

## 📖 Documentación Oficial

Según la [documentación oficial de IBM](https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects-your-sandbox-project):

> "A project is where you work with data and models by using tools. When you sign up for watsonx.ai, your sandbox project is created automatically, and you can start working in it immediately."

## ✅ Ventajas del Sandbox Project

1. **Creación Automática** - Ya está listo cuando te registras
2. **Ahorro de Tiempo** - No necesitas configurar nada
3. **Listo para Usar** - Puedes empezar inmediatamente
4. **Perfecto para Hackathons** - Ideal para desarrollo rápido

## 🔧 Cómo Usar el Sandbox Project

### Paso 1: Acceder a watsonx.ai

```
1. Ve a: https://dataplatform.cloud.ibm.com/wx/home
2. Inicia sesión con tu cuenta de IBM Cloud
3. El Sandbox Project ya está creado automáticamente
```

### Paso 2: Encontrar el Sandbox Project

```
1. En watsonx.ai, haz clic en "Projects" en el menú
2. Selecciona "View all projects"
3. Busca el proyecto llamado "Sandbox" o similar
4. Haz clic en el proyecto
```

### Paso 3: Obtener el Project ID

```
1. Dentro del Sandbox Project, ve a la pestaña "Manage"
2. En la sección "General" → "Details"
3. Copia el "Project ID" (formato UUID)
4. Ejemplo: 12345678-1234-1234-1234-123456789abc
```

### Paso 4: Usar el Project ID

```bash
# Agregar a tu archivo .env
WATSONX_PROJECT_ID=tu_sandbox_project_id_aqui
```

## 🆚 Sandbox vs Proyecto Nuevo

| Característica | Sandbox Project | Proyecto Nuevo |
|----------------|-----------------|----------------|
| **Creación** | Automática | Manual |
| **Tiempo** | 0 minutos | 2-3 minutos |
| **Configuración** | Ninguna | Nombre, descripción |
| **Listo para usar** | ✅ Inmediato | ⏳ Después de crear |
| **Recomendado para hackathon** | ✅ Sí | ⚠️ Opcional |

## 💡 Recomendación para el Hackathon

**Usa el Sandbox Project** porque:
- ✅ Ya está creado y listo
- ✅ Ahorras 2-3 minutos de configuración
- ✅ Es perfecto para desarrollo rápido
- ✅ Tiene todas las capacidades necesarias

## 📝 Actualización de las Guías

Las siguientes guías han sido actualizadas con esta información:

1. **Guía Completa en Español**: `docs/GUIA_CREDENCIALES_ES.md`
   - Sección 2: watsonx.ai
   - Paso 1: Acceder al Sandbox Project

2. **Guía Rápida en Español**: `docs/GUIA_RAPIDA_ES.md`
   - Paso 2: watsonx.ai (5 min)

3. **Script Interactivo**: `scripts/interactive_setup.sh`
   - Step 2/5: watsonx.ai Project

## 🔍 Cómo Verificar que Tienes el Sandbox Project

```bash
# Después de obtener el Project ID, verifica la conexión
source .venv/bin/activate
python scripts/test_connections.py
```

Si la conexión es exitosa, verás:
```
✓ watsonx.ai: CONNECTED
✓ Found model: ibm/granite-3-8b-instruct
```

## ❓ Preguntas Frecuentes

### ¿Puedo crear un proyecto nuevo en lugar del Sandbox?

Sí, puedes crear un proyecto nuevo si lo prefieres, pero **no es necesario** para el hackathon. El Sandbox Project tiene todas las capacidades que necesitas.

### ¿El Sandbox Project tiene limitaciones?

No, el Sandbox Project tiene las mismas capacidades que cualquier otro proyecto en watsonx.ai. Es completamente funcional.

### ¿Puedo usar el Sandbox Project para producción?

El Sandbox Project es ideal para desarrollo y pruebas. Para producción, se recomienda crear proyectos específicos con nombres descriptivos.

### ¿Qué pasa si no veo el Sandbox Project?

Si no ves el Sandbox Project:
1. Verifica que hayas completado el registro en watsonx.ai
2. Espera unos minutos (puede tardar en aparecer)
3. Refresca la página
4. Si aún no aparece, crea un proyecto nuevo manualmente

## 📚 Referencias

- [IBM Docs: Your sandbox project](https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects-your-sandbox-project)
- [IBM Docs: Creating a project](https://www.ibm.com/docs/en/watsonx/saas?topic=projects-creating-project)
- [IBM Docs: Finding the project ID](https://www.ibm.com/docs/en/SSYOK8/wsj/analyze-data/fm-project-id.html)

## ✅ Checklist Actualizado

Para el hackathon, tu checklist de watsonx.ai ahora es:

- [ ] Acceder a watsonx.ai
- [ ] Encontrar el Sandbox Project (ya creado)
- [ ] Obtener el Project ID del Sandbox
- [ ] Agregar WATSONX_PROJECT_ID al archivo .env
- [ ] Verificar conexión con `python scripts/test_connections.py`

**Tiempo total**: ~3 minutos (en lugar de 5-7 minutos)

---

## 🎉 Resumen

**¡No necesitas crear un proyecto nuevo!** El Sandbox Project está listo y esperándote. Solo necesitas:

1. Acceder a watsonx.ai
2. Encontrar el Sandbox Project
3. Copiar el Project ID
4. Agregarlo a tu `.env`

**Ahorro de tiempo**: 2-3 minutos  
**Complejidad**: Reducida  
**Resultado**: Mismo proyecto funcional

---

*Última actualización: 30 de enero de 2026*  
*Equipo: AI Kings 👑*
