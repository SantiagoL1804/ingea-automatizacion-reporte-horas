import re
import sys
from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright, expect

from report_reader import get_previous_week_report_path, load_report_rows

dev_url = "http://localhost:3000"
dev_username = "santiago.larrique"
dev_password = "tachi00&"
dev_cliente_id = "9"  # Select by visible text
dev_proyecto_id = "22"
dev_subproyecto_id = "81"  # TODO: Add subproject name after checking available options

prod_url = "https://ingea-web.fly.dev"
prod_username = "santiago.larrique"
prod_password = "tachi00&"
prod_cliente_id = "9"  # TODO: Add client id
prod_proyecto_id = "22"  # TODO: Add project id
prod_subproyecto_id = "81"  # TODO: Add subproject id

def run(playwright: Playwright, rows) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{dev_url}/users/sign_in")
    page.get_by_role("textbox", name="Username").click()
    page.get_by_role("textbox", name="Username").fill(dev_username)
    page.get_by_role("textbox", name="Contraseña").click()
    page.get_by_role("textbox", name="Contraseña").fill(dev_password)
    page.get_by_role("checkbox", name="Recordarme").check()
    page.get_by_role("button", name="Iniciar sesión").click()
    
    # Wait for navigation after login
    page.wait_for_load_state("networkidle")
    
    page.locator(".btn").first.click()

    for row in rows:
        page.get_by_role("link", name=" Nuevo registro (libre)").click() 
        page.wait_for_timeout(2000)

        cliente = page.get_by_label("Cliente")
        if cliente.is_visible():
            page.get_by_label("Cliente").select_option(value=dev_cliente_id)
            page.wait_for_timeout(1000)
            page.get_by_label("Proyecto", exact=True).select_option(value=dev_proyecto_id)
        
        page.wait_for_timeout(1000)
        page.get_by_label("Subproyecto", exact=True).select_option(value=dev_subproyecto_id)

        page.get_by_role("textbox", name="Fecha").fill(row["Fecha"])
        page.get_by_role("spinbutton", name="Horas").click()
        page.get_by_role("spinbutton", name="Horas").fill(row["Horas"])
        page.get_by_label("Tipo").select_option(row["Tipo"])
        page.get_by_label("Etapa").select_option(row["Etapa"])
        page.get_by_label("Area", exact=True).select_option(row["Area"])
        page.get_by_label("Lugar Trabajo").select_option(row["Lugar Trabajo"])
        page.get_by_role("textbox", name="ID Tarea (Planner/Jira)").click()
        page.get_by_role("textbox", name="ID Tarea (Planner/Jira)").fill(
            row["ID Tarea (Planner/Jira)"]
        )
        page.get_by_role("textbox", name="Comentario").click()
        page.get_by_role("textbox", name="Comentario").fill(row["Comentario"])
        page.get_by_role("button", name="Guardar").click()

    # ---------------------
    input("Press Enter to close browser...") # ELIMINAR DESPUES DE TERMINAR
    context.close()
    browser.close()


with sync_playwright() as playwright:
    report_path = get_previous_week_report_path()
    if not report_path.exists():
        print(f"❌ Report not found: {report_path}")
        print("Generate it first in reporte_excel/reportes before running this script.")
        sys.exit(1)
    rows = load_report_rows(Path(report_path))
    run(playwright, rows)