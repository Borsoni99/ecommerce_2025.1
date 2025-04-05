# Gunicorn configuration file
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = (multiprocessing.cpu_count() * 2) + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 600
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'gunicorn_ecommerce'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (disabled for Azure App Service)
keyfile = None
certfile = None

# Reload
reload = False

# Debugging
capture_output = True
enable_stdio_inheritance = True 