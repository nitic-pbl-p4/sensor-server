from rich.logging import RichHandler
import logging
from rich.console import Console
from rich.highlighter import ReprHighlighter

# Richを用いたロガー用の設定
# Refer: https://rich.readthedocs.io/en/latest/logging.html
FORMAT = "%(levelname)s %(asctime)s %(message)s %(pathname)s:%(lineno)d"
logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logging.debug("Rich をロガーとして設定しました")

# Richを用いたコンソール出力用の設定
# Refer: https://github.com/Textualize/rich#using-the-console
console = Console()
highlighter = ReprHighlighter()
