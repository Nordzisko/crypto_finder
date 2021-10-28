worker_class = "aiohttp.worker.GunicornUVLoopWebWorker"
proc_name = "crypto_finder"

bind = ":8899"

accesslog = "-"  # send access log to stdout
