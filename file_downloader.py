import os
import rich
import rich.prompt
import sys
import time
import yt_dlp
import subprocess
import importlib

download_folder = "/data/data/com.termux/files/home/storage/downloads"

def check_and_install(package):
    if importlib.util.find_spec(package) is None:
        rich.print(f"[yellow]Instalando {package}...[/yellow]")
        subprocess.run(["pip", "install", package], check=True)
        rich.print(f"[green]{package} instalado[/green]")
    else:
        rich.print(f"[green]{package} ya esta instalado[/green]")

def check_dependencies():
    try:
        dependencies = ["yt-dlp", "ffmpeg", "rich"]
        for package in dependencies:
            check_and_install(package)
        rich.print(f"Dependencias instaladas")
    except subprocess.CalledProcessError:
        title()
        rich.print("[red]Error al instalar dependencias. Asegurese de que pip este instalado y funcionando.[/red]")
        time.sleep(1)
        exit(1)

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()

def title():
    clear_screen()
    rich.print("[bold on blue]<====  Descargador de archivos ====>[/bold on blue]\n")

def main_menu():
    rich.print("[bold]1.[/bold] Descargar archivo")
    rich.print("[bold]2.[/bold] Configuraciones")
    rich.print("\n[bold]0.[/bold] Salir")

def exit_program():
    title()
    rich.print("[italic]Hecho por P3rcha")
    rich.print("\nSaliendo...")
    sys.exit(0)

def main():
    while True:
        title()
        main_menu()
        option = rich.prompt.Prompt.ask("\nIngrese una opción")

        try:
            option = int(option)
        except ValueError:
            rich.print("[red]Por favor, ingrese un número válido![/red]")
            time.sleep(1)
            continue

        if option == 1:
            download_file()
        elif option == 2:
            config()
        elif option == 0:
            exit_program()
        else:
            rich.print("[red]Escoge una opción válida![/red]")
            time.sleep(1)

def download_file():
    while True:
        title()
        rich.print("[bold]Ingrese el URL del archivo")
        rich.print("O ingrese 0 para volver al menú")
        url = rich.prompt.Prompt.ask("\n[bold blue]※> [/bold blue]URL").strip()

        if url == "0":
            return
        elif not url:
            rich.print("[red]El URL no puede estar vacío, intente de nuevo[/red]")
            time.sleep(1)
            continue
        elif not (".com" in url or ".net" in url or ".me" in url or ".org" in url or ".be" in url):
            rich.print("[red]Por favor, ingrese un URL válido (que contenga .com, .net, .org, .me o .be)[/red]")
            time.sleep(1)
            continue
        else:
            while True:
                title()
                rich.print("1. Para descargar MP4 (Video)")
                rich.print("2. Para descargar MP3 (Audio)")
                rich.print("3. Para descargar JPG (Imagen)")
                rich.print("\n0. Para volver al menú")
                
                download_option = rich.prompt.Prompt.ask("\n[blue]•[/blue] Escoge una opción")

                try:
                    download_option = int(download_option)
                except ValueError:
                    rich.print("[red]Por favor, ingrese un número válido![/red]")
                    time.sleep(1)
                    continue
                
                if download_option == 1:
                    download_video(url)
                elif download_option == 2:
                    download_audio(url)
                elif download_option == 3:
                    download_image(url)
                elif download_option == 0:
                    return
                else:
                    rich.print("[red]Opción inválida.[/red]")
                    time.sleep(1)

def download_video(url):
    os.makedirs(download_folder, exist_ok=True)
    file_output = f"{download_folder}/%(title)s.%(ext)s"
    options = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": file_output,
        "merge_output_format": "mp4",
    }

    try:
        title()
        rich.print("[bold]Descargando en formato MP4...[/bold]")
        rich.print(f"[gray]Ruta de descarga: {download_folder}[/gray]")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        file_path = file_output % {'title': 'video_name', 'ext': 'mp4'}

        rich.print("[green]Descarga completada con éxito[/green]")

        notify_media_store(file_path)
    except Exception as e:
        rich.print(f"[red]Error durante la descarga: {e}[/red]")
    time.sleep(2)

def download_audio(url):
    os.makedirs(download_folder, exist_ok=True)
    file_output = f"{download_folder}/%(title)s.%(ext)s"
    options = {
        "format": "bestaudio/best",
        "outtmpl": file_output,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            },
            {
                "key": "FFmpegMetadata"
            }
        ],
        "postprocessor_args": [
            "-vn",
        ],
        "prefer_ffmpeg": True,
    }

    try:
        title()
        rich.print("[bold]Descargando en formato MP3...[/bold]")
        rich.print(f"[gray]Ruta de descarga: {download_folder}[/gray]")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        rich.print("[green]Descarga completada con éxito[/green]")

        notify_media_store(download_folder)
    except Exception as e:
        rich.print(f"[red]Error durante la descarga: {e}[/red]")
    time.sleep(2)

def download_image(url):
    os.makedirs(download_folder, exist_ok=True)
    file_output = f"{download_folder}/%(title)s.%(ext)s"
    options = {
        "format": "bestimage",
        "outtmpl": file_output,
    }

    try:
        title()
        rich.print("[bold]Descargando imagen...[/bold]")
        rich.print(f"[gray]Ruta de descarga: {download_folder}[/gray]")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        file_path = file_output % {'title': 'image_name', 'ext': 'jpg'}

        rich.print("[green]Descarga completada con exito[/green]")

        notify_media_store(file_path)
    except Exception as e:
        rich.print(f"[red]Error durante la descarga: {e}[/red]")

    time.sleep(2)

def config():
    while True:
        title()
        rich.print("[bold]Configuraciones actuales:[/bold]")
        if download_folder == "/data/data/com.termux/files/home/storage/downloads":
            rich.print(f"[bold]1.[/bold] Directorio de descargas: '{download_folder}'[cursive dim] / Por defecto[/cursive dim]")
        else:
            rich.print(f"[bold]1.[/bold] Directorio de descargas: '{download_folder}'")
        rich.print("\n[bold]0.[/bold] Regresar al menú principal")

        option = rich.prompt.Prompt.ask("\nIngrese una opción")
        
        if option == "0":
            return
        else:
            title()
            rich.print("[red]Esta opción aún no está lista, o es una opción inválida[/red]")
            time.sleep(1)

def notify_media_store(file_path):
    try:
        subprocess.run(["am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file://{file_path}"], check=True)
        print(f"Galeria se actualizo en: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error al actualizar la galeria: {e}")

if __name__ == "__main__":
    check_dependencies()
    main()
