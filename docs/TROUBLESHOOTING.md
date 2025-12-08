# 🐛 Guía de Solución de Problemas

## ❌ Error 403: "You are not subscribed to this API"

### Síntoma

Al ejecutar el dashboard, ves:

```
❌ Error 403: {"message":"You are not subscribed to this API."}
```

Pero cuando pruebas en Postman, **funciona correctamente**.

### Causa

RapidAPI requiere **headers HTTP específicos** que Postman agrega automáticamente, pero Python no.

### Solución

Ya está corregido en el código actual. El `api_consumer.py` ahora incluye:

```python
self.headers = {
    'x-rapidapi-key': api_key,
    'x-rapidapi-host': 'betfair-sports-data-fast-and-reliable.p.rapidapi.com',
    'Accept': 'application/json',  # ← OBLIGATORIO
    'User-Agent': 'Mozilla/5.0'     # ← OBLIGATORIO
}
```

### Verificación

1. **Actualiza el código:**
   ```bash
   git pull origin main
   ```

2. **Verifica tu API key:**
   ```bash
   cat .env | grep FOOTBALL_API_KEY
   ```

3. **Ejecuta con modo debug:**
   El código ahora imprime los headers que envía:
   ```
   🔍 Llamando: https://...
   🔑 Headers: {'x-rapidapi-key': '...', ...}
   📊 Params: {...}
   📡 Status: 200
   ```

4. **Prueba de nuevo:**
   ```bash
   streamlit run app.py
   ```

---

## ⚠️ Otros Problemas Comunes

### 1. "ModuleNotFoundError: No module named 'X'"

**Solución:**
```bash
pip install -r requirements.txt
```

### 2. "API Key no configurada"

**Verificar:**
```bash
# ¿Existe el archivo .env?
ls -la .env

# ¿Tiene contenido?
cat .env

# Si no existe, crear desde ejemplo
cp .env.example .env
```

Luego editar `.env` y agregar tu key de RapidAPI.

### 3. "Rate limit alcanzado"

**Causas:**
- Has excedido tu cuota mensual
- Demasiadas requests en poco tiempo

**Solución:**
```env
# En .env, aumentar el intervalo de refresh
REFRESH_INTERVAL=1800  # 30 minutos en vez de 15
```

### 4. Dashboard se congela o no responde

**Solución:**
```bash
# Detener (Ctrl+C en la terminal)
# Reiniciar
streamlit run app.py
```

### 5. "Error al instalar scipy en Windows"

**Solución:**
```powershell
# Instalar Visual C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Luego:
python -m pip install --upgrade pip setuptools wheel
pip install scipy
pip install -r requirements.txt
```

### 6. "No se muestran partidos en vivo"

**Posibles causas:**
- No hay partidos en este momento
- Las ligas seleccionadas no tienen partidos
- La API no devuelve datos

**Verificar:**
1. Activar modo Mock para ver si el dashboard funciona
2. Probar con otras ligas
3. Verificar que la API responde en Postman

---

## 🔍 Debugging Avanzado

### Ver logs de requests HTTP

El código ahora imprime información de debug:

```python
🔍 Llamando: https://betfair-sports-data-fast-and-reliable.p.rapidapi.com/getCompetitions
🔑 Headers: {
    'x-rapidapi-key': '6428f42...', 
    'x-rapidapi-host': 'betfair-sports-data-fast-and-reliable.p.rapidapi.com',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}
📊 Params: {'id': '1'}
📡 Status: 200
```

### Probar API manualmente en Python

```python
import requests

url = "https://betfair-sports-data-fast-and-reliable.p.rapidapi.com/getCompetitions"
headers = {
    'x-rapidapi-key': 'TU_KEY_AQUI',
    'x-rapidapi-host': 'betfair-sports-data-fast-and-reliable.p.rapidapi.com',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}
params = {'id': '1'}

response = requests.get(url, headers=headers, params=params)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### Verificar suscripción en RapidAPI

1. Ir a [RapidAPI Dashboard](https://rapidapi.com/developer/billing)
2. Verificar "My Subscriptions"
3. Buscar "Betfair Sports Data"
4. Confirmar que está activa

---

## 📧 Soporte

Si el problema persiste:

1. **Verificar que tienes la última versión:**
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```

2. **Abrir un Issue en GitHub:**
   - [football-betting-predictor-lite/issues](https://github.com/piranga8/football-betting-predictor-lite/issues)
   - Incluir:
     - Mensaje de error completo
     - Output de `pip list`
     - Sistema operativo

3. **Probar con modo Mock:**
   Si el problema es con la API, usa el modo Mock mientras lo resuelves:
   - En el sidebar: ✅ "Usar datos de prueba (Mock)"

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Tienes Python 3.9 o superior (`python --version`)
- [ ] Instalaste las dependencias (`pip install -r requirements.txt`)
- [ ] Existe el archivo `.env` con tu API key
- [ ] La API key es correcta y la suscripción está activa
- [ ] Hiciste `git pull` para obtener la última versión
- [ ] Probaste en Postman y funciona
- [ ] El modo Mock funciona correctamente

---

**Última actualización:** Diciembre 2025
