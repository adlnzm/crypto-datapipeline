import json 
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from utils.logger import get_logger
from utils.json_utils import json_safe

logger = get_logger(__name__)

STATE_FILE = Path(".pipeline_state.json")

def load_state() -> Dict :
    if not STATE_FILE.exists() :
        return {}
    
    with open(STATE_FILE, "r") as f :
        return json.load(f)
    
def save_state(state: Dict) :
    with open(STATE_FILE, "w") as f :
        json.dump(state, f, indent=2, default=json_safe)

def get_last_run(pipeline_name: str) -> Optional[str] :
    state = load_state()
    return state.get(pipeline_name)

def update_last_run(pipeline_name: str) :
    state = load_state()
    state[pipeline_name] = {
        "last_run": datetime.utcnow().isoformat()
    }
    save_state(state)
    logger.info(f"State updated for pipeline: {pipeline_name}")