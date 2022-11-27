"""
This module implements and instantiates the common configuration class used in the project.
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
import sys
import tempfile
from pathlib import Path
from typing import Dict, Optional, Union, Any
import os 
# from loguru import logger


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["ConfManager", "conf_mgr"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Configuration Manager                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class ConfManager:
    """Configuration Manager class"""

    file_path: Path = Path(__file__).parent.resolve()

    data_dir: Path = f"{file_path}/data"
    data_stock_raw_dir: Path = f"{file_path}/data/stock_raw/"

    list_symbol_csv_dir: Path = os.path.join(data_dir, "list_symbol_raw.csv")
    
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    Path(data_stock_raw_dir).mkdir(parents=True, exist_ok=True)
    

# ─────────────────────────────────────────────── ConfManager instance ─────────────────────────────────────────────── #

conf_mgr: ConfManager = ConfManager()
