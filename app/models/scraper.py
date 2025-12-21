from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import asyncio

class FacebookScraperModel:
    def __init__(self, auth_path="facebook_auth.json"):
        self.auth_path = auth_path

    async def fetch_posts(self, url_perfil, max_scrolls=50):
        print(f"---Iniciando con credenciales: {self.auth_path}---")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)

            #Cargar cookies
            try:
                context = await browser.new_context(storage_state=self.auth_path)
            except FileNotFoundError:
                print(f"---ERROR. No se econtró el archivo: {self.auth_path}---")
                await browser.close()
                return []
            
            page = await context.new_page()
            
            print(f"---Entrando a la URL: {url_perfil}---")
            await page.goto(url_perfil)

            #Esperar el primer post
            try:
                await page.wait_for_selector("div[dir='auto']", timeout=20000)
            except:
                print("---No se encontraron posts o la carga es muy lenta.---")
                await browser.close()
                return []

            #Scroll infinito
            print(f"--- Iniciando Scroll ---")
            last_height = await page.evaluate("document.body.scrollHeight")
            intentos_sin_cambios = 0

            for i in range(max_scrolls):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  

                espera = random.randint(3000, 6000)
                await page.wait_for_timeout(espera)

                new_height = await page.evaluate("document.body.scrollHeight")
                if new_height == last_height:
                    intentos_sin_cambios += 1
                    print (f". -> Sin cambios... (Intento {intentos_sin_cambios}/3)")
                    if intentos_sin_cambios >= 3:
                        print("--- Final del historial disponible. ---")
                        break
                else:
                    intentos_sin_cambios = 0
                    print(f".  -> Bloque {i+1}/{max_scrolls} cargado.")
                last_height = new_height

            #extracción de HTML
            print("--- Extrayendo contenido... ---")
            content = await page.content()
            await browser.close()

            return self._parse_data(content)
        
    def _parse_data(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text_elements = soup.find_all("div", attrs={"dir": "auto"})

        datos = []
        vistos = set()
        
        print(f"--- Se encontraron {len(text_elements)} bloques de texto potenciales. Filtrando... ---")

        for element in text_elements:
            texto_limpio = element.get_text(separator="\n", strip=True)
            
            # FILTROS DE LIMPIEZA:
            # 1. Longitud: Descartamos "Me gusta", "Comentar", fechas cortas, nombres solos.
            # 2. Duplicados: Si ya guardamos ese texto exacto, lo saltamos.
            if len(texto_limpio) > 15 and texto_limpio not in vistos:
                datos.append(texto_limpio)
                vistos.add(texto_limpio)
        
        return datos