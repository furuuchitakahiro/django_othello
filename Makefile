.PHONY: help

MYSQL_USER = root
MYSQL_PASSWORD = eeYuji6Cvu4lieY6
MYSQL_DATABASE = dev_othello_api_db

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


# Django commands

shell: ## Django の shell を起動
	docker-compose run --rm api sh -c "sleep 1 && python ./othello/manage.py shell"

makemigrations: ## Django でマイグレーションファイルを作成
	docker-compose run --rm api sh -c "sleep 1 && python ./othello/manage.py makemigrations"

migrate: ## Django でマイグレート
	docker-compose run --rm api sh -c "sleep 1 && python ./othello/manage.py migrate"

loaddata: ## Django で初期データを読み込み
	-docker-compose run --rm api sh -c "sleep 1 && ./utils/loaddata.dev.sh"


# Custom commands

bash: ## api コンテナに bash でログイン
	docker-compose run --rm api bash

attach: ## api コンテナに attach する
	docker attach othello-api

mysql:
	docker-compose run --rm api sh -c "sleep 1 && mysql -u $(MYSQL_USER) -h db -p$(MYSQL_PASSWORD)"

redis-cli:
	docker-compose run --rm api sh -c "redis-cli -h cache"

clean_database: ## データベースを初期化
	docker-compose run --rm api sh -c "sleep 1 && mysql -u $(MYSQL_USER) -h db -p$(MYSQL_PASSWORD) -e'drop database $(MYSQL_DATABASE);' && mysql -u $(MYSQL_USER) -h db -p$(MYSQL_PASSWORD)  -e'create database $(MYSQL_DATABASE);'"

clean_migrations: ## マイグレーションファイルの削除
	rm ./api/othello/*/migrations/[^__init__]*.py

copy_packages: ## site-packages api/.site-packages にコピー ( エディター補完 )
	docker-compose run --rm api sh -c "pip install -r requirements.txt && rm -rf .site-packages/* && cp -r /usr/local/lib/python3.7/site-packages/* .site-packages"

clean_pycache: ## 全ての __pycache__ を削除
	docker-compose run --rm api sh -c "find . -name "__pycache__" -type d | xargs rm -rf"


# bulk commands

reset: clean_database migrate loaddata ## データベースをリセット
