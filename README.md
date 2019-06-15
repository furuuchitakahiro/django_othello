# Django Othello

## このリポジトリは？

このリポジトリは[私](https://github.com/furuuchitakahiro)のサーバサイドコードのポートフォリオです。

仕事を一緒にさせていただく方、もしくは私に興味を持っていただいた方のために向けて私がどのようなコードを実装するか知ってもらうのが目的です。

突然ですが、私のサーバサイド実装を表現するためにテーマとして、オセロを題材とさせていただきました。
なぜ、オセロを題材としたかというと「みんなが知っていて、ある程度アルゴリズムを必要とする」と判断して題材とさせていただきました。

このリポジトリで実装されているコードは今まで培ってきたものであり、様々な技術記事、実装経験に基づき作られています。
もちろん、オセロをサービスとして提供したことはありませんが、節々の実装のエッセンスは今まで実装してきたものに共通しています。

## 自己紹介

- 名前: 古内貴博
  - [Facebook](https://www.facebook.com/takahiro.furuuchi.37)
  - [Twitter](https://twitter.com/furuuchin)
  - Mail: furuuchi[at]anyflow.co.jp
- 所属: [Anyflow inc.](https://anyflow.co.jp/)
- 職業: サーバサイドエンジニア
- ある程度評価された記事
  - [Django REST Framework で API サーバーを実装して得た知見まとめ(OAuthもあるよ）](https://qiita.com/furuuchin/items/c6d6230aa327ad7b337a)
  - [「Dish」 を支えるランチ推薦アルゴリズム](https://note.mu/furuchin/n/neaaadbd60aee)

## 準備

起動する前に必要なコマンドです。順番に実行してください。
Docker と Docker Compose, make はインストールされていることを前提としています。

1. `git clone git@github.com:furuuchitakahiro/django_othello.git`
  - もしくは `git clone https://github.com/anyflowinc/anyflow-api.git`
2. `cd django_othello`
3. `docker-compose build`
4. `docker-compose up db`
  - [Note] End of list of non-natively partitioned tables のような表記が出たら Control + C で終了
5. `make reset`

以上が完了したら[起動](#起動)するだけです ! :tada:

## 起動

`docker-compose up`

## 使い方 ( 一人で遊ぶ )

1. ユーザーを作成 ( Post /api/othello_users )
2. マッチングを作成 ( Post /api/matchings )
3. ログアウト ( Post /api/auth/logout )
4. ユーザー作成  ( Post /api/othello_users )
5. マッチング ( Patch /api/matchings/:slug )
  - このときの `:slug` は「2. マッチングを作成」で生成されたものです
6. 反転 ( Post /api/games/:slug/board )
  - このときの `:slug` は「5. マッチング」のときに生成されたゲームのものです
7. 「6. 反転」をゲーム終了まで繰り返す

詳しいリクエストボディは [Postman](#postman) を参照してください。

## Postman

- [collection.json](./django_othello.postman_collection.json)
- [environment.json](./django_othello.postman_environment.json)


## 機能

- オセロ
  - 取得
  - 反転処理
- ユーザー
  - 作成
  - 取得
- マッチング
  - 作成
  - 取得
  - マッチング
    - 同時にゲームを生成

## アーキテクチャ

- Docker
- Docker Compose
- Python
- [**django**](https://github.com/django/django)
- [**django REST framework** ( DRF )](https://github.com/encode/django-rest-framework)
- MySQL
- Redis

## Q & A

### Q「開発者 / Anyflow inc. に興味があります」

**A**「[自己紹介](#自己紹介)の連絡先のどれかからご連絡ください！」

### Q「クライアントないんだけど」

**A**「もしかしたらそのうち作るかもしれません。:bow: ( 誰か作って )」

### Q「MySQL のバージョン低くない ?」

**A**「本番環境の実装はありませんが GCP の [Cloud SQL](https://cloud.google.com/sql/?hl=ja) を意識しております。」

### Q「Redis のバージョン低くない ?」

**A**「本番環境の実装はありませんが GCP の [Memory Store](https://cloud.google.com/memorystore/?hl=ja) を意識しております。」

### Q「他の make コマンドは ?」

**A**「`make help`」
