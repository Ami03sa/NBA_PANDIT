import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Model Configuration
DEFAULT_MODEL = "gpt-4o-mini"
ORCHESTRATOR_MODEL = "gpt-4o"

# Search Configuration
TRUSTED_NBA_SOURCES = [
    'statmuse.com',
    'nba.com',
    'espn.com',
    'basketball-reference.com',
    'theathletic.com',
    'bleacherreport.com',
]

# Agent Settings
AGENT_CONFIG = {
    'search_agent': {
        'temperature': 0.1,
        'max_tokens': 2000,
        'search_context_size': 'low'
    },
    'data_agent': {
        'temperature': 0.1,
        'max_tokens': 3000
    },
    'visualization_agent': {
        'temperature': 0.2,
        'max_tokens': 2000
    },
    'orchestrator': {
        'temperature': 0.3,
        'max_tokens': 4000
    }
}

# Visualization Settings
VIZ_CONFIG = {
    'save_charts': True,
    'output_dir': './outputs',
    'chart_style': 'seaborn',
    'default_figsize': (10, 6),
    'dpi': 300
}

# Create output directory if it doesn't exist
os.makedirs(VIZ_CONFIG['output_dir'], exist_ok=True)

# Cache Settings (for future optimization)
CACHE_ENABLED = True
CACHE_EXPIRY_HOURS = 24

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "nba_chatbot.log"