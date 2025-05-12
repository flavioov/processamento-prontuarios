import asyncio
import pathlib
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from docx import Document

from graph import LLMGraph


class NewDocxHandler(FileSystemEventHandler):
    async def on_created(self, event):
        if not event.is_directory:
            path = pathlib.Path(event.src_path)
            if not is_valid_docx_file(path):
                if path.suffix == ".docx":
                    print(f"📄 Novo prontuário (.docx) detectado: {path}")
                    asyncio.create_task(process_docx_file(path))


async def process_docx_file(file_path: Path):
    try:
        content = await load_docx_content(file_path)
        graph_builder = LLMGraph()
        graph_builder.set_filename(file_name=file_path.name)
        graph = graph_builder.get_graph()
        await graph.ainvoke({"document_content": content})
    except Exception as e:
        print(f"❌ Erro ao processar {file_path.name}: {e}")


def _read_docx(file_path: Path) -> str:
    document = Document(file_path)
    print(f"📄 Conteúdo do documento carregado")
    return "\n".join([para.text for para in document.paragraphs])


async def load_docx_content(file_path: Path, retries=5, delay=0.5) -> str:
    for attempt in range(retries):
        try:
            return await asyncio.to_thread(_read_docx, file_path)
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise RuntimeError(f"Falha ao carregar {file_path.name}") from e
    return ""


async def is_valid_docx_file(file_path: Path) -> bool:
    filename = file_path.name
    return (
        filename.startswith("~$")  # MS Word lock file
        or filename.startswith(".~lock")  # LibreOffice lock file
        or file_path.stat().st_size > 0  # avoid empty files
    )


async def watch_folder(folder_path: str):
    folder = Path(folder_path)
    output_folder = "docs/output"

    tasks = []
    for file in folder.glob("*.docx"):
        if await is_valid_docx_file(file):
            output_name = file.name.removesuffix(".docx") + ".txt"
            output_path = Path(output_folder + "/" + output_name)
            if output_path.exists():
                print(f"⚠️ Output já existe para o arquivo {file.name}, ignorando...")
                continue

            print(f"📂 Processando arquivo pré-existente: {file.name}")
            tasks.append(process_docx_file(file))  # don't await here!

    # Run them concurrently
    if tasks:
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(watch_folder("docs/input"))
