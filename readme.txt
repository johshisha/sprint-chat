***botの使い方***
helpコマンド
    -bot (-h, --help, help): botの使い方を表示する．

pingコマンド
    −bot ping : ステータスをチェックする．

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
        できるだけ引数の材料名だけで作れる料理を推薦する．推薦元の内容によっては他の材料を使うレシピもある…
        引数: 空白区切りの一つ以上の材料．．

    −bot cook trends
        cookpad.comで今人気の食材を使った料理を推薦する．

aliasコマンド
    -bot alias list : 登録されているaliasの一覧を返す．
    -bot alias add 'name' 'content': aliasを登録する．name:aliasの名前, content:aliasの内容．(登録の際は，どこからどこがコマンドなのか明示するため''を付けてください．)
    -bot alias delete name: aliasを削除する． name:aliasの名前．
    -bot alias delete -all: aliasをすべて削除する．