# els_utils

## Dependency

 - python >= 3.6
 - curl
 - jq

## install

```Bash
cd ~
git clone https://github.com/aokad/els_utils.git
cd els_utils
python setup.py build install
```

## How To Use

### 1. kibana

#### 1.1 現在のオブジェクトを確認する

dashboard, visualization, index-pattern, all, challenge のいずれかを `type` に指定する

```Bash
elsu-kibana list --type dashboard

type=dashboard
bash ./scripts/kibana-find.sh ${type}
```

 - all を設定すると全オブジェクトの id を表示する

```Bash
elsu-kibana list all

bash ./scripts/kibana-find.sh --type all
```

 - [bateira向け] challenge を設定すると challenge-id を表示する

```Bash
elsu-kibana list challenge

bash ./scripts/kibana-find.sh --type challenge
```

#### 1.2 オブジェクトを破棄する

デフォルトインデックスを除いてダッシュボード、ビジュアライゼーション、インデックスパターンを削除する
（データは残す）

 - 全てのオブジェクトを削除する場合

```Bash
elsu-kibana remove --type all

bash ./scripts/kibana-remove.sh all
```

 - challenge-id を指定する場合

```Bash
elsu-kibana remove --type challenge --challenge_id ${challenge-id}

bash ./scripts/kibana-remove.sh challenge ${challenge-id}
```

 - オブジェクトを指定する場合

dashboard, visualization, index-pattern のいずれかを `type` に指定する

```Bash
elsu-kibana remove --type dashboard --object_id ${object-id}

type=dashboard
bash ./scripts/kibana-remove.sh ${type} "${object-id}"
```

### 2. Elastic Search

#### 2.1 データベース（Elastic Search における Index）一覧をみる

簡易表示

```
elsu-es list --type db

bash ./scripts/es-find.sh db list
```

詳細も表示

```
elsu-es list --type db --detail

bash ./scripts/es-find.sh db list-detail
```


#### 2.2 データベースのテーブル（Elastic Search における Type）を確認する

```
elsu-es view --type table --index munchkin-strelka2-analyzed

index=c-cat-mutation-20181107-strelka2-analyzed
bash ./scripts/es-find.sh table ${index}
```

#### 2.3 データベースのレコード（Elastic Search における Document）を確認する

```
elsu-es view --type record --index munchkin-strelka2-analyzed

index=c-cat-mutation-20181107-strelka2-analyzed
bash ./scripts/es-find.sh record ${index}
```

#### 2.4 データベース削除

```
elsu-es remove --index munchkin-strelka2-analyzed

index=c-cat-mutation-20181107-strelka2-analyzed
bash ./scripts/es-remove.sh ${index}
```

