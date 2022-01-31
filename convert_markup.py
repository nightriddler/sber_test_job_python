import csv
import pathlib
from dataclasses import dataclass
from io import TextIOWrapper
from typing import List, Tuple

import typer


def get_files(
    catalog: str, recursive: bool, suffix_markup: str, extension: str
) -> List[str]:
    """
    Осуществляет поиск в каталоге и выдает список путей найденных файлов.

    По-умолчанию, recursive = False, ищет файлы только в каталоге.
    extension и suffix_markup - исключают поиск файлов с указанным расширением и суффиксом
    """
    if recursive:
        files = pathlib.Path(catalog).rglob(f"*{extension}")
    else:
        files = pathlib.Path(catalog).glob(f"*{extension}")
    return [
        str(i) for i in list(files) if not str(i).endswith(f"{suffix_markup+extension}")
    ]


@dataclass
class ConvertMarkup:
    """
    Класс осуществляет конвертацию разметки BRAT в BIO.

    Атрибуты
    --------
    roots : List[str]
        список путей конвертируемых файлов
    suffix_markup : str
        суффикс который необходимо добавить к названию файла при конвертации. По-умолчанию - "_bio"
    extension : str
        расширение сохраняемого файла. По-умолчанию - ".ann"
    count: int
        количество сконвертированных файлов

    Методы
    ------
    convert_all():
        Конвертация всех файлов из списка путей self.roots.

    convert_markup():
        Конвертация файла по указанному пути.

    def convert_in_bio():
        Преобразование файла в кортеж списков.

    def write_csv():
        Сохраняет списки в файл по указанному пути.

    def check_file():
        Проверка наличие файла по указанному пути.

    def replace_comma():
        Убирает запятые из строки и возвращает её.

    def result():
        Получить количество сконвертированных файлов.
    """

    roots: List[str]
    suffix_markup: str = "_bio"
    extension: str = ".ann"
    __count: int = 0

    def convert_all(self) -> None:
        """
        Конвертация всех файлов.

        Возвращаемое значение
        ---------------------
        None
        """
        list(map(self.convert_markup, self.roots))

    def convert_markup(self, root: str) -> None:
        """
        Конвертация файла разметки BRAT в BIO по указанному относительному расположению.

        Возвращаемое значение
        ---------------------
        None
        """
        file = root[:-4] + self.suffix_markup + self.extension
        if pathlib.Path(file).exists():
            typer.echo(f"Файл {root} уже сконвертирован.")
            return

        with open(root, encoding="utf-8", newline="") as read_file:
            words, tags, entities = self.convert_in_bio(read_file)  # type: ignore

            if words and tags and entities:
                self.write_csv(file, words, tags, entities)

    def convert_in_bio(
        self, file: TextIOWrapper
    ) -> Tuple[List[str], List[str], List[str]]:
        """
        Преобразование файла в кортеж списков из сущностей, имен и тэгов разметки BIO.

        Например:
        --------
        T25	MET 864 922	обеспеченности населения качественными торговыми площадями
        T26	CMP 853 863	увеличения
        --------
        ->
        --------
        T25	MET-B обеспеченности
        T25	MET-I населения
        T25	MET-I качественными
        T25	MET-I торговыми
        T25	MET-I площадями
        T26	O увеличения
        --------

        Возвращаемое значение
        ---------------------
        Tuple[List[str], List[str], List[str]]
        """
        word_list, tag_list, entity_list = [], [], []
        for line in file.readlines():
            line_proc = line.split()
            entity = line_proc[0]
            tag = line_proc[1]
            words = line_proc[4:]

            if len(words) == 1:
                word_list.append(self.replace_comma(words[0]))
                tag_list.append("O")
                entity_list.append(entity)

            if len(words) > 1:
                count_word = 0
                for word in words:
                    word_list.append(self.replace_comma(word))
                    if len(word) <= 2:
                        tag_list.append("O")
                    else:
                        if count_word == 0:
                            tag_list.append(tag + "-B")
                        else:
                            tag_list.append(tag + "-I")
                        count_word += 1
                    entity_list.append(entity)
                count_word = 0

        return word_list, tag_list, entity_list

    def write_csv(
        self, file: str, words: List[str], tags: List[str], entities: List[str]
    ) -> None:
        """
        Сохраняет списки в файл по указанному пути.

        Возвращаемое значение
        ---------------------
        none
        """
        with open(file, "w", encoding="utf-8", newline="") as csv_write:
            writer = csv.writer(csv_write, delimiter=" ")
            for i in range(len(words)):
                writer.writerow([entities[i], tags[i], words[i]])
            self.__count += 1

    def replace_comma(self, word: str) -> str:
        """
        Возвращает строку без запятых.

        Возвращаемое значение
        ---------------------
        str
        """
        return word.replace(",", "")

    @property
    def result(self) -> int:
        """
        Возвращает количество сконвертированных файлов.

        Возвращаемое значение
        ---------------------
        int
        """
        return self.__count


def main(
    catalog: str = typer.Argument(
        "",
        help="Поиск файлов в указнном каталоге. По-умолчанию, поиск в текущей директории. Возможен относительный путь: folder1/folder2",
    ),
    suff_conv: str = typer.Option(
        "_bio", help="Суффикс для добавления к конвертируемым файлам."
    ),
    init_extension: str = typer.Option(".ann", help="Расширение искомого файла."),
    final_extension: str = typer.Option(
        ".ann", help="Расширение сконвертированного файла."
    ),
    recursive: bool = typer.Option(
        False, help="Осуществлять рекурсивный поиск вглуб каталога."
    ),
):
    """
    Модуль для поиска и конвертации файлов разметки BRAT в разметку BIO.
    """
    search_file = get_files(catalog, recursive, suff_conv, init_extension)
    converter = ConvertMarkup(search_file, suff_conv, final_extension)
    converter.convert_all()
    typer.echo(
        f"Сконвертированно файлов: {converter.result}"
        if converter.result
        else "Файлы для конвертации не найдены."
    )


if __name__ == "__main__":
    typer.run(main)
