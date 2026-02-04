# import matplotlib.pyplot as plt
# import pandas as pd
import polars as pl
# import seaborn as sns


def pl_info(
    df: pl.DataFrame,
    memory_usage: bool = True,
    max_col_width: int = 20
) -> None:
    """
    Выводит краткую информацию о Polars DataFrame, 
    аналогично pandas.DataFrame.info().

    Функция отображает:
        - Класс объекта
        - Индекс строк (диапазон)
        - Количество колонок
        - Информацию по каждой колонке: индекс, название, количество не-null
          значений, тип данных
        - Сводку типов данных
        - Использование памяти (опционально)

    Parameters
    ----------
    df : pl.DataFrame
        DataFrame для анализа
    memory_usage : bool, default True
        Если True, показывает примерное использование памяти в KB/MB
    max_col_width : int, default 20
        Максимальная ширина для отображения названий колонок

    Returns
    -------
    None
        Функция только выводит информацию в консоль

    """
    if not isinstance(df, pl.DataFrame):
        raise TypeError(f"Expected polars.DataFrame, got {type(df)}")

    n_rows, n_cols = df.shape

    # Заголовок
    print("<class 'polars.DataFrame'>")
    print(f"RangeIndex: 0 to {n_rows-1} ({n_rows} entries)")
    print(f"Columns: {n_cols} entries")

    if n_cols == 0:
        print("Empty DataFrame")
        return

    # Информация по колонкам
    print(f" #   {'Column':<{max_col_width}} Non-Null Count  Dtype    ")
    print(f"---  {'-' * max_col_width} --------------  -----    ")

    # Получаем количество null значений одним запросом (эффективнее)
    null_counts = df.null_count().to_dict(as_series=False)

    for i, col in enumerate(df.columns):
        non_nulls = n_rows - null_counts[col][0]
        dtype = df.schema[col]

        # Обрезаем длинные названия колонок
        display_col = (
            col[:max_col_width-3] + "..."
            if len(col) > max_col_width else col
        )

        print(
            f"{i:>3}  {display_col:<{max_col_width}} "
            f"{non_nulls:<14}  {dtype}"
        )

    # Сводка по типам данных (группируем одинаковые типы)
    dtype_counts: dict[str, int] = {}

    for dtype in df.dtypes:
        dtype_str = str(dtype)
        dtype_counts[dtype_str] = dtype_counts.get(dtype_str, 0) + 1

    dtype_summary = ", ".join([f"{dtype}({count})" if count > 1 else dtype
                              for dtype, count in dtype_counts.items()])
    print(f"dtypes: {dtype_summary}")

    # Использование памяти
    if memory_usage:
        memory_bytes = df.estimated_size()
        if memory_bytes < 1024:
            memory_str = f"{memory_bytes} bytes"
        elif memory_bytes < 1024 * 1024:
            memory_str = f"{memory_bytes / 1024:.1f} KB"
        else:
            memory_str = f"{memory_bytes / (1024 * 1024):.1f} MB"
        print(f"memory usage: {memory_str}")
