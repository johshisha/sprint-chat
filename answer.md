## デプロイ情報
#### サービスURL
http://johshisha.mydns.jp/

#### リポジトリURL
https://github.com/johshisha/sprint-winter

#### 使用言語
- python

#### 主なライブラリ
- redis,json,gevent,commands,flask,flask_sockets,re,bs4,pickle,requests,collections,Flask, etc..

####  ホスティングサービス
- 自宅サーバー（raspberry pi3にサーバを構築）

## 独自コマンドの実装
#### 追加したコマンドと説明
```
helpコマンド
    -bot (-h, --help, help): botの使い方を表示する．
todoコマンド
    -bot todo list : 登録されているToDoの一覧を返す．
    -bot todo add name content: ToDoを登録する．name:ToDoの名前, content:ToDoの内容．
    -bot todo delete name: ToDoを削除する． name:ToDoの名前．
    -bot todo delete -all: ToDoをすべて削除する．
cookコマンド
    −bot cook search ingredient1 [ingredient2] ...
        引数の材料名から料理を検索し，表示する．
        引数: 空白区切りの一つ以上の材料．
    −bot cook remain ingredient1 [ingredient2] ...
        できるだけ引数の材料名だけで作れる料理を推薦する．推薦元の内容によっては他の材料を使わなければならないレシピもある…
        引数: 空白区切りの一つ以上の材料．．
trends
    −bot cook 
        cookpad.comで今人気の食材を使った料理を推薦する．
aliasコマンド
    -bot alias list : 登録されているaliasの一覧を返す．
    -bot alias add 'name' 'content': aliasを登録する．name:aliasの名前, content:aliasの内容．
                                    (登録の際は，どこからどこがコマンドなのか明示するため''で囲う必要あり．)
    -bot alias delete name: aliasを削除する． name:aliasの名前．
    -bot alias delete -all: aliasをすべて削除する．

```


## 創意工夫 & 作り込み
#### 作り込んだコマンド / 機能
今回，私が実装したかった内容は，料理推薦Botです．
私は一人暮らしをしているのですが，たまにしか料理をしないのでたまに買い込んでしまったときに使い切れずに残ってしまうことが多々ありました．
Cookpadさんなどが料理レシピを公開してくださっていていろんな料理が簡単に作れるようになったのですが，こういった残り物を処理しようと思った時に，
レシピを検索すると他にも必要となる食材が多く，残っている食材だけでは料理ができず，結局使わないということが大きな要因でした．
友人に聞いても同じような理由で食材が残ってしまうとのことなので，これを解消できればみんなが喜ぶのではないか！ということで，今回料理推薦Botを作成しました．

具体的には，cookコマンドを作成し，いくつかの機能をつけました．（cookpad.comを利用して推薦させていただきました．）
'search'は材料を引数としてそれらを使った料理レシピを推薦してくれます．これは単純に引数とした材料を用いる料理をCookpadさんから推薦する機能です．
次に，'remain'の機能ですが，こちらが今回実装したかった残り物だけで作成できるレシピを推薦してくれる機能です．こちらの詳細は創意工夫点で説明させていただきます．
また，もうひとつ，今晩の夕食を決めかねている主婦の方のために，cookpad.comで今人気の食材を用いたレシピを推薦してくれる機能も付与しました．
これで主婦の方の負担が減ればいいなと思います．

またおまけとして，いくつかの機能を追加で実装しました．
まずTodo機能です．登録，閲覧，削除，一括削除などの機能があります．
TodoはすべてRedisで管理しているので素早く処理ができるかと思います．
次に，helpコマンドを作成しました．これでコマンドの一覧と使い方を確認できます．
また，aliasコマンドを実装し，打つのがめんどうなコマンドを省略できるようにしました．

しかし，今回の実装はSPRINTに提出するための実装ですので，ユーザ登録などの機能は実装されていません．
なのでTodoやaliasの内容はアクセスしている全員が登録，削除できてしまうという欠点があります．
今後，本格的なサービス公開に向けてユーザ登録やRoomの作成機能を実装する必要があります．


#### 創意工夫したポイント
今回，残り物の食材だけで作れるレシピの推薦機能を主として実装しました．
"残り物の食材だけで"という条件設定に苦労しました．
というのも，引数とした食材と，レシピ中の食材の類似度を算出するのですが，
cookpad.comではユーザが自由にレシピを投稿できるため，材料の記述方法に一貫性がありません．
例えば，"玉ねぎ"という食材でも，ユーザによっては"たまねぎ"や，"玉葱"など様々な記述方法があります．
そのため，普通に類似度を算出した場合，記述方法による影響が顕著に出てしまいます．
そこで，Yahooさんの形態素解析APIを用いて，食材をすべて形態素解析し，統一した表記に変換してから類似度を算出しました．
また，ユーザの中には，調理手順で使い分けるために，食材に記号を付けて管理している方もおられます．
そこで，これらの記号もすべて形態素解析によって取り除きました．

これらの処理で，類似度算出の前処理はできたのですが，料理レシピには食材だけでなく，調味料も記載されています．
これらを含めて類似度を算出すると調味料の数による影響が出てしまいます．
調味料は家庭に常備してあるのが一般的だと思うので，これらは類似度算出には含めない処理が必要でした．
そこで，Web上の調味料辞典とレシピの食材のマッチングを取り，一致するものは類似度算出から除外しました．
この際にも，調味料辞典とユーザの表記の違いのため，形態素解析により表記を統一しました．
また，調味料辞典が膨大な量の調味料を含んでいるため，マッチングの処理が重たくなってしまったので，pythonのcollectionsライブラリを用いてオーダーを減らしました．

これらの工夫をすることで，ある程度の精度で推薦することができるようになりました．
今回は，Cookpadさんにご迷惑がかからないように，推薦対象のデータを少なくしているため少し精度が低いですが，データを増やすことでかなり高精度の推薦ができるかと思います．
また，Cookpadさんや，YahooさんのAPIをかなりの回数叩いているので，処理が重くなっています．
工夫点としては，マルチスレッドでのアクセスを行って，処理を軽くしています．この工夫を行うことで15s以上かかっていた処理が6s前後で処理できるように成りました．
しかしまだまだ遅い状態です．使用する際は温かい目で見守っていただけると幸いです．
また，チャットにおいてテキストだけの行き来だとつまらないかなということで，本当はスタンプ等を実装したかったのですが，HTMLタグの使用ができるようにして代用しています．
タグ（h1,imgなど）をしようしてもらい，自由に表現をできるようにしています．（scriptタグはエスケープしています．）

以上が今回の実装の説明になります．
大変長くなりましたが，ここまで読んでいただきありがとうございました．