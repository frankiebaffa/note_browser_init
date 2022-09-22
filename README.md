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

The file located [here](./note_browser_init.py) will generate `index.md` files
inside every directory containing markdown files. This `index.md` file will
contain links for all nested directories and files. It will also generate a
*Description* section if the directory contains a `description.md` file. It
generates a document header on each `.md` file containing a fully-linked path
from the root to the document as well as the document name.

**Before running script**

[![Markdown viewer no navigation][no_nav]][no_nav]

**After running script**

[![Markdown viewer with navigation][nav]][nav]

## Example<span id="root-example"></span>

```bash
cd "$YOUR_NOTES_DIR"
/path/to/./note_browser_init.py --path "$PWD"
```

[no_nav]: readme/note_browser_no_nav.png
[nav]: readme/note_browser_nav.png
