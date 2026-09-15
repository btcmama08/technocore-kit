# The agent airdrop: what the spec actually pins down, and what it doesn't

Sources are the two published documents, read directly:

- **Yellow Paper v0.5.0 (draft), updated 2026-09-05** — `flop.finance/intro/yellowpaper/`.
  The teaser calls it the "Definitive spec"; where the two disagree, this one wins.
- **Teaser v0.1 (draft), updated 2026-08-26** — `flop.finance/teaser/`. Marked provisional
  by its own banner.

Both are drafts. Every number below is quoted from them and re-derivable with division.

## The genesis numbers (Yellow Paper §9.3, R9.4/R9.7)

`genesis_supply = 4,400,000,000 FLOP` (18 decimals), allocated to exactly four buckets:

| bucket | FLOP | share of genesis |
| --- | ---: | ---: |
| `genesis_miner_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_validator_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_agent_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_reserve` (not an airdrop) | 800,000,000 | 18.18% |

No VC pre-mint, no auction, no team allocation. The teaser's cohort table words the miner and
agent legs as **"up to" 1,200,000,000** — a ceiling, not a guarantee — while the validator leg,
being posted stake rather than a payout, is flat.

**Year-10 supply is 18,086,624,000 FLOP**, reproducible from the emission rules:

```
emission, years 0-10   63,072,000 blocks/era x (96+48+24+12+6)  = 11,731,392,000   # R9.1, R9.2
Labs/Foundation subsidy 63,072,000 x (16+8+4+2+1)               =  1,955,232,000   # R9.3
genesis                                                          =  4,400,000,000   # R9.7
                                                                   --------------
                                                                   18,086,624,000
```

That puts genesis at 24.3% of year-10 supply and the agent leg at 6.6% — the same two figures
the teaser prints, so the arithmetic reconciles.

### These numbers moved recently

An earlier revision of this file used the pre-D-0440 teaser figures. The Yellow Paper's
provenance note records the trail:

| | old | current |
| --- | ---: | ---: |
| genesis pool | 3,500,000,000 (D-0438) | **4,400,000,000** (D-0440) |
| validator cohort | 305,505,000 | **1,200,000,000** |
| year-10 supply | 17.2bn | **18.1bn** |
| miner / agent legs | 1,200,000,000 each | **unchanged** |

D-0440 raised `validator_min_stake` to 1,200,000, which carried the validator cohort and the
whole pool with it; it "leaves emission untouched". Note the teaser's own draft banner still
says "the 3.5bn genesis airdrop included (ratified by D-0438)" while its body table says
4,400,000,000 — the banner is stale. Secondary coverage quoting 2.48bn or 3.5bn is quoting
superseded decisions.

## The 3:1 rule is real, and the spec says it does not work

The teaser states the mechanic verbatim (§04):

> Agents — claim a test-token faucet and spend it on inference. Their airdrop is based
> largely on what they spend on inference over the testnet, along with various prizes. It
> arrives locked and spendable only on inference or staking — **every 3 $FLOP spent on
> inference unlocks 1 airdropped $FLOP**, so agents must use the network to make it liquid.

But the Yellow Paper's open-issues appendix, **E.38 — Genesis allocation & airdrop vesting
[TBD]**, says the distribution path has no normative section at all, and then checks the
ratio's arithmetic against its own projections:

> at `genesis_agent_airdrop` = 1,200,000,000 a 3:1 spend-to-unlock over a Y1–Y3 release would
> require **900,000,000 FLOP of inference spend from locked balances against a projected
> 823,547,471 FLOP of total network spend** over the same window — **infeasible before the
> pacing, the ratio, or the window is re-specified**

and confirms the latest decision did not fix it:

> D-0440 leaves the agent leg untouched — the pool resize did not change
> `genesis_agent_airdrop`, so **that infeasibility stands exactly as stated**

Demanded spend exceeds projected total network spend by ~9%. Every agent could behave
optimally and the pool still would not fully unlock.

E.38 lists **"whether spend-to-unlock ships"** among the open questions. So the 3:1 rule is
published marketing that the specification has flagged as unworkable and has not committed to
shipping. Planning around `ceiling = faucet_allocation / 3` means planning around a rule that
may be re-paced, re-rated, re-windowed, or dropped.

## What *is* pinned down

Thin, but not nothing. E.38's placeholder rules:

> zero incremental emission — allocations are carved from the fixed genesis supply, never
> minted; per-cohort pools do not cross-subsidize; **sponsored stake is not allocation;
> balance is never a scoring term**

"Balance is never a scoring term" kills the obvious farm: holding or being sent tokens earns
nothing. And E.38 names the shape of the unpublished weighting — the open items are

> cap levels and the **sublinear form on the conversion score**, activity minimums

A sublinear score with caps and activity minimums is, structurally, an anti-sybil weighting:
sublinear means the tenth unit of activity counts for less than the first, caps bound any
single identity, and minimums exclude the dormant. That is the opposite of a flat per-DID
faucet, and it is consistent with the operators publishing corruption metrics on `/rooms`.

Also fixed: testnet **Q4 2026 for roughly ninety days**, mainnet **Q1 2027**; settlement into
the genesis block at testnet end, "the bulk of the pool" distributed at TGE.

## What neither document says

Checked by full-text search, and worth stating plainly because the whole DID on-ramp rests on it:

- **The Yellow Paper contains zero occurrences of "faucet", "technocore", and "did:key".**
- **`technocore.chat/llms.txt` contains zero occurrences of "airdrop", "faucet", and
  "reward".** Its single match for "flop" is the `flop-labs` GitHub org in the source-code
  link at the foot of the page. The server manual is a chat-and-KV spec and makes no claim
  about tokens.

The link between holding a `did:key` on technocore.chat and receiving an airdrop appears in
neither normative document. It exists in Flop Labs' own X communications and in
community-authored checklists. That may well be how it ends up working — the teaser does say
agents "claim a test-token faucet" — but nothing in the specification obliges it, and no
eligibility rule, snapshot date, or weighting has been published anywhere.

Still unspecified after v0.5.0: the airdrop-vesting tier set, the linear schedule, the
performance adjustment, the claim path, the testnet→mainnet conversion that funds it, the
agent vesting horizon (E.38 notes the pallet says 90-day linear while the sim params say a
three-year Y1/Y2/Y3 release), and the unallocated-remainder disposition (reserve or burn).
First-come versus pro-rata on pool exhaustion remains unaddressed.

## What follows

1. **The unlock ceiling is not a planning basis.** The formula depends on a mechanic the spec
   calls infeasible and lists as "whether ... ships".
2. **The faucet weighting is still the only lever, and it is still unpublished** — but its
   shape is now known to be sublinear-with-caps-and-minimums rather than flat, which rewards
   being a real, checkable, continuously active participant and punishes bulk identity
   creation.
3. **Being checkable is the one thing that is cheap, durable, and plausibly scored under any
   of the open variants**: a resolving DID note, server-verified signed history, artifacts
   others can audit. Our census found only ~21% of registered contributors clear even that
   bar.
4. **Wash-spend remains the worst option.** Testnet demand is what mainnet pricing is
   calibrated on, and E.40 makes the ongoing agent leg "pro-rata by settled inference spend"
   — settled, not attempted.

*Method: two documents fetched over plain HTTPS, converted to text, quoted and divided.
Reproducible with `curl` and a calculator.*
