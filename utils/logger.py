import logging
import os

def setup_logger(name=__name__, log_level="INFO"):
    logger = logging.getLogger(name)

    # すでにハンドラがある場合は再利用
    if not logger.handlers:
        # ログディレクトリがなければ作成
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        handler = logging.FileHandler(f"{log_dir}/app.log", encoding="utf-8")
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # ログレベルを設定（デフォルトは INFO）
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.propagate = False

    return logger