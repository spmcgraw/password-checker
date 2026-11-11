# Password Checker

A command-line tool that reads the login passwords stored in a [Proton Pass](https://proton.me/pass) vault and checks each one against the [Have I Been Pwned](https://haveibeenpwned.com/Passwords) "Pwned Passwords" database to see whether it has appeared in a known data breach.

> **Your passwords never leave your machine.** Each password is hashed locally with SHA-1, and only the first 5 characters of the hash are sent to the Pwned Passwords API. The match is done locally against the list it returns. This is the API's [k-anonymity](https://haveibeenpwned.com/API/v3#PwnedPasswords) model.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- [Proton Pass CLI](https://proton.me/pass) (`pass-cli`) installed and signed in
- The [`requests`](https://requests.readthedocs.io/) library (see the note under [Known limitations](#known-limitations))

## Usage

From this directory:

```bash
uv run passwordchecker
```

For each login in the vault, the tool prints one of:

```
<password> for <title> was found <n> times... you should probably change your password
<password> was NOT found. Carry on!
```

## Project layout

```
passwordChecker/
├── pyproject.toml
└── src/passwordchecker/
    └── main.py      # Proton Pass access, HIBP lookup, CLI entry point
```

## Roadmap

- [ ] Stop printing passwords in plaintext; report only the item title and breach count
- [ ] Declare `requests` in `pyproject.toml` (`uv add requests`); a fresh install currently fails without it
- [ ] Make the vault name configurable (currently hard-coded to `Personal` in `main()`)
- [ ] Check more item types than `login`
- [ ] Add tests

## Security notes

- **The current output prints each password in plaintext.** Run the tool only in a private terminal, and don't share or log its output (fixing this is the first roadmap item).
- Passwords are read from Proton Pass at runtime and are never written to disk by this tool.
- A match means the password has appeared in a breach somewhere, not that your account was compromised. Change any matched password, and don't reuse it.
