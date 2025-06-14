import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path("backend/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configure logging format
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Bias monitoring logger
    bias_logger = logging.getLogger("bias_monitoring")
    bias_handler = RotatingFileHandler(
        log_dir / "bias_monitoring.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    bias_handler.setFormatter(log_format)
    bias_logger.addHandler(bias_handler)
    bias_logger.setLevel(logging.INFO)
    
    # Model decisions logger
    model_logger = logging.getLogger("model_decisions")
    model_handler = RotatingFileHandler(
        log_dir / "model_decisions.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    model_handler.setFormatter(log_format)
    model_logger.addHandler(model_handler)
    model_logger.setLevel(logging.INFO)
    
    return root_logger

# Create logger instances
logger = logging.getLogger(__name__)
bias_logger = logging.getLogger("bias_monitoring")
model_logger = logging.getLogger("model_decisions") 