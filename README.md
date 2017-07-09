# pastebin-mirror

Mirror [Pastebin.com](https://pastebin.com) to a local SQLite database or flat text files. Archives all new and trending pastes in real-time.

## Getting Started

### Archive Trending

To archive only the 18 trending posts each hour you need an API Key from pastebin. This is free but does require creating an account with pastebin. Once you've registered, you can find your API key [here](https://pastebin.com/api).

### Archive All New

Archiving all pastes in real-time requires a PRO LIFETIME account ($50 one-time payment). Once you purchase a PRO LIFETIME account, you must [whitelist](https://pastebin.com/api_scraping_faq) your [public IP address](http://whatismyip.org/) (strangely, you do not need an API key to archive all new posts). Once that is done, you should be free to use this tool for life, or more realistically, as long as pastebin is still kickin'.

### Download

```bash
# download
git clone https://github.com/brannondorsey/pastebin-mirror
cd pastebin-mirror

# run in "full" mode, archiving all new AND trending pastes to pastebin.db 
python3 pastebin-mirror --output pastebin.db --trending --api-key <YOUR_API_KEY>
```

## Download Only Trending Pastes

You can download only trending pastes without a PRO LIFETIME account like so:

```bash
python3 pastebin-mirror --output pastebin.db --no-mirror --trending --api-key <YOUR_API_KEY>
```

## Dowload Only New Pastes

Inversely, omitting the `--trending` flag only downloads new pastes (`--mirror` is enabled by default). In this mode you may omit the `--api-key` flag:

```bash
python3 pastebin-mirror --output pastebin.db
```

## Saving Pastes as Flat Text Files

Pastes can optionally be saved as raw text files instead of to an SQLite database. To do this, simply run `pastebin-mirror` with the `--output-format flat-file` option. When output format is `flat-file`, `--output` is interpreted as a directory path instead of a database file. Pastes are saved in the output directory like `PASTE_ID.txt`, where `PASTE_ID` is the unique ID assigned to the paste by pastebin (e.g. `output_directory/0eBX2nS3.txt`).

When using flatfile output a `metadata/` folder is created in the output directory. Information about each paste is included in this folder, saved with identical basenames to the raw paste content in the output directory.

Contents of `output_directory/metadata/0eBX2nS3.txt`:
```
key: 0eBX2nS3
timestamp: 1499615402
size: 5079
expires: 0
title: Doom-Mates: Indigestion
syntax: text
user: Protom
``` 

If `pastebin-mirror` is called with the `--trending` option, trending pastes will be saved inside of `output_directory/trending`. Information about trending pastes are also included in `output_directory/metadata`.

## Output to `stdout` and `stderr`

`pastebin-mirror` outputs the paste ids of successfully downloaded pastes to `stdout` only. All additional/noisy info logging is output to `stderr`. This means that you can reliably use `pastebin-mirror` as a tool in a larger pipeline, triggering some event when pastes are downloaded.

### Output `stdout` Only

```bash
$ python3 pastebin-mirror --output-format flat-file --output pastebin 2>/dev/null
mUzadurz
BiqtCmKW
SCG7eBRk
G758hYSR
pQTcXyNg
BUxnxESb
V7LTSvan
Geu3cuEH
XJGib81F
GkYJ9WvT
TgCpcF6S
PecJnApM
jt7Dym1j
rv9FMc7P
```

### Output `stderr` Only 

```bash
$ python3 pastebin-mirror --output-format flat-file --output test 1>/dev/null
[*] Fetching 11 new pastes
[*] Waiting 30 seconds before next paste scrape
[*] Fetching 17 new pastes
[*] Waiting 30 seconds before next paste scrape
[*] Fetching 20 new pastes
[*] Waiting 30 seconds before next paste scrape
[!] Interrupted by user, exiting
```

## Usage

```
usage: pastebin-mirror [-h] -o OUTPUT [-f {sqlite,flat-file}] [-r RATE] [-t]
                       [-m] [-n] [-k API_KEY] [-v]

Pastebin mirror tool. Save publicly uploaded pastes in real-time to an SQLite
database or as flat text files. Optionally archive trending pastes as well.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output SQLite database file or directory name if
                        --output-format=flat-file
  -f {sqlite,flat-file}, --output-format {sqlite,flat-file}
                        output format
  -r RATE, --rate RATE  seconds between requests to the pastebin scrape API.
                        minimum 1 second.
  -t, --trending        archive trending pastes (runs once per hour)
  -m, --mirror          archive pastebin in real-time using the scrape API.
                        Requires a PRO LIFETIME account to whitelist your IP
                        address.
  -n, --no-mirror       do not archive pastebin using the scrape API.
  -k API_KEY, --api-key API_KEY
                        pastebin API key. only required with --trending option
  -v, --version         show program's version number and exit

```

## License and Attribution

This software is free to use under the terms of the [MIT license](LICENSE).

The original `paste-mirror` (version `0.0.1`) was written by [James Ward](https://github.com/imnotjames). Version `1.0.0` is a major overhaul authored by [Brannon Dorsey](https://github.com/brannondorsey). See the [CHANGELOG](CHANGELOG.md) for changes.
