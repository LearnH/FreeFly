workers = 2  # 通常为 2*CPU核数+1
threads = 2
worker_class = 'gunicorn.workers.gthread.ThreadWorker'
keepalive = 5