## Публикация `os_script` в PyPI

- [x] **1. Имя пакета**
  - Выбрано: `os-script` (свободно).
  - В `pyproject.toml` сейчас `name = "os_script"` — на PyPI это то же имя (нормализация `-`/`_`).

- [x] **2. Аккаунты**
  - Аккаунт на `https://pypi.org` есть.
  - (Опционально) `https://test.pypi.org` для теста.

- [x] **3. Файлы проекта**
  - Есть `os_script/` + `__init__.py`, `pyproject.toml`, `README.md`, `LICENSE.txt`.
  - Метаданные в `pyproject.toml` заполнены (`version` 0.5.4, deps, license, urls).

- [x] **4. Проверка локально**
  - `python -m pip install -e .` — ок.
  - `import os_script` работает, `os_script_version()` → `0.5.4`.

- [x] **5. Сборка дистрибутивов**
  - Из корня: `python build_and_install.py`
  - Скрипт синхронизирует версию из `os_script_version()` → `pyproject.toml`, делает `python -m build`, ставит wheel из `dist/`.

- [x] **6. Загрузка на TestPyPI**
  - Токены: `C:\Users\hex\.pypirc` (username `__token__`, password — API token).
  - Установить: `python -m pip install --upgrade twine`.
  - Загрузить: `python -m twine upload --repository testpypi dist/*`.
  - В новом virtualenv:  
    `python -m pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple os-script`.

- [x] **7. Публикация на PyPI**
  - Когда тест прошёл, загрузить в боевой PyPI:  
    `python -m twine upload dist/*`.
  - Проверить страницу проекта на `https://pypi.org/project/os-script/` и установку `pip install os-script`.

- [x] **8. Новые релизы**
  - Поднять версию в `os_script_version()` (`os_script/os_script.py`).
  - `python build_and_install.py`, затем `python -m twine upload dist/*`.
