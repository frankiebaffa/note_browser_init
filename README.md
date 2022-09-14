# ReadMe

_ _ _

# ToC

- [Viewing](#root-viewing)
- [Index Generation](#root-index-generation)
- [Example](#root-example)

_ _ _

## Viewing<span id="root-viewing"></span>

The intended method of viewing these documents is through the
[Markdown Viewer](https://github.com/simov/markdown-viewer) browser plugin and
by navigating to the system file path in your web browser.

## Settings<span id="root-settings"></span>

The following settings for the **Markdown Viewer** are used for best viewing:

```json
{
	"THEME": {
		"dropdown1": "GITHUB-DARK",
		"wide_toggle": "OFF"
	},
	"COMPILER": {
		"dropdown1": "REMARK",
		"breaks_toggle": "OFF",
		"footnotes_toggle": "OFF",
		"gfm_toggle": "ON",
		"sanitize": "OFF"
	},
	"CONTENT": {
		"autoreload_toggle": "OFF",
		"emoji_toggle": "OFF",
		"mathjax_toggle": "OFF",
		"scroll_toggle": "ON",
		"toc_toggle": "OFF"
	}
```

Navigate to the details for the extension and find the option `Allow access to
file URLs` and toggle it to ON.

## Index Generation<span id="root-index-generation"></span>

The file located [here](./note_browser_init.py) will generate all of the
necessary `index.md` files throughout this repository. Re-running is only
necessary when new files are added.

## Example<span id="root-example"></span>

```bash
./note_browser_init.py --path /home/username/notes_directory
```

