"""Централизованная настройка логирования для фреймворка."""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Создает и настраивает логгер для модуля.
    
    Args:
        name: Имя логгера (обычно __name__ модуля)
        level: Уровень логирования (по умолчанию INFO)
        format_string: Формат строки логов (по умолчанию стандартный формат)
        
    Returns:
        Настроенный объект Logger
    """
    logger = logging.getLogger(name)
    
    # Если логгер уже настроен, возвращаем его
    if logger.handlers:
        return logger
    
    # Уровень логирования
    if level is None:
        level = logging.INFO
    
    logger.setLevel(level)
    
    # Формат логирования
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    formatter = logging.Formatter(format_string)
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # Предотвращаем дублирование логов
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Получить логгер для модуля.
    
    Удобная функция для быстрого получения настроенного логгера.
    
    Args:
        name: Имя логгера (обычно __name__ модуля)
        
    Returns:
        Настроенный объект Logger
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Test message")
    """
    return setup_logger(name)

