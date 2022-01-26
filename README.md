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
Для командной строки используется библиотека [`typer`](https://typer.tiangolo.com/), для конвертации и импорта библиотека `pandas`.

### Развертка проекта

```
git clone https://github.com/nightriddler/sber_test_job_python.git
cd sber_test_job_python
python -m venv venv
source venv/Scripts/activate 
pip install -r requirements.txt
```
## Описание
Приложение для конвертации файлов в указанном каталоге.
```
$ python convert_markup.py test
```
Данная команда по-умолчанию:
 - Осуществляет поиск файлов с расширением `.ann` в каталоге `test`
 - Найденные файлы конвертирует и сохраняет  в этой же директории с суффиксом `_bio` и расширением `.ann`.

## Принцип конвертации
>В качестве тестов взята [полная разметки текста с проекта RuREBus](https://github.com/dialogue-evaluation/RuREBus/).

Файл `test/example.ann`
```
T26	CMP 853 863	увеличения
T28	ECO 2801 2907	производства бумаги и бумажных изделий, прочих готовых изделий, прочих транспортных средств и оборудования
T200	ECO 8162 8217	производстве прочих транспортных средств и оборудования
R12	TSK Arg1:T26 Arg2:T28
```
Будет преобразован и сохранен в файл `test/example_bio.ann`:
```
T26	O	увеличения
T28	O	и
T28	ECO-B	производства
T28	ECO-I	бумаги
T28	O	и
T28	ECO-I	бумажных
T28	ECO-I	изделий
T28	ECO-I	прочих
T28	ECO-I	готовых
T28	ECO-I	изделий
T28	ECO-I	прочих
T28	ECO-I	транспортных
T28	ECO-I	средств
T28	ECO-I	оборудования
T200	ECO-B	производстве
T200	ECO-I	прочих
T200	ECO-I	транспортных
T200	ECO-I	средств
T200	O	и
T200	ECO-I	оборудования
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
Имеется следующая структура
```
root
├── folder1            
|   ├── test1.csv      - тестовый файл для конвертации
│   └── folder2        
|       └── test2.csv  - тестовый файл для конвертации
└── convert_markup.py 

```
При запуске из `root`

```
$ python convert_markup.py folder_1 --recursive --suff-conv _new_markup --init-extension .csv --final-extension .txt
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
>При повторном запуске этой команды, найденные файлы с таким же именем, суффиксом и расширением не будут сконвертированы о чем последует уведомление:
>```
>Файл C:\root\folder1\test1.csv уже сконвертирован.
>Файл C:\root\folder1\folder2\test2.csv уже сконвертирован.
>Файлы для конвертации не найдены.
>```
>
## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)
