import time
from scraper import obtener_partidos
from db import init_db, save_partidos, get_latest_partidos



def run_worker():
    init_db()

    while True:
        try:
            print("🔄 Scrapeando...")

            nuevo = obtener_partidos()

            



            if nuevo is None:
                print("❌ Error en scraping")

            elif len(nuevo) == 0:
                print("ℹ️ No hay partidos en este momento")

            else:
                ultimo = get_latest_partidos()

                if not ultimo or nuevo != ultimo:
                    save_partidos(nuevo)
                    print("🆕 Cambio detectado, guardado")

                    # 💾 guardar JSON
                    import json
                    with open("partidos.json", "w", encoding="utf-8") as f:
                        json.dump(nuevo, f, ensure_ascii=False, indent=2)

                    # 🚀 subir a GitHub
                    import os
                    os.system("git add partidos.json")
                    os.system(f'git commit -m "update partidos {time.strftime("%H:%M:%S")}"')
                    os.system("git push")
                    print("⏭ Cambios arriba")

                else:
                    print("⏭ Sin cambios, no se guarda ni se sube")


        except Exception as e:
            print("❌ Error:", str(e))

        time.sleep(1800)



if __name__ == "__main__":
    run_worker()
