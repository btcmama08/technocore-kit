#!/usr/bin/env python3
"""close-1 registration and verification, for the Close Call contest.

Three subcommands, all driven by the contest's own published config:

  status    time to lock, the current sweep, and whether the official rooms are listed
  register  post the one signed owner message that mints 10,000 POLF  (needs --yes)
  verify    ask the referee's rooms whether this key was actually minted

Why this exists: the contest's registration is a single signed message, and the
open issues on the contest repo (#17, #24, #26) are participants who posted one
and cannot tell whether it took. So registering is one line; confirming it is
the part worth automating.

Design rules, deliberate:
  - The private key never leaves this machine. Nothing here prints, copies or
    transmits it; signing is technocore_agent's, and the passphrase prompt is its.
  - Every timing and limit value is read live from the contest's contest.json,
    never hardcoded here. The repo's README describes the contest as a "draft";
    the config's `opening` and `lock` are what actually decide whether it is live.
  - `verify` parses only the referee's own JSON fields and prints findings. It
    does not echo room text, because a trading room is whatever strangers typed.
  - `register` writes nothing until you pass --yes, and refuses a host other
    than technocore.chat so a mistyped TECHNOCORE_URL cannot collect a signature.

Usage:
    python3 scripts/close1.py status
    python3 scripts/close1.py register            # dry run: shows the exact text
    python3 scripts/close1.py register --yes      # signs and posts
    python3 scripts/close1.py verify
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CONFIG_URL = (
    "https://raw.githubusercontent.com/flop-labs/"
    "technocore-close-call-challenge/main/contest.json"
)
EXPECTED_HOST = "https://technocore.chat"
RECORD = ROOT / "close1-record.json"
SEASON = "close-1"
USER_AGENT = "technocore-kit-close1/1"

# `status` and `verify` touch no key, so they must not need the signing stack:
# technocore_agent pulls in `cryptography`, which is exactly the dependency you
# do not want standing between you and "am I registered?". It is imported only
# by `register`, where a signature is genuinely required.


def agent():
    """technocore_agent, imported on demand. Only signing needs it."""
    sys.path.insert(0, str(ROOT))
    try:
        import technocore_agent as ta
    except Exception as e:  # a broken or absent cryptography build lands here
        sys.exit(
            f"cannot load technocore_agent ({e.__class__.__name__}: {e}).\n"
            "Signing needs it; run ./setup.sh first. `status` and `verify` do not."
        )
    return ta


def base_url() -> str:
    import os
    return os.environ.get("TECHNOCORE_URL", EXPECTED_HOST).rstrip("/")


def get(path: str, timeout: int = 30) -> tuple[int, str, dict]:
    req = urllib.request.Request(
        base_url() + path, headers={"User-Agent": USER_AGENT, "Accept": "text/plain, application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers or {})


def read_did() -> str:
    """The public did:key from did.txt. Reads no key material."""
    f = ROOT / "did.txt"
    if not f.exists():
        sys.exit(f"no {f.name} — run: python3 technocore_agent.py init")
    did = f.read_text().strip()
    if not did.startswith("did:key:z6Mk") or len(did) != len("did:key:") + 48:
        sys.exit(f"{f.name} does not hold an ed25519 did:key: {did[:24]!r}…")
    return did


# --------------------------------------------------------------------------- config


def load_config(timeout: int = 30) -> dict:
    """The contest's own machine-readable config. Never cached, never assumed."""
    req = urllib.request.Request(CONFIG_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            sys.exit(f"contest.json returned {resp.status}; refusing to guess the rules")
        cfg = json.loads(resp.read().decode("utf-8"))
    for key in ("contest_id", "opening", "first_sweep", "lock", "sweep_seconds", "rooms"):
        if key not in cfg:
            sys.exit(f"contest.json is missing {key!r}; refusing to act on a partial config")
    return cfg


def ts(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def sweep_now(cfg: dict, now: dt.datetime) -> int:
    """Sweep n runs at first_sweep + (n-1)*sweep_seconds, so n counts from 1."""
    elapsed = (now - ts(cfg["first_sweep"])).total_seconds()
    step = int(cfg["sweep_seconds"])
    return int(elapsed // step) + 1 if elapsed >= 0 else 0


def sweep_time(cfg: dict, n: int) -> dt.datetime:
    return ts(cfg["first_sweep"]) + dt.timedelta(seconds=(n - 1) * int(cfg["sweep_seconds"]))


def human(delta: dt.timedelta) -> str:
    total = int(delta.total_seconds())
    sign = "" if total >= 0 else "-"
    total = abs(total)
    return f"{sign}{total // 86400}d {total % 86400 // 3600}h {total % 3600 // 60}m"


# --------------------------------------------------------------------------- guards


def require_expected_host() -> None:
    if base_url() != EXPECTED_HOST:
        sys.exit(
            f"TECHNOCORE_URL is {base_url()!r}, not {EXPECTED_HOST!r}.\n"
            "Refusing to sign for another host — a signature is only as safe as "
            "where it is sent. Unset TECHNOCORE_URL, or pass --allow-host if you "
            "really mean it."
        )


def require_live(cfg: dict, now: dt.datetime) -> None:
    if now < ts(cfg["opening"]):
        sys.exit(f"the contest opens at {cfg['opening']}; nothing to register yet")
    if now >= ts(cfg["lock"]):
        sys.exit(f"the lock at {cfg['lock']} has passed; registration is closed")


# --------------------------------------------------------------------------- rooms


def listed_rooms(cfg: dict) -> tuple[dict[str, bool], str]:
    """Which official rooms the server lists, plus the listing's last-modified.

    The listing is served with s-maxage=86400, so it can be a day old; the
    header is returned so the caller can say so instead of implying it is live.
    """
    status, body, headers = get("/rooms?limit=200")
    if status != 200:
        sys.exit(f"/rooms returned {status}")
    modified = headers.get("last-modified", headers.get("Last-Modified", "unknown"))
    names = {line.split()[0][3:] for line in body.splitlines() if line.startswith("/r/")}
    wanted = list(cfg["rooms"]["trading"]) + list(cfg["rooms"]["referee"])
    return {room: room in names for room in wanted}, modified


# --------------------------------------------------------------------------- commands


def cmd_status(args: argparse.Namespace) -> None:
    cfg = load_config()
    now = dt.datetime.now(dt.timezone.utc)
    n = sweep_now(cfg, now)
    print(f"contest     {cfg['contest_id']}  (rules {cfg.get('rules_version', '?')})")
    print(f"now         {now.isoformat(timespec='seconds')}")
    print(f"opened      {cfg['opening']}")
    print(f"lock        {cfg['lock']}   in {human(ts(cfg['lock']) - now)}")
    print(f"settles     {cfg.get('final_price_time', '?')}")
    print(f"sweep       {n} of {cfg.get('lock_sweep', '?')} (every {cfg['sweep_seconds']}s)")
    print(f"mint        {cfg.get('mint')} POLF per key, once")
    print(f"prize       {cfg.get('prize_pool')} {cfg.get('prize_unit')} "
          f"to {cfg.get('prize_places')} places, claim within "
          f"{cfg.get('claim_window_days')} days")

    rooms, modified = listed_rooms(cfg)
    print(f"\nrooms listed (snapshot, last-modified {modified}):")
    for room, present in rooms.items():
        print(f"  {'listed    ' if present else 'NOT LISTED'}  {room}")
    live = now < ts(cfg["lock"])
    if not all(rooms.values()):
        if live:
            print("\n  A missing room matters: the referee docs say trades posted in a room\n"
                  "  after it is unlisted are not applied, with no visible error.")
        else:
            # After the lock the referee stops posting, its rooms go quiet, and the
            # server unlists a quiet room. Unlisted is not gone: llms.txt defines it
            # as "reachable, never enumerated", so the reads below still work.
            print("\n  Expected after the lock: a quiet room gets unlisted, which only stops\n"
                  "  it being enumerated. The reads below prove it is still reachable.")

    # The room listing above is a daily snapshot, but a room *read* is not cached,
    # so the referee's own rooms are the live view of the contest.
    print("\nreferee (live):")
    price = [q for q in referee_posts("d-close1-price", limit=2) if q.get("t") == "price"]
    if price:
        posted = price[-1].get("n")
        # The contest's last sweep is lock_sweep; the clock keeps going but the
        # referee does not, so comparing against a still-advancing sweep number
        # would report a growing "lag" for a contest that simply finished.
        due = min(n, int(cfg["lock_sweep"])) if "lock_sweep" in cfg else n
        print(f"  latest sweep posted  {posted}   (due {due}, lag {due - posted})")
        if due - posted > 2:
            print("    the referee is behind; nothing is settled until its flow room says so")
        elif not live:
            print(f"    the contest ended at sweep {due}; this is the last sweep there is")
    else:
        print("  no price post readable — cannot tell whether the referee is running")

    state = [q for q in referee_posts("d-close1-state", limit=2) if q.get("t") == "state"]
    if state:
        print(f"  owner keys registered  {state[-1].get('owners'):,}"
              if isinstance(state[-1].get("owners"), int)
              else f"  owner keys registered  {state[-1].get('owners')}")
        print(f"  trading rooms          {state[-1].get('rooms')}")

    pnl = [q for q in referee_posts("d-close1-pnl", limit=2) if q.get("t") == "pnl"]
    if pnl:
        top = pnl[-1].get("top") or []
        scores = []
        for entry in top:
            for field in (entry if isinstance(entry, (list, tuple)) else [entry]):
                if isinstance(field, str) and not field.startswith("did:"):
                    try:
                        scores.append(float(field))
                    except ValueError:
                        pass
        print(f"  mark                   {pnl[-1].get('mark')}")
        if scores:
            bar = sorted(scores, reverse=True)[: cfg.get("prize_places", 3)]
            print(f"  top scores             {', '.join(f'{v:+,.2f}' for v in bar)}")
            print(f"  positive in top {len(top):<3}    {sum(1 for v in scores if v > 0)}")
            if live and len(bar) >= cfg.get("prize_places", 3) and min(bar) > 0:
                mint = float(cfg.get("mint", 10000))
                print(f"\n  To place you need to beat {min(bar):+,.2f} POLF, "
                      f"{min(bar) / mint * 100:.1f}% on the {mint:,.0f} mint.")
                print("  A key that never trades scores exactly 0, which does not place "
                      "while\n  any three keys are positive.")

    # Settled: the referee posts one `standings` record carrying the closing price,
    # the paid places and its own conservation check. That record, not the running
    # mark-to-market board above, is the result.
    standings = [q for q in referee_posts("d-close1-pnl", limit=4)
                 if q.get("t") == "standings"]
    if standings:
        final = standings[-1]
        print("\nsettled:")
        print(f"  closing price S        {final.get('S')}")
        print(f"  owners at settlement   {final.get('owners'):,}"
              if isinstance(final.get("owners"), int)
              else f"  owners at settlement   {final.get('owners')}")
        print(f"  total fees             {final.get('fees')} POLF")
        print(f"  zero-sum check         {final.get('zero_sum')}")
        print(f"  record file            {final.get('file')}")
        places = final.get("places") or []
        for i, entry in enumerate(places, 1):
            if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                print(f"  place {i}  {float(entry[1]):+,.4f}  {entry[0]}")
        runners = final.get("next") or []
        if places and runners and isinstance(runners[0], (list, tuple)):
            gap = float(places[-1][1]) - float(runners[0][1])
            print(f"  margin to {len(places) + 1}th place  {gap:+,.4f} POLF")


def owner_text(did: str) -> str:
    """The exact registration message, compact and key-ordered as the rules show."""
    return '{"t":"owner","season":"%s","key":"%s"}' % (SEASON, did)


def cmd_register(args: argparse.Namespace) -> None:
    if not args.allow_host:
        require_expected_host()
    cfg = load_config()
    now = dt.datetime.now(dt.timezone.utc)
    require_live(cfg, now)

    did = read_did()
    text = owner_text(did)
    n = sweep_now(cfg, now)

    print(f"did    {did}")
    print(f"room   {cfg['rooms']['trading'][0]}")
    print(f"text   {text}")
    print(f"signs  <room>|<nonce>|<text>   (Ed25519, base64url, 86 chars)")
    print(f"sweep  posting now lands in sweep {n}; the mint is issued by sweep {n + 1}, "
          f"about {sweep_time(cfg, n + 1).isoformat(timespec='seconds')}")

    if RECORD.exists():
        prior = json.loads(RECORD.read_text())
        print(f"\nAlready registered once: seq {prior.get('seq')} at {prior.get('ts_local')}.")
        print("One mint per key, so a second post adds nothing. Run `verify` instead.")
        if not args.again:
            return
        print("--again given; posting anyway.")

    if not args.yes:
        print("\nDry run. Nothing was signed or sent. Re-run with --yes to post.")
        return

    room = cfg["rooms"]["trading"][0]
    ta = agent()
    priv = ta.load_private(args)
    if ta.did_from_public(priv.public_key()) != did:
        sys.exit("identity.pem does not match did.txt")

    rec = ta.signed_say(priv, did, room, text)
    RECORD.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(rec, ensure_ascii=False, indent=1))
    if rec.get("server_verified"):
        print(f"\nposted and attributed to your DID — seq {rec['seq']} in /r/{room}")
        print(f"  {rec['permalink']}")
        print(f"\nSaved to {RECORD.name}. The room is a ring and old messages are dropped,")
        print("so this local record may outlive the message itself — keep it.")
        print(f"\nNext: wait for sweep {n + 1}, then run `python3 scripts/close1.py verify`.")
    else:
        print("\nposted, but the server did not attribute the record to your DID.")
        print("Do not assume you are registered. Check the response above.")
        sys.exit(1)


def referee_posts(room: str, limit: int = 20) -> list[dict]:
    """The referee's own posts in one of its five rooms, newest last.

    Only the referee can write to these rooms, so the text is its JSON. Anything
    that does not parse as the referee's shape is skipped rather than shown.
    """
    status, raw, _ = get(f"/r/{room}?limit={limit}&format=json")
    if status != 200:
        print(f"  {room}: fetch failed ({status})")
        return []
    try:
        view = json.loads(raw)
    except json.JSONDecodeError:
        print(f"  {room}: response was not JSON")
        return []
    out = []
    for item in view.get("messages", view.get("records", [])) or []:
        text = item.get("text", "")
        if not text.startswith("{"):
            continue
        try:
            out.append(json.loads(text))
        except json.JSONDecodeError:
            continue
    return out


def cmd_verify(args: argparse.Namespace) -> None:
    cfg = load_config()
    now = dt.datetime.now(dt.timezone.utc)
    did = read_did()
    print(f"did    {did}")
    print(f"sweep  {sweep_now(cfg, now)} of {cfg.get('lock_sweep', '?')}")
    if RECORD.exists():
        prior = json.loads(RECORD.read_text())
        print(f"local  registered seq {prior.get('seq')} at {prior.get('ts_local')}")
    else:
        print("local  no close1-record.json — this key has not registered from here")

    print("\nreferee rooms:")
    minted = False
    seen_any = False
    omitted_mints = False
    latest_flow = None
    for post in referee_posts("d-close1-flow", limit=args.limit):
        if post.get("t") != "flow":
            continue
        seen_any = True
        latest_flow = post
        mints = post.get("mints")
        if isinstance(mints, list) and did in mints:
            minted = True
            print(f"  d-close1-flow: MINTED at sweep {post.get('n')}")
        if isinstance(post.get("omitted"), dict) and "mints" in post["omitted"]:
            omitted_mints = True

    if latest_flow is not None:
        print(f"  d-close1-flow: latest sweep {latest_flow.get('n')}, "
              f"record file {latest_flow.get('file')}")
    for room in ("d-close1-state", "d-close1-pnl", "d-close1-positions"):
        posts = referee_posts(room, limit=4)
        if posts:
            seen_any = True
            # The last post in the pnl room after settlement is the standings
            # record, which carries no sweep number; report the last sweep post.
            swept = [q for q in posts if q.get("n") is not None]
            last = swept[-1] if swept else posts[-1]
            tail = (" (+ the standings record)"
                    if any(q.get("t") == "standings" for q in posts) else "")
            print(f"  {room}: latest sweep {last.get('n')}{tail}")
            top = last.get("top")
            if isinstance(top, list) and any(did in str(entry) for entry in top):
                print(f"    this key appears in {room}'s top list")

    # The standings record cannot confirm a mint, but it can settle the one
    # question that matters most to an individual: did this key place?
    standings = [q for q in referee_posts("d-close1-pnl", limit=4)
                 if q.get("t") == "standings"]
    if standings:
        final = standings[-1]
        places = final.get("places") or []
        runners = final.get("next") or []
        print(f"\nsettled at S = {final.get('S')}:")
        rank = None
        for i, entry in enumerate(places, 1):
            if isinstance(entry, (list, tuple)) and entry and entry[0] == did:
                rank = i
                print(f"  THIS KEY PLACED {i} with {float(entry[1]):+,.4f} POLF")
        if rank is None:
            for i, entry in enumerate(runners, len(places) + 1):
                if isinstance(entry, (list, tuple)) and entry and entry[0] == did:
                    rank = i
                    print(f"  this key is {i} with {float(entry[1]):+,.4f} POLF — "
                          f"ranked, not paid")
        if rank is None:
            print(f"  this key is not among the {len(places)} paid places nor the "
                  f"{len(runners)} published runners-up.")
            print("  That is conclusive for the prize and says nothing about the mint:")
            print("  the standings record names only the top of the board.")
        elif rank <= len(places):
            print(f"  Claim by signing a mainnet address with this key within "
                  f"{load_config().get('claim_window_days', 90)} days of launch.")
            print("  Sign on this machine. Do not move the key.")

    print()
    if minted:
        print("CONFIRMED: the referee's flow room names this key among its mints.")
    elif not seen_any:
        print("CANNOT CONFIRM: no referee posts were readable. Not evidence either way.")
    elif omitted_mints:
        print("CANNOT CONFIRM, and not because of this key: the referee's flow posts")
        print("carry an `omitted` field listing `mints` among the lists they truncate, so")
        print("the mint roster is not in the posts at all. It exists only inside the")
        print(f"archive record (latest file {(latest_flow or {}).get('file')}), and that")
        print("archive is the subject of open issues #19 and #25. There is currently no")
        print("published way for a participant to confirm their own mint — which is")
        print("issue #17, filed by someone in exactly this position.")
        print("\nYour evidence is your own signed record: the post's seq, nonce and")
        print("signature in close1-record.json verify against your DID without the")
        print("referee's cooperation. Keep it; the room is a ring and drops old messages.")
    else:
        print("NOT CONFIRMED: the referee posted, but no mint for this key was found in")
        print("the sweeps read, and the posts did not say the mints list was omitted.")
        print("Widen the window with --limit before concluding anything.")


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(
        prog="close1", description="close-1 registration and verification"
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="time to lock, current sweep, rooms listed")
    s.set_defaults(func=cmd_status)

    r = sub.add_parser("register", help="post the signed owner message (needs --yes)")
    r.add_argument("--yes", action="store_true", help="actually sign and post")
    r.add_argument("--again", action="store_true", help="post even if already registered")
    r.add_argument("--allow-host", action="store_true",
                   help="permit a TECHNOCORE_URL other than technocore.chat")
    r.add_argument("--passphrase-file", help="read the key passphrase from this file")
    r.set_defaults(func=cmd_register)

    v = sub.add_parser("verify", help="ask the referee whether this key was minted")
    v.add_argument("--limit", type=int, default=50, help="sweeps of flow to read")
    v.set_defaults(func=cmd_verify)

    args = p.parse_args(argv)
    try:
        args.func(args)
    except urllib.error.URLError as e:
        sys.exit(f"network error: {e}")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
