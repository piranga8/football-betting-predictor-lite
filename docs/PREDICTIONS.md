# 🎯 Guía de Predicciones

## 📊 Fuentes de Datos

El dashboard combina datos de **dos fuentes** para proporcionar información completa:

### 1. Football API 7 - Datos en Tiempo Real

- ⚽ Marcadores actuales
- ⏱️ Minuto del partido
- 🟥 Tarjetas rojas
- 🏆 Competiciones
- 📅 Jornadas/Rounds

### 2. PrimaTips - Predicciones y Odds

- 🎯 Predicción favorita (1, X, 2)
- 💰 Cuotas (odds)
- 📊 Probabilidades implícitas
- 🔗 Link al análisis completo

---

## 🤝 Cómo se Emparejan los Datos

### Matching Automático

El sistema usa **similitud de nombres** para emparejar partidos:

```python
# Football API 7
"Manchester United" vs "Bournemouth"

# PrimaTips
"Man United" vs "Bournemouth"

# Similitud: 85% → Match encontrado ✅
```

### Algoritmo de Matching

1. Normalizar nombres (minúsculas, sin espacios extra)
2. Calcular similitud con `SequenceMatcher`
3. Promediar similitud de ambos equipos
4. Si similitud > 70% → Match válido

### Ejemplos de Matching

| Football API 7 | PrimaTips | Similitud | Match |
|----------------|-----------|-----------|-------|
| Manchester United | Man United | 85% | ✅ |
| FC Barcelona | Barcelona | 92% | ✅ |
| Atlético Madrid | Atletico Madrid | 98% | ✅ |
| Real Betis | Betis | 68% | ❌ |

---

## 📊 Cómo se Calculan las Probabilidades

### Probabilidades Implícitas

Las odds (cuotas) se convierten en probabilidades:

```python
Probabilidad = 1 / Odd
```

### Ejemplo Práctico

**Odds:**
- Local: 1.80
- Empate: 3.50
- Visitante: 6.00

**Cálculo:**
```python
prob_home = 1 / 1.80 = 0.556 (55.6%)
prob_draw = 1 / 3.50 = 0.286 (28.6%)
prob_away = 1 / 6.00 = 0.167 (16.7%)

# Total = 100.9% (overround de 0.9%)
```

**Normalización:**
```python
total = 0.556 + 0.286 + 0.167 = 1.009

prob_home = 0.556 / 1.009 = 0.551 (55.1%)
prob_draw = 0.286 / 1.009 = 0.283 (28.3%)
prob_away = 0.167 / 1.009 = 0.165 (16.5%)

# Total = 100.0% ✅
```

---

## 📝 Tipos de Predicciones

### Predicciones Simples

- **1**: Victoria local
- **X**: Empate
- **2**: Victoria visitante

### Predicciones Dobles (Double Chance)

- **1X**: Local o Empate
- **12**: Local o Visitante
- **X2**: Empate o Visitante

### Selección de Predicción

La predicción favorita se selecciona por:

1. **Tip destacado** (si existe) → Prioridad
2. **Menor odd** → Mayor probabilidad implícita

---

## 🖥️ Visualización en el Dashboard

### Sección de Predicciones

Para cada partido con predicción:

```
🎯 Predicción: Victoria Local
[Ver en PrimaTips]

Cuotas: 1: 1.80 | X: 3.50 | 2: 6.00

[================= Local: 55.1% =================]
Local: 55% | Empate: 28% | Visitante: 17%
```

### Componentes

1. **Badge verde**: Predicción favorita
2. **Link**: Abre el análisis completo en PrimaTips
3. **Cuotas**: Odds para 1, X, 2
4. **Barra de probabilidad**: Visual de la predicción
5. **Desglose**: Probabilidades de todos los resultados

---

## ⚙️ Configuración

### Habilitar/Deshabilitar Predicciones

En el sidebar:

- ☑️ **Mostrar predicciones**: Activa el scraping y matching
- ☐ **Mostrar predicciones**: Solo muestra datos de Football API 7

### Performance

**Con predicciones activadas:**
- 1 request a Football API 7
- 1 request de scraping a PrimaTips
- ~3-5 segundos total

**Con predicciones desactivadas:**
- 1 request a Football API 7
- ~2-3 segundos total

---

## 📊 Estadísticas de Matching

El dashboard muestra:

```
📊 Total Partidos: 15
🔴 En Vivo: 3
⚽ Goles: 12
🟥 Tarjetas Rojas: 1
🎯 Con Predicción: 10  ← Partidos que hicieron match
```

**Tasa de matching típica:** 60-80%

### ¿Por qué no todos los partidos tienen predicción?

1. **Diferentes fuentes de datos**: PrimaTips puede no cubrir todas las ligas
2. **Nombres diferentes**: Umbral de similitud no alcanzado
3. **Timing**: Partido no disponible en PrimaTips aún

---

## 🔧 API del Scraper

### Uso Básico

```python
from src.data.primatips_scraper import PrimaTipsScraper

scraper = PrimaTipsScraper()

# Predicciones de hoy
predictions = scraper.get_predictions_today()

# Predicciones de fecha específica
predictions = scraper.get_predictions_by_date('2025-12-15')

# Solo partidos en vivo (ayer, hoy, mañana)
live_preds = scraper.get_live_predictions()
```

### Estructura de Datos

```python
{
    'id': '12345',
    'home_team': 'Manchester United',
    'away_team': 'Bournemouth',
    'teams': 'Manchester United - Bournemouth',
    'minute': "67'",
    'is_live': True,
    'home_score': 2,
    'away_score': 1,
    'predicted': '1',
    'predicted_name': 'Local',
    'odds': {
        'home': 1.80,
        'draw': 3.50,
        'away': 6.00
    },
    'probabilities': {
        'home': 0.551,
        'draw': 0.283,
        'away': 0.165
    },
    'link': 'https://primatips.com/tips/2025-12-15#g_12345',
    'date': '2025-12-15',
    'source': 'PrimaTips'
}
```

---

## 🔗 Match Matcher API

### Uso Básico

```python
from src.utils.match_matcher import (
    find_matching_prediction,
    enrich_matches_with_predictions
)

# Buscar predicción para un partido
match = {...}  # Partido de Football API 7
predictions = [...]  # Lista de predicciones

prediction = find_matching_prediction(match, predictions, threshold=0.7)

# Enriquecer todos los partidos
enriched_matches = enrich_matches_with_predictions(matches, predictions)
```

### Configurar Umbral de Similitud

```python
# Umbral bajo: más matches pero menos precisión
prediction = find_matching_prediction(match, predictions, threshold=0.6)

# Umbral alto: menos matches pero más precisión
prediction = find_matching_prediction(match, predictions, threshold=0.8)

# Default: 0.7 (balance)
```

---

## ⚠️ Limitaciones

### 1. Scraping

- **No es API oficial**: Depende de la estructura HTML de PrimaTips
- **Puede fallar**: Si PrimaTips cambia su diseño
- **Rate limiting**: Evitar hacer demasiadas requests

### 2. Matching

- **Imperfecto**: Basado en similitud de nombres
- **Falsos negativos**: Partidos que existen pero no coinciden
- **Falsos positivos**: Muy raros con threshold 0.7

### 3. Predicciones

- **Informativas**: No son garantía de resultado
- **Dependen de odds**: Reflejan el consenso del mercado
- **No son consejos**: Usar solo como referencia

---

## 🔮 Futuras Mejoras

### v2.0

- ⏳ Modelo Poisson propio basado en datos históricos
- ⏳ Comparación: PrimaTips vs Poisson
- ⏳ Tracking de precisión de predicciones
- ⏳ Múltiples fuentes de predicciones

### v2.1

- ⏳ Predicciones in-play dinámicas
- ⏳ Actualización de probabilidades según minuto
- ⏳ Impacto de tarjetas rojas en predicción
- ⏳ Gráficos de evolución de probabilidades

---

## 🤔 FAQ

### ¿Por qué usar scraping en vez de API?

PrimaTips no ofrece API pública. El scraping es la única forma de obtener sus predicciones automáticamente.

### ¿Es legal hacer scraping?

Sí, siempre que:
- Solo leas información pública
- No sobrecargues el servidor
- Respetes robots.txt
- No redistribuyas comercialmente

### ¿Cómo mejorar el matching?

Puedes ajustar el `threshold` en `match_matcher.py`. Valores recomendados:
- 0.6: Más matches, menos preciso
- 0.7: Balance (default)
- 0.8: Menos matches, más preciso

### ¿Qué pasa si PrimaTips cambia su HTML?

El scraper dejará de funcionar. Habría que actualizar los selectores CSS en `primatips_scraper.py`.

### ¿Puedo agregar otras fuentes de predicciones?

¡Sí! Solo necesitas:
1. Crear un nuevo scraper (ej: `otro_sitio_scraper.py`)
2. Usar el mismo formato de salida
3. Agregar al `match_matcher`

---

**Última actualización:** 15 de Diciembre, 2025
