import os

PORT = os.getenv('PORT', '5000')
bind = "0.0.0.0:" + PORT
workers = 1
log_level = "info"
