import logging


def create_logger(name, level=logging.INFO):
    logging.basicConfig(
        filename="execution.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s - %(message)s",  # Setup record output
        datefmt="%H:%M:%S",
    )

    console_output = logging.StreamHandler()
    console_output.setLevel(logging.DEBUG)

    # Setup console output
    formatter = logging.Formatter(
        "[%(asctime)s] SOURCE %(name)-12s: %(levelname)-8s %(message)s", datefmt="%H:%M:%S"
    )
    console_output.setFormatter(formatter)
    logging.getLogger("").addHandler(console_output)
    return logging.getLogger(name)