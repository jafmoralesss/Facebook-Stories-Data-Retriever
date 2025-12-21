import asyncio
from app.controllers.main_controller import MainController

if __name__ == "__main__":
    app = MainController()

    try:
        asyncio.run(app.run_process())

    except KeyboardInterrupt:

        print("\n Proceso detenido por el usuario.")