from app.models.scraper import FacebookScraperModel
from app.views.report_generator import WordReportView

class MainController:
    def __init__(self):
        self.model = FacebookScraperModel()
        self.view = WordReportView()

    async def run_process(self):
        print("\n>>> Iniciando proceso de extracción")


        url_objetivo = "https://www.facebook.com/me"

        posts = await self.model.fetch_posts(url_perfil=url_objetivo, max_scrolls=50)

        if posts:
            print(f">>> Se han recuperado {len(posts)} publicaciones. Generando reporte...")
            self.view.generate_report(posts)
        else:
            print(">>> El modelo no regresó datos. Verificar conexión o inicio de sesión")

        print("\n>>> Proceso finalizado \n")