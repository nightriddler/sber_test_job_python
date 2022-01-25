import csv
import os
from dataclasses import dataclass
from typing import List, Optional

import pandas
import typer


@dataclass
class SearchFile:
    """
    Класс осуществляет поиск файлов в каталоге.

    Атрибуты
    --------
    catalog : str
        каталог в котором производится поиск, либо относительный путь каталога
    recursive : bool
        True поиск в глубину. По-умолчанию - False.
    suffix_markup : str
        суффикс который необходимо исключить при поиске файлов. По-умолчанию - "_bio"
    extension : str
        расширение искомых файлов. По-умолчанию - ".ann"

    Методы
    ------
    get_current_dir():
        Получить путь текущего каталога.

    get_files_from_current_dir():
        Получить файлы из текущего каталога.
    """

    catalog: Optional[str] = None
    recursive: Optional[bool] = False
    suffix_markup: Optional[str] = "_bio"
    extension: Optional[str] = ".ann"

    def get_current_dir(self) -> str:
        """
        Получить путь текущего каталога.

        Если self.catalog не указан - поиск в директории с запускаемым модулем (допускается относительный путь к каталогу).

        Возвращаемое значение
        ---------------------
        None
        """
        curr_dir = os.getcwd()
        if self.catalog:
            transform_dir = self.catalog.replace("/", "\\")
            curr_dir = curr_dir + f"\\{transform_dir}"
        return curr_dir

    def get_files_from_current_dir(self) -> List[str]:
        """
        Осуществляет поиск в каталоге.

        По-умолчанию, self.recursive = False, ищет файлы только в каталоге.
        self.extension и self.suffix_markup - исключают поиск файлов с указанным расширением и суффиксом

        Возвращаемое значение
        ---------------------
        List[str]
        """
        find_files = []
        for root, dirs, files in os.walk(self.get_current_dir()):
            if not self.recursive:
                return [
                    os.path.join(root, name)
                    for name in files
                    if name.endswith(self.extension)
                    and not name.endswith(f"{self.suffix_markup+self.extension}")
                ]
            find_files += [
                os.path.join(root, name)
                for name in files
                if name.endswith(self.extension)
                and not name.endswith(f"{self.suffix_markup+self.extension}")
            ]
        return find_files


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
    """

    roots: List[str]
    suffix_markup: Optional[str] = "_bio"
    extension: Optional[str] = ".ann"
    count: int = 0

    def convert_all(self) -> str:
        """
        Конвертация всех файлов.

        Возвращаемое значение
        ---------------------
        None
        """
        list(map(self.convert_markup, self.roots))

    def convert_markup(self, root) -> None:
        """
        Конвертация файла разметки BRAT в BIO по указанному относительному расположению.

        Например:
        --------
        T25	MET 864 922	обеспеченности населения качественными торговыми площадями
        T26	CMP 853 863	увеличения
        --------
        ->
        --------
        T25	MET-B	обеспеченности
        T25	MET-I	населения
        T25	MET-I	качественными
        T25	MET-I	торговыми
        T25	MET-I	площадями
        T26	O	увеличения
        --------

        self.suffix_markup и self.extension - добавляют суффикс и расширение к указанному файлу.
        Каждый сконвертированный файл - self.count += 1

        Возвращаемое значение
        ---------------------
        None
        """
        word_list, tag_list, entity_list = [], [], []
        filename_convert = root[:-5] + self.suffix_markup + self.extension
        if os.path.exists(filename_convert):
            return
        with open(root, encoding="utf-8", newline="") as read_file:
            file_reader = csv.reader(read_file)

            for line in file_reader:
                line = line[0].split()
                entity = line[0]
                tag = line[1]
                words = line[4:]

                if len(words) == 1:
                    word_list.append(words[0])
                    tag_list.append("O")
                    entity_list.append(entity)

                if len(words) > 1:
                    count_word = 0
                    for word in words:
                        word_list.append(word)
                        if count_word == 0:
                            tag_list.append(tag + "-B")
                        else:
                            tag_list.append(tag + "-I")
                        entity_list.append(entity)
                        count_word += 1
                    count_word = 0
        if entity_list and tag_list and word_list:
            dataframe_with_bio = pandas.DataFrame(
                list(zip(entity_list, tag_list, word_list))
            )
            dataframe_with_bio.to_csv(
                filename_convert, sep="\t", header=False, index=False
            )
            self.count += 1

    @property
    def get_count(self) -> int:
        """
        Количество сконвертированных файлов.

        Возвращаемое значение
        ---------------------
        int
        """
        return self.count


def main(
    catalog: Optional[str] = typer.Argument(
        "",
        help="Поиск файлов в укзанном каталоге. По-умолчанию, поиск в текущей директории. Возможен относительный путь: folder1/folder2",
    ),
    suff_conv: Optional[str] = typer.Option(
        "_bio", help="Суффикс для добавления к конвертируемым файлам."
    ),
    init_extension: Optional[str] = typer.Option(
        ".ann", help="Расширение искомого файла."
    ),
    final_extension: Optional[str] = typer.Option(
        ".ann", help="Расширение сконвертированного файла."
    ),
    recursive: Optional[bool] = typer.Option(
        False, help="Осуществлять рекурсивный поиск вглуб каталога."
    ),
):
    """
    Модуль для поиска и конвертации файлов разметки BRAT в разметку BIO.
    """
    search = SearchFile(catalog, recursive, suff_conv, init_extension)
    conv = ConvertMarkup(
        search.get_files_from_current_dir(), suff_conv, final_extension
    )
    conv.convert_all()
    print(
        f"Сконвертированно файлов: {conv.get_count}"
        if conv.get_count
        else "Файлы для конвертации не найдены."
    )


if __name__ == "__main__":
    typer.run(main)
