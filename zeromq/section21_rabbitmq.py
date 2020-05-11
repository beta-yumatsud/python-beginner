from zeromq import tasks

result = tasks.build_server.delay()
# 結果を待つ場合は下記
# result = tasks.build_server()
# 複数実行
# result = tasks.build_servers.delay()
# callback実行
# result = tasks.build_servers_with_cleanup.delay()
# chain
# result = tasks.deploy_customer_server.delay()
print("doing...")
print(result)

