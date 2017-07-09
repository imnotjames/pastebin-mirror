# Changelog

Original implementation by [James Ward](https://github.com/imnotjames). Overhaul, and support for archiving trending pastes and saving as flat text files by [Brannon Dorsey](https://github.com/brannondorsey).

## 1.0.0

- Add command-line arguments
- Optionally archive trending pastes
- Optional output to flat text files
- Improve logging (logs archived paste ids to `stdout` and info to `stderr`)
- Fix bug that saved timestamps as size and vice versa
- Fix bug that ignored database filename included as CLI argument
- Fix bug that where scraping API limit=250 was being ignored
- Add `CHANGELOG.md`
- Add substantial content to `README.md`

## 0.0.1

- Original implementation by [James Ward](https://github.com/imnotjames)
