import re
from playwright.sync_api import Playwright, sync_playwright, expect

dev_url = "http://localhost:3000"
dev_username = "santiago.larrique"
dev_password = "tachi00&"
dev_cliente_id = "9"  # Select by visible text
dev_proyecto_id = "22"
dev_subproyecto_id = "81"  # TODO: Add subproject name after checking available options

prod_url = "https://ingea-web.fly.dev"
prod_username = "santiago.larrique"
prod_password = "tachi00&"
prod_cliente_text = ""  # TODO: Add client name
prod_proyecto_text = ""  # TODO: Add project name
prod_subproyecto_text = ""  # TODO: Add subproject name

def run(playwright: Playwright) -> None:
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
    # A PARTIR DE ACA, LOOPEAR POR CADA REGISTRO EN EL EXCEL
    page.get_by_role("link", name=" Nuevo registro (libre)").click()    
    # Wait for the Cliente dropdown to be loaded with options
    page.wait_for_timeout(2000)  # Wait 2 seconds for dropdown to populate
    page.get_by_label("Cliente").select_option(value=dev_cliente_id)
    page.wait_for_timeout(1000)  # Wait for Proyecto dropdown to populate
    page.get_by_label("Proyecto", exact=True).select_option(value=dev_proyecto_id)
    page.wait_for_timeout(1000)  # Wait for Subproyecto dropdown to populate
    page.get_by_label("Subproyecto", exact=True).select_option(value=dev_subproyecto_id)
    page.get_by_role("textbox", name="Fecha").fill("2025-11-03")
    page.get_by_role("spinbutton", name="Horas").click()
    page.get_by_role("spinbutton", name="Horas").fill("4")
    page.get_by_label("Tipo").select_option("Técnico")
    page.get_by_label("Etapa").select_option("00-Otro")
    page.get_by_text("Area Seleccione el area00-").click()
    page.get_by_label("Area", exact=True).select_option("00-Otro")
    page.get_by_label("Area", exact=True).click()
    page.get_by_label("Lugar Trabajo").select_option("Oficina")
    page.get_by_role("textbox", name="ID Tarea (Planner/Jira)").click()
    page.get_by_role("textbox", name="ID Tarea (Planner/Jira)").fill("IAPP-583")
    page.get_by_role("textbox", name="Comentario").click()
    page.get_by_role("textbox", name="Comentario").fill("Arreglo atributos suministros")
    page.get_by_role("button", name="Guardar").click()

    # ---------------------
    input("Press Enter to close browser...") # ELIMINAR DESPUES DE TERMINAR
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)