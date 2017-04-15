# Cooking Chat
Sprintというオンラインハッカソンで作成  
残っている食材だけで作れるレシピを検索してくれるBOT  
その他もろもろ

## 備考
2016年6月作成  
2017年4月サーバ停止  

## python-version
python2.7.9

## 実装機能
[readme.txt](./readme.txt)に記載  
[answer.md](./answer.md)にハッカソンで指定されていた実装アピールポイント等を記載  

## HOWTO
password/password_sample.pyを参考に，password/password.pyを作成
```
pip install -r requirements.txt
redis-server &
gunicorn -k flask_sockets.worker chat:app
```

## 結果
優秀賞  
企業賞

### 言い訳
昔のcommit履歴が汚すぎて，passwordとかcommitしてるものもあって，管理めんどくさかったので削除した．
もう触ることがないと思うので記念程度にとりあえずその時点で最新だったコードだけ保管．
