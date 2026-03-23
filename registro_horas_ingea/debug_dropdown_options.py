from playwright.sync_api import sync_playwright

dev_url = "http://localhost:3000"
dev_username = "super.admin"
dev_password = "Aa123456"

def debug_options():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Login
        page.goto(f"{dev_url}/users/sign_in")
        page.get_by_role("textbox", name="Username").fill(dev_username)
        page.get_by_role("textbox", name="Contraseña").fill(dev_password)
        page.get_by_role("checkbox", name="Recordarme").check()
        page.get_by_role("button", name="Iniciar sesión").click()
        
        # Wait for navigation after login
        page.wait_for_load_state("networkidle")
        
        page.locator(".btn").first.click()
        page.get_by_role("link", name=" Nuevo registro (libre)").click()
        
        # Wait for page to load
        page.wait_for_timeout(2000)
        
        # Get all options from Cliente dropdown
        options = page.locator('select#dedicacion_cliente_id option').all()
        
        print("\n=== Available Cliente Options ===")
        for option in options:
            value = option.get_attribute('value')
            text = option.inner_text()
            print(f"Value: '{value}' | Text: '{text}'")
        
        # Select INGEA and wait for projects to load
        print("\n=== Selecting INGEA cliente ===")
        page.get_by_label("Cliente").select_option(label="(ingea) INGEA")
        page.wait_for_timeout(1500)
        
        # Get all options from Proyecto dropdown
        proyecto_options = page.locator('select#dedicacion_proyecto_id option').all()
        
        print("\n=== Available Proyecto Options (for INGEA) ===")
        for option in proyecto_options:
            value = option.get_attribute('value')
            text = option.inner_text()
            print(f"Value: '{value}' | Text: '{text}'")
        
        # If there are projects, select the first one and get subprojects
        if len(proyecto_options) > 1:
            first_proyecto_text = proyecto_options[1].inner_text()
            print(f"\n=== Selecting first proyecto: {first_proyecto_text} ===")
            page.get_by_label("Proyecto", exact=True).select_option(index=1)
            page.wait_for_timeout(1500)
            
            # Get all options from Subproyecto dropdown
            subproyecto_options = page.locator('select#dedicacion_subproyecto_id option').all()
            
            print("\n=== Available Subproyecto Options ===")
            for option in subproyecto_options:
                value = option.get_attribute('value')
                text = option.inner_text()
                print(f"Value: '{value}' | Text: '{text}'")
        
        print("\n=== Keep browser open to inspect ===")
        input("Press Enter to close browser...")
        
        context.close()
        browser.close()

if __name__ == "__main__":
    debug_options()
