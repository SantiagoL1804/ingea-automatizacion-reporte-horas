Scripts disponibles:

1. branch_monitor.py - Detecta cambios de rama y maneja timers:
◦  ✅ Detecta la rama actual
◦  ✅ Para el timer si cambia de rama
◦  ✅ Inicia nuevo timer con la nueva rama (excepto main)
◦  ✅ Guarda el estado en .last_branch
2. continuous_monitor.py - Monitor continuo:
◦  ✅ Ejecuta el monitor cada X segundos (por defecto 30s)
◦  ✅ Manejo de Ctrl+C para parar suavemente
◦  ✅ Logs detallados con timestamps
3. clockify_timer.py - Timer básico con detección de rama
Cómo usar:
cd /home/santiago/ingea-automatizacion-reporte-horas
source clockify_env/bin/activate

# Monitor una vez
python3 branch_monitor.py

# Monitor continuo (cada 30 segundos)
python3 continuous_monitor.py

# Monitor continuo cada 60 segundos
python3 continuous_monitor.py 60

Para automatizar con cron:
# Ejecutar monitor cada 2 minutos durante horas de trabajo
*/2 9-18 * * 1-5 /home/santiago/ingea-automatizacion-reporte-horas/clockify_env/bin/python /home/santiago/ingea-automatizacion-reporte-horas/branch_monitor.py >> /home/santiago/ingea-automatizacion-reporte-horas/branch_monitor.log 2>&1

Lo que hace automáticamente:

•  🔄 Cambias de rama → Para timer actual + Inicia timer nuevo
•  🌿 Vas a main → Para timer actual (no inicia nuevo)
•  ✅ Te quedas en la misma rama → No hace nada
•  📝 Formato del timer: "Se trabaja en nombre-de-rama(con espacios)"