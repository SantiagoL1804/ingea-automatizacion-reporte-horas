# Generador de Reportes Excel desde Clockify

Este módulo procesa registros de tiempo de Clockify y genera una planilla Excel formateada con integración opcional de Jira.

## Características

- ✅ Extrae registros de tiempo de Clockify
- ✅ Genera Excel con formato específico y 9 columnas
- ✅ Agrega automáticamente registro de "Descanso" (0.5 horas) por cada día trabajado
- ✅ Determina lugar de trabajo (Remoto/Oficina) según día de la semana
- ✅ Busca IDs de Jira (IAPP-XX) en descripciones o mediante API
- ✅ Formato Excel profesional con colores y bordes

## Estructura de Columnas

1. **Subproyecto**: Nombre del proyecto en Clockify
2. **Fecha**: Formato mm/dd/aaaa
3. **Horas**: Duración calculada del registro
4. **Tipo**: "Técnico" (o "Descanso" para el registro diario de 0.5h)
5. **Etapa**: Siempre "00-Otro"
6. **Area**: Siempre "00-Otro"
7. **Lugar Trabajo**: 
   - "Remoto": Miércoles, Viernes, Sábado, Domingo
   - "Oficina": Lunes, Martes, Jueves
8. **ID Tarea (Planner/Jira)**: Extrae IAPP-XX del texto o busca en Jira
9. **Comentario**: Descripción del registro de Clockify

## Configuración

### Variables de Entorno Requeridas

Ya existen en tu `.env`:
```bash
CLOCKIFY_API_KEY=...
CLOCKIFY_WORKSPACE_ID=...
CLOCKIFY_USER_ID=...
CLOCKIFY_PROJECT_ID=...
```

### Variables de Entorno Opcionales (Jira)

Agrega estas líneas a tu `.env` si quieres integración completa con Jira:

```bash
# Jira Configuration (opcional)
JIRA_URL=https://tu-dominio.atlassian.net
JIRA_EMAIL=tu-email@ejemplo.com
JIRA_API_KEY=tu-api-key-de-jira
```

**Nota**: Si no configuras Jira, el sistema igual funciona y extrae IDs de Jira (IAPP-XX) directamente del texto de descripción.

### Cómo obtener API Key de Jira

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click en "Create API token"
3. Copia el token generado
4. Úsalo en `JIRA_API_KEY`

## Instalación de Dependencias

```bash
cd ~/ingea-automatizacion-reporte-horas
source clockify_env/bin/activate
pip install openpyxl requests python-dotenv
```

## Uso

### Opción 1: Generar reporte del mes actual

```bash
cd ~/ingea-automatizacion-reporte-horas/reporte_excel
python excel_generator.py
```

Esto generará un archivo `reporte_horas_YYYYMM.xlsx` con todos los registros del mes actual.

### Opción 2: Usar como módulo en Python

```python
from datetime import datetime
from excel_generator import ClockifyToExcelConverter

converter = ClockifyToExcelConverter()

# Define rango de fechas
start_date = datetime(2025, 11, 1)
end_date = datetime(2025, 11, 30)

# Genera el reporte
converter.generate_report(
    start_date=start_date,
    end_date=end_date,
    output_file="reporte_noviembre_2025.xlsx"
)
```

### Opción 3: Personalizar por línea de comandos

Puedes crear un wrapper script para facilitar el uso:

```python
#!/usr/bin/env python3
import sys
from datetime import datetime
from excel_generator import ClockifyToExcelConverter

if len(sys.argv) >= 3:
    start = datetime.strptime(sys.argv[1], '%Y-%m-%d')
    end = datetime.strptime(sys.argv[2], '%Y-%m-%d')
    output = sys.argv[3] if len(sys.argv) > 3 else f"reporte_{start.strftime('%Y%m%d')}_{end.strftime('%Y%m%d')}.xlsx"
else:
    print("Uso: python generate_report.py YYYY-MM-DD YYYY-MM-DD [output.xlsx]")
    sys.exit(1)

converter = ClockifyToExcelConverter()
converter.generate_report(start, end, output)
```

## Funcionalidades Detalladas

### Búsqueda de IDs de Jira

El sistema busca IDs de Jira en este orden:

1. **Extracción directa**: Busca patrones `IAPP-\d+` en la descripción
2. **API de Jira** (si está configurada): Busca por similitud de texto en el resumen
3. **Fallback**: Retorna `N/A` si no encuentra nada

### Registro de Descanso Automático

Por cada día que tenga al menos un registro de tiempo, se agrega automáticamente:
- Subproyecto: "General"
- Horas: 0.5
- Tipo: "Descanso"
- Comentario: "Descanso diario"

### Cálculo de Lugar de Trabajo

- **Remoto**: Miércoles (2), Viernes (4), Fin de semana (5, 6)
- **Oficina**: Resto de días laborables

## Ejemplo de Salida

El Excel generado tendrá este aspecto:

| Subproyecto | Fecha | Horas | Tipo | Etapa | Area | Lugar Trabajo | ID Tarea | Comentario |
|-------------|--------|-------|------|-------|------|---------------|----------|------------|
| SINUY-ING | 11/04/2025 | 2.5 | Técnico | 00-Otro | 00-Otro | Oficina | IAPP-123 | Se trabaja en feature login |
| General | 11/04/2025 | 0.5 | Descanso | 00-Otro | 00-Otro | Oficina | | Descanso diario |
| SINUY-ING | 11/06/2025 | 4.0 | Técnico | 00-Otro | 00-Otro | Remoto | IAPP-124 | Se trabaja en fix database |
| General | 11/06/2025 | 0.5 | Descanso | 00-Otro | 00-Otro | Remoto | | Descanso diario |

## Solución de Problemas

### Error: "No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Error: "❌ Error fetching Clockify entries"
- Verifica que las variables de entorno estén correctamente configuradas
- Verifica tu conexión a internet
- Verifica que tu API key de Clockify sea válida

### IDs de Jira no se encuentran
- Asegúrate de incluir el ID (ej: IAPP-123) en la descripción del registro de Clockify
- O configura las variables de Jira para búsqueda automática

## Archivos

- `excel_generator.py`: Módulo principal
- `README.md`: Esta documentación
- `timers_fetcher.py`: (Para implementar fetcher independiente si lo necesitas)

## Pasos

- cd reporte_excel
- python3 generate_report.py --last-week