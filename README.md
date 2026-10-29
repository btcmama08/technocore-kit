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

> 📦 **2026-10-29 追記 — 公式パッケージが npm に出ました。ただし運営が指定した確認手段はまだ揃っていません。**
> 10/26 に名前だけ公開されて 404 だった5つが、**10-29 04:00:46〜04:03:01 UTC に依存順で一斉に publish**
> されました: `@flop-labs/contracts@0.1.1` → `client@0.2.1` → `pi@0.3.1` → `sdk@0.4.0` → `cli@0.4.0`。
> **版は文書の RC と完全一致**、`repository` は `github.com/flop-labs/flop-core`、maintainer は
> `svidyuk` 1名、ライセンスは `MIT OR Apache-2.0`、各パッケージに `0.0.0-stage` の兄弟版あり。
> **install 時に走るスクリプト（preinstall/postinstall）はどれにも入っていません。**
> → **状況証拠は「運営本人のリリース」を強く支持します。**
>
> **それでも今は入れないでください。理由は運営自身の指示です。** `/docs/upgrade` は今日も不変で:
>
> > Their presence in this guide does not mean they are available on npm or PyPI. Obtain the
> > release operator's publication receipt before installing.
>
> **その receipt がまだ出ていません。** さらに公式リンク一覧（https://flop.finance/official/ 、
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
> 運営自身がこう断っています:
>
> > Package versions below are prepared for publication after review and merge. Their presence
> > in this guide does not mean they are available on npm or PyPI. Obtain the release operator's
> > publication receipt before installing.
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
