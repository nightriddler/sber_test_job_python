# sber_test_job_python
Тестовое задание для Сбера.

## Задание:
>Необходимо разработать CLI приложение для конвертации NER-разметки документов.
>
>Конвертация разметки:
>
>- Необходимо решить задачу конвертацию разметки из формата BRAT в формат BIO.
>- Спроектировать и реализовать интерфейс командной строки.
>- В качестве примера разметки можно использовать данные соревнования RuREBus

## Реализация
Для командной строки используется библиотека [`typer`](https://typer.tiangolo.com/), для конвертации и импорта библиотеки - `pandas` и `csv`.

### Развертка проекта

```
git clone https://github.com/nightriddler/sber_test_job_python.git
cd sber_test_job_python
python -m venv venv
source venv/Scripts/activate 
pip install -r requirements.txt
```
## Описание

```
$ python convert_markup.py test
```
Данная команда осуществляет поиск файлов с расширением `.ann` в указанном каталоге, найденные файлы конвертирует и сохраняет  в этой же директории с суффиксом `_bio` и расширением `.ann`.

Файл `test/example.ann`
```
T25	MET 864 922	обеспеченности населения качественными торговыми площадями
T26	CMP 853 863	увеличения
R12	TSK Arg1:T25 Arg2:T26
```
Будет преобразован и сохранен в файл `test/example_bio.ann`:
```
T25	MET-B	обеспеченности
T25	MET-I	населения
T25	MET-I	качественными
T25	MET-I	торговыми
T25	MET-I	площадями
T26	O	увеличения
```

## Интерфейс CLI

```
$ python convert_markup.py --help 
Usage: convert_markup.py [OPTIONS] [CATALOG]

  Модуль для поиска и конвертации файлов разметки BRAT в разметку BIO.

Arguments:
  [CATALOG]  Поиск файлов в укзанном каталоге. По-умолчанию, поиск в текущей
             директории. Возможен относительный путь: folder1/folder2
             [default: ]

Options:
  --suff-conv TEXT                Суффикс для добавления к конвертируемым
                                  файлам.  [default: _bio]
  --init-extension TEXT           Расширение искомого файла.  [default: .ann]
  --final-extension TEXT          Расширение сконвертированного файла.
                                  [default: .ann]
  --recursive / --no-recursive    Осуществлять рекурсивный поиск вглуб
                                  каталога.  [default: no-recursive]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Пример
```
root
├── folder1            
|   ├── test1.csv      - тестовый файл для конвертации
│   └── folder2        
|       └── test2.csv  - тестовый файл для конвертации
└── convert_markup.py 

```
При запуске из `root`:

```
$ python convert_markup.py some_folder_1 --recursive --suff-conv _new_markup --init-extension .csv --final-extension .txt
```
Будет произведен рекурсивный поиск в каталоге `folder1` и далее `folder2` файлов с расширением `.csv` при конвертации, файлы будут сохранены с суффиксом `_new_markup` и расширением `.txt`.

В результате:
```
root
├── folder1            
|   ├── test1.csv                 - тестовый файл для конвертации
|   ├── test1_new_markup.txt      - сконвертированный файл 
│   └── folder2
|       ├── test2.csv             - тестовый файл для конвертации         
|       └── test2_new_markup.txt  - сконвертированный файл
└── convert_markup.py 
```
Результатом выполнения будет сообщение в командной строке:
```
Сконвертированно файлов: 2
```

## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)
