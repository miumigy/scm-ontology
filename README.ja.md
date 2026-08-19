# SCM Ontology

> **サプライチェーン・マネジメント（SCM）のためのフレームワーク非依存の基準意味モデルです。企業データ、基準事実、グラフ推論、投影、そして将来のSCM OS実装を接続しつつ、ソースシステム固有の意味論が暗黙に「真実」になることを防ぎます。**

[![CI](https://github.com/miumigy/scm-ontology/actions/workflows/ontology.yml/badge.svg)](https://github.com/miumigy/scm-ontology/actions)

**[English](./README.md) | 日本語**

## このプロジェクトが存在する理由

企業のSCMデータは豊富である一方、分断されています。ERP、WMS、TMS、APS、計画、物流、調達、製造、分析などの各システムは、それぞれ固有の識別子、意味論、時間的ルール、前提条件を持っています。

SCM Ontologyは、これらの異なる表現と、その下流にあるグラフ／推論アプリケーションの間に位置する、**意味統制基盤**を提供します。

中心となる設計原則は次のとおりです。

> **基準情報は統治されるものであり、対応付け、類似度計算、推論、投影、またはデータ取り込みが成功したことだけを理由として、暗黙に生成されることはありません。**

## SCM Ontologyとは

**SCM Ontology**は、サプライチェーン・マネジメントのためのフレームワーク非依存の基準意味モデルです。サプライチェーンを記述する基準エンティティ、関係、イベント、状態、制約、意思決定、KPI、リスクを、特定のERP / WMS / TMS / APSや計画製品の語彙から独立して定義します。

これは、企業内の根拠情報を対応付けるための**統治された語彙**です。異なるソースシステムの情報を共通の意味空間で扱い、特定のソースシステムが暗黙に「正解」になることなく、相互に推論できるようにします。

## SCM OSとは

**SCM OS**（サプライチェーン・オペレーティングシステム）は、基準意味モデルの上に構築される**統治された運用レイヤー**です。基準事実と基準グラフの状態を、説明可能なビジネス意思決定へ変換します。

```text
企業の根拠情報 → 統治された基準化 → 基準グラフ / 状態
→ ビジネス上の問い → 説明可能な推論 → シミュレーション / 最適化
→ 承認 / 統治 → 実行 → 結果 → 基準イベント
→ 次の意思決定
```

SCM OSは、状態、統治、承認、実行境界、監査を担います。AIやエージェントは**推論または提案を提供するプロバイダとしてのみ**動作し、基準情報を直接変更することはありません。

## 現在の状況

**リファレンス・アーキテクチャと統治されたリファレンス・ランタイム：完成 — 一次公開 / リリース候補の準備段階**

SCM Ontologyの意味モデルとSCM OSリファレンス・ランタイムは、統治された認知ループ全体をカバーしています。具体的には、観測、意思決定コンテキストの構築、ルール／LLMによる推論プロバイダ、提案の検証、承認／統治、実行（インメモリかつ副作用なし）、業務ワークフロー、監査／再現、永続グラフ・バックエンド（リレーショナルおよびNeo4j）、クローズドループ実行、リファレンス・データ・アダプタ、制約付き自律制御などです。

これは**リファレンス実装としての品質を示すリリース**であり、あらゆる本番用コネクタ、グラフデータベース、スケジューラ、データ取り込みエンジンが実装済みであることを意味しません。次の目標は **SCM Ontology v0.1 / SCM OSリファレンス v0.1** の一次公開です。

一次公開の標準実行経路と受入検証は、次のコマンドで実行できます。

```bash
PYTHONPATH=src python -m scm_ontology.primary_launch --self-check
PYTHONPATH=src python -m scm_ontology.primary_launch_acceptance --self-check
```

過去の開発で使用した `Sxxx`、`Mxx`、`Px-x` の識別子は、トレーサビリティのためマイルストーン文書に残しています。現在の一次公開の対象範囲については、[ドキュメント・マップ](#ドキュメントマップ) と [`docs/launch/`](docs/launch/README.md) を参照してください。

## クイックスタート

新しい環境で一次公開の標準実行経路と受入検証を実行します。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

export PYTHONPATH=src
python -m scm_ontology.validator
python -m scm_ontology.primary_launch --self-check
python -m scm_ontology.primary_launch_acceptance --self-check
pytest -q
```

標準実行経路は、統治されたリファレンス・ランタイムを、決定的かつ内容アドレス付きの1つの結果へ組み立てます。**外部への副作用は発生せず、基準情報も変更しません。** 詳細なシナリオは [`docs/launch/golden-path.md`](docs/launch/golden-path.md)、L5受入チェックリストは [`docs/launch/acceptance.md`](docs/launch/acceptance.md) を参照してください。

リポジトリ内で開発する利用者であれば、概念の理解に約5分、実行に約10分、拡張に約30分で到達できることを目指しています。

## アーキテクチャ概要

```mermaid
flowchart LR
    A[企業システム\nERP / WMS / TMS / APS / Planning] --> B[情報源の根拠と出所]
    B --> C[変換 / 対応付け境界]
    C --> D[基準識別子]
    D --> E[基準事実]
    E --> F[事実バージョンとライフサイクル]
    F --> G[競合 / 解決]
    F --> H[履歴照会]
    F --> I[基準グラフ]
    I --> J[投影]
    J --> K[実体化]
    K --> L[無効化 / 依存関係への影響]
    L --> J
    J --> M[投影間の整合性]
    M --> N[運用統治]
    N -. 統治された適用 .-> F
```

### 意味境界

```mermaid
flowchart TB
    subgraph SOURCE[企業システム上の表現]
        ERP[ERP]
        WMS[WMS]
        TMS[TMS]
        APS[APS / Planning]
        EXT[その他の情報源]
    end

    subgraph BOUNDARY[統治された変換境界]
        MAP[対応付け]
        GAP[意味の差異]
        AMB[曖昧さ]
        PROV[出所 / 根拠情報]
    end

    subgraph CANONICAL[基準意味レイヤー]
        ID[基準識別子]
        FACT[基準事実]
        VER[事実バージョン]
        GRAPH[基準グラフ]
    end

    ERP --> MAP
    WMS --> MAP
    TMS --> MAP
    APS --> MAP
    EXT --> MAP
    MAP --> GAP
    MAP --> AMB
    MAP --> PROV
    MAP --> ID
    ID --> FACT --> VER --> GRAPH
```

**重要：対応付けは状態変更ではありません。** 対応付けの結果は、明示的な統治された適用ステップによって基準状態が作成・変更されるまでは、根拠情報を伴う提案／結果として扱われます。

## 機械可読な基準レジストリ

```mermaid
flowchart LR
    MODEL[基準モデル\nPython意味レジストリ] --> REG[機械可読レジストリ\nregistry/canonical-registry.v0.2.json]
    REG --> LOAD[機械可読レジストリ読込器]
    LOAD --> VALIDATE[検証と一意性確認]
    VALIDATE --> DRIFT[PythonとJSONの差異検出]
    DRIFT --> MAP[基準化]
    MAP --> FIX[複数ソースを想定したテスト用データ]
    FIX --> GRAPH[基準グラフ・ランタイム]
```

レジストリは**意味上の語彙を定義する成果物であり、ストレージ・スキーマではありません。** 安定した概念識別子、概念レイヤー、世界レイヤー、説明、関係述語、エンドポイント、カテゴリなどを保持します。リポジトリに格納されたレジストリは `src/scm_ontology/canonical_model.py` と照合・検証されるため、意味上のドリフトは見えにくいドキュメント不整合ではなく、テスト失敗として検出されます。

[`registry/canonical-registry.v0.2.json`](registry/canonical-registry.v0.2.json) と [`docs/roadmap-post-m8.md`](docs/roadmap-post-m8.md) を参照してください。

## 基準情報のライフサイクル

```mermaid
stateDiagram-v2
    [*] --> proposed
    proposed --> active: 統治された適用
    active --> superseded: 新しい統治済みバージョン
    active --> disputed: 統治された異議申立て
    active --> invalidated: 統治された無効化
    active --> retired: 統治された廃止
    disputed --> active: 明示的な解決
    disputed --> invalidated: 明示的な解決
    superseded --> [*]
    retired --> [*]
    invalidated --> [*]
```

すべての事実バージョンは、再構築に必要となる出所情報（出所・証跡）、ソース識別情報、スコープ、時間的基準、ライフサイクル履歴、統治上の判断を保持します。

## 読み取り・派生・変更の境界

```mermaid
flowchart LR
    READ[読み取り / 履歴照会]
    REASON[推論 / 分析]
    PROJ[投影 / 実体化]
    INV[無効化 / 整合性確認]
    WRITE[統治された適用]
    CANON[(基準情報)]

    CANON --> READ
    CANON --> REASON
    CANON --> PROJ
    CANON --> INV
    READ -->|読み取り専用| OUT[観測可能な結果]
    REASON -->|読み取り専用| OUT
    PROJ -->|読み取り専用| OUT
    INV -->|読み取り専用| OUT
    WRITE -->|明示的な状態変更境界| CANON

    style WRITE stroke-width:3px
    style CANON stroke-width:3px
```

基本姿勢は**読み取り専用**です。基準情報を変更できる唯一の経路は、明示的かつ統治された適用ステップです。

## 開発履歴

詳細なマイルストーンとスライス契約（過去の `M8` / `Sxxx` 開発シーケンス）は、[`docs/milestones/`](docs/milestones/) および `docs/` の定義・仕様インデックスに保存されています。これらはエンジニアリング上の開発履歴であり、一次公開の主要な表面ではありません。現在のプロダクトとしての表面は [`docs/launch/`](docs/launch/README.md) で定義されています。

## 非妥協の不変条件

1. **基準情報を暗黙に変更しない** — 対応付け、推論、照会、投影、実体化、無効化、再現、復旧は、基準情報を黙って変更しません。
2. **基準情報と派生結果を混同しない** — 推論、集計、類似度、確信度、投影の結果は、基準事実とは区別されたまま保持されます。
3. **出所情報を失わない** — ソース識別情報と根拠情報は、統治された結果に紐付いたまま保持されます。
4. **履歴を失わない** — 事実バージョン、ライフサイクル遷移、競合、解決、投影、無効化を再構築できます。
5. **不確実性を失わない** — 未解決、競合、陳腐化、一部欠損、失敗、未サポート、不明といった結果を観測可能な状態に保ちます。
6. **再現を第一級の機能とする** — 統治された意思決定と実行は、履歴を暗黙に書き換えることなく再現できます。
7. **スコープを明示する** — Enterprise、Tenant、Organization、Productなどの境界を暗黙に拡張しません。
8. **ベンダー固有の意味論を基準オントロジーの外に置く** — 明示的に統治対象とし、バージョン管理しない限り、ベンダー固有の意味論を基準オントロジーへ持ち込みません。

## このリポジトリが提供するもの／提供しないもの

### 提供するもの

- SCMの基準意味モデル
- 統治された語彙と関係モデル
- 企業データを基準化するための定義・仕様レイヤー
- 基準グラフとグラフ推論の基盤
- 投影とSCM OSアプリケーションの基盤
- 回帰テストによって保護された実行可能な仕様

### 現時点では提供しないもの（一次公開の境界）

**SCM Ontology v0.1** / **SCM OSリファレンス v0.1** はリファレンス実装です。統治されたリファレンス・アーキテクチャを実証するものであり、以下を提供済みであるとは主張しません。

- SAP / ERP / WMS / TMS / APSの汎用コネクタ・スイート
- 本番規模のグラフデータベース製品、または本番HA / SLA
- マルチテナントSaaS、エンタープライズIAM、セキュリティ認証
- 自律的なオントロジー学習エージェント、またはグラフへ直接書き込むエージェント
- 無制限の自律実行、または暗黙の外部副作用
- 対応付け、推論、投影、取り込みが成功しただけで、データが基準情報になる仕組み
- Optimizer / APSの代替製品、または本番規模の取り込み / スケジューラ

これらの境界を明確にすることは弱点ではなく、リファレンス実装としての主張の信頼性を高めるための重要な設計です。実際の企業システム連携、マルチテナント展開、エンタープライズIAM、運用監視、性能・スケール対応、より高度なSCMアプリケーションは、一次公開後のテーマです（[`BACKLOG.yaml`](BACKLOG.yaml) を参照）。

## ドキュメント・マップ

| 領域 | エントリーポイント |
|---|---|
| プロジェクト概要 | `README.md` |
| ドキュメント・インデックス | `docs/README.md` |
| 現行アーキテクチャ | `docs/architecture/current-architecture.md` |
| 機械可読レジストリ | `registry/canonical-registry.v0.2.json` |
| レジストリ・ローダー | `src/scm_ontology/machine_registry.py` |
| マイルストーンと受入 | `docs/milestones/` |
| M8クローズ契約 | `docs/milestones/S310-m8-acceptance-closure.md` |
| 意味定義・仕様 | `docs/semantics/` および関連文書 |
| バックログ／将来実装 | `BACKLOG.yaml` |
| エージェント開発ルール | `AGENTS.md` |
| 一次公開インデックス | `docs/launch/README.md` |
| 標準実行経路 | `docs/launch/golden-path.md` |

## 開発思想

```mermaid
flowchart LR
    I[調査] --> M[モデル化]
    M --> C[定義・仕様]
    C --> T[テスト]
    T --> D[文書化]
    D --> P[PR]
    P --> G[統治されたマージ]
    G --> I
```

CIがGreenであることは必要条件ですが、十分条件ではありません。**テストはGreenにするために弱めるのではなく、意味上の境界を守るために存在します。**

## ロードマップ

開発は、無制限に増加する内部管理番号 `Sxxx` / `Mxx` / `Phase-x-x` ではなく、**リリースを軸として管理します。** 現在の目標は次のとおりです。

- **SCM Ontology v0.1** / **SCM OSリファレンス v0.1** — 一次公開 / リリース候補。統治されたリファレンス・アーキテクチャは完成しており（[開発履歴](#開発履歴)を参照）、公開対象は標準実行経路とL5受入です。

一次公開後は `v0.1.0`、`v0.2.0`、`v0.3.0` のようにリリース単位で進め、新しい機能開発をその時点で新しいロードマップに再定義します。正式な引き継ぎ方針と非主張事項については [`docs/primary-launch-handoff.md`](docs/primary-launch-handoff.md) を参照してください。

## 貢献ガイド

- 最初に [`AGENTS.md`](AGENTS.md) を読んでください。基準情報境界、出所情報、統治、再現などの非妥協の不変条件を定義しています。
- 一次公開後のアイデアについて、新しいPhaseを開始したり、新しい `Sxxx` 番号を発行したりしないでください。まず、**一次公開の阻害要因**、**公開前の重要な改善**、**一次公開後のバックログ** のどれに該当するかを判断し、必要に応じて [`BACKLOG.yaml`](BACKLOG.yaml) に記録してください。
- 新しい定義・仕様を導入する前に、既存の統治された定義・仕様を組み合わせて解決できないかを検討してください。
- すべてのSchema / 定義・仕様の変更には検証とテストを追加してください。CIをGreenにするためにテストや受入条件を弱めてはいけません。
- ブランチ運用は `main` → 集中した機能ブランチ → CI → PR → Review → 統治されたマージ の流れに従ってください。

## ライセンス

このプロジェクトは[MIT License](./LICENSE)の下で公開されています。

Copyright (c) 2026 miumigy.
