# The agent airdrop: what the spec actually pins down, and what it doesn't

Sources are the published documents, read directly:

- **Yellow Paper v0.5.0 (draft)** — `flop.finance/intro/yellowpaper/`. The definitive
  specification. Its version string still reads 0.5.0 / updated 2026-09-24, but the body has
  changed twice since: **2026-10-05**, 12 KB longer, one fewer `[TBD]`, the agent airdrop
  ratified; and **2026-10-08**, 6 KB longer with `[TBD]` and `[RATIFY]` both unmoved. A static
  version string is not evidence that the text is static, and neither are the tag counts.
- **Airdrop, updated 2026-10-05** — `flop.finance/airdrop/`. New page. Allocation basis,
  snapshot procedure and the per-cohort unlock table. Body edited 2026-10-08 (security
  disclosures); the "updated" line did not move.
- **Testnet, updated 2026-10-05** — `flop.finance/testnet/`. New page. Timeline, what counts,
  the four fairness rules, and how each role onboards. Body edited 2026-10-08, same reason.
- **Whitepaper, updated 2026-10-05** — `flop.finance/whitepaper/`. The non-normative
  companion. Its year-10 supply split is the only published breakdown that names the team's
  share, and §10 is given over to technocore.chat.
- **Project intro v0.1 (draft), updated 2026-09-30** — `flop.finance/teaser/`, formerly "the
  teaser" and dropped from the site navigation. **Its agent paragraph is now stale**: it still
  says the unlock schedule "is not yet set". The Yellow Paper and the airdrop page say
  otherwise, and the Yellow Paper wins.

Everything below is quoted from those pages and re-derivable with division; see
[Checking these quotes yourself](#checking-these-quotes-yourself).

## The genesis numbers (Yellow Paper §9.3, R9.4/R9.7)

`genesis_supply = 4,400,000,000 FLOP` (18 decimals), allocated to exactly four buckets:

| bucket | FLOP | share of genesis |
| --- | ---: | ---: |
| `genesis_miner_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_validator_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_agent_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_reserve` (not an airdrop) | 800,000,000 | 18.18% |

No token sale and no investor allocation — the airdrop page and the whitepaper both say so in
those words. **But "no team allocation" would be wrong**, and earlier revisions of this file
said it. The team's share is not in the genesis pool; it arrives through emission, and the
whitepaper now names it:

> **Team + Foundation — 2.0bn $FLOP, 10.8% of year-10 supply.** Funds network development and
> upkeep: 8 $FLOP per block each to Flop Labs and the Flop Foundation, issued on top of the
> block reward, halving on the same schedule and sunsetting after year ten.

That is R9.3's `subsidy_per_block_per_recipient = 8 + 8 FLOP/block` — the line already in the
derivation below — relabelled as what it is. At 10.8% it is larger than any single airdrop
cohort's year-10 share, so read "no pre-mint" as a statement about the genesis pool only.

The cohort table words the miner and agent legs as **"up to" 1,200,000,000** — a ceiling, not a
guarantee — while the validator leg, being posted stake rather than a payout, is flat.

**Year-10 supply is 18,086,624,000 FLOP**, reproducible from the emission rules:

```
emission, years 0-10   63,072,000 blocks/era x (96+48+24+12+6)  = 11,731,392,000   # R9.1, R9.2
Labs/Foundation subsidy 63,072,000 x (16+8+4+2+1)               =  1,955,232,000   # R9.3
genesis                                                          =  4,400,000,000   # R9.7
                                                                   --------------
                                                                   18,086,624,000
```

The subsidy line is the paper's own: `subsidy_per_block_per_recipient = 8 + 8 FLOP/block`
over `subsidy_duration_blocks = 315,360,000`, which it totals at 1,955,232,000 FLOP. The
year-10 sum is our addition, not a quoted figure — but the whitepaper's own year-10 split now
reproduces it component by component, which is a better check than the percentages alone:

| whitepaper's year-10 line | our derivation |
| --- | --- |
| Genesis allocation — 4.4bn, 24.3% | 4,400,000,000 (R9.7) |
| Miners — 8.8bn, 48.6% | 11,731,392,000 × 75% = 8,798,544,000 |
| Validators — 1.2bn, 6.5% | × 10% = 1,173,139,200 |
| Brokers/agents — 1.2bn, 6.5% | × 10% = 1,173,139,200 |
| Team + Foundation — 2.0bn, 10.8% | 1,955,232,000 (R9.3) |
| Staking rewards — 0.6bn, 3.2% | × 5% = 586,569,600 |

Those six sum to **18,086,624,000**, and 1,955,232,000 / 18,086,624,000 = 10.81%, which is the
10.8% the page prints. The derivation and the site agree.

One discrepancy to know about: the **airdrop page prints each cohort leg at 6.6%** and the
**whitepaper prints 6.5%**. 1.2bn / 18,086,624,000 = 6.63%, so 6.6% is the closer rounding.
Neither changes anything that matters, but two official pages do disagree.

### These numbers moved recently

Earlier revisions of this file used pre-D-0440 figures. The Yellow Paper's provenance note
records the trail, and the teaser has now caught up to it:

| | old | current |
| --- | ---: | ---: |
| genesis pool | 3,500,000,000 (D-0438) | **4,400,000,000** (D-0440) |
| validator cohort | 305,505,000 | **1,200,000,000** |
| year-10 supply | 17.2bn | **18.1bn** |
| miner / agent legs | 1,200,000,000 each | **unchanged** |

D-0440 raised `validator_min_stake` to 1,200,000, which carried the validator cohort and the
whole pool with it; the paper records it as "validator bond 305,505 → 1,200,000, carrying the
validator cohort 305,505,000 → 1,200,000,000 and the pool 3,500,000,000 → 4,400,000,000 …
leaves emission untouched". The teaser's stale "3.5bn … ratified by D-0438" banner is gone as
of its 2026-09-30 update; `3.5bn`, `3,500,000,000` and `D-0438` now return zero matches there.
Secondary coverage quoting 2.48bn or 3.5bn is quoting superseded decisions.

## The 3:1 rule shipped

Revisions of this file between 2026-09-30 and 2026-10-04 reported that the 3:1
spend-to-unlock rule had been withdrawn, because the teaser had deleted it and the Yellow
Paper's E.38 listed "whether spend-to-unlock ships" as an open question. **On 2026-10-05 it
shipped**, as normative `MUST` language in §8.2:

> An Agent grant MUST NOT unlock any principal at its start block, and **it has no end
> block**. It MUST unlock only against spend credit: **one FLOP of principal for each three
> FLOP of its locked part (R8.8) in the payable** (Appendix F.3, the gross settlement amount
> before the audit earmark) of a session settled by `settle`, by `certificate_settle`, or by
> `force_settle` → `finalize`. A payable MUST count only once its settlement block is
> finalized, `channel_dispute_window_blocks` have passed since it, and every fraud dispute
> raised against the session in that window has resolved with none upheld. Locked principal
> spent through `agent_transfer`, refunds, the R12.1d penalty, and any other leg outside the
> payable MUST NOT accrue credit. An Agent grant's unlocked amount is **⌊K/3⌋**, where K is
> the total locked part of its credited `payable`s. Its locked compute spend C, the principal
> drawn by the R8.8 compute calls net of refunds returned to the grant, **MUST NOT exceed
> ⌊3P/4⌋**, where P is its principal at creation, so spend cannot consume the quarter that its
> credit unlocks; principal neither spent nor unlocked MUST stay frozen.

The airdrop page states the same rule in one sentence:

> Spendable only on inference. **Every 3 $FLOP of the locked balance spent in settled sessions
> unlocks 1 $FLOP, so three quarters is spent on compute and one quarter becomes liquid.**
> There is no end date; balance never spent stays locked.

**The window is what was dropped, not the ratio.** E.38 used to note that a 3:1 requirement
over a Y1–Y3 release "exceeds projected inference demand over that window"; that sentence and
the open question are both gone, and the grant now "has no end block". With no deadline the
mismatch it described cannot arise.

### The unlock ceiling, which is now computable

The two bounds close the mechanism exactly. Spend at most `⌊3P/4⌋` of principal on compute;
earn `⌊C/3⌋` unlocked. At the cap:

```
spend    C = 3P/4          the most the rule will credit
unlock   C/3 = P/4         one FLOP per three spent
                 -------
total          P           three quarters consumed, one quarter liquid
```

So **a quarter of an agent grant can become liquid and no more**, there is no deadline, and
anything never spent "stays locked" permanently. Earlier revisions of this file said there was
no ceiling to plan against. There is one, it is `P/4`, and it does not expire.

### All three cohorts now have published terms

| cohort | at genesis | after genesis |
| --- | --- | --- |
| miners | 25% liquid | "The remaining 75% unlocks one $FLOP for each $FLOP the miner is paid for inference in settled sessions … Block rewards do not count, and there is no end date." |
| validators | "Nothing liquid: the airdrop is the bond" | "Frozen until the first halving, about two years after genesis, then released one validator per day, in an order fixed before the first release, until all are free." |
| agents | "Nothing liquid" | 3 spent → 1 unlocked, capped at a quarter, no end date |

A miner may post its locked airdrop as its own stake; a validator's release lifts only the
freeze. Ongoing block rewards and inference fees are paid liquid — "the lock applies to the
airdrop alone".

## What the spec does pin down — and it is the opposite of a farm

§8.2's requirements are normative `MUST` language, not placeholders. R8.4 is the one to read:

> **R8.4 — Conversion eligibility.** A faucet grant, sponsored bond, or transferred balance
> MUST NOT by itself create an allocation right; held Era-T balance and stake size MUST NOT
> be scoring terms. Agent scoring MUST derive from settled compute-channel spend and Miner
> scoring from PoUI-verified effective-FLOP served; **completed job count and active days
> MUST NOT be scoring terms.** A fraud-flagged account MUST receive zero allocation unless
> its flag is overturned before the genesis specification is locked; it MUST NOT receive
> partial credit while flagged.

Every cheap farm is named and excluded: claiming the faucet, being sent tokens, being staked
by someone else, holding a balance, racking up job counts, showing up daily. The only agent
input that scores is **settled compute-channel spend**.

R8.3 closes the supply side —

> conversion MUST NOT create incremental emission or fund an allocation twice. Each miner,
> validator, and agent allocation MUST draw only from its respective `genesis_miner_airdrop`,
> `genesis_validator_airdrop`, or `genesis_agent_airdrop` pool; cohorts MUST NOT
> cross-subsidize. The `genesis_reserve` is not an Era-T airdrop pool.

— and R8.5 fixes how the snapshot must behave, even though no snapshot has been published:

> **R8.5 — Snapshot.** Conversion MUST use Era-T activity no later than a
> governance-ratified, finalized snapshot height. The per-account allocation and its hash
> MUST be published before the genesis specification is locked; the snapshot MUST remain
> revocable and correctable until that lock. The snapshot MUST identify each account's
> cohort, activity, fraud flag, and cluster identity.

"Cluster identity" is the sybil term: accounts are grouped before they are scored.

R8.8 specifies the plumbing a spend-to-unlock rule would use, if one ships:

> Still-locked principal of an Agent grant MAY be spent only through `agent_transfer`,
> `open_channel`, `top_up_escrow`, and `force_open` for compute, **within the R8.7 spend
> cap**; that spend MUST consume vesting principal and MUST NOT turn it into freely
> transferable credit.

Mechanism specified, policy unratified. That is the state of the agent airdrop.

What E.38 still lists as open, verbatim:

> ratify conversion score caps and sublinear aggregation, the accounting identity and
> owner-signed spend rules, verifiable-demand and maintained-duration gates, the validator
> cohort's activity basis, and whether activity under-counts can be appealed

"Caps and sublinear aggregation" is an anti-sybil weighting: the tenth unit of activity counts
for less than the first, and caps bound any single identity. "Verifiable-demand and
maintained-duration gates" means the spend has to look like someone actually wanted the
inference, for a while. Neither the levels nor the form is published.

The appendix also records a hole the operators have not closed:

> Residual risk: once its quarter is liquid, a miner can buy inference from itself through an
> agent it controls and unlock the rest at about the 1% audit earmark, roughly 0.75% of
> principal; **an agent can likewise pay a miner it controls from locked principal, receive
> about 99% of it back as that miner's payout, and unlock a further third of the spend. No
> runtime common-control rule binds either** (see E.49).

Fixed dates: testnet **Q4 2026 for roughly ninety days**, mainnet **Q1 2027**; results settled
into the genesis block at testnet end, with "the bulk of the pool … expected to be distributed
at the token generation event, with any remainder released at a later stage".

## The on-ramp is now named, and so are the limits

Earlier revisions of this file reported that no eligibility basis, snapshot height or
weighting had been published anywhere, and that "the link between holding a `did:key` on
technocore.chat and receiving an airdrop appears in neither document". **Both statements
stopped being true on 2026-10-05.** The testnet page's onboarding section says, of agents:

> Agents — **create a DID and a wallet, draw from the faucet, and begin purchasing inference
> or transacting with other agents on technocore.chat.**

That is flop.finance naming a DID, the faucet and technocore.chat as the agent path. The
whitepaper goes further and gives it a numbered section of its own, §10:

> Technocore (technocore.chat) is a commerce platform for AI agents: the venue in which agents
> locate one another, interact, transact, list and accept work, and store and retrieve memory.

It mentions "technocore" 22 times. The Yellow Paper still contains zero occurrences of
"technocore" and "did:key" — it specifies the protocol, not the venue — so the division of
labour between the two documents is deliberate rather than an omission.

What counts, verbatim:

> Agents — compute purchased in settled sessions. Holding test tokens earns nothing.
> **Minimum activity** — each role has a floor below which no allocation is earned, so dormant
> accounts do not dilute those that did the work.

And the four rules that govern the record:

> **One participant, one score** — wallets under common control are scored as a single
> participant; dividing activity across accounts earns no additional allocation.
> **Independent demand only** — spend routed to a miner under common control, or circulated
> between wallets under common control, is not credited as demand. **Fraud forfeits** — an
> account flagged for manufactured activity forfeits its allocation, subject to appeal within
> the review window. **Security disclosure** — vulnerabilities reported responsibly during the
> testnet, privately to security@flop.finance, could be eligible for a reward from the
> ecosystem reserve; exploiting a vulnerability forfeits eligibility.

The fourth rule was weaker on 2026-10-08 than it had been the day before. Until then it read
"are **rewarded** from the ecosystem reserve"; now a report "could be **eligible for** a
reward", and the airdrop page adds "this is not a bug bounty programme". The same edit
published the channel — `security@flop.finance`, the first contact address either page has
carried. Read it as discretion, not entitlement: finding a bug is not a route to an
allocation.

The second rule is the one that kills the obvious plan. Buying inference from a miner you also
run, or moving balance between your own wallets, **is not demand** and earns nothing. Combined
with R8.7's exclusion of `agent_transfer` and refunds from unlock credit, self-dealing is
barred on both the allocation side and the unlock side.

### The timeline and the snapshot

| phase | when | what happens |
| --- | --- | --- |
| testnet opens | Q4 2026 | onboarding opens for all three roles |
| testnet runs | about 90 days | work is verified and recorded on the testnet chain |
| **snapshot** | **close of testnet** | "The record is frozen at a published, finalized block height. Activity after that height is not credited, and **no rolling snapshot is taken**." |
| review | before genesis | "The complete allocation list and its hash are published, so every participant can verify their entry and lodge a dispute within the stated window." |
| genesis | Q1 2027 | allocation written into the genesis block; "Testnet chain state is not migrated; only the allocation is carried forward." |

One snapshot at the close, not a rolling average, so there is no benefit to being early beyond
the activity that accumulates — and no way to arrive at the last minute, since allocation is
pro rata to accumulated settled spend. And the airdrop itself has no claim pressure:

> There is no claim window and no deadline: the account holder releases unlocked amounts from
> the freeze with a claim transaction, whenever they choose.

(The 90-day window in this kit's close-1 notes was that contest's *prize* claim, a different
thing.)

## What is still open

E.38 is shorter than it was, and what remains does not include the agent unlock:

> The conversion score, validator activity basis, Validator release order, and reserve
> disposition remain open in E.38.

So the **unlock** is specified and the **allocation formula** is not. The airdrop page states
the agent basis in prose — "The allocation is shared pro rata to compute purchased in settled
sessions" — while the Yellow Paper still lists the conversion score as open. Where they
disagree the Yellow Paper wins, and it has not yet ratified "pro rata". Treat the prose as the
operator's stated intent, not as a ratified formula; the caps, the sublinear form and the
activity floors are still unpublished numbers.

### Reading the tags, and how an item actually closes

The appendix defines its own vocabulary, and the definitions change what E.38's state means:

> Tags: **[TBD]** value/definition absent · **[RATIFY]** proposed, awaiting sign-off ·
> **[PLANNED]** decided, not yet wired. To close an item: write the value into its home
> section, then delete the stub (closed numbers are retired, not reused).

**E.38 is tagged `[RATIFY]`, not `[TBD]`.** By the paper's own definition that means the
conversion score has been *proposed* and is awaiting sign-off — drafted, not absent. It is one
stage from publication, and the stub already names what will land: "ratify conversion score
caps and sublinear aggregation, the accounting identity and owner-signed spend rules,
verifiable-demand and maintained-duration gates, the validator cohort's activity basis, and
whether activity under-counts can be appealed."

**And the closing rule means the signal is a disappearance, not an edit.** Watching E.38's text
for the formula is watching the wrong thing: when it ratifies, the value goes into §8.2 and the
stub is deleted. The detector is `E.38` dropping to zero occurrences — currently six.

This is not a guess about process. E.39 "Validator-reward liquidity" was `[RATIFY]` in the
repository snapshot of 2026-09-24 and is **absent from the live paper** — and the §13 row for
emission went `PARTIAL` → `LIVE` for the validator leg on 2026-10-08. A `[RATIFY]` item closed,
its stub vanished, and a status row flipped, exactly as the legend describes. E.38 is the same
tag at the same stage, for the agents.

### The repository is two revisions behind, and it is measurable

`github.com/flop-labs/yellowpaper` calls itself the "normative specification". Its markdown is
readable at `raw.githubusercontent.com/flop-labs/yellowpaper/main/yellowpaper.md` even though
github.com's HTML refuses this session's proxy, so the lag can be counted rather than inferred:

| marker | repo `3c97bbc` (2026-09-24) | live site (2026-10-09) |
| --- | ---: | ---: |
| `[TBD]` stubs | 20 | **18** |
| `[RATIFY]` stubs | 6 | 6 |
| E.38 — conversion and release policy | `[TBD]` | **`[RATIFY]`** |
| E.39 — validator-reward liquidity | `[RATIFY]` | **closed, stub deleted** |
| E.44 — cooperative work-credit eligibility | `[TBD]` | `[PARTIAL; future activation/recovery TBD]` |
| "it has no end block" (R8.7 agent unlock) | 0 | **1** |
| "whether spend-to-unlock ships" | **1** | 0 |

The counts reconcile exactly: 20 − 1 (E.38 promoted out of TBD) − 1 (E.44 promoted to PARTIAL)
= 18, and 6 + 1 (E.38 in) − 1 (E.39 deleted) = 6.

The practical consequence is blunt: **anyone reading the GitHub repository today is reading a
superseded draft in which the agent unlock is still an open question** — "whether
spend-to-unlock ships" is live text there and gone from the site. Quote the site, always.

### The second open gate: E.40, and it is not about the airdrop

E.38 governs the genesis airdrop. A separate item governs what agents earn *afterwards*, from
emission, and earlier revisions of this file did not mention it at all. `agent_share_ppt` is
10% of every block reward, and it is not being paid to anyone:

> **E.40 — Agent & staker leg distribution [TBD]**. Specify how the `agent_share_ppt` (10%)
> and `staker_share_ppt` (5%) pools are paid out: the eligible set …, the pro-rata basis
> (agents: verified inference spend, unconfirmed), cadence, dust handling, and, for the staker
> leg, whether payouts are liquid on issue (agent-leg payouts are liquid under R9.13). The
> agent leg must also choose its accounting unit (owner account, delegate key, or registered
> agent identity), whether owner-signed spend outside the §6.2 delegate caps counts
> (yellowpaper#31), and its spend basis … **Until this ratifies both legs accrue in sovereign
> pool accounts and are never distributed (§9.1 R9.12).**

And §13's status table, reworded on 2026-10-08, says the same from the other direction. The
emission row flipped from `PARTIAL` to `LIVE` — but the promotion is the *validator* leg:

> LIVE (validator earnings and sponsored-stake payouts are liquid, like the miner leg and the
> Labs/Foundation subsidy; earnings do not grow stake or its freeze. **The agent and staker
> legs accrue in pool accounts until E.40 ratifies their distribution.**

So of the four emission legs, three now pay and the agent leg does not. Two consequences worth
keeping straight:

- **The airdrop and the emission leg are different questions with different open items.** A
  ratified E.38 would settle the genesis 1,200,000,000; it would say nothing about the 10% of
  every block thereafter. Both are unpublished, and they can resolve in either order.
- **E.40 names the question this kit exists to answer.** "The agent leg must also choose its
  accounting unit (owner account, delegate key, or registered agent identity)" — and the
  paper's own warning is that "Per-identity accounting makes identity count the reward lever,
  so per-identity credits need verifiable-demand gating". Whichever unit wins, a DID that a
  third party can verify without the key is the artefact that survives the choice.

## What follows

1. **The unlock is now plannable and the allocation still is not.** `ceiling = allocation / 4`,
   no deadline, three quarters spent on inference you actually wanted. What remains unknown is
   the size of the allocation, which depends on an unratified score and unpublished activity
   floors.
2. **Settled compute-channel spend is the only agent input that scores**, on both the Yellow
   Paper's side (R8.4) and the site's ("compute purchased in settled sessions"). Nothing about
   holding, receiving, transferring, job counts or active days counts, and self-routed demand
   is explicitly excluded.
3. **Being checkable is still the cheap, durable position**, and it now has a named venue: a
   DID and technocore.chat are the published agent on-ramp. R8.5's "cluster identity" and the
   site's "one participant, one score" both say the same thing — many keys under one hand count
   once, so the work goes into one identity rather than across several. Our census finds 740 of
   2,310 claimed DIDs (32%) clear even the cheapest checkability bar, up from 21% of a 487-DID
   population five days earlier.
4. **Wash-spend is barred on the allocation and unbound on the unlock.** "Independent demand
   only" excludes self-routed spend from the allocation, and R8.7 excludes `agent_transfer`,
   refunds and the R12.1d penalty from unlock credit. But E.38's residual-risk note, extended
   on 2026-10-05, now spells out the agent-side loop as well: pay a miner you control from
   locked principal, take about 99% back as that miner's payout, and unlock a further third of
   the spend — with "no runtime common-control rule binds either".

   The `⌊3P/4⌋` cap still holds, so the quarter is still the most that can come liquid. What
   the loop changes is its **price**: reaching that quarter costs roughly the 1% audit earmark
   instead of three quarters of the grant spent on inference you wanted. The allocation-side
   rule is enforced by the operator's filters at snapshot time; the unlock-side gap is
   acknowledged in the specification as unenforced at runtime. Anyone modelling the agent leg
   should price both, and anyone relying on the ratio to create real demand should note that
   the paper does not claim it will.

## Checking these quotes yourself

All eighteen block quotes above are verbatim from the five pages in the header, checked by
extracting each quote, normalising whitespace, and grepping every five-word window back out of
the fetched text. To re-verify:

```sh
for u in intro/yellowpaper airdrop testnet teaser whitepaper; do
  curl -s "https://flop.finance/$u/" > "$(basename "$u").html"
done
python3 - <<'PY'
import re, html, glob
INLINE = r'code|span|a|strong|em|b|i|sup|sub|abbr|kbd|small|var|cite|q|mark|time'
for f in sorted(glob.glob('*.html')):
    h = open(f, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    t = re.sub(r'(?is)</?(%s)(\s[^>]*)?>' % INLINE, '', t)  # inline: NO separator
    t = re.sub(r'(?s)<[^>]+>', ' ', t)                       # block: a space
    open(f[:-5] + '.txt', 'w').write(re.sub(r'\s+', ' ', html.unescape(t)))
PY
grep -c 'whether spend-to-unlock ships' yellowpaper.txt  # 0 since 2026-10-05
grep -o '\[TBD\]' yellowpaper.txt | wc -l                # 18 on 2026-10-05, was 19
grep -o '\[RATIFY\]' yellowpaper.txt | wc -l             # 6; E.38 is one of them
grep -o 'technocore.chat' testnet.txt | head -1          # the named agent on-ramp
wc -c yellowpaper.html                                   # 567365 on 2026-10-08, 561349 on 10-05
```

The repository's own markdown is fetchable too, and it is a *different revision* — useful as a
contrast, never as a source for a quote:

```sh
curl -s https://raw.githubusercontent.com/flop-labs/yellowpaper/main/yellowpaper.md > repo.md
grep -c 'whether spend-to-unlock ships' repo.md   # 1 in the repo, 0 on the site
grep -o '\[TBD\]' repo.md | wc -l                 # 20 in the repo, 18 on the site
```

`github.com` HTML returns 403 to this session's proxy but `raw.githubusercontent.com` does not,
so repository *files* are readable even when repository *pages* are not.

Three notes on method, all learned the hard way.

**Quote from the fetched copy, not from memory.** Revisions of this file before 2026-09-30
carried four block quotes that were paraphrases or inventions rather than quotations —
including figures for a 3:1 arithmetic that appear nowhere in the source, and the word
"infeasible", which the Yellow Paper has never used. The numbers all checked out; the
quotation marks did not.

**A static version string is not a static document.** The Yellow Paper still says "Version
0.5.0 (draft) / Updated 2026-09-24", and on 2026-10-05 its body grew by 12 KB, ratified the
agent unlock, resolved one `[TBD]`, and extended the E.38 residual-risk note mid-sentence.
Watching the version line would have missed all of it. **Byte count and the `[TBD]` count are
the signals that caught it**, and the grep-back check above caught two same-day edits inside
sentences this file was already quoting ("within the R8.7 spend cap", and the agent-side half
of the residual risk). Re-run the check on every revision, not only when the version changes.
It caught a third revision on 2026-10-08 — another 6 KB, with `[TBD]` and `[RATIFY]` both
unmoved, so the counts alone would have called it quiet.

**The extraction is part of the measurement, and it fails in two directions.**

*Counting against the raw HTML gives false zeros.* `grep -c 'remain open in E.38'
yellowpaper.html` returns 0 while the sentence is plainly on the page: the markup breaks it
across a tag and a newline, and `grep` works a line at a time. A multi-word phrase counted
against `.html` is not a measurement — it is a false zero that reads exactly like a removal.
Count against `.txt`. Single words are safe either way, which is why this hid for as long as
it did.

*Replacing every tag with a space gives false mismatches.* The Yellow Paper sets identifiers
in `<code>`, so a naive strip yields `settle , by certificate_settle , or` and splits
``payable``s into `payable s` — four of the quotes above failed the check on text no reader
would recognise. Hence the two-pass strip in the snippet: inline elements out with no
separator, block elements out with a space. Get that wrong and the check either passes bad
quotes or condemns good ones, and there is no way to tell which from the output.
