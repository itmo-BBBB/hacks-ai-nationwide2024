# Техническая документация

В данном разделе описана ML часть решения, т.е. выбранный алгоритм, подход и процесс обучения.
Все зависимости, используемые в директории `ml`, находятся в `pyproject.toml` файле в корне репозитория. 
В директории `notebooks` находятся все эксперименты, бейзлайн и обучения моделей.
В директории `models` находятся `cbm` файлы двух сохраненных финальных обученных моделей.

## Сборка датасета для `catboost`

Скрипт по сборке запускается как **(доп. параметры сборки можно узнать через `--help`)**:
```bash
python build-catboost-dataset.py --train train_events.csv --target train_targets.csv
```

Предварительно обрабатывает входные CSV-файлы для обучения на основе составных ключей для юзера и видео.
- Объединяет таблицы в одну.
- Применяет локализацию часового пояса к полю `"event_timestamp"`.
- Добавляет `"value_counts"` на основе `"viewer_uid"`.

Возвращает предварительно обработанный фрейм данных.

Аналогичной командой можно собрать test датасет **(тот, в котором нет target значения)**.
```bash
python build-catboost-test.py --test test_events.csv
```

## Baseline решение

Решается две отдельных не связанных друг с другом задачи классификации бинарной **(для пола)** и мульти классовой **(для возрастов)**
постановки с помощью `Catboost` классификатора. Весь бейзлайн представлен в файле [`catboost-baseline`](./notebooks/catboost-baseline.ipynb). 
Схема решения выглядит следущим образом:
- Предобработка данных после сборки датасета
  - Категориальные признаки обрабатываются как категориальные **(внутри модели `onehot`)**
  - `timestamp` данные делятся на года, месяцы, часы и т.д. с переводом в `int` + с `sin` и `cos` кодированием часов **(это происходит еще на этапе создания датасета)**
  - Текстовые данные **(`"title"`)** обрабатываются с помощью настроенного `BPE` токенизатора внутри самого классификатора
  - Весь датасет и бОльшая часть препроцессинга происходят в рамках инициализации модели и создании `Pool` объекта
- Обучение двух разных классификаторов с проверкой на валидацией соответствующих метрик
- Агрегация данных и подсчет статистик
  - Каждая строка датасета определяется уникальным значением id пользователя и видео => 
    предсказывая для каждой строки какой-то результат, мы делаем предсказание для конкретного видео **(т.к. у одного id пользователя может быть несколько id видео)**.
    Чтобы это исправить, берем какую-нибудь статистику по всем видео предсказания для каждого пользователя. В нашем случае классификации это будет мода предсказанных категорий. 

## Финальное решение

Исследовав базовое решение, пришли к выводу, что:
- Необходимо более точно настроить классификаторы **(для этого запускаем `optuna` максимизацию метрик для моделей [возраста](./notebooks/catboost-optuna-age.ipynb) и [пола](./notebooks/catboost-optuna-gender.ipynb))**
- Можно убрать те признаки, которые не вносят вклад в предсказание, но при этом заставляют тратить вычислительные мощности. Таковыми являются топ N низких признаков по feature importance в catboost
  **(например, месяц и год, т.к. они в данных у всех одинаковые)**
  
Подобрав параметры и настроив модели, обучаем финальные варианты в [`catboost-train-main`](./notebooks/catboost-train-main.ipynb) и замеряемся на тестовых данных в [`catboost-test-main`](notebooks/catboost-test-main.ipynb).
