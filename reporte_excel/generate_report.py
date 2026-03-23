#!/usr/bin/env python3
"""
Script de línea de comandos para generar reportes Excel desde Clockify
"""
import sys
import argparse
from datetime import datetime, timedelta
from excel_generator import ClockifyToExcelConverter


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Genera reportes Excel desde registros de Clockify',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Reporte del mes actual
  python generate_report.py --current-month

  # Reporte del mes anterior
  python generate_report.py --last-month

  # Reporte de la semana anterior (lunes a domingo)
  python generate_report.py --last-week

  # Reporte de rango específico
  python generate_report.py --start 2025-11-01 --end 2025-11-30

  # Reporte de los últimos 7 días
  python generate_report.py --last-days 7

  # Reporte con nombre de archivo personalizado
  python generate_report.py --current-month --output mi_reporte.xlsx
        """
    )
    
    parser.add_argument(
        '--start',
        type=str,
        help='Fecha de inicio (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--end',
        type=str,
        help='Fecha de fin (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--current-month',
        action='store_true',
        help='Genera reporte del mes actual'
    )
    
    parser.add_argument(
        '--last-month',
        action='store_true',
        help='Genera reporte del mes anterior'
    )
    
    parser.add_argument(
        '--last-week',
        action='store_true',
        help='Genera reporte de la semana anterior (lunes a domingo)'
    )
    
    parser.add_argument(
        '--last-days',
        type=int,
        help='Genera reporte de los últimos N días'
    )
    
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Nombre del archivo de salida (default: reporte_horas_YYYYMM.xlsx)'
    )
    
    return parser.parse_args()


def get_date_range(args):
    """Determina el rango de fechas basándose en los argumentos"""
    today = datetime.now()
    
    if args.current_month:
        start_date = datetime(today.year, today.month, 1)
        end_date = today
        default_filename = f"reporte_horas_{today.strftime('%Y%m')}.xlsx"
        
    elif args.last_month:
        # Primer día del mes anterior
        first_day_current = datetime(today.year, today.month, 1)
        last_day_previous = first_day_current - timedelta(days=1)
        start_date = datetime(last_day_previous.year, last_day_previous.month, 1)
        end_date = last_day_previous
        default_filename = f"reporte_horas_{last_day_previous.strftime('%Y%m')}.xlsx"
        
    elif args.last_week:
        # Lunes de la semana anterior
        start_date = today - timedelta(days=today.weekday() + 7)
        # Domingo de la semana anterior
        end_date = start_date + timedelta(days=6)
        
        # Ignorar días del mes anterior - ajustar start_date al 1° del mes actual si es necesario
        first_day_current_month = datetime(today.year, today.month, 1)
        if start_date < first_day_current_month:
            start_date = first_day_current_month
            print(f"⚠️  Nota: Se ajustó la fecha de inicio al 1° del mes actual ({start_date.strftime('%Y-%m-%d')})")
        
        default_filename = f"reporte_horas_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.xlsx"
        
    elif args.last_days:
        end_date = today
        start_date = today - timedelta(days=args.last_days)
        default_filename = f"reporte_horas_ultimos_{args.last_days}_dias.xlsx"
        
    elif args.start and args.end:
        try:
            start_date = datetime.strptime(args.start, '%Y-%m-%d')
            end_date = datetime.strptime(args.end, '%Y-%m-%d')
            default_filename = f"reporte_horas_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx"
        except ValueError as e:
            print(f"❌ Error: Formato de fecha inválido. Use YYYY-MM-DD")
            print(f"   Detalle: {e}")
            sys.exit(1)
    else:
        # Por defecto: mes actual
        start_date = datetime(today.year, today.month, 1)
        end_date = today
        default_filename = f"reporte_horas_{today.strftime('%Y%m')}.xlsx"
    
    # Usa el nombre de archivo personalizado si se proporcionó
    output_file = args.output if args.output else default_filename
    
    return start_date, end_date, output_file


def main():
    """Función principal"""
    args = parse_arguments()
    
    # Obtiene el rango de fechas
    start_date, end_date, output_file = get_date_range(args)
    
    # Valida que la fecha de inicio sea antes que la de fin
    if start_date > end_date:
        print("❌ Error: La fecha de inicio debe ser anterior a la fecha de fin")
        sys.exit(1)
    
    print(f"📅 Generando reporte:")
    print(f"   Desde: {start_date.strftime('%Y-%m-%d')}")
    print(f"   Hasta: {end_date.strftime('%Y-%m-%d')}")
    print(f"   Archivo: {output_file}")
    print()
    
    # Crea el conversor y genera el reporte
    try:
        converter = ClockifyToExcelConverter()
        converter.generate_report(start_date, end_date, output_file)
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
