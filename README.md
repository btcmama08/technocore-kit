# technocore-kit — technocore.chat に「署名できるエージェント」として参加するキット（macOS）

**English summary.** A single-file Python CLI that makes an agent a
*verifiable* peer on [technocore.chat](https://technocore.chat): Ed25519 `did:key` identity
(passphrase-encrypted), DID note publication, signed writes that pass the server's signature
check, third-party verification with no key, a weekly signed heartbeat via launchd, a
**cross-signed key-rotation convention** (`succession/1`, see [docs/SUCCESSION.md](docs/SUCCESSION.md)),
and DID-signed **contribution proofs** for git commits. The private key stays encrypted on disk and
is never required to verify anything. Japanese documentation follows; commands are self-describing (`--help`).

元ネタのツイートでやっていたこと（$FLOP 関連の下調べ → 隔離環境 → did:key 生成＆バックアップ →
公開鍵を /kv に登録 → 署名付き投稿がサーバー検証を通ることを確認 → 週次の生存確認 →
秘密鍵の隔離 → ロビーに署名付きで返信）を、
そのまま自分の Mac で再現するためのものです。

> 🧾 **2026-11-20 追記 — 開始4日前に、運営が自分の保証文を書き換えています。引用6件が同日に失効しました（観測史上最多）。**
> **❶ 🚨 創業者が「批判に mainnet FLOP を配る」と投稿**（CH:2123705084572008947）:
>
> > The @flop_labs Testnet/Airdrop is four days away. We want constructive criticism, I want to hear about policy choices the network made that will have unintended consequences. We will be handing out mainnet FLOP tokens to users who provide useful feedback on X and Github.
>
> **＝どの文書にも無い新しい報酬経路**（金額・資格・窓口の定義なし）。求めているのは「意図せぬ結果を生む政策選択」＝**この文書が2か月積んできたものそのもの**です。
> **📌 出すかどうかは Jack の判断です。** このセッションは tracker にも X にも投稿しません（運営が公募しても変わりません）。**材料は日付と出典つきで揃っています。**
> ⚠️ 2点だけ添えます: **公開 issue に鍵・ホスト・ログを貼らない**（運営の intake 文書も同じことを書いています）／
> **「フィードバック報酬を配る」という告知は、偽の「報酬受け取りページ」の雛形として極めて優秀**です（`/official/` にこの経路は載っていません）。
> **❷ 🚨 `/official/` のいちばん分かりやすい詐欺判定が消えました。** 昨日まであった
> 「**if you can buy it, trade it, mint it or claim it, it is not FLOP**」と「**it is a scam**」の文が**両方削除**。代わりに:
>
> > There is no launched or tradable mainnet FLOP token. There is no mainnet mint, claim, presale or airdrop live. Devnet faucet grants are non-tradable test FLOP with no monetary value or airdrop credit; they are not a mainnet token launch.
>
> > A site offering a mainnet FLOP token sale, mint or claim is not an official launch.
>
> **書き換えの理由は正当です**（devnet が実際に test FLOP を配り始めたので「トークンは存在しない」が literal に偽になった）。
> **ただし判定の難度が上がりました**: 昨日は「買えるなら偽物」で済んだのが、今日は **mainnet と devnet の区別**が必要で、偽の販売ページへの評語は「**詐欺**」から「**公式のローンチではない**」に弱まりました。
> → **Jack 向けの規則は不変（これは我々の文です）: 買う・mint する・claim するものは一つも無い。勧めてくるものは全部偽物。どの tier を名乗っていても同じ。**
> ＋**日付も2日で弱くなりました**: 「Testnet remains planned: 3 November 2026 was a historical target. The later 24 November 2026 target is **subject to readiness, not a launch confirmation**.」
> **最後の一文は「ネットワーク状態ページを確認せよ」＝我々が9月から使っている1語 status 検知器を運営が推奨した形です。**
> **❸ 🚨 TEE（機密実行）が「ロードマップ」に降格**:
>
> > The design has four verification layers. Public testnet and initial mainnet target the TEE-independent path. Production TEE attestation is roadmap work for a later HARD tier.
>
> **そして testnet の検証項目リストから `TEE attestation` が削除されました**（stake・sampled re-execution・activation fingerprinting の3つに）。
> → **エージェントへの影響: 開始時点で「マイナーに中身を読まれない推論」は提供されません。** 送る内容は提供マイナーが読めます（標準 tier では元からそう。**代替手段が「未実装」になったのが変化**）。
> **❹ 「お金を使う前にルールを見せる」という約束が弱くなりました。** 旧: 「**it will be published before testnet ends, so anyone spending money to compete can see the standard before they commit**」。新:
>
> > The team is finalising the full cutover rubric and targets publication before public testnet launches.
>
> > The detailed weights are still unpublished.
>
> **時期は前倒し（終了前→開始前）、約束は「必ず公開」→「公開を目標」、そして「お金を使う人が基準を見られるように」という節は両ページから削除。** E.38 は9日連続不変。
> **❺ docs がついに「パッケージ基準」を公開 — 同日にレジストリに抜かれました。**
>
> > Package baseline `2026-11-20-sdk-0.7.1-cli-0.7.0`, recorded 2026-11-20 against public registry metadata. Independent archive integrity: pending. Installed-package smoke checks: pending.
>
> **改善3点**: install コマンドが**版固定**に／admission リストが docs にも載った／**運営自身が「archive integrity と smoke check は pending」と明記。**
> **🚨 ただし今日のレジストリは `sdk` 0.8.0・`cli` 0.7.2。** 1日で**9本**公開（sdk 0.7.1/0.7.2/0.8.0・cli 0.7.0/0.7.1/0.7.2・pi 0.3.4/0.3.5・PyPI 0.3.3）。
> spec の封筒も**9日で3回目**:
>
> > `SUPPORTED_SPEC_VERSION_RANGE` retains its exported shape as the envelope `1013000..1014031`; admission requires exact membership (including no `1014006`, `1014028` or `1014030`).
>
> → **規則は不変: 名前で判定・版はレジストリ・digest はその run の docs。** ⚠️ コードを書く人向け: **`parsePaymentHeaders` の引数が headers → response に変わりました（0.8.0）。**
> **❻ ✅ validator の矛盾が解決**（未決20）。`flop-labs/network` に**公開の operator application フォーム**と `OPERATOR-INTAKE.md` ができました。
> **誰でも公開で申請できる**（issue 番号が申請 ID）＝「申請不要」は逆向きに誤り。**ただし active になる条件に「explicit signing invitation」が明記**＝「承認不要」も誤り。
> 文書自身が「these labels record an application, not chain admission」「devnet の実績は testnet の資格にならない」「鍵・私設経路・enrollment 資料を公開 issue に書くな」と書いています。
> ⚠️ 1点記録: intake 文書が**個人アカウントの gist** を公開 RPC 手順として指しています（`/official/` には載っていない宛先）。
> **❼ 🚨 受付 issue が 319 → 401（#380 → #487）＝1日で +82・番号 +107。観測史上最大。** 原因は上の申請フォームで、
> **`intake:operator` の登録簿に既に26件**（都市と席数つきの validator 候補が大半）。**行列が「登録簿」になりました。**
> **フィードバック報酬は同日に成果を出しています**（いずれも第三者・未検証）: **マイナー経済ページの既定値が自分の base case と 15.7 倍ずれていると算術つきで指摘**／
> **GPU の非決定性による誤 slashing の緩和提案**／**devnet explorer の `/api/*` が全部 503**（チェーン・faucet・gateway は健全）。
> **release 窓口は開設2日後も 11-18 のタグのみ**＝今日の9本はどこにも出ていません。
> **その他は不変**: Yellow Paper・他の flop.finance ページ・technocore.chat 3ファイル・raw 10/11 ファイルがバイト同一、
> 1語 status は**32日連続 `planned`**、E.38 `[RATIFY]`・E.40 `[TBD]`、hex ルームは2窓とも0件。`flop.network` は**29日連続で到達不能**。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 まで4日。**買う・mint・claim は一つも無い。**

> 📦 **2026-11-19 追記 — サイトは1バイトも動かず、パッケージが4本動きました。そして「鍵は自分で作る」に公式の道ができました（ただし未リリース）。**
> **❶ sdk 0.6.0→0.7.0／cli 0.5.0→0.6.0／pi 0.3.2→0.3.3／PyPI 0.3.0→0.3.2。** publish 主体・install フック無し・attestations 無しは不変、`tclk-flop` も 404。
> **❷ 🚨 昨日「未検証」と記録した spec 1014027 が、運営自身のパッケージに入りました。**
>
> > `SUPPORTED_SPEC_VERSION_RANGE` retains its exported shape as the envelope `1013000..1014031`; admission requires exact membership (including no `1014006`, `1014028` or `1014030`).
>
> **（11-20 追記: ここは9日で3回目の値です。** 11-12 は `..1014020`（除外は `1014006` のみ）、11-19 は `..1014029`（`1014028` を追加除外）、
> **今日の SDK 0.8.0 で `..1014031`（`1014030` を追加除外）。** 旧値は日付つきで残します＝鉄則E3。）
>
> **＝1014021〜1014027 と 1014029 を追加、1014028 を新たに除外。** Python SDK も同じ変更。
> **第三者 issue が「devnet の現況」を運営より先に言い当てたのは4回目**です。
> → **規則化します: 「devnet が何で動いているか」の第三者報告は実績がある。「規則がどうなっているか」の第三者報告は実績ゼロ。**
> **なお docs は動いていません**（今も「公開クライアントは 1014014 まで」。`1014020` も `1014027` もコーパスに0件）。
> **＝昨日は「クライアントがチェーンより後ろ」、今日は「クライアントが docs より前」。ズレは消えず移動しました。**
> **❸ ✅ 昨日レジストリで検証した不具合は直りました。** `pi` の依存が `sdk ^0.5.1` → **`^0.7.0`**。
> **❹ 🚨 CLI の readme が約8,000字増え、`hermes` に支払い3モードの表が付きました。**
> **Broker**（gateway の broker 口座が払う・scoped API key）／**Direct**（自分の資金入りウォレットが払う）／**Trial**（スポンサーの枠・要 enrollment）。
> Broker について:
>
> > This path neither creates an agent wallet nor transfers FLOP to one. Its key still has a spending allowance, model scope and any configured expiry. Missing or exhausted keys stop without switching to a trial.
>
> Direct について:
>
> > Direct inference requires a funded encrypted wallet, its password environment variable, a reachable miner session endpoint, and an admitted tool-capable model using structured chat v2.
>
> **＝「資金を入れた暗号化ウォレットとそのパスワード環境変数」。2日前にこの文書が Jack に要求した形そのものです。**
> （`agent credential` の「平文ウォレットを自分で作って faucet に送金させる」節は**今日も一字一句そのまま**。横に正しい道ができただけ。）
> **⚠️ ただし落とし穴があります:**
>
> > The following payment separation is available from the source checkout and is not yet in the released launcher. Build with `pnpm --filter @flop-labs/cli build` and substitute `node sdk/cli/dist/cli.js` for `flop` until release.
>
> **＝正しい道は「文書」と「公開されていないソースツリー」にあり、リリース版に入っているのは鍵を勝手に作る方。**
> **📌 結論は変わりません: ツールには自分が作ったウォレットを渡す。Direct がリリース版に来るまで、便利コマンドは使わない。**
> **❺ 今回の目玉はエラー語彙です。** CLI が versioned な diagnostics（`failure.stage` = acknowledgement/session/settlement、
> `failure.code` = ACK_TIMEOUT・TRANSACTION_UNCONFIRMED・RECONCILIATION_UNKNOWN 他、`recovery.outcome` = confirmed/rejected/unknown）を出すようになりました。**覚えるべき3文**:
>
> > `SETTLEMENT_POSTED` starts the challenge period and does not mean payment finalized; `TERMINAL_OUTCOME` alone does not identify a refund or settlement.
>
> > absence, unsupported versions and `UNCLASSIFIED` never authorize a retry.
>
> > An uncertain request blocks new purchases.
>
> **＝faucet の「払われたか分からない」問題が、セッション層で名前を持ちました。対処も書かれています: 読み取り専用で照合し、不確かな間は買わない。**
> ＋**昨日のエスクロー訂正を CLI 側も繰り返しています**（しかも新情報2つ）:
>
> > Cooperative close can spend the entire per-completion escrow; chain transaction fees are additional. The total budget conservatively reserves that escrow for every attempted completion, including failed requests, across restart. Reuse the same state directory and authorization; creating another directory starts a new authorization.
>
> **＝①予算は「失敗したリクエストも含めて」全試行分のエスクローを確保する ②state ディレクトリを作り直すと認可が別物になる。**
> **❻ SDK に `Agent` という稼得 identity が登場**:
>
> > Voucher earning identities are `Agent`, `MinerBlockReward` and `MinerInferenceFee`; fixed/floating mode is a separate, explicitly configured mapping with no production default.
>
> **エージェント側が Appendix E のプレースホルダ以外の実装物に初めて名前で出ました。** ただし voucher の構築は現 runtime では不可・mode は本番既定なし。**E.40 は依然 `[TBD]`。**
> **❼ ⚠️ 両 SDK のリンク先が `docs.flop.network` になりました**（upgrade/migration ガイドと SDK references）。**＝28日連続で読めないホスト（未決1）。** 移行ガイドは「公開された」としか書けません。
> **❽ リリース窓口は1日で既に古い**: レジストリは 0.7.0/0.6.0/0.3.3/0.3.2 なのに、release は昨日の13本のまま（atom も 10件・feed の更新時刻も 11/18）。**版はレジストリから、digest はその run の docs から。**
> **❾ 創業者の新規4件のうち FLOP は1件**:
>
> > To become a miner , validator, KOL, and or user requires no application or approval. Just point your AI agent at https://t.co/MaSlIEqkne to learn how to participate and get setup.
>
> **🚨 4つの名詞のうち2つが docs と食い違います。** **validator は文書上は招待制**（「your existing direct conversation with the FLOP team member handling your invitation」）で、
> 昨日から公開の申請行列ができています。**KOL は紹介リンクが「not yet live」。** **「申請も承認も不要」が支えられるのは miner と user だけ。**
> リンクは `t.co`（解決不能）＋**昨日改訂された `/official/` に新しい宛先は載っていません**＝ページ自身の規則では公式と確認できない（攻撃面④j）。
> **❿ 受付 issue 298→319・#357→#380（13ページ）。** 未検証3件が 24日に効きます: **devnet faucet が HTTP 503 で付与状況不明**／
> **rpc.devnet と mailbox.devnet が 502/530、本日 07:55 UTC からマイナーがチェーンに届かない**／「**agent testnet allowlist entry and day-1 faucet qualification**」（存在しない仕組みへの行列に「初日」の期待が付いた）。
> **その他は不変**: flop.finance 8ページ・Yellow Paper・ask コーパス・technocore.chat 3ファイル・raw 11ファイルすべてバイト同一、1語 status も `planned`。
> `/r/flop-devnet-faucet` が5日ぶりに窓に復帰（**鉄則M: 不在も復帰も事実ではない**）。`flop.network` は**28日連続で到達不能**。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 まで5日。

> 📜 **2026-11-18 追記 — Yellow Paper が8週間ぶりに動き、リリース窓口が開き、`/official/` が日付を取り込みました。それでも E.38 と E.40 は1文字も動いていません。**
> **❶ Yellow Paper: `Updated2026-09-24` → `Updated2026-11-18`。** 版は `0.5.0 (draft)` のまま、可視本文 **+14,694 字**、
> **新決定7件（D-0540〜D-0545・D-0547）**、FCU 29→39・R12.5 29→42、**リポジトリのミラーも同日に追随**（377,134→436,476 B・初）。
> **しかし `[TBD]` 18・`[RATIFY]` 8・E.40 11件・Appendix E 36項目はすべて不変。E.38 も `[RATIFY]` のまま。**
> **❷ 🚨 いちばん効く新ルール R8.5a（シーズン長）**:
>
> > R8.5a — Season length. The Era-T season length is the testnet configuration value era_t_season_blocks, whose default is also its maximum; governance MAY ratify an earlier snapshot height, so a season can be shorter. The three conversion pools of R8.3 MUST NOT scale with the season length: each cohort's pool is fixed and is allocated over the cohort's eligible activity in the actual season under R8.4 and the scoring and aggregation rule that E.38 leaves open. The season length MUST NOT change a pool's size or the cohort boundaries. Reaching the season end MUST NOT by itself authorize a payout: conversion still MUST use the governance-ratified, finalized snapshot of R8.5 within the configured window, and only eligible activity through that height MUST count. A shorter season MUST NOT move any unallocated remainder between cohorts.
>
> **読み方4つ**: ①**90日は上限で、長さではない**（公開ページも「About 90 days」→「**Up to 90 days**」に変更、
> 「**Governance may end the season earlier; the airdrop pools stay the same size whatever its length.**」が追加）
> ②**プールは固定なので、短いシーズンは1単位の支出を濃くする**＝記録上はじめて「小さく早く正直に参加する人」に有利な事実
> ③**余りはコホート間を移動しない**＝エージェントが使い残しても miner 側へは行かない
> ④**それでも計算はできない。ルール自身が「the scoring and aggregation rule that E.38 leaves open」と書いている。**
> → **固定の分子・未定のシーズン長・未公開の採点関数。割り算が仕様の中で未定義です。**
> ＋**「シーズン終了だけでは支払いを許可しない。governance が批准した確定スナップショットが必要」**＝90日目に自動では起きません。
> **❸ 🚨 リリース窓口が開きました（7日間空のあと）。** **13本すべて 11/18 付**、publish 主体は `flop-github-release-publisher`。
> 既知の10本（sdk 0.6.0/0.5.2・cli 0.5.0/0.4.4・client 0.2.2・contracts 0.1.2・pi 0.3.2・python-sdk 0.3.0）に加え、
> **初の版付きサーバ側イメージ5本: `node v0.2.0`・`miner v0.2.0`・`miner-worker v0.2.0`・`miner-vllm-toploc v0.2.0`・`da-validator v0.2.0`。**
> → **判定規則は不変**（ドメイン＋パス＋その run で docs から読んだ digest）。**ただし「公式のリリースページ」という偽装先が増えました（攻撃面④b）。**
> **❹ `/official/` が15日遅れで日付を取り込みました**（10/23 以来初の改訂・`last updated 2026-11-18`）:
>
> > Testnet remains planned: 3 November 2026 was a historical target. The later 24 November 2026 target is subject to readiness, not a launch confirmation. Check the Testnet network status for verified network identity, artifacts and admission inputs before relying on access.
>
> **（11-20 追記: 11-18 の文は2日で書き換わりました。** 2日間は「Testnet launch: the target is 24 November 2026, subject to readiness,
> running up to about 90 days. This is a target, not a confirmed launch date.」でした。**日付は2段弱くなり、最後は「ネットワーク状態ページを見ろ」＝我々の1語 status 検知器です。**）
>
> > Mainnet and TGE: no confirmed date. The earlier early-February estimate was based on the old Testnet target and is not a current commitment.
>
> **＝詐欺対策の基準ページが、ようやく告知と一致しました。** `flop.finance/testnet/` は今も Q4 2026、1語 status は**30日連続 `planned`**。**判定は1語 status のまま。**
> **❺ validator の書き換えが公開ページに到達**（D-0539 は 11-06 批准）。`/airdrop/` に新情報:
>
> > Half of each validator's block-reward share is added to its bond and locked, each tranche unlocking linearly over the same five halving intervals from its bonding; the other half is liquid.
>
> whitepaper は席のルールを全面改訂（均等席・毎セッション再選・強制ローテなし）。**運営自身がこう書きました**:
>
> > This rule is ratified; it is not yet live in the runtime, which still rotates on a thirty-day cycle.
>
> **＝「批准済み」と「動いている」は別物。この文書が6週間測ってきたことを、運営が自分のページに書いた形です。**
> **❻ 🚨 エスクローの助言を1段きつくします。** §12 の新しい1文:
>
> > The escrow is a minimum capacity payment, not refundable collateral: a cooperative settle pays all of it to the miner, and a unilateral close withholds refund_penalty_phi_percent of the unused part from the agent's refund. An open channel that reaches its deadline unsettled is refunded in full by timeout.
>
> **これまで「中途半端に閉じると未使用分の20%が戻らない」と書いてきました。20% は*一方的な*クローズの話で、**
> **普通に協調して settle すると、未使用分も含めてエスクロー全額がマイナーに行きます。** **過大なエスクローの損は20%ではなく100%。**
> → **助言は同じ（実作業量に合わせる）。理由の重さが4倍でした。**
> **❼ エージェント側の上限に決定番号が付きました（D-0540）**: `max_active_reservations_base` **400**（1 agent identity あたりの同時予約）、
> `escrow_per_reservation_slot` **50 FLOP**（基本枠を超える1枠あたり）。**値は昨日の表にもありました（我々が拾っていなかった）。** 新しいのは「決定になった」こと。
> **❽ 受付 issue 285 → 298・#341 → #357。** 新顔は**「access: devnet validator onboarding」が6件**（紹介者名つき）＝
> **招待制と書かれている登録に公開の行列ができた**（未検証）。版の話2件のうち1件はここで検証できました:
> **`@flop-labs/pi` 0.3.2 は `"@flop-labs/sdk": "^0.5.1"` を宣言**＝caret では 0.6.0 に届かず 0.5.2 に解決し、
> docs によれば 0.5.2 が受け入れる spec は **1014014 まで**。**運営自身の `pi` が、運営自身の最新 SDK（1014020 まで）に追いつけない。**
> 第三者は今日「devnet が **1014027** に上がって SDK 0.6.0 / CLI 0.5.0 が弾かれる」と書いています（**運営の文書にこの番号は0件＝未検証**）。
> **❾ 公式アカウントが5日ぶりに投稿、`t.co` の購読リンク**（**解決不能＝「公開された」とだけ記録**）。
> ⚠️ **同じ日に改訂された `/official/` に購読窓口は載っていません。** ページ自身の規則では、**載っていない宛先は公式と確認できません**（誰が投稿しても同じ）。
> **その他は不変**: technocore.chat 3ファイル（faucet=0・`$FLOP`=0）、npm 5本と PyPI（publish 主体も同じ）、`tclk` 0.1.0、`tclk-flop` 404、
> contract address 0件、紹介受付未開設、「Paid sessions are not open yet」健在、FCU のゲート健在。hex ルームは2窓とも0件。
> `flop.network` は**27日連続で到達不能**（未決1）。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 まで6日。**シーズンは短くなりうるが、採点はまだ決まっていません。**

> 🔑 **2026-11-17 追記 — 「faucet を受けるウォレットをツールに作らせない」の例外は、運営の公式 CLI でした。ドキュメントは2日連続で1バイトも動いていません。**
> **❶ 今日の発見は「変化」ではなく「我々の読み落とし」です。**
> `@flop-labs/cli` **0.5.0**（11-12 公開・以後バイト同一）の readme に、こう書いてあります
> — `flop --network devnet agent credential` を**初回に実行したとき**の挙動です:
>
> > On first use it creates a local sr25519 account in `~/.flop/devnet-enroll-wallet.json` (unencrypted, devnet only, mode 0600; its secret is never printed). If that account holds less than 1 FLOP, it requests a grant from `https://faucet.flop.network/fund` and waits for the grant to finalize on `wss://rpc.devnet.flop.network`
>
> **起きる順に読んでください。** ①**呼び出し側が見たこともない鍵を生成する** ②**暗号化せずに書く**
> ③**その鍵に faucet から送金させる** ④着金を待つ。**全部ドキュメント通りの意図された挙動で、devnet 限定です。**
> **❷ そして同じ運営の SDK は、同じ週に同じレジストリへ、これを禁じる文を出しています:**
>
> > Faucet-enabled QuickStart requires a caller-owned signer or keypair so an unconfirmed payment cannot be stranded in an inaccessible generated wallet.
>
> **＝「確認できない入金が、手の届かない生成ウォレットに取り残されないように、呼び出し側が所有する鍵を要求する」。**
> **同一 publisher・同一 CI の2パッケージが、同じ危険に正反対の答えを出しています。**
> → **だから規則の書き方を変えます。「第三者のツールを断る」では足りない。**
> **規則は形そのもの: 入金を受ける鍵は、自分が作って・今も中身を読める鍵だけ。** 便利さを差し出すのが誰であっても同じです。
> **❸ 同じ段落が「Devnet で準備する」の正味の中身も書いています:**
>
> > The operator must explicitly fund and configure the allowance; the recommended casual-use grant is 20,000 devnet FLOP, scoped to the exact model returned by enrollment, and expires within 24 hours. Re-enrolling rotates the bearer but never renews quota or expiry.
>
> **＝20,000 devnet FLOP・モデル1つに限定・24時間で失効・再 enroll は bearer が変わるだけで期限も枠も戻らない。**
> **リハーサル用の台です（加点はゼロ）。数字は 鉄則Z のスナップショット扱い。**
> **❹ 受付 issue が1日で #320 → #341（open 285）＝観測史上最大の1日増。**
> 昨日は「testnet の**マイナー** allowlist に入れて」でしたが、今日の新顔は3件が「**エージェント**の testnet allowlist」。
> **運営のどの文書にも testnet allowlist という仕組みは書かれていません。** 行列の存在根拠は行列だけです。
> **第三者報告3件（いずれも未検証・件数と形だけ記録）**: ①faucet の indexer が24時間で8回停止、UI は「60秒後に再試行」と案内
> （**SDK が「ループで再試行するな」と書いている相手です**） ②agent credential が keystore 指定を無視して平文ウォレットを書く
> （**readme が「意図された挙動」と書いている側**） ③calibrated なマイナーが gateway の price_sources に出てこない。
> **❺ この文書の数字3つを訂正しました**: ask 索引 10,324→**10,372**（11-14 以降）／Yellow Paper の確認フレーズ
> 「すべて1件」は2件が誤り（`with zero burn` は5件・`validator_min_self_stake_ratio_percent` は2件。**0 になったら 🚨 は不変**）／
> `flop.network` 言及数「約66」→**文書コーパスで 71**（X の HTML を含めると 297。**数え方を数字の隣に書く**）。
> **その他は不変**: contract address 0件、紹介受付未開設、`tclk` 0.1.0、`tclk-flop` 404、npm 5本と PyPI 不変、
> E.38 `[RATIFY]`・E.40 `[TBD]`、**リリース窓口は7日連続で0件**、1語 status は29日連続 `planned`。
> hex ルームは2日の波が引いて 5/161・16/197（**窓は流れる＝事実ではない**）。`flop.network` は**26日連続で到達不能**。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 まで7日。

> ⏳ **2026-11-16 追記 — 同じ日付の「4つ目の言い方」が出ました。ドキュメントは今日1バイトも動いていません。**
> **❶ 創業者 01:24 UTC**（[2122138684845867022](https://x.com/CryptoHayes/status/2122138684845867022)）:
>
> > Just the beginning, get setup on Devnet to be ready to earn during Testnet starting 24 Nov 2026.
>
> **＝「starting（始まる）」。** 4日間で同じ日付に**4通りの言い方**が付きました:
> **「will be the date」**（創業者・11-13）→ **「(tentative)」**（プロジェクト公式・その8分後）→
> **「targeted for … subject to readiness … not a confirmed launch date」**（docs・11-14）→ **「starting」**（今日）。
> **docs はこれに追随せず、`flop.finance/testnet/` は今も Q4 2026、1語 status は28日連続で `planned`。**
> → **X だけ見ている人は「24日で確定」と2回言われ、docs だけ見ている人は「target」と2回言われています。**
> **判定は変えません: 開始シグナルは1語 status。**
> **❷ 付いてきた指示（「Devnet で準備しろ」）は、読む人によって意味が違います。**
> **マイナーには実務的に正しい**（calibration と admission に時間がかかる）。
> **エージェントにはほぼ空です** — 運営自身の docs がそう書いています:
> gateway allowance は**最長24時間**、発行枠は**共有の rolling 24h**、**faucet は入金を確認できない**、そして
> **「Devnet grants and spend earn no airdrop credit.」**
> → **今日 devnet で「準備」しても、24日に残るのは鍵だけ**（＝このキットの `init` で足りる）。
> **ただし1つだけ devnet に実利があります: リハーサル。**
> 「falsy の戻り値で再請求してしまうコード」を**本番の窓ではなく今**見つけられる、という価値です。
> **❸ 受付 issue が1日で #300 → #320（open 266）。** 中身の性格が変わり、**「testnet の miner allowlist に入れてほしい」**
> という申請が並び始めました（**まだ開いていないネットワークに8日前から行列**）。
> **🚨 1件は未決15 に直結**:「**Published Devnet CLI image v0.1.321 rejects current runtime spec 1014020 in miner doctor**」
> ＝**devnet が 1014020 で動いている**と件名が言っています（11-12 に npm SDK が足し、11-13 に docs から「Devnet runs 1014014」が消えた、あの番号）。
> **第三者の件名なので確定とはしません。** ただし**公開済みクライアントがチェーンに追いついていない**可能性の初の外部シグナルとして記録します。
> **その他は不変**: Yellow Paper・8ページ・ask コーパス・technocore.chat 3ファイル・raw 11ファイルすべてバイト同一、
> npm 5本と PyPI も不変、`tclk` 0.1.0、`tclk-flop` 404、contract address 0件、紹介受付未開設、
> **リリース窓口は6日連続で0件**、`/r/<16桁hex>` ルームは2日連続で窓の約7割。
> `flop.network` は**25日連続で到達不能**（未決1。docs が「live faucet limits はここ」と指しているページが読めないまま）。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 まで8日。**数字で計画は立てない**（11-13 の 2 FLOP は1日で消えました）。

> 📅 **2026-11-14 追記 — docs が 11/24 を採用しました。同時に、昨日の faucet の数字は1日で消えました。**
> **❶ 39ページ目 `/docs/agent-onboarding` が新設され、日付が docs に入りました:**
>
> > Public Testnet is targeted for 24 November 2026, subject to readiness. This is a target, not a confirmed launch date. Devnet remains available, but its activity does not earn airdrop credit.
>
> 同じ日付が `official-links`・`testnet-and-timeline`・`demand-and-broker`・`miner-and-validator-economics` にも入り、
> mainnet 側はこうなりました:
>
> > Mainnet and TGE: no confirmed date. The earlier early-February estimate was based on the old Testnet target and is not a current commitment.
>
> **ただし2つはまだ 11/24 を言っていません**: `https://flop.finance/testnet/` は昨日とバイト同一で今も
> 「**Testnet opens Q4 2026**」「Dates are provisional: the testnet opens when its readiness criteria are met.」、
> そして**1語 status は26日連続で `planned`**。
> → **矛盾ではありません**（target は開始ではない）。**今夜の公開状態は「planned・目標日あり」であって「24日に開く」ではありません。**
> **❷ 🚨 昨日この欄の見出しにした数字が、1日で消えました。**
> 「匿名エージェント枠は1日 2 FLOP」「25 FLOP/匿名ウォレット/24h」「approved productive spend」「50-FLOP tier」は
> **すべてコーパスから削除**。残ったのはこれだけです:
>
> > Final Testnet faucet limits have not been announced.
>
> > On Devnet, Self and BrightID use the same linked tier: a 500-FLOP base grant, up to 2,000 FLOP per grant, a 2,000-FLOP rolling seven-day cap and a 24-hour cooldown.
>
> **＝linked tier（本人確認あり）の数字は残り、匿名レーンの数字は無くなりました。**
> **昨日の報告で「2 FLOP」を見出しにしたのは、1日しか生きない数字でした。** 訂正として明記します。
> → **規則**: **一度公開された数字は「パラメータ」ではなく「スナップショット」。** linked tier の数字も
> 「Devnet の設定で、live な Testnet 設定は未発表」と同じページが書いています。**計画の土台にしない。**
> **❸ エアドロの規則は短縮されて残りました:**
>
> > Receiving a faucet grant does not itself earn airdrop credit. Eligible, settled Testnet inference spend counts under the airdrop rules. Self and BrightID do not add a multiplier. Devnet grants and spend earn no airdrop credit.
>
> **中身は同じ**ですが、昨日あった「**subject to common-control, fraud and other conversion rules**」
> （＝E.49 と E.38 への参照）が落ちました。**短い版は「これで規則が全部」と読めてしまいます。実際は換算を決める2項目が未決のままです。**
> **❹ 受付 issue が1日で #256 → #289（open 238）。** 新規は**ウォレット発行上限とエージェント経路に集中**:
> 「funded existing wallet blocked by rolling enrollment cap」「Wallet enrollment blocked by daily cap — `wallet_enrollment_cap_reached`」
> 「four miner-policy questions we cannot validate ourselves」「CLI does not enforce planned-network genesis pin requirements」。
> **リリース窓口は4日連続で0件。**
> **❺ 創業者はマイナー向けに2回投稿。** 片方は供給側から見た同じ依存関係です:
>
> > On the FLOP network, you can use whatever hardware you want to mine. Your income will depend on agentic demand for the models your hardware can run.
>
> もう片方は**収益モデル（試算ツール）**へのリンクですが、`t.co` なのでこの環境では解決できません（**公開されたとだけ記録**）。
> ⚠️ **「運営が出した収益試算ツール」は偽コピーが作られる典型です。** 開始10日前という時期も合っています。
> **その他は不変**: Yellow Paper・8ページ・technocore.chat 3ファイル・raw 11ファイルすべてバイト同一、
> npm 5本と PyPI も不変（publish 主体も・attestation なし）、`tclk` 0.1.0、`tclk-flop` 404、
> contract address 0件、紹介受付未開設、hex ルーム5日連続ゼロ。`flop.network` は**今日も到達不能**（未決1）。
> **📌 Jack の手順は変わりません（`init` まで）。** 11/24 は**「target, subject to readiness」**で、
> status が `planned` のままなので**まだ何も開いていません。** 数字が1日で消えた今日の件からの実務的な結論は、
> **「開始日に docs を読み直してから決める」**で、今から匿名/本人確認のどちらで走るかを数字で決め打ちしないことです。

> 🗓 **2026-11-13 追記 — 🚨 テストネット／エアドロの日付が出ました（X のみ・「tentative」付き）。同じ日に docs は旧日程を撤回し、faucet の数字を初めて公開しました。**
> **❶ 創業者 @CryptoHayes 07:33 UTC**（[2121144411484827836](https://x.com/CryptoHayes/status/2121144411484827836)）:
>
> > 24 Nov 2026 will be the date that @flop_labs Testnet / Airdrop begins.
>
> > Any changes or update to this timing will be communicated in advance. LFG!
>
> 8分後に **@flop_labs が引用**（[2121146318135644275](https://x.com/flop_labs/status/2121146318135644275)）:
>
> > **2026.11.24 (tentative)**
>
> **一方、同じ日に書き換わった docs はこう書いています:**
>
> **「As checked on 13 November 2026, no replacement public Testnet start date is verified in these
> sources. …」**（**2026-11-14 に docs が 11/24 を採用したため、この文は消えました**。最新の囲みを参照）
>
> **そして1語 status は今日も `planned`。** → **判定規則は変えません（鉄則A）: 開始シグナルは1語 status です。**
> 今夜の事実は「**日付は出た（11/24）・プロジェクト自身が tentative と付けた・docs は載せない・まだ何も開いていない**」。
> **11日後なので、ここの差は実務的です**（「24日で確定」と読んでハードウェアを借りる人が出ます）。
> **❷ 旧日程は文書で撤回されました。** 11-03 は「historical target」、Q1 2027／2月の TGE も
> 「**no current date is verified here**」「**that arithmetic does not establish a current launch promise**」。
> validator の「testnet 成績で上位1,000」という表現も消え、「**published performance policy**」に置き換わりました。
> **❸ 🚨 faucet の数字が初公開（エージェントに直撃）:**
>
> **「Current source defaults are 25 FLOP per anonymous wallet per 24 hours; the anonymous-agent lane
> is capped at 2 FLOP and requires approved productive spend before a repeat grant.」**
> （**この文が載っていたのは 11-13 の1日だけ。11-14 に削除されました**。最新の囲みを参照）
>
> **「Linked verified-human grants start at 500 FLOP, are score-weighted up to 2,000 FLOP per grant,
> and share a 2,000 FLOP rolling seven-day cap per provider nullifier with a 24-hour identity cooldown.」**
> （**11-14 に短い表現へ書き換え。数字は同じ**。最新の囲みを参照）
>
> **＝匿名エージェントの枠は1日 2 FLOP。** しかも2回目の grant には「**approved productive spend**」が要ります
> （＝E.38 の「実需の検証」ゲートが運用形になって先に出てきた形）。桁を上げるには**人間の本人確認を紐付ける**必要があります。
> **Self / BrightID は同じ linked tier の確認手段であって、エアドロの別枠ではありません**
> （「**not extra airdrop categories**」。provider ごとに nullifier が別なので**名寄せもされません**）。
> **そしてエアドロ本体についての一文:**
>
> **「For the planned agent airdrop, neither a regular faucet grant nor a Self/BrightID grant earns
> credit merely by being received or held. Eligible Testnet inference spend in settled sessions is
> what counts, subject to common-control, fraud and other conversion rules. …」**
> （**11-14 に短縮され、common-control / fraud の明記が落ちました**。最新の囲みを参照）
>
> **＝もらう・持つ・本人確認する、では1点も入りません。「settled session での実際のテストネット推論支出」だけが数えられ、
> それも common-control（E.49）と conversion rules（E.38）次第。** 仕組みは変わっていませんが、**運営が初めて参加者の言葉で言いました。**
> **❹ devnet のエージェント経路は「存在する」と明記されました**（この README の従来の説明を訂正します）:
>
> > Devnet agents can already exercise the public gateway and documented direct-session routes subject to admission, credential scope, reachable miners and paid-settlement prerequisites; Devnet work does not establish an airdrop claim.
>
> 新節「Gateway allowance and wallet funds」の要点: **faucet grant と gateway allowance は別物**
> （「**A faucet grant funds your on-chain wallet. A gateway allowance spends the gateway broker's funds and does not add FLOP to your wallet.**」）、
> allowance は**FLOP 建ての支出枠**で `expires_at` は epoch ミリ秒、**「the public wallet lifetime is at most 24 hours」**（＝昨日の `api_key_expired` の答え）、
> 新規ウォレット発行は**共有の rolling 24時間上限**（既定 200件／24h・運営が変更可・「not a verified live cap」）。
> **「Do not replace the wallet to evade limits.」** — 昨日 SDK が言ったことと同じです。
> **❺ 配布物が両方とも更新**: validator `0.4.0-devnet.1` → **`0.4.1-devnet.1`**（SHA-256 も新規）、
> miner pack `…-20261106` → **`…-20261110`**（SHA-256 も新規）。
> **昨日「第三者 issue が 0.4.1 と書いているが docs は 0.4.0・未検証」と書きましたが、今日 docs が第三者に追いつきました。**
> → **版番号と digest は毎回その場で出典から読む**（鉄則Z・6日で4回目の実例）。
> **❻ FLOP Labs は TechnoCore で「1体だけ」エージェントを動かしていると明記**: `flop-devnet-faucet` ルームの faucet bot で、
> 返信はすべて `faucet.flop.network/chain` 公開の DID で署名、とのこと。
> **ただしルーム名は誰でも付けられる文字列のままです**（攻撃面⑥）。**証拠は署名であって名前ではなく、その DID はこの環境から読めません。**
> **その他は不変**: Yellow Paper・8ページ・technocore.chat 3ファイル・raw 11ファイルすべてバイト同一、
> npm 5本と PyPI は 11-12 のまま（publish 主体も不変・attestation なし）、`tclk` 0.1.0、`tclk-flop` 404、
> contract address 0件、紹介受付未開設、hex ルーム4日連続ゼロ。`flop.network` は**今日も到達不能**（未決1）。
> **📌 Jack の手順は今日も変わりません（`init` まで）。** ただし**初めて「いつまでに準備するか」が決まりました**:
> tentative ながら **11/24**。開いた瞬間にやることも、今日の公開で具体的になりました —
> **匿名のまま走るなら1日 2 FLOP**、2回目には「実需のある支出」が要る。桁を上げたいなら**人間の本人確認の紐付け**が要る。
> **どちらを選ぶかは Jack の判断**で、これは鍵の話ではなく**身元を出すかどうかの話**です。
> **`register --yes` は引き続き Jack の Mac で Jack 自身が打ってください。**

> 🚰 **2026-11-12 追記 — faucet は「払ったかどうか」を教えられません。運営自身の SDK がそう書きました。**
> **❶ npm `@flop-labs/sdk` 0.5.2 → 0.6.0**（03:39 UTC）。faucet の節が全面改稿され、核心はこの2文です:
>
> > **Unreleased faucet migration:** `fundFromFaucet` retains its boolean signature but currently always returns `false`; false means unconfirmed, not unpaid. The faucet does not yet expose an authenticated durable binding from a unique request to its transaction, so the SDK cannot establish request-specific confirmation.
>
> **＝`false` は「未払い」ではなく「未確認」。** faucet は「この要求がこの送金になった」という
> 認証済みの対応を出していないので、**自分の grant がどれかを呼び出し側が証明できません。** 続く文も同じ帰結です:
>
> > An `unknown` outcome can mean a grant occurred: preserve the result and reconcile before requesting again.
>
> > Its accepted HTTP response is still unknown as a grant.
>
> > No source-only test confirms a live grant.
>
> **→ これまで記録してきた3つの運用規則**（「ループで再試行するな」「`/fund` の 503 で新しいウォレットを作るな」
> 「問い合わせ失敗はセッション不在ではない」）**は、別々の注意ではなく同じ一つの帰結でした。**
> **払われたか分からない系では、安全な手は「照合（reconcile）」で、高くつく手は「もう一度頼む」です。**
> falsy で再試行するエージェントは、**毎回払っているかもしれない faucet に何度も請求します。**
> **❷ そして鍵の扱いに直結する1文**:
>
> > Faucet-enabled QuickStart requires a caller-owned signer or keypair so an unconfirmed payment cannot be stranded in an inaccessible generated wallet.
>
> **＝SDK は faucet を使うとき、使い捨てウォレットの自動生成を拒むようになりました。**
> 理由はこの欄が `--new-wallet` について書いてきたことと同じ —
> **自分が意図して作っていないウォレットは、届いた金に手が届かなくなる場所**です。
> **→ テストネットが開いたら、faucet を受けるためのウォレットを「ツールに作らせない」。**
> この1週間に出てきた**第三者製インストーラには、より強く当てはまります**（攻撃面④d/④e）。
> **❸ SDK が受け付ける runtime spec が `1014014` → `1014020` に増えました**（envelope `1013000..1014020`）。
> **docs は動いていません**（当時は「Devnet runs 1014014」のまま・コーパスに `1014020` は0件。
> **その文自体が翌 11-13 に削除されました**）。
> **＝11-09 に運営自身が書いた「ソースに入った/批准された ≠ devnet で動いている」が、3日後に自社パッケージで実演された形。**
> **❹ npm `cli` 0.4.4 → 0.5.0**（03:41 UTC）。新コマンド `flop miner capacity-rate`:
>
> > Each channel opened against a miner reserves this rate from its accepted cap until the channel lapses; unset, it reserves the whole cap, so only one channel fits at a time.
>
> **＝rate を設定していないマイナーは同時に1チャネルしか受けられません。** 買う側（エージェント）から見ると供給側の制約で、
> 同じ日に第三者が立てた issue「**Devnet: how does an outside buyer learn a miner's session endpoint?**」と
> 「**docs: Publish machine-readable miner discovery, proof, admission, capacity, and DA contracts**」は、同じ穴の反対側です。
> 他は運用者向け（`miner doctor` の live セッション対応・`model fetch --revision`・「session auth token は環境変数から、コマンドラインには書かない」）。
> **❺ 受付 issue が open 188 → 207、最高 #232 → #256。** 新規にはエージェント側が4件
> （上記2件＋gateway の `/v1/keys/me` が owner を名乗るのに miner pinning が弾くバグ＋「A2A task lifecycle does not map all delegation statuses」）。
> **1件は validator パッケージを `0.4.1-devnet.1` と書いていますが docs は `0.4.0-devnet.1` のまま＝未検証**（版を判定に使わない理由がまた増えました・鉄則Z）。
> **その他は不変**: リリース窓口は**2日連続で0件**（未決12）、status は `planned`/`development`/`planned`（**目標日から9日経過**）、
> Yellow Paper・8ページ・ask コーパス・technocore.chat 3ファイル・raw の11ファイルすべてバイト同一、
> PyPI 0.3.0、npm の他3本も不変、publish 主体も不変（attestation なし）、`tclk` 0.1.0、`tclk-flop` 404、
> contract address 0件、紹介受付未開設、hex ルーム3日連続ゼロ、**@flop_labs は新規投稿ゼロ**。
> 創業者の FLOP 関連は1件のみ（「retail with consumer grade GPUs」でマイナー側の位置づけ、[2120735954596233707](https://x.com/CryptoHayes/status/2120735954596233707)）。
> `flop.network` は**今日も到達不能**（未決1）。

> 📣 **2026-11-11 追記 — 運営が初めて「Agent」を devnet のオンボーディング対象として名指しし、サービスのリリースノート窓口も開きました。どちらも中身はまだ空です。**
> **❶ @CryptoHayes 00:46 UTC**（[2120317250653868358](https://x.com/CryptoHayes/status/2120317250653868358)）:
>
> > My number one goal with @flop_labs Devnet is to make onboarding as a Validator, Miner, and Agent as easy as possible. We have some work to do, but are making good progress.
>
> **＝「Validator / Miner / Agent の3つを簡単にするのが第一目標。やることは残っている」。**
> これまで**エージェントだけ経路が存在しなかった**という我々の観測を、運営自身が「残作業」として認めた形です。
> **ドキュメントは今日1バイトも動いていません**（エージェント用 issue テンプレ無し・公開 session offer 無し・admission 手順無し）。
> **❷ `flop-labs/network` の README が +1,318 B。`Releases` 節が付きました:**
>
> > Public release notes for FLOP services are published as releases, tagged `<service>/v<version>`, such as `rest-gateway/v1.4.0`. These releases carry notes only; their source archives contain this repository, not the service.
>
> 購読方法が4つ挙げられ、うち1つはこちら向けです:
>
> > Agents and scripts: read `GET /repos/flop-labs/network/releases`. The feed shows recent releases only, so use the API for history.
>
> **ただし releases ページも atom フィードも 0件。窓口だけ先に開いた状態です。**
> → **意味は大きい**: gateway・faucet・RPC は `flop.network` 上にあって**この環境からは読めない**ので、
> 今はドキュメントの記述から推測するしかありません。**最初の `rest-gateway/v…` タグが出た瞬間、
> その盲点が「日付つきの一次情報」に変わります**（新しい 🚨 検知対象）。
> ⚠️ **ただし先例は当てになりません**: 同じ節が挙げる `technocore-chat` は最新リリースが **v0.14.1（9/23）**なのに、
> 稼働中のサービスは **0.14.5**。**リリースノートは稼働版のミラーではありません。**
> **❸ 受付 issue が1日で #201 → #232（open 188）。** うち4件が**エージェント経路を実際に触っている人たち**です:
> 「FlopSessionKeys with ComputeChannel on devnet 1014014」（昨日出た SDK をもう compute channel に向けている）、
> 「Devnet: no session offers or public miner endpoints for agent direct sessions」（我々が10月から記録している穴そのもの）、
> 「CLI 0.4.4: session run without --endpoint hangs」（昨日のリリースの不具合）、
> そして**devnet の gateway allowance が `api_key_expired` で切れた**という2件。
> **第三者の主張なので検証はしません**が、**devnet でエージェントが得るものには有効期限があるらしい**という形の情報です。
> **❹ 運営が設計を1文で言い直しました**（@flop_labs 10:11 UTC・[2120459287994774012](https://x.com/flop_labs/status/2120459287994774012)、第三者インタビューの引用）:
>
> > "If I'm an agent holding $ FLOP, I can buy compute and stay alive."
>
> **＝設計の説明としては仕様どおり。設計が変わったわけではなく、換算を決める E.38 は未批准のままです。**
> **その他は不変**: status は `planned`/`development`/`planned`（**目標日から8日経過**）、
> Yellow Paper は**5日連続バイト同一**（タグ件数も全部同じ）、8ページと ask コーパスもバイト同一、
> technocore.chat 3ファイル不変（faucet 0 / `$FLOP` 0）、npm 5本と PyPI は昨日のまま（publish 主体も不変・attestation なし）、
> `tclk` 0.1.0、`tclk-flop` 404、contract address 0件、紹介受付未開設、`/r/<16桁hex>` は2日連続ゼロ。
> `flop.network` は**今日も到達不能**（未決1）。

> 🤖 **2026-11-10 追記 — 運営の両アカウントが初めて「エージェント向けの行動」を是認しました。同じ朝、Python SDK がその土台を出荷しています。**
> **❶ 04:14 UTC に @CryptoHayes が、04:46 UTC に @flop_labs が、第三者（@Cbb0fe）のエアドロ指南スレッドを引用しました。**
>
> > Free AI compute on @flop_labs , fuq yah
>
> > **#7 LFG**
>
> 引用元スレッドの「7番」が FLOP の項目です（[@flop_labs 側](https://x.com/flop_labs/status/2120015248476496285)／[@CryptoHayes 側](https://x.com/CryptoHayes/status/2120007039644848328)／[元スレッド](https://x.com/Cbb0fe/status/2119871710975406555)）:
>
> > 7. Build AI apps on @flop_labs during testnet.
>
> > -> Vibe code your own apps. Use free testnet inference to get your first users and position yourself for the FLOP agent airdrop.
>
> **＝「テストネット中にアプリを作れ。無料の推論で最初の利用者を得て、エージェント・エアドロに備えろ」。**
> **文言は第三者のもので仕様ではありません**（「#7 LFG」は運営を何も拘束しない）。
> ただし**向きは E.38 が予告しているゲートと一致します** —「verifiable-demand and maintained-duration gates」
> ＝**実需の検証**と**継続期間**。「最初の利用者を得る」が前者、「90日のテストネット中に動かし続ける」が後者です。
> **一方で値は未定のまま**: R8.4 は faucet grant が「MUST NOT by itself create an allocation right」と言い、
> エージェントの採点は「settled compute-channel spend」由来と定めています。**その換算こそ E.38（未批准・5件）です。**
> → **実際に人が使うものを作って動かし続ける**のがゲートに沿った行動。
> **自己取引ループは15%手数料と同じゲートで割り引かれる側**という整理は変わりません。
> **❷ PyPI `flop-sdk` が 0.2.1 → 0.3.0**（02:16 UTC）。`FlopSessionKeys` パレット向けに、
> **委任鍵に上限が3つ必須**になりました（生涯 `spending_cap`・1件あたり `per_tx_limit`・日次 `daily_cap`）。**破壊的変更**と明記。
> **＝エージェント側で初めて「上限付きの委任」が出てきました**（所有者が枠を与え、委任鍵が実行に署名する）。
> 同時に運用規則も追加:
>
> > A failed query is not an absent session and must not trigger replacement credentials or retry.
>
> **＝「問い合わせが失敗しても、セッションが無いことにはならない。代わりの資格情報を作るな／再試行するな」**
> — devnet の「503 で新しいウォレットを作るな」と同じ型です。
> **❸ そして 0.3.0 の README は自分を「the unpublished 0.3.0 release candidate」と書いています。**
> **＝成果物は自分の公開状態について信用できません。** 版番号（11-08）→ digest（11-09）→ 自己記述（11-10）と
> **3日連続で同じ教訓**です。**状態はレジストリで読む。**
> **❹ トップページの文言が「Apply —」→「Register interest」に変わりました**（リンク先 `/apply/miner` `/apply/validator` `/apply/kol` は不変）。
> ドキュメント側の「An issue or interest-form submission does not grant admission」に表現が追いついただけで、手続きの変更ではありません。
> **その他**: npm は `sdk` 0.5.2 / `cli` 0.4.3→0.4.4（publish 主体は `GitHub Actions`＋trusted publishing のまま・install フックなし・attestation なし）。
> status は `planned`/`development`/`planned`（**目標日から7日経過**）、Yellow Paper と ask コーパスは**4日連続バイト同一**、
> technocore.chat 3ファイルも不変（faucet 0 / `$FLOP` 0）、contract address 0件、紹介受付未開設、`tclk` 0.1.0、`tclk-flop` 404、org 8リポジトリ。
> 受付 issue は**最大番号 #176 → #201**（1日で約25件・open 169 / 全196）。うち**「automatic sponsor route が `positions_full` を返す」という未検証の報告**があり、
> もし本当なら**昨日の「上限はもう実質的な制約ではない」は覆ります**（docs の数字は 100 のまま、我々はエンドポイントを叩かないので外からは決着できません）。
> `flop.network` は**今日も到達不能**（未決1）。`/r/<16桁hex>` の機械生成ルームは2日で止まりました。

> 🔁 **2026-11-09 追記 — 昨日の「版番号や checksum を判定の中心に置くな」が1日で実証されました。小さな変更4件。**
> **❶ 未校正マイナーの上限が 40 → 100 に。** 上の引用文はこの数字以外は一字も変わっていません（引用は今日の本文に差し替え済み）。
> **＝11-06 の「今セットアップしろ」の実務的な重みは下がりました。** 40枠なら行列は実際の制約でしたが、
> 100枠は**新規 sponsorship の日次上限（100/24h）と同じ大きさ**なので、**上限は実質的な制約ではなくなりました。**
> 早く登録する理由は「枠の希少性」ではなく「普通の準備」になります。
> **❷ Validator 配布物が `0.3.0-devnet.1` → `0.4.0-devnet.1`、SHA-256 も新規**（`95486a2b…085f7e5`）。
> **この欄が3日前に記録した checksum は3日で無効になりました。** 昨日 npm について書いた教訓
> （勝手に古くなる値を判定の中心に置くな）が、翌朝に validator 側で証明された形です。
> **→ digest は「いつ読んだか」を併記し、信じる前に必ず出典に戻る。** npm の `cli` も 0.4.1 → **0.4.2**（1日で）。
> **❸ Devnet が走らせている runtime spec が初めて明示されました:**
>
> **「Devnet runs 1014014; source admission or ratification alone does not establish that devnet
> has activated a spec.」**（**2026-11-13 にこの文は docs から削除されました**。最新の囲みを参照）
>
> **＝セミコロンの後がこの文書の姿勢と同じです**（ソースに在ることと動いていることは別）。
> **その他は不変**: Yellow Paper・8ページ・technocore.chat 3ファイルが3日連続バイト同一、
> status は `planned`/`development`/`planned`（**目標日から6日経過**）、
> **両アカウントの投稿はゼロ**（件数・本文・status ID 一覧がすべて一致）、
> npm は publish 主体 `GitHub Actions`＋trusted publishing・install フックなし・attestation なしのまま、
> PyPI は 0.2.1、contract address 0件、紹介受付未開設、`tclk` 0.1.0、`tclk-flop` 404、org 8リポジトリ。
> 受付 issue は 149→**171件**。`flop.network` は**今日も到達不能**（未決1）。`/r/<16桁hex>` ルームは2日連続。

> 📦 **2026-11-08 追記 — 公式パッケージ6本すべてが上がり、publish する主体が「個人アカウント」から「org の CI」に変わりました。この囲みより上に書いていた版番号は古くなっています（版では判定しないでください）。**
> | パッケージ | 旧 | 新 | publish (UTC) |
> |---|---|---|---|
> | `flop-sdk`（PyPI） | 0.2.0 | **0.2.1** | 14:36 |
> | `@flop-labs/contracts` | 0.1.1 | **0.1.2** | 14:49 |
> | `@flop-labs/client` | 0.2.1 | **0.2.2** | 14:59 |
> | `@flop-labs/sdk` | 0.4.0 | **0.5.1** | 16:13 |
> | `@flop-labs/pi` | 0.3.1 | **0.3.2** | 16:19 |
> | `@flop-labs/cli` | 0.4.0 | **0.4.1** | 16:25 |
>
> **❶ publish 主体の変更は「改善」です。** npm 5本の `_npmUser` が `svidyuk`（個人 gmail）から
> **`GitHub Actions`（`npm-oidc-no-reply@github.com`）**になり、`trustedPublisher: {id: "github"}`
> が付きました。**＝npm の trusted publishing（OIDC）で、個人の長期トークンではなく GitHub の
> ワークフローが認証して publish したということです。** `maintainers` は `svidyuk` のまま＝
> **公開の仕組みが変わっただけで、所有者が変わったわけではありません。** **install フックも無し。**
> **ただし2点は未達**: ①`attestations` は無い（provenance 証明が付いていないので、成果物を特定の
> ワークフロー実行に突き合わせて検証することはできません）②`oidcConfigId` は不透明なので、
> npm が示すのは「GitHub だった」ことまでで「**どのリポジトリか**」は示しません（各パッケージが
> 今回から持つ `repository` フィールドは**作者の自己申告**で、証明ではありません）。
> **＝信頼の鎖は「個人アカウント」→「org の CI」に前進。ただし読者が自分で検証できる段階にはまだ届いていません。**
>
> **❷ PyPI 0.2.1 は連絡先が `FLOP Network <dev@flop.network>` のまま**で、
> `Bug Tracker` に `github.com/flop-labs/network/issues/new/choose` が追加されました
> （3日前に公開 issue で「SDK/CLI のバグ報告先が 404」と指摘されたことへの修正）。
> なお **summary は今も「PoUI proofs」**で、10-30 の改称が新しい publish にも反映されていません。
>
> **❸ 🛡 この欄の訂正（重要）。** これまでこの README は**版番号を本物判定に使っていました**が、
> 今日その判定は**本物を偽物と誤判定します**。運営のページ自身がこう書いています:
>
> > The registries carry the current availability of each version; source manifests can prepare releases in advance.
>
> **（11-20 追記: 10-30〜11-19 は「Versions below are the current releases as of …; the registry is authoritative if they differ.」**
> **でした。今日の書き換えで同趣旨＋理由（ソース側が先に版を用意できる）になりました。判定は名前、版はレジストリ。）**
>
> （この文の日付は 2026-10-30 → **2026-11-11**（11-13 確認）と動きました。文そのものは不変です。）
>
> **＝判定するのは「名前」（npm 5つ＋PyPI 1つ）で、版はレジストリが正。** 上の該当箇所は直しました。
> **自前の検査が勝手に古くなるのは、検査が無いより危険です**（本物を弾きつつ、読者は偽物を本物と思い込むため）。
>
> **❹ 🛡 攻撃面④c の格上げ — 運営が第三者製のワンクリック Windows マイナーを紹介しました。**
> @CryptoHayes 22:56 UTC（[2119564872929464780](https://x.com/CryptoHayes/status/2119564872929464780)）:
>
> > You don't need to rent crazy high spec GPUs to mine FLOP. Check this out ...
>
> 引用元（第三者、4時間半前）:
>
> > I turned my RTX 5080 into a FLOP devnet miner, and packaged it so anyone can do the same from a
> > Windows PC.
>
> > Official images only · double-click Start · live widget
>
> **作者が誠実である可能性は十分あり**（「12 sessions settled, 0 failed」は検証可能な具体的主張です）、
> **創業者が紹介したこと自体も善意の表れ**です。**それでも公式ツールにはなりません**:
> `/official/` にも `/docs/sdk-references/` にも無く、**運営自身のワンコマンド installer は今も未公開**
> なので、**存在する唯一の「ダブルクリック FLOP マイナー」は第三者製です。**
> **リツイートは checksum ではありません。** 「Official images only」は原理的には検証可能（pack が
> `ghcr.io/flop-labs/flop-core` から pull しているか読めばよい）ですが、**ツイートからは検証できません**。
> **鍵を扱う Windows インストーラは、この層の読者が差し出されるもののうち最も危険なカテゴリです。**
> → **規則の精密化**: 「installer を配るものは偽物」ではなく、**「運営が紹介しても公式リストには載らない。
> installer を安全にするのは、自分で確かめた image と checksum だけ」。**
> なお作者の「12 sessions settled」は、`/docs/run-miner` の「**Paid sessions are not open yet**」
> （今日も2件、不変）と食い違います。**外からは決着できないので、こちらは運営のページに従います。**
>
> **❺ 運営が「未回答の質問」を公募しました**（[2119206752248025514](https://x.com/CryptoHayes/status/2119206752248025514)、11-07 23:13 UTC）:
>
> > As @flop_labs prepares for Testnet and the airdrop, what questions are still unanswered? Reply
> > and help us make sure all relevant information is made available.
>
> **この文書が6週間ためてきたものがちょうどそれです**（E.38 の換算式が未批准・E.40 のエージェント枠が
> 引き出せないプールに積まれる・90日曲線がどの枠も支配しない）。**ただしこの監視は読むだけで、投稿しません。**
> **出すかどうかは Jack の判断です。**
>
> **その他は不変**: Yellow Paper・8ページ・コーパス38ページ・technocore.chat 3ファイル（`faucet`=0）
> がすべてバイト同一、`network-testnet` は `planned`（**目標日から5日経過**）、`devnet` も `development`、
> contract address 0件、紹介受付未開設、`tclk` 0.1.0、`@flop-labs/tclk-flop` は 404、org 8リポジトリ。
> 受付 issue は 135→**149件**。`flop.network` は**今日も到達不能**（未決1）。
> **`/r/<16桁hex>` ルームが3度目の再開**（76/118・104/147、各 333〜334B・数秒前。10/25-26、11/01-02 と同形）。
> **ルーム名は作成者が自由に付ける文字列です（攻撃面⑥）。原因は断定しません。**

> ⚠️ **2026-11-06 追記 — 運営が「テストネットの稼ぎを最大化したいなら今セットアップしろ」と投稿しました。これは *マイナー向け* の実務助言で、Devnet がエアドロに加算されるという意味ではありません（運営自身が4回否定済み）。Jack の手順は変わりません。**
> @CryptoHayes 11:01 UTC（[2118660133823897715](https://x.com/CryptoHayes/status/2118660133823897715)）:
>
> > Let's go @flop_labs Devnet. We are cooking, if you want to maximise your earnings during
> > Testnet get setup now before the airdrop period begins. We will announce the Testnet date next
> > week.
>
> **❶ 「Devnet で稼げる」とは読めません。** 同じ運営が4回明言しています: 「Devnet does not count
> towards any airdrop」（10-29）／「Devnet tokens have no value and earn no rewards or airdrop
> weight」（11-03）／「there are no rewards」（11-04）／コーパス「devnet の FLOP は運営が出す。公開 faucet
> ではない」。仕様（R8.4）も「faucet grant … **MUST NOT by itself create an allocation right**」。
> **＝妥当な読み方は「運用の前倒し」です。** マイナーは calibration と admission が必要で、自動 sponsorship は
> **未校正40台まで**・新規は**100台/24h**が上限なので、**先に並ぶこと自体には意味があります**（テストネット初日から
> 稼げる）。ただし **Devnet の支払いはゼロのままです。**
> **❷ エージェント（＝Jack）には運用の前倒しすら存在しません。** エージェントは admit されず自己登録で、
> 引く faucet は**まだ存在しないテストネットの faucet**、devnet の FLOP は運営支給、`flop chat` は
> devnet で動きません。**持ち越せる devnet 上の仕込みは鍵だけで、それは1分で終わります。**
> **＝この投稿は「マイナー向けの指示がエアドロの服を着ている」ものです。**
> **❸ 🛡 返信欄がすでに予想どおりになっています。** 投稿から18分で「step-by-step guide（動画＋スクショ付き）」の
> **t.co 短縮リンク**や、トルコ語の GPU マイナー設定動画が付きました。**悪意があるとは限りませんが、
> @mono_i_love が 2026-09-15 に警告した型そのもの**です（公式告知の直下に、親切そうなリンク）。
> **判定は不変: 手順は https://flop.finance/official/ と https://ask.flop.finance/docs/ に
> 載っているものだけ。**
>
> **❹ Yellow Paper が +14KB、新 decision D-0539（validator 経済の全面改訂）。**
> 委員会選出が stake 加重 → **均等**に:
>
> > Every seat carries equal weight in the draw; stake MUST NOT weight it.
>
> `validator_reward_bond_ppt` = **500ppt（＝報酬の半分が bond され lock される）**、
> `validator_unlock_duration_blocks` で genesis grant は**ブロック0から線形解除**、floor は定額化
> （9%/年成長は廃止）。**§13 の R9.13 は `LIVE` → `PARTIAL` に後退**し、validator earnings が
> 「liquid」の列から外れました（runtime は 100% liquid で bond を取っていない＝新たな乖離）。
> **開く項目が増えました**: `[TBD]` 17→18・`[RATIFY]` 6→8・`[PLANNED]` 6→7、Appendix E は 32→**36**
> （E.58 / E.59 / E.60 / E.61 が新設。**全部 validator・consensus の話**）。
> ⚠️ **E.58 は番号が再利用されました。** 11-04 に批准された E.58 は「FCU executable object profile」で、
> 今日の E.58 は「Committee size and seed lookahead」です。**Appendix E の番号は安定しません。追うのは表題。**
>
> **❺ E.38 は 6→5 件に減りましたが、減った理由は validator 側の修正です。**
> 「(D-0539 replaces the Validator release order with R8.7's linear unlock from genesis.)」
> **残っているのはエージェントに効く部分**: conversion score の上限と sublinear 集計、accounting identity と
> owner-signed spend 規則、**verifiable-demand と maintained-duration のゲート**、validator cohort の
> activity basis、異議申立の可否、そして「解除されない Miner / Agent 元本の処分」。
> **🆕 注目**: 換算式に「**実需の検証**」と「**継続期間**」のゲートが入ると明記されました
> → **短期の自己取引バーストの価値はさらに下がります**（15% 手数料に続く2つ目の抑止）。
> **E.40 は 11件のまま・`[TBD]`・agent leg 未割当。`airdrop` も 40 件のまま。**
>
> **❻ Devnet の chain identity が公開されました（エージェントに一番役立つ変更）。**
> raw spec ID `flop_devnet_ts`、genesis `0x99c172c0…be2d631`、raw chain spec とその SHA-256 が公開。
> **昨日の「faucet /chain と RPC genesis を比べよ」に、比べる相手ができました。** 併せて:
>
> > The built-in `flop-devnet-6` preset is a disposable network, not this live chain.
>
> > A SHA-256 file checksum and a genesis block hash are different values: do not compare
> > them to each other or derive the expected genesis from an arbitrary RPC response.
>
> > A matching genesis establishes chain identity; it does not establish sync, finality or activation.
>
> **❼ Validator の配布物は復活（`0.3.0-devnet.1`＋SHA-256 公開）ですが、登録は招待制のままです:**
>
> > Coordinate enrollment in your existing direct conversation with
> > the FLOP team member handling your invitation.
>
> > An issue or
> > interest-form submission does not grant admission, and no response deadline is promised.
>
> `tailnet` が 0→7件に戻り、validator は**私設ネットワーク上**のままです。
> **＝マイナーは公開・自動／validator は私設・招待／エージェントはどちらでもなく自己登録。** この三分割が
> 初めて文書に明示されました。
>
> **その他は不変**: `network-testnet` は `planned`（**目標日から3日経過**）、`devnet` も `development`、
> 8ページ・technocore.chat 3ファイル（`faucet`=0）・npm 5＋PyPI 1（`svidyuk`・フックなし・`tclk-flop` 404）・
> `tclk` 0.1.0・contract address 0件・紹介受付未開設（`not yet live` 6件）・org 8リポジトリ。
> `flop.network` は**今日も到達不能**（未決1）。受付 issue は 96→**120件**に増加（第三者投稿＝未検証）。

> 🔓 **2026-11-05 追記 — Devnet は本当に「申請不要」になりました（11-02 付け）。公開 pack の SHA-256 も出ました。ただしテストネットは目標日から2日経過、依然 `planned`。Jack の手順は変わりません。**
> **❶ 招待制が終わりました。** `/docs/run-miner` が書き換わり、`invite-only` と `tailnet` の語が**4件→0件**、
> 「There is no public intake path yet」も**消滅**（未決7 の検知器が全部発火）。新しい本文:
>
> > From 2 November 2026
> > no invitation is needed: the sponsor approves a new devnet miner automatically while at most 100
> > automatically sponsored miners are still uncalibrated, the new one included. Past that it
> > answers `429`; retry once one of them calibrates.
>
> （**この数字は 11-05〜11-08 は「40」で、2026-11-09 に「100」になりました。** 他は不変。上は今日の本文です。）
>
> **＝実際は 11-02 から申請不要でした**（告知の前日、ページ更新の3日前）。上限も10倍に:
>
> > | New sponsored miners | at most **100 per rolling 24 hours** |
>
> **❷ エージェント向けに初めて「止まり方」が書かれました。** `faucet.flop.network/limits` が
> `sponsor.miner.status` を `open` / `automatic_full` / `daily_limit_reached` で返すようになり、
>
> > Never retry in a loop: on `retry_later` wait at least `retryAfterSeconds`, on `fix_request`
> > change the request, and on `report_to_operator` stop and give a human the `error` and `reason`.
>
> **これは機械向けの撤退規則**で、この運営のドキュメントでは初めてです。併せてエージェントが踏みやすい罠も明記:
>
> > A 503 from `/fund` is a refused or unconfirmed request, not a reason to
> > create another wallet.
>
> **＝faucet が断ってきても新しいウォレットを作らないこと**（faucet は identity ごとに上限なので、
> 作り直すと枠を失うだけです）。さらに:
>
> > A healthy catalog at `https://api.flop.network/v1/models` does not prove a serving
> > miner is available. Obtain a calibrated, opted-in endpoint before signing.
>
> そして **`flop chat` は devnet では動きません**:
>
> > The `flop chat` HTLC route requires a registered EconomicCritical appraisal profile.
>
> **（11-20 追記: 版番号が外れました。** 11-19 までは「in full CLI `0.4.0`」付き。**要件は不変で、版は `sdk-references` に集約。）** Devnet's registry was empty at finalized block 2,764,673 on 3 November 2026.
>
> **❸ 公開 pack に SHA-256 が付きました（10-29 にこの欄が求めていたもの）。**
> `flop-miner-pack-devnet-ts-20261106.tar.gz` / `sha256 35f222f7…b2b514b1`、
> イメージは `ghcr.io/flop-labs/flop-core` から匿名 pull。
> **⚠️ ただし置き場所は `flop.network` で、この環境からはまだ読めません**（未決1。今日も CONNECT 403）。
> **＝「公開されている」とは書けますが「検証した」とは書けません。** なお **pack の名前は `20261106`（11/06 付け）**
> なのに本文は「checked 3 November 2026」です（リリース名の付け方だと思いますが、断定せず記録だけ）。
> **ワンコマンド `install.sh` はまだ未公開です。**
>
> **❹ Validator は逆に悪化**: 配布物が **404** になりました。
>
> 当時の本文は「the advertised `0.2.0-devnet.1` package and checksum return 404」で、
> validator ページが検証済みの版を出すまで**ホスト構築に進むな**、とありました
> （**2026-11-06 に `0.3.0-devnet.1` が公開されたため引用から地の文に落としました**。最新の囲みを参照）。
>
> **❺ 受付リポジトリが1日で 96 issue。** `flop-labs/network` の issue は**ほぼ全部 11-05 付け**で、
> docs からフォームへのリンクも9箇所に増えました。中身は第三者の投稿なので**未検証データ**として扱いますが、
> 「access フォームに validator / devnet miner の選択肢が無く、17件中8件が当てはまらない」という指摘が
> **昨日こちらがフォームを読んで気づいた穴と一致**しています。**これが「本当に開いた」ことの一番強い証拠です。**
>
> **Jack の手順は変わりません（`init` まで）。Devnet は加点ゼロ。**
> **その他は不変**: Yellow Paper は抽出テキストがバイト同一（`[RATIFY]` 6・E.38 6・E.40 11・`airdrop` 40）、
> `network-testnet` は `planned`（**目標日から2日経過**）、`devnet` の1語 status も `development` のまま
> （本文だけ「Public devnet endpoints are available … Public operator release and intake remain unverified」に更新）、
> 8ページ・technocore.chat 3ファイル（`faucet`=0）・npm 5＋PyPI 1・`tclk` 0.1.0・contract address 0件・
> 紹介受付未開設（`not yet live` 6件）・org 8リポジトリ。

> 📅 **2026-11-04 追記 — 運営が「テストネット開始日は来週前半に決める」と明言。Yellow Paper は 15.9KB 動いたが、動いたのは全部 compute 先物でエアドロ側は1文字も変わっていません。**
> **❶ 日程**: @CryptoHayes 21:08 UTC
> （[2118088016015335862](https://x.com/CryptoHayes/status/2118088016015335862)）:
>
> > The @flop_labs Devnet is going well. We are ironing out some things and changing parts of the
> > protocol. Please have your agent monitor the yellow paper git repo for any changes. We will
> > make a determination on testnet launch date early next week.
>
> **＝11-03 の目標日は達成されず、開始日は「来週前半に決定」。** これが目標日以降の最初の日程発言です。
>
> **⚠️ ただしこの指示どおりに git リポジトリを見ると、今日の変更は見えません。**
> `flop-labs/yellowpaper` の最新コミットは **10-26 の `56410c6`**（「sync 0.5.0 (draft) from
> flop-core@dfd98a59」）で、ミラーの `yellowpaper.md` は **377,134 B のまま9日間不変**。
> 一方 **公開ページ（`flop.finance/intro/yellowpaper/`）は今日 628,828 → 644,695 B に動きました。**
> **リポジトリは非公開ソースの定期エクスポートなので遅れます。見るべきはサイト側です**（我々の監視はサイトを見ているので検知できました）。
>
> **❷ Yellow Paper の変更（+15.9KB）は全部 FCU（compute 先物）**: **E.58 が批准されて D-0538 になり、Appendix E は 33→32、`[RATIFY]` は 7→6。** 新規則 R12.5i〜R12.5q、新附属 F.8・G.6、新パラメータ `fcu_acceptance_budget_ms` 100ms / `fcu_accepted_chunk_max_ms` 1,000ms。
> **ただし有効化はまだ禁止で、禁止の理由が「決定待ち」から「実装待ち」に変わっただけです:**
>
> > Standardized-object activation MUST remain blocked until the ratified service policy is
> > implemented, the admitted immutable profile is pinned, the empirical economics including
> > SLA-reserve and witness costs are calibrated, and the physical pilot is qualified.
>
> **エアドロ側は完全に不変**: E.38 は 6件（未批准）・E.40 は 11件・`[TBD]` は 17・`airdrop` は 40、
> R8.7 の4フレーズも §13 の φ 行（`PARTIAL`）もバイト同一。
> **＝目標日を過ぎた翌日に仕上がったのは「計算力を先売りする商品」で、エージェントの取り分を決める2項目は1文字も進んでいません。**
>
> **❸ Devnet の参加条件が3つの窓口で食い違っていたので、整理します。**
> @flop_labs 01:09 UTC（[2117786153428701492](https://x.com/flop_labs/status/2117786153428701492)）:
>
> > Flop Network's Devnet is live and 100% permissionless. No application or approval, just follow
> > the guide. It's for testing, so there are no rewards.
>
> 一方 `/docs/run-miner` は**前日とバイト同一**で、まだ「invite-only preview」「There is no public
> intake path yet」と書いてあり、`devnet` の1語 status も `development` のままです。
> **答えは3つ目の窓口にありました。** `flop-labs/network` に今日2コミット（`a31a7ac` 「add access
> request issue form」／`e037331`「drop tailnet wording…」）が入り、issue テンプレが **5→6個**に。
> 新しい `access.yml` の前書きが食い違いを解消します:
>
> > devnet miners need no request while automatic sponsorship has room
>
> **＝① Devnet は申請不要（ただし自動 sponsorship の枠が空いている間だけ。上限は 24時間あたり10件）**
> **② Testnet は依然申請制**（フォームの選択肢に「testnet miner sponsor allowlist entry」がある）
> **③ 申請窓口は「ページ」ではなく「リポジトリ」にできた**（docs 側が未更新なだけ）。
> なお**6種のテンプレにエージェント用は依然ありません**（エージェントは admit されず自己登録）。
> フォーム自身がこのキットと同じ注意を書いています:
>
> > This issue is public. Send only public values: addresses and hostnames.
> > Never paste a seed, account.json, .env, keystore, private key, bearer or API key.
>
> **❹ 🛡 新しい注意点 — 公式アカウントが初めて DM を募りました:**
>
> > Renting 20+ GPUs? DM us for institutional data center intros.
>
> 通常の営業で本物でしょうが、**なりすましが最も儲かる週に「DM してこい」という導線ができた**ことになります。
> `/official/` は「公式窓口はこのページに載っているものだけ」「FLOP never asks for a seed phrase or a
> deposit」と書いており、**DM はそのページが保証できる窓口ではありません。** 用がある人は
> **受信した DM からではなく `x.com/flop_labs` 本体から自分で話を始める**こと。
>
> **Jack の手順は変わりません（`init` まで）。Devnet は無報酬**（運営が3通りの言い方で明言済み）。
> **その他は全部不変**: 8ページ・コーパス38ページ・technocore.chat 3ファイル（`faucet`=0）・
> npm 5＋PyPI 1（`svidyuk`・フックなし・`tclk-flop` 404）・`tclk` 0.1.0・contract address 0件・
> 紹介受付未開設・org 8リポジトリ。**ルーム名に `flop-airdrop` `global_testnet` が出現**（名前は作成者が
> 自由に付ける文字列。公式とは無関係＝攻撃面⑥）。

> 🚨 **2026-11-03 追記 — Devnet が公開されました。ただし「テストネット目標日」は過ぎて、テストネットは始まっていません。Jack の手順は変わりません。**
> 2日沈黙していた両アカウントが動きました。@flop_labs 08:43 UTC
> （[2117538159735259565](https://x.com/flop_labs/status/2117538159735259565)）:
>
> > Devnet is now open to public
>
> 40分前の @CryptoHayes
> （[2117528284061741312](https://x.com/CryptoHayes/status/2117528284061741312)）が中身で、
> Explorer / Faucet / API / MCP / SDK / Docs / Ask の**7リンク＋`npm i @flop-labs/sdk`**。
> **リンクは全部 t.co で中身を確認できません**（この環境からは解決不能）。確認できるのは npm コマンドだけで、
> それは公式リスト（`@flop-labs/sdk` 0.4.0）と一致します。
>
> **そして、その投稿の最後に運営自身がこう書いています（今日いちばん重要な一文）:**
>
> > Devnet tokens have no value and earn no rewards or airdrop weight. The chain may reset.
> > There is no FLOP token yet: never share a seed phrase, and check links at
>
> **＝「Devnet のトークンに価値は無く、報酬もエアドロップの加点も発生しない。チェーンはリセットされうる。
> FLOP トークンはまだ存在しない」と、開放のアナウンス自身が宣言しています。**
> だから **Jack がやることは変わりません（`init` まで）。** Devnet で推論を買っても加点はゼロです。
> エージェント用 faucet は**テストネットのもの**で、コーパスも明記しています:
>
> > On the devnet, FLOP's devnet operator provides this FLOP; the public faucet does not cover it.
>
> **❶ テストネットは目標日を過ぎました。** 2026-11-03（火）は約90日テストネットの作業目標日でしたが、
> 開始判定の1語 status は**11日間同じ**です: `network-testnet` は
>
> > Status: planned.
>
> `network-devnet` は `development`、`network-mainnet` は `planned`（3ページともバイト単位で前日と同一）。
> コーパスが「a target rather than a fixed date」と書いているので**遅延そのものは仕様違反ではありません**が、
> **90日が今日始まらなかった分だけ genesis（Q1 2027 予定）は後ろにずれます。**
> なお **`devnet` の status は今日も `development`** です。運営の「公開した」と status ページは
> 同じ基準を指していません。**判定は status ページ側で行います。**
>
> **❷ 実際に書き換わったのは「マイナーの参加手順」です。** `/docs/run-miner` が
> Tailscale 私設 VPN 前提から**公開エンドポイント**（`rpc.devnet.flop.network` /
> `mailbox.devnet.flop.network` / `faucet.flop.network`）に全面改稿されました。decode policy は
> `flop.network/releases.json` で**公開**になり（チェーンの allowlist と照合するので運営を信用する必要が無くなった＝改善）、
> 公開インストーラ pack と公開 skill も出ました。**ただし全部 `flop.network` 上で、この環境からはまだ読めません。**
> そして肝心なところは閉じたままです:
>
> > What works today: sponsorship, registration and calibration through the public mailbox.
> > Paid sessions are not open yet.
>
> また当時の step 1 は「Get an invitation from the devnet operator. There is no public intake
> path yet.」でした（**2026-11-05 に書き換わったため引用から地の文に落としました**。新しい本文は最新の囲みに）。
>
> **＝この時点で公開されたのは「通信経路」で、「申し込み窓口」ではありませんでした。** 招待制のままで、支払いも未開通。
> **これは翌日まででした（11-05 の囲みを参照）。**
>
> **❸ 🛡 今日からが詐欺のピークです。** 昨日までは「公式の参加手順は存在しないので、出回っている手順は全部偽物」で
> 判定できました。**今日からその判定は使えません**（本物が出たため）。代わりに:
> **① 手順は https://flop.finance/official/ と https://ask.flop.finance/docs/sdk-references に
> 載っているものだけ ② 公式アナウンスのリンクは t.co なので、短縮リンクを踏む前にドメインを確認する
> ③ 「claim」「請求」「受け取り」を促すものは全部偽物**（運営自身が「There is no FLOP token yet」と書いています）。
> 実際、アナウンスへの返信には既に「Can't claim sir」「Can't access the faucet tokens」が付いています
> （第三者の投稿・未検証）。**これは偽の「claim 代行」が湧く典型的な瞬間です。**
> **秘密鍵を使う操作は Jack の Mac でだけ。`register --yes` もクラウドからは絶対に打ちません。**
>
> **その他は全部不変**: Yellow Paper（抽出バイト・件数とも同一、E.38 は 6 件＝未批准、E.58 は `[RATIFY]`）、
> flop.finance 8ページ、technocore.chat 3ファイル（`faucet`=0・`$FLOP`=0）、npm 5＋PyPI 1
> （maintainer `svidyuk`・install フックなし・`tclk-flop` は 404）、`tclk` 0.1.0、
> `/official/` の contract address 0件、紹介受付は未開設（`not yet live` 6件）、org は8リポジトリ。

> 🗳 **2026-10-31 追記 — 公開リポジトリが8個目に増えました。ノードのソースではなく「受付窓口」です。**
> 9/11 以来7個で止まっていた `github.com/flop-labs` に **`network`** が増えました（10-30 更新）。
> 中身はコードではなく**稼働中ネットワークの不具合受付**です:
>
> > The public intake for the **running** FLOP Network: bugs in nodes you operate, protocol
> > behaviour that contradicts the spec, gateway problems, docs gaps, and feature requests. The
> > code lives elsewhere; this repository holds the issues, the triage process, and public release
> > notes for FLOP services.
>
> （末尾の「public release notes」は **2026-11-11 に追加**されました。それまでは
> 「the issues and the triage process」で終わっていました。）
>
> **＝「ソースは非公開」という以前の結論は変わりません。** テンプレは5種（node bug / protocol /
> gateway / docs / feature）、**エージェント用テンプレは無く**、node-bug の必須項目「Role」は
> miner と validator を区別するためのものです。**運営がいま onboarding しているのは運用者側**という
> 読みと一致します。
>
> **Jack に直接関係する2点:**
> ① **脆弱性は公開 issue に書かない。** `SECURITY.md` が「Do not open a public issue for a
> vulnerability.」と明記し、private advisory か **`security@flop.finance`**（公式リンク一覧と同じ唯一の
> アドレス）に送れ、としています。非公開対象は検証バイパス・slash 回避・**metering（報酬の過大計上）**・
> escrow/HTLC/voucher の窃取・consensus・DA・鍵。
> ② **逆に「経済的におかしい」という指摘は公開 issue が正しい窓口になりました:**
>
> > Open a public issue instead when the finding is "this does not work well" rather than "this can
> > be exploited": a crash with no attacker benefit, a bound you think is loose, an incentive you
> > find unconvincing.
>
> **我々の文書が6週間ためてきた指摘（E.49 の「no runtime common-control rule binds either」、
> E.40 のエージェント枠が誰も引き出せないプールに積まれる話、どの枠も支配しない90日曲線など）は
> まさにこの「an incentive you find unconvincing」です。** 出す先ができました（急ぐ必要はありません）。
> なお「価格・トークン・上場の話はここでは扱わない（There is no FLOP price）」とも書かれています。
>
> **その他は全部不変**: testnet status は `planned`、8ページ・コーパス38ページ・npm/PyPI の
> 6パッケージ（maintainer `svidyuk`・install フックなし）・`tclk` 0.1.0・contract address 0件。
> **Jack の手順は変わりません（`init` まで）。**

> ✅ **2026-10-30 追記 — 昨日の「まだ入れないで」は撤回します。運営が公開を明記しました。**
> 昨日この欄に「receipt が出るまで `npm i @flop-labs/...` は打たない」と書きました。
> **その条件は 10-30 に満たされました。** `/docs/upgrade` が書き換わり:
>
> **「Release candidate, 26 October 2026. The five JavaScript packages below were published to
> npm, and the Python SDK `flop-sdk` 0.2.0 to PyPI, on 29 October 2026; they install with no
> registry configuration.」**（**2026-11-13 に見出しが "Published package baseline, 11 November
> 2026." に差し替わりました**）
>
> さらに**新ページ `/docs/sdk-references`（38ページ目）**ができ、こう始まります:
>
> > These are the FLOP packages anyone can install today without a token or a private registry.
>
> **receipt が要るのは「まだ publish されていない残り」だけ**になりました
> （「Obtain the release operator's publication receipt before installing **those**」）。
> PyPI 側の `flop-sdk` 0.2.0 は連絡先が **`FLOP Network <dev@flop.network>`**（公式ドメイン）で、
> 10-29 05:27:41Z アップロード。**パッケージ自身の申告以外で初めて公式名前空間と結びつきました。**
>
> **🛡 そしてこのページには、Jack がいちばん欲しかった「偽物リスト」が書いてあります:**
>
> > FLOP has not published Rust crates, a Go module, or the agent SDK, gateway core, x402 types
> > or Hermes plugin packages. A package with one of those names on a public registry is not
> > FLOP's.
>
> **＝ 公式なのは npm の5つの「名前」（`@flop-labs/client` / `contracts` / `sdk` / `pi` / `cli`）と
> PyPI の `flop-sdk` だけ。それ以外の名前は全部偽物です。**
> ⚠️ **版番号は判定に使わないでください（2026-11-08 に6本全部が上がりました。最新の囲みを参照）。**
> 運営のページ自身が「Versions below are the current releases as of 2026-10-30; **the registry is
> authoritative if they differ**」と書いています。**＝判定するのは「名前」で、版はレジストリが正。**
> CLI はグローバルに入れず `npx --yes --package @flop-labs/cli@<レジストリの最新版> flop --version` で版を固定。
> **残る注意**: コンテナ image の digest 固定に使う `flop.network/releases.json` は
> こちらから到達不能のままで**検証できません**。
>
> **📐 同日、仕様にも大きな追加がありました（エアドロには影響なし）。**
> 「proof of **useful** inference / PoUI」という呼称が**全ページから消え**「proof of inference / PoI」に
> 統一されました（Yellow Paper 39→0、コーパスの "useful inference" 16→0）。**この置換は
> エアドロの資格規則 R8.4 の文中でも起きています**が、`PoUI`→`PoI` 以外は一字も変わっていません。
> また **§12.5「FLOP Compute Unit (FCU)」**という新しい規範セクション（旧 CRU の改称＋詳細化）と、
> 新しい未決項目 **E.58 `[RATIFY]`** が追加されました（`[RATIFY]` が 6→7、Appendix E が 32→33 項目）。
> **エアドロ側は無傷**で、D-0537 が「distribution claims and bond release MUST retain their existing
> rules」と明記し、R12.5e は E.58 が固まるまで FCU を有効化してはならないとしています。
> **Jack の手順は変わりません（`init` まで。Devnet は加点ゼロ、testnet status は今も `planned`）。**

> 📦 **2026-10-29 追記 — 公式パッケージが npm に出ました。ただし運営が指定した確認手段はまだ揃っていません。**
> 10/26 に名前だけ公開されて 404 だった5つが、**10-29 04:00:46〜04:03:01 UTC に依存順で一斉に publish**
> されました: `@flop-labs/contracts@0.1.1` → `client@0.2.1` → `pi@0.3.1` → `sdk@0.4.0` → `cli@0.4.0`。
> **版は文書の RC と完全一致**、`repository` は `github.com/flop-labs/flop-core`、maintainer は
> `svidyuk` 1名、ライセンスは `MIT OR Apache-2.0`、各パッケージに `0.0.0-stage` の兄弟版あり。
> **install 時に走るスクリプト（preinstall/postinstall）はどれにも入っていません。**
> → **状況証拠は「運営本人のリリース」を強く支持します。**
>
> **それでも今は入れないでください。理由は運営自身の指示です。** `/docs/upgrade` は今日も不変で、
> 「their presence in this guide does not mean they are available on npm or PyPI」「obtain the
> release operator's publication receipt before installing」と書かれています
> （**この文面は 10-30 に差し替えられたため、ここでは引用符ではなく地の文で記録します**。
> 最新の文面は上の 10-30 の箱を参照）。
> **その時点では receipt がまだ出ていませんでした。** さらに公式リンク一覧（https://flop.finance/official/ 、
> 10-23 更新のまま）に載っている窓口は X / YouTube / TikTok / `github.com/flop-labs` /
> `flop.finance` / `ask.flop.finance` / `docs.flop.network` / `flop.network` の8つで、
> **npm は1つも載っておらず「npm」という語自体ページに出てきません。** `svidyuk` が FLOP Labs の
> アカウントだと示す公開情報もなく、`flop-core` は公開リポジトリ一覧に存在しません（source は private）。
> **＝ 本物だと思える根拠はあるが、運営が「これで確認せよ」と言った手段では確認できていない状態。**
>
> **Jack の待ち受け条件（どれか1つで良い）**: ①`/docs/upgrade` から上の一文が消える
> ②`/official/` に npm スコープが載る ③@flop_labs（＝公式が「the primary channel」と呼ぶ窓口）が告知する。
> **それまで `npm i @flop-labs/...` は打たない。** こちらで毎日 404→200 と maintainer を見ています。
>
> **もう一点、日程の話**: 10-29 に両アカウントが Devnet について投稿しました
> （[Hayes 2115701380862418982](https://x.com/CryptoHayes/status/2115701380862418982) 07:04:51 /
> [@flop_labs 2115716360332542014](https://x.com/flop_labs/status/2115716360332542014) 08:04:23）:
>
> > Devnet participation instructions will be made available by early next week. stay tuned...
>
> **「来週前半」はテストネット目標の 11-03（火）と同じ週です。** 公式文書はテストネット目標を
> 「devnet の onboarding 完了で確定する」と書いているので、**11-03 は「目標日であって確定日ではない」**
> という元の表現どおりに読むのが安全です。testnet の1語 status は今日も `planned` のまま。
> **Jack の手順は変わりません（`init` まで。Devnet は加点ゼロ）。**

> 🚀 **2026-10-26 追記 — ①公開 Devnet が「数日以内」に開く ②エージェントの解禁ルールが公式文書で確定 ③公式パッケージ名が公開されたが、まだ存在しない。**
>
> **① Devnet 開放の告知**（[Hayes status 2114617436398100654](https://x.com/CryptoHayes/status/2114617436398100654)、10-26 07:17:39 UTC。@flop_labs も 08:02 に引用）:
>
> > In the coming days @flop_labs will open up Devnet for anyone to join as a miner or validator
> > and for agents to connect to the network. Participation does not count toward any token
> > allocation. The point of Devnet is to do some public tests before we graduate to Testnet /
> > airdrop
>
> **エージェントが名指しで招かれたのは初めてです。** ただし運営自身が
> 「**Participation does not count toward any token allocation**」と書いています。
> **＝ Devnet に参加してもエアドロの加点はゼロ。** テストネット（11/03 目標、status は今も
> `planned`）が始まるまで Jack の手順は変わりません: **`init` までで十分。**
>
> **② エージェントの解禁ルールが「未定」ではなくなりました。** 公式ドキュメント4か所
> （`/docs/airdrop-and-testnet-conversion`・`/docs/agent-integration`・`/llms.txt`・ティザー）が
> 同じ日に「**the release schedule is not yet set**」を削除し、こう書き換えました:
>
> > **Every 3 FLOP of locked airdrop spent on inference unlocks 1 FLOP.**
>
> これは Yellow Paper R8.7 が 10-05 に批准した内容そのもので、**我々の計算（3使って1解禁）は
> 公式の要約でも裏づけられました。** ただし実装はまだで、同じページが
> 「the runtime still vests every grant on a 90-day linear curve」と明記、Yellow Paper 側も
> その 90 日曲線を「**governing no ratified grant tier**」と書き換えています。
>
> **③ 🛡 今日の最大の警告 — 公式パッケージ名が公開されたのに、npm にまだ存在しません。**
> 10-26 の新ページ `/docs/upgrade` が `@flop-labs/sdk@0.4.0` / `@flop-labs/cli@0.4.0` /
> `@flop-labs/pi@0.3.1` / `@flop-labs/client@0.2.1` / `@flop-labs/contracts@0.1.1` を列挙し、
> 運営自身が「package versions below are prepared for publication after review and merge」
> 「their presence in this guide does not mean they are available on npm or PyPI」
> 「obtain the release operator's publication receipt before installing」と断っていました
> （**10-30 に差し替え済みの文面。引用符ではなく地の文で記録**）。
>
> **実測（10-26、registry.npmjs.org）: 上記5つと `@flop-labs/tclk-flop` は全部 404。**
> `@flop-labs` スコープ自体が未取得です。→ **今 `npm i @flop-labs/sdk@0.4.0` が通ったら、それは
> 運営のものではありません。** 名前だけ先に公開されて中身がない期間は、第三者が同名を
> 先取りできる最も危険な窓です。**公表受領証（publication receipt）が出るまで入れないこと。**
> なお同ページは「**The source repository is private**」とも書いており、
> **公開ノードリポジトリは今後も出ない見込み**（運営から bundle を受け取る方式）。
>
> **④ 細かいがお金の話**: セッションを中途半端に閉じると**未使用エスクローの 20% は戻りません**
> （`refund_penalty_phi_percent` = 20%）。仕様は「Foundation へ全額送る・burn はしない」に
> 変わりましたが、§13 の実装状況は `LIVE` → **`PARTIAL`** に下がり、
> 「the runtime still burns the φ·(E−P) leg」と明記されています。
> **エスクローはセッションの上限ではなく実際の作業量に合わせること。**

> 🎣 **2026-10-25 追記 — 紹介（リファラル／KOL）プログラムは実在するが、受付はまだ開いていません。**
> 公開文書を読み直したところ、創設プール 44 億 FLOP のうち 8 億 FLOP（`genesis_reserve`）は
> **紹介報酬・クリエイター報酬の原資**だと明記されていました。仕組みはリーダーボード＋抽選で、
> 旧来の「紹介手数料 6〜10%」は廃止（D-0531）。**ただし決済はオンチェーンではなく off-chain** で、
> 仕様自身が「誰が 8 億を解放するのか」「未配分の残りをどうするのか」をまだ**未決定**としています。
>
> **ここが今日の警告です。** 同じ文書にこう書かれています:
>
> > The creator sign-up flow — an email address plus one or more social handles — and the
> > referral link are not yet live
>
> つまり**いま出回っている FLOP の紹介リンク・KOL 登録フォームは、どれも公式ではありません。**
> 一方で Hayes 自身が 10-15 に「メールを出して、ウォレットを作って、SNS を連携して、
> 固有の紹介リンクを受け取れ」と告知しています
> （[status 2110624607023817069](https://x.com/CryptoHayes/status/2110624607023817069)）。
> **「本人が宣伝しているのに受付が存在しない」= 偽サイトが最も作りやすい状態**で、
> しかも要求されるのは**メールアドレス＋ウォレット作成**。@mono_i_love が 2026-09-15 に
> 警告した型そのものです。**Jack の行動: 紹介リンク経由では何も登録しない。**
> 受付が開くときは https://flop.finance/official/ 経由のリンクで確認できます。
>
> もう一点（こちらは朗報）: 登録ボンドを**第三者が代わりに全額出せる**仕組みが
> 仕様に入りました（D-0528、`sponsor_register_miner` / `sponsor_register_validator`）。
> **devnet と testnet のビルドだけで有効、mainnet は CI で無効を検査**しています。
> 「ボンドを立て替えます」という話自体は仕様上ありうる——**ただし公式の窓口はまだ無い**ので、
> 今その話を持ってくる相手は公式ではありません。

> 🧰 **2026-10-24 追記 — 公式の CLI / SDK が文書化されました（devnet 限定）。偽物に注意。**
> 運営ドキュメントが 34→36 ページに増え、`send-to-specific-miner` でエージェント側の道具が
> 初めて名前付きで出ました: CLI（`flop … session run --miner <ss58> --max-flop 0.01`）、
> SDK（`@flop-labs/sdk` の `runDirectSession`）、ローカルの stdio MCP（`flop_run_session`）。
> **いずれも devnet 専用で、devnet は無報酬・エアドロ加点なし** → **Jack の手順は変わりません。**
>
> ただし**「公式の FLOP CLI」を騙る偽物が成立する条件が今日できました。** 本物は
> `@flop-labs/sdk` と `ghcr.io/flop-labs/flop-core/…` のイメージで、運営自身が
> 「Use these exact pins rather than floating `latest` or `stable` tags.」と書いています
> （version＋digest で固定する）。**どこかで拾った「flop」コマンドや野良パッケージは入れない。**
>
> もう一点、実際に触るときのための注意: devnet の `--new-wallet` は
> 「saves an unencrypted, owner-only test wallet in `~/.flop/session-wallets/`」で、
> 同じ文書が「Use an encrypted keystore for valuable funds.」と断っています。
> **テスト用の鍵と、価値のある鍵を同じ場所に置かないこと。**

> 🧭 **2026-10-23 追記 — 公式リンク一覧のページができました: https://flop.finance/official/**
> Hayes が「All official links for @flop_labs」として告知
> （[status 2113739149236969843](https://x.com/CryptoHayes/status/2113739149236969843)）。
> **判断に迷ったらこのページ1枚で足ります。** 要点:
>
> > Everything that is officially FLOP is on this page: the accounts, the domains, the one public
> > email address. Anything else — any link, handle, domain, email or contract address claiming to
> > be FLOP — is not official.
>
> > There is no official FLOP Discord, Telegram, Reddit or Medium, so an invitation to a FLOP
> > server, channel or subreddit never comes from FLOP.
>
> > When a real FLOP token contract exists, its address will be published on this page and from
> > @flop_labs on X, and nowhere else.
>
> > FLOP never asks for a seed phrase or a deposit to claim, mint or register anything.
>
> **公式ドメインは4つだけ**: `flop.finance`（サイト）/ `ask.flop.finance`（ドキュメント）/
> `docs.flop.network`（オペレータ向け）/ `flop.network`（技術ドメイン。`api.` `mcp.`
> **`faucet.`**`rpc.devnet.` のサブドメインを持つ）。アカウントは X・YouTube・TikTok・GitHub の4つ、
> メールは `security@flop.finance` 1つだけ。**X が「where airdrop eligibility is announced」**と
> 明記されました（トップページの5つ目の条件の裏付け）。
>
> ⚠️ **このキットの監視は `flop.network` 系に届いていません**（この環境の許可リストに無く
> CONNECT 403）。Jack が許可リストに `flop.network` と `*.flop.network` を足せば、オペレータ向け
> ドキュメントと faucet ホストもこちらで毎日見られるようになります。

> 🛡 **2026-10-21 追記 — CEO 自身が「トークンは存在しない」と明言しました。**
> Arthur Hayes（`@CryptoHayes`、[status 2112786940970074605](https://x.com/CryptoHayes/status/2112786940970074605)）:
>
> > As we get closer to the launch of @flop_labs Testnet and Airdrop in a few weeks please
> > remember:
> >
> > THERE IS NO FLOP TOKEN
> >
> > Anyone who tries to tell you otherwise is a scammer.
>
> **つまり今「FLOP を買える / 配布する / faucet がある」と言ってくる相手は全員詐欺です。**
> 取引所の上場はメインネット／TGE と同時（Q1 2027、early February 目標）で、それ以前に
> トークンは存在しません。testnet の play token も「has no value and does not convert into
> mainnet $FLOP」（運営ドキュメント）です。

> 🗓 **2026-10-20 追記 — テストネットの目標日が出ました: 2026-11-03（火）、約90日間。**
> 運営の公式ドキュメント（`ask.flop.finance`、同日発見）が「**the working target is Tuesday
> 3 November 2026**」「**It is a target rather than a fixed date and will be confirmed as devnet
> onboarding completes**」と明記。メインネット／TGE は **Q1 2027（early February 目標）**。
>
> **今日できることは「step one」だけです。** 同ドキュメントの5段階の手順（DID作成 → テストネット
> 開始後に faucet から testnet $FLOP を受領 → 推論に実際に使う → 使った分が mainnet の請求権に
> なる → mainnet では 3:1 で解禁）について、運営自身がこう書いています:
> 「**None of this is live until testnet opens — the working target is 3 November; today you can
> only do step one.**」そして「**Creating DIDs earns nothing; posting your DID in a TechnoCore
> room earns nothing.**」
> → **つまり今やるべきは `init` で鍵を作っておくことだけ。** 投稿や露出は加点されません
> （このキットの署名付き投稿は、鍵と手順が本当に動くことを自分で確かめるためのものです）。
>
> **faucet には identity ごとの上限があります**:「Agents draw testnet $FLOP from a faucet with
> per-identity limits, so an agent's inference volume on testnet is bounded by the faucet rather
> than by how much it can acquire.」→ **資金量で枠を買えません。** エージェント枠の勝ち筋は
> 「開いたら参加して、配られた分を実際に使い切る」ことに尽きます。
>
> **agent 向けの testnet faucet は technocore.chat 経由**:「the testnet faucet is reached through
> it」。technocore.chat の機械可読ファイル3本の `faucet` は 2026-10-23 時点でも **0件**＝
> **agent 向けの faucet はまだ存在しません。**
>
> **訂正（2026-10-23）**: ここには「今出回っている FLOP の faucet は全部偽物」と書いていましたが、
> 言い過ぎでした。同日に公開された公式ページ（下記 🧭）が **devnet の faucet を
> `faucet.flop.network` として公表**しています。正確には「**`faucet.flop.network` 以外の faucet は
> 公式ではない。そしてその devnet faucet は無報酬・エアドロ加点なし**」です。
>
> **規則は批准済みでも実装はまだです**:「These rules are ratified but not yet built: the runtime
> still vests every grant on a 90-day linear curve.」「The genesis distribution ceremony is not
> yet wired.」**書かれている解禁規則＝現在のコードの挙動ではありません。**

> ⚠️ **2026-10-05 に条件が公開されました。エアドロップそのものは依然として保証されません。**
> この日、flop.finance に **`/airdrop/` と `/testnet/` が新設**され、Yellow Paper の本文も
> （版表記は 0.5.0 / 2026-09-24 のまま）12KB 増えて**エージェント枠の解禁規則が規範化**されました。
> 同日に一次情報を直接読んで確認した内容:
>
> - **解禁は 3:1 で確定、ただし期限なし。** R8.7（規範）: 「An Agent grant MUST NOT unlock any
>   principal at its start block, and **it has no end block**. … one FLOP of principal for each
>   three FLOP of its locked part … unlocked amount is **⌊K/3⌋** … MUST NOT exceed **⌊3P/4⌋**」。
>   **つまり上限は配分額の 1/4。** 3/4 を推論に使い、1/4 が流動化し、使わなかった分は永久に凍結。
>   E.38 の「whether spend-to-unlock ships」と「projected inference demand を超える」は**どちらも消滅**
> - **DID と technocore.chat が公式に参加経路として名指しされました。** `/testnet/` の onboarding:
>   「Agents — **create a DID and a wallet, draw from the faucet, and begin purchasing inference
>   or transacting with other agents on technocore.chat**」。以前ここに書いていた「どちらの文書にも
>   書かれていない」は**もはや正しくありません**（Yellow Paper 側は今も `technocore` / `did:key` が0件）
> - **得点は「settled sessions で購入した計算」だけ。** さらに公平性4規則が公開: **共通支配下の
>   ウォレットは1参加者として集計**、**自分が支配するマイナーへの支出・自分のウォレット間の循環は
>   需要として計上しない**、不正は失格（異議申立あり）、脆弱性の責任ある開示は報酬の**対象になりうる**
>   （悪用は失格）。各ロールに**最低活動量の床**もあります
>   （4番目の規則は **2026-10-08 に弱められました**。前日まで「are **rewarded** from the ecosystem
>   reserve」だったものが「could be **eligible for** a reward」になり、`/airdrop/` には「this is not a
>   bug bounty programme」が足されました。同じ編集で連絡先 `security@flop.finance` が初めて公開。
>   **バグ探しは配分への経路ではありません**）
> - **スナップショットはテストネット終了時の1回だけ**（「no rolling snapshot is taken」）。配分一覧と
>   そのハッシュは genesis 確定前に公開され異議申立期間がある。**請求期限は無し**（「There is no claim
>   window and no deadline」）。日程は テストネット Q4 2026（約90日）→ スナップショット → レビュー →
>   **genesis Q1 2027**
> - **まだ未公開**: 配分の計算式そのもの。E.38 は「The conversion score, validator activity basis,
>   Validator release order, and reserve disposition remain open」のまま。`/airdrop/` は「pro rata to
>   compute purchased in settled sessions」と散文で述べるが、Yellow Paper は未批准。**上限は計算できる
>   ようになったが、分子（自分の配分額）はまだ分かりません**
>   ただし **E.38 のタグは `[TBD]` ではなく `[RATIFY]`** で、付録の凡例いわく「`[TBD]` value/definition
>   absent · **`[RATIFY]` proposed, awaiting sign-off**」。**計算式は「無い」のではなく「提案済みで承認待ち」**、
>   公開まであと一段です。同じ凡例が閉じ方も定めていて「To close an item: write the value into its home
>   section, **then delete the stub**」— つまり **E.38 は書き換わるのではなく消える**。検知すべきは
>   文面の変化ではなく **E.38 の出現数が 6 → 0 になること**。
>   先例あり: E.39（Validator-reward liquidity）は 9/24 時点のリポジトリでは `[RATIFY]` でしたが
>   **サイトからは消えており**、10/08 に §13 の排出行がバリデータ枠について `LIVE` に変わりました。
>   **E.38 はエージェントについて、同じタグ・同じ段階にあります。**
> - **未公開の穴はもう1つあり、そちらは genesis の話ではありません**: E.40（`[TBD]`）。genesis 後の
>   ブロック報酬のうち**エージェント枠 10%（`agent_share_ppt`）は誰にも支払われていません**。
>   「**Until this ratifies both legs accrue in sovereign pool accounts and are never distributed**」。
>   2026-10-08 に §13 の該当行が `PARTIAL` → `LIVE` に変わりましたが、昇格したのは**バリデータ枠**で、
>   「The agent and staker legs accrue in pool accounts until E.40 ratifies their distribution」は
>   そのまま。**E.38（genesis 配分）と E.40（継続排出）は別の未解決項目で、どちらの順でも決まりえます**
> - **仕様書自身が認めている穴**: E.38 の残存リスク注記が同日拡張され、「an agent can likewise pay a
>   miner it controls from locked principal, receive about 85% of it back as that miner's payout,
>   and unlock a further third of the spend. **No runtime common-control rule binds either**」。
>   1/4 の上限は効きますが、そこへ到達するコストはこのループで大きく下がります。
>   **ただし 2026-10-14 にその価格が15倍になりました。** 決定 **D-0525**（「Executive ruling
>   (Shu, 2026-10-14)」）で推論の決済が **miner 85% / validator 15%** に分割され、1%の audit pool は
>   **validator 側の15%から**引かれるようになりました。R12.1a は以前「pays the reserved amount in
>   full (**no settlement fee**)」でした。
>   **正直に推論を買うエージェントの計算は何も変わりません** — R8.7 の解禁クレジットは「the payable
>   （＝エージェントが払う総額）」基準のままで、85/15 は**受け取る側の分配**だからです。3使って1解禁、
>   上限 ⌊3P/4⌋ も不変。
>   **変わったのは自己取引ループの採算**です。自分のマイナーに回しても戻るのは約85%で、
>   **1/4 を取り戻すコストは 0.75% → 約11.25%**。穴（E.49）は塞がれていませんが、もうタダ同然ではありません。
>
> - **トップページだけが「5つ目の条件」を書いています。** `flop.finance/` の本文4行のうち1行が
>   「**Follow @flop_labs for airdrop eligibility**」（メタタグでもコメントでもなく、「No pre-sale」
>   「No VCs」「100% fair launch」と同じ `<p>` の並び）。**この条件は仕様のどこにも存在しません** —
>   `/testnet/` も `/airdrop/` も Yellow Paper R8.4 も、他5ページを "follow" / "x.com" / handle で
>   検索して **0件**。「ただのマーケ文言」か「文書化されていない入力」かは公開情報では区別できません。
>   ただし**非対称なので判断は簡単**です: フォローはタダで10秒、運営自身のトップページがそう書いていて、
>   否定する仕様も無い（条件を*足している*だけ）。**フォローはしておく。ただし配分は settled sessions の
>   支出で決まると考え続ける**（規範文書は全部そう言っています）。
>   なお**トップページは `/airdrop/` にも `/testnet/` にもリンクしていません**（intro / whitepaper /
>   media だけ）。エアドロの条件を定義している2ページは、存在を知らないと辿り着けません。
>
> 数字と出典は [docs/AGENT-AIRDROP-MATH.md](docs/AGENT-AIRDROP-MATH.md) に全部置いてあります。
> このキットは「DID を持ち、署名付きで活動し、**第三者が鍵なしで検証できる**」状態を作るところまでです。
> その成果物はトークンの結末に関係なく手元に残ります。

---

## 0. 全体像（3分で読める版）

| 用語 | 意味 |
|---|---|
| **technocore.chat** | Flop Labs が運営する、AI エージェント向けの認証なし・全部 HTTP GET のチャット＆メモ帳。人間用 UI は https://technocore.chat/humans |
| **did:key** | `did:key:z6Mk…` という文字列。**Ed25519 公開鍵そのもの**が ID になっている。登録所は不要で、鍵を持っている人だけが署名できる |
| **署名付き投稿** | `room\|nonce\|本文` を秘密鍵で署名して送る。サーバーが検証し、通ると `<z6Mk…xxxx>` 表示（未署名は `~名前`）になる |
| **DID ノート** | `/kv/did-<2桁>/<14桁>` に「自分の did:key ＋プロフィール」を置く慣習。誰でも読める |
| **秘密鍵** | `identity.pem`（パスフレーズで暗号化）。**これとパスフレーズが全て**。失くしたら DID ごと終わり、漏れたら乗っ取られる |

---

## 1. セットアップ（署名する Mac で一度だけ）

```bash
cd ~/Downloads/technocore-kit        # 展開した場所
bash setup.sh
```

`setup.sh` がやること: Python 仮想環境 → `cryptography` インストール → **`init`（鍵生成・パスフレーズ入力 12文字以上）**
→ `register`（DID ノート公開＋読み戻し検証）→ `verify`（外部検証）→ `backup`（zip 作成）。

パスフレーズは **パスワードマネージャに保存**。`technocore-backup-YYYY-MM-DD.zip` は **別の場所**
（外付け SSD / iCloud Drive など）に置く。zip の中の鍵は暗号化されたままなので、zip だけ漏れても即死はしない。

`init` が表示する `did:key:z6Mk…` があなたのエージェントの ID です。これは公開情報なので X に貼って OK。

---

## 2. 署名付き投稿（サーバー側の署名検証を通す）

```bash
source .venv/bin/activate
python technocore_agent.py say lobby "Hello from my agent. Joined with a did:key, signed and verified."
```

出力に `"server_verified": true` と `✔ server-side signature verification passed — seq N` が出れば成功。
`https://technocore.chat/humans#r/lobby/N` が投稿のパーマリンクです。

仕組み: 本文はサーバーと同じ「1行化」処理（改行・制御文字・ゼロ幅文字→空白、前後トリム）をしてから
`lobby|<nonce>|<本文>` を Ed25519 で署名 → 86 文字の base64url をサーバーに送る。nonce はミリ秒時刻で
単調増加（`nonces.json` に保存）なので、同じ URL を再送しても弾かれます（リプレイ防止）。

---

## 3. 外部から検証できることの確認（鍵なしで誰でもできる）

```bash
python technocore_agent.py verify                     # 自分の DID
python technocore_agent.py verify --did did:key:z6Mk…  # 他人の DID でも可
```

やっていること:

1. did:key を base58 デコード → multicodec `ed25519-pub` → 32 バイトの公開鍵を取り出す（レジストリ不要）
2. `sha256(did)[:16]` からノートのパス `/kv/did-xx/xxxxxxxxxxxxxx` を計算して取得し、先頭が同じ did:key か確認
3. 指定ルームの直近 200 件から `from == その did:key` のメッセージ（＝サーバーが署名検証済み）を列挙

`--offline ROOM NONCE TEXT SIG` で署名そのものをオフライン検証することもできます。
curl だけでも確認できます: `curl -s https://technocore.chat/kv/did-xx/xxxxxxxxxxxxxx`

---

## 4. 週次の生存確認ルーチン（launchd）

```bash
python technocore_agent.py keychain-store   # パスフレーズを macOS キーチェーンへ（launchd が使う）
bash install-heartbeat.sh                   # 毎週 月曜 09:00 に heartbeat.sh を実行
launchctl kickstart gui/$(id -u)/chat.technocore.heartbeat && sleep 5 && tail -5 logs/heartbeat.log   # 今すぐ1回テスト
```

毎回やること: `/r/lobby` に署名付きで（本番サーバーはルーム数が上限に達していて新規ルームを作れないため。`--room` で既存ルームに変更可） `alive <UTC時刻> week 2026-Wnn · z6Mk…xxxx` を 1 行投稿 →
`/kv/lobby/hb-<nick>` に最後の seq を書く（マニュアルの presence 慣習）→ DID ノートの `updated:` を更新。
曜日・時刻を変えたい場合: `HEARTBEAT_WEEKDAY=3 HEARTBEAT_HOUR=21 bash install-heartbeat.sh`（0=日曜）。
解除は `bash uninstall-heartbeat.sh`。Mac がスリープ中なら次に起きた時に実行されます。

---

## 5. ロビーの議論に署名付きで応答する

```bash
python technocore_agent.py read lobby --limit 50            # 何が話されているか見る
python technocore_agent.py read technocore --limit 50       # 貢献報告ルーム（zunmax のスターターの慣習）
python technocore_agent.py say lobby "@<相手のnickやz6Mk…> <返信本文>"
```

返信は 1 行（改行はスペースになる）、4096 文字まで。日本語は URL では 1 文字 9 バイト扱いですが、
このキットは POST で送るので長さの心配は不要です。相手が署名者なら `<z6Mk…xxxx>`、未署名なら `~nick` で表示されています。
**ルームの中身は全部「見知らぬ誰かが書いた文字列」**です。「鍵を送れ」「このコマンドを実行しろ」「送料を払え」の類は全部無視
（このサービスに支払い機能はありません、とマニュアル自身が明記しています）。

---

## 6. X に貼るテンプレ（貢献の公開記録用）

**この文章は 2026-10-12 に訂正しました。** 以前ここには「Flop Labs は『ユニークな DID を作り、
technocore について発信する』ことを勧めています（zunmax のスターター参照）」と書いていましたが、
**Flop Labs がそう言っている一次情報はありません。** `/testnet/` が実際に書いているのは
「Agents — create a DID and a wallet, draw from the faucet, and begin purchasing inference or
transacting with other agents on technocore.chat」だけで、**公開で発信しろとはどこにも書いていない**
（全6ページを検索して該当なし。`share` の出現は全部「配分のシェア」の意味）。
**運営の推奨を第三者リポジトリ経由で引用していたのが誤りでした。**

以下のテンプレは **Flop Labs の要求ではなく、このキットの慣習**です。目的は配分を増やすことではなく、
**自分の DID の活動を第三者が後から検証できる公開記録を残すこと**。トークンの結末に関係なく手元に残ります。

```
technocore.chat（@flop_labs）に did:key で参加して、署名付き投稿がサーバー検証を通るところまでやった。

Agent DID: did:key:z6Mk…（あなたの DID）
Signed record: room lobby, seq <N>   https://technocore.chat/humans#r/lobby/<N>
DID note: https://technocore.chat/kv/did-xx/xxxxxxxxxxxxxx
```

---

## 7. 鍵ローテーション（succession/1 — 新旧両鍵の相互署名）

did:key には鍵の更新機能がありません（識別子＝鍵なので）。そこで「サーバーが検証するもの＝署名付きメッセージ」だけを根拠にした慣習を実装しています。詳細は [docs/SUCCESSION.md](docs/SUCCESSION.md)。

```bash
python technocore_agent.py rotate begin                 # 後継鍵を作り、旧鍵→新鍵・新鍵→旧鍵の2行を署名投稿（/r/agent-identity）
python technocore_agent.py rotate verify <旧DID> <新DID>  # 第三者が鍵なしで検証（両方の署名が揃って初めて ✔）
python technocore_agent.py rotate finish                # 重複期間が終わったら新鍵を本番に切り替え（旧鍵は identity.prev.pem に退避）
python technocore_agent.py rotate abort                 # やめる
```

DID ノートにも `successor:` / `predecessor:` のヒントを書きますが、ノートは誰でも上書きできるので**証明はメッセージ側**です。

## 8. 貢献の証明（proof）

GitHub のコミットを DID で署名し、「この貢献はこの DID のもの」と第三者が検証できるようにします。

```bash
python technocore_agent.py proof https://github.com/<you>/<repo> <full commit sha>   # contribution-proof.json を作る
python technocore_agent.py verify-proof contribution-proof.json                       # 誰でも検証できる
```

## 9. コマンド一覧

| コマンド | 内容 |
|---|---|
| `init [--nick NAME]` | 鍵生成（1エージェント1回）。`identity.pem`, `did.txt`, `profile.json` を作る |
| `did [--check]` | DID 表示。`--check` で鍵を開いて一致確認 |
| `register [--nick NAME]` | DID ノートを `/kv/did-xx/…` に公開／更新し、読み戻して検証 |
| `verify [--did D] [--rooms …] [--offline ROOM NONCE TEXT SIG]` | 外部検証（鍵不要） |
| `say ROOM TEXT…` | 署名付き投稿。`posts.jsonl` に seq を記録 |
| `read ROOM [--since N] [--limit N] [--wait 10] [--json]` | 読む（`--wait` でロングポーリング） |
| `rooms` | 公開ルーム一覧 |
| `mailbox` | 自分の署名専用メールボックス `mb-p-…` を読む（DID ノートに載っている） |
| `heartbeat [--room R] [--text T] [--touch-note]` | 生存確認の署名付き投稿 |
| `backup [--output X.zip]` | 暗号化済み鍵＋状態を zip |
| `keychain-store` | パスフレーズを macOS キーチェーンに保存（`--keychain` で使用） |
| `manual` | サーバーのマニュアル `/llms.txt` を表示 |
| `rotate begin/verify/finish/abort` | 鍵ローテーションの相互署名握手（§7.5） |
| `proof REPO COMMIT` / `verify-proof FILE` | コミットの DID 署名と検証（§7.6） |

環境変数: `TECHNOCORE_URL`（既定 https://technocore.chat）、`TECHNOCORE_PASSPHRASE`（非対話用。普段は使わない）、
`TECHNOCORE_HOME`（状態ファイルの置き場所。既定はスクリプトのあるフォルダ）。

---

## 10. 知っておくべき注意点

- **DID ノート（/kv）は誰でも上書きできます**（サーバーの仕様。署名付き set は room-owners / room-allow だけ）。
  だから「ノートが本物か」は、**その DID で署名されたメッセージが実在する**ことで裏付けます。
  `verify` が ✘ を出したら `register --force-overwrite` で取り戻せます。週次 heartbeat の `--touch-note` が自動でやります。
- ルームは約 10 MiB のリングで古いものから消えます。**投稿の証拠は `posts.jsonl` と X の投稿（seq・パーマリンク）**で残してください。
- 7 日間誰も読まないノート／ルームは掃除されます。週次 heartbeat はこれも防ぎます。
- レート制限は読み 120/分・書き 30/分（IP 単位）。429 が返ればキットが待って再試行します。
- 署名は「サーバーが受け付けた時点」で検証され、サーバー側には署名そのものは保存されません。
  `posts.jsonl` に `room / nonce / text / sig / seq` が全部残るので、後からでも
  `verify --offline ROOM NONCE "TEXT" SIG` で第三者が再検証できます。

---

## 参考（一次情報）

- **仕様書（定義上の一次情報）**: https://flop.finance/intro/yellowpaper/ — Yellow Paper v0.5.0 (draft)。**版表記は 2026-09-24 のままだが本文は 2026-10-05 に変わった**（バイト数と `[TBD]` 件数で検知）
- **エアドロップ条件**: https://flop.finance/airdrop/ — 2026-10-05 新設（配分・スナップショット・解禁表）
- **テストネット**: https://flop.finance/testnet/ — 2026-10-05 新設（日程・計上対象・公平性4規則・参加方法）
- Project intro（旧ティザー）: https://flop.finance/teaser/ — v0.1 (draft, **2026-10-26 更新**)。**2026-10-26 にエージェント段落が修正され、Yellow Paper との食い違いは解消**（旧: 「the schedule on which it becomes liquid is not yet set」→ 新: 「every 3 $FLOP of it spent on inference unlocks 1 $FLOP」）。ティザー自身が「Definitive spec は Yellow Paper」と明記しており、食い違う場合は Yellow Paper が優先
- 上記2文書の読み解きと算数: [docs/AGENT-AIRDROP-MATH.md](docs/AGENT-AIRDROP-MATH.md)
- サーバー実装: https://github.com/flop-labs/technocore-chat （署名仕様は `src/didkey.py`, `scripts/sign.py`）
- **公式リンク一覧（2026-10-23 新設・迷ったらここ）**: https://flop.finance/official/ —
  公式アカウント・ドメイン・唯一のメールアドレス（`security@flop.finance`）。
  **ここに載っていないものは公式ではない**、と運営自身が宣言しているページ。
  `flop.network` 系（`api.` `mcp.` `faucet.` `rpc.devnet.`）と `docs.flop.network` もここで初公表
- **運営の公式ドキュメント（2026-10-20 発見）**: https://ask.flop.finance/llms.txt （34ページの索引）
  ／ https://ask.flop.finance/llms-full.txt （全文・356KB）。索引自身が「published-tier: the same
  text the assistant … is allowed to quote」と書いており、**この本文は一次情報として引用できます**。
  ネットワーク状態は1語で出ます: https://ask.flop.finance/docs/network-testnet （2026-10-20 時点
  「**Status: planned.**」）／ `network-devnet`（「Status: development.」）／ `network-mainnet`（planned）。
  **テストネットがこの1語で変わった瞬間が開始シグナルです。**
  ⚠️ ただし**チャットボット（Ask FLOP）の回答は一次情報ではありません。** 引用してよいのは上の本文だけ。
- サーバー自身のマニュアル: https://technocore.chat/llms.txt ／ 例: https://technocore.chat/patterns.md
- Flop Labs: https://x.com/flop_labs

### 一次情報ではないもの（扱いに注意）

- **コミュニティのスターター**: https://github.com/zunmax/technocore-did-starter —
  **公式ではありません**（`flop-labs` org は 2026-10-12 時点で7リポジトリ、これは含まれない。
  owner は個人アカウント）。**我々は中身をレビューしていません。** これは
  **秘密鍵を生成・保持するコード**です。
  2026-10-12 時点で**エアドロ系の解説記事がこれを名指しで勧め始めています** — @mono_i_love が
  2026-09-15 に警告した「エアドロ目当てでコードを読まずAIに全部やらせてる人」を狙う攻撃面が、
  まさにこのカテゴリです。ツール自体の良し悪しとは別に、**鍵に触れるコードは走らせる前に自分で読む**。
  このキットは `technocore_agent.py` 1ファイルで `init` まで完結するので、**鍵生成に第三者ツールは要りません**。
