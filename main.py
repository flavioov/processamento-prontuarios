import pathlib
import time

from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from docx import Document

from graph import MyGraph


class NewDocxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            path = pathlib.Path(event.src_path)
            if not is_valid_docx_file(path):
                print(f"📄 Novo prontuário detectado: {path.name}")
                if path.suffix == ".docx":
                    print(f"📁 New .docx file detected: {path}")
                    content = load_docx_content(path)
                    graph = MyGraph(file_name=path.name).get_graph()
                    graph.invoke({"document_content": content})


# Load DOCX file content
def load_docx_content(file_path: Path, retries=5, delay=0.5) -> str:
    for attempt in range(retries):
        try:
            document = Document(file_path)
            content = "\n".join([para.text for para in document.paragraphs])
            print(f"📄 Conteúdo do documento carregado")
            return content
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                raise RuntimeError(
                    f"Falha ao abrir {file_path.name} após {retries} tentativas."
                )
    return ""


def is_valid_docx_file(file_path: Path) -> bool:
    # Ignore temporary or lock files
    filename = file_path.name
    return (
        filename.startswith("~$")  # MS Word lock file
        or filename.startswith(".~lock")  # LibreOffice lock file
        or file_path.stat().st_size > 0  # avoid empty files
    )


def watch_folder(folder_path: str):
    folder = Path(folder_path)
    # ✅ First, process all existing .docx files
    for file in folder.glob("*.docx"):
        if is_valid_docx_file(file):
            print(f"📂 Processando arquivo pré-existente: {file.name}")
            content = load_docx_content(file)
            graph = MyGraph(file_name=file.name).get_graph()
            graph.invoke({"document_content": content})

    observer = Observer()
    handler = NewDocxHandler()
    observer.schedule(handler, folder_path, recursive=False)
    observer.start()
    print(f"📁 Watching for new .docx files in: {folder_path}")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_folder("docs/input")
