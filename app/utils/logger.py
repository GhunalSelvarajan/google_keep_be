import logging


class ColoredFormatter(logging.Formatter):
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;228m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt: str):
        super().__init__()
        self.fmt = fmt
        self.formats = {
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record) -> str:  # type: ignore
        log_format = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_format, datefmt="%H:%M %p")
        return formatter.format(record)


class CustomLogger:
    def __init__(self) -> None:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(logging.INFO)
        stdout_handler.setFormatter(
            ColoredFormatter(
                "Filename: %(filename)s | %(levelname)s | %(asctime)s | Function: [%(funcName)s] | Message: %(message)s"
                " | LineNumber: %(lineno)s"
            )
        )
        self.custom_logger = logging.getLogger(__name__)
        self.custom_logger.setLevel(logging.INFO)
        self.custom_logger.addHandler(stdout_handler)

    def info(self, message: str) -> None:
        self.custom_logger.info(
            message,
            stacklevel=2,
        )

    def debug(self, message: str) -> None:
        self.custom_logger.debug(
            message,
            stacklevel=2,
        )

    def warning(self, message: str) -> None:
        self.custom_logger.warning(
            message,
            stacklevel=2,
        )

    def error(self, message: str) -> None:
        self.custom_logger.error(
            message,
            exc_info=True,
            stacklevel=2,
        )

    def critical(self, message: str) -> None:
        self.custom_logger.critical(
            message,
            exc_info=True,
            stacklevel=2,
        )


logger = CustomLogger()
