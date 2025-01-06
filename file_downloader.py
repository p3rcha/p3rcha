import os
import rich
import rich.prompt
import sys
import time
import yt_dlp
import subprocess

download_folder = "/data/data/com.termux/files/home/storage/downloads"

def check_dependencies():
    try:
        subprocess.run(["pip", "install", "-U", "yt-dlp", "ffmpeg", "rich"], check=True)
        rich.print(f"Dependecias instaladas")
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
    title()
    main_menu()
    option = rich.prompt.Prompt.ask("\nIngrese una opcion")

    try:
        option = int(option)
    except ValueError:
        rich.print("[red]Por favor, ingrese un numero valido![/red]")
        time.sleep(1)
        main()

    if option == 1:
        download_file()
    elif option == 2:
        config()
    elif option == 0:
        exit_program()
    else:
        rich.print("[red]Escoga una opcion valida![/red]")
        main()

def download_file():
    title()
    rich.print("[bold]Ingrese el URL del archivo")
    rich.print("O ingrese 0 para volver al menu")
    url = rich.prompt.Prompt.ask("\n[bold blue]※> [/bold blue]URL").strip()
    if url == "0":
        main()
    elif not url:
        rich.print("[red]El URL no puede estar vacio, intente de nuevo[/red]")
        time.sleep(1)
        download_file()
    elif not (".com" in url or ".net" in url or ".me" in url or ".org" in url):
        rich.print("[red]Por favor, ingrese un URL valido (que contenga .com, .net, .org o .me)[/red]")
        time.sleep(1)
        download_file()
    else:
        title()
        rich.print("1. Para descargar MP4 (Video)")
        rich.print("2. Para descargar MP3 (Audio)")
        rich.print("3. Para descargar JPG (Imagen)")
        rich.print("\n0. Para volver al menu")
    
        download_option = rich.prompt.Prompt.ask("\n[blue]•[/blue] Escoge una opcion")

        try:
            download_option = int(download_option)
        except ValueError:
            rich.print("[red]Por favor, ingrese un numero valido![/red]")
            time.sleep(1)
            return download_file()
        
        if download_option == 1:
            download_video(url)
        elif download_option == 2:
            download_audio(url)
        elif download_option == 3:
            download_image(url)
        elif download_option == 0:
            main()
        else:
            rich.print("[red]Opcion invalida.[/red]")
            time.sleep(1)
            download_file()

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

        rich.print("[green]Descarga completada con exito[/green]")

        notify_media_store(file_path)
    except Exception as e:
        rich.print(f"[red]Error durante la descarga: {e}[/red]")

    time.sleep(2)
    main()

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
            }
        ],
    }

    try:
        title()
        rich.print("[bold]Descargando en formato MP3...[/bold]")
        rich.print(f"[gray]Ruta de descarga: {download_folder}[/gray]")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        file_path = file_output % {'title': 'audio_name', 'ext': 'mp3'}

        rich.print("[green]Descarga completada con exito[/green]")

        notify_media_store(file_path)
    except Exception as e:
        rich.print(f"[red]Error durante la descarga: {e}[/red]")

    time.sleep(2)
    main()

def download_image(url):
    main()

def config():
    title()
    rich.print("[bold]Configuraciones actuales:[/bold]")    
    if download_folder == "/data/data/com.termux/files/home/storage/downloads":
        rich.print(f"[bold]1.[/bold] Directorio de descargas: '{download_folder}'[cursive dim] / Por defecto[/cursive dim]")
    else:
        rich.print(f"[bold]1.[/bold] Directorio de descargas: '{download_folder}'")
    rich.print("\n[bold]0.[/bold] Regresar al menu principal")

    option = rich.prompt.Prompt.ask("\nIngrese una opcion")
    
    if option == "0":
        main()
    else:
        title()
        rich.print("[red]Esta opcion aun no esta lista, o es una opcion invalida[/red]")
        time.sleep(1)
        config()

def notify_media_store(file_path):
    os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{file_path}")

if __name__ == "__main__":
    check_dependencies()
    main()
