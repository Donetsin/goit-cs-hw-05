import os
import asyncio
import aiofiles
import argparse
import logging
from pathlib import Path


# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def read_folder(source_path, output_path):
    tasks = []
    for root, _, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_path))

    await asyncio.gather(*tasks)

async def copy_file(file_path, output_path):
    try:
        extension = file_path.suffix.lower()
        if not extension:
            extension = "no_extension"

        target_folder = output_path / extension.lstrip('.')
        target_folder.mkdir(parents=True, exist_ok=True)

        target_file = target_folder / file_path.name

        async with aiofiles.open(file_path, mode='rb') as source:
            content = await source.read()
            async with aiofiles.open(target_file, mode='wb') as target:
                await target.write(content)

        logging.info(f"Файл: {file_path} скопійований у: {target_file}")

    except Exception as e:
        logging.error(f"Помилка копіювання файлу ({file_path}): {e}")

def main():
    parser = argparse.ArgumentParser(description = "Сортування файлів за ризширенням у підпапки.")
    parser.add_argument("source_folder", type = str, help = "Шлях до початкової папки")
    parser.add_argument("output_folder", type = str, help = "Шлях до цільової папки, куди будуть скопійовані файли")

    args = parser.parse_args()

    source_path = Path(args.source_folder)
    output_path = Path(args.output_folder)

    if not source_path.exists():
        logging.error(f"Початкової папки {source_path} не існує.")
        return

    if not output_path.exists():
        logging.info(f"Цільова папка {output_path} не існує. Створюємо папку.")
        output_path.mkdir(parents=True, exist_ok=True)

    asyncio.run(read_folder(source_path, output_path))

if __name__ == "__main__":
    # Формат виклику програми: python task_01.py source_folder output_folder
    main()
