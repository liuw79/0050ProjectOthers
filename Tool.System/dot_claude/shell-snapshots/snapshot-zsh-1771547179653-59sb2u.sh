# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
cimg () {
	local dir="$HOME/Desktop/claude-images" 
	mkdir -p "$dir"
	local file="$dir/$(date +%Y%m%d_%H%M%S).png" 
	if pngpaste "$file" 2> /dev/null
	then
		echo "$file"
	else
		echo "剪贴板没有图片"
		rm -f "$file"
	fi
}
pimg () {
	local tmp="/tmp/clipboard-image-$$.png" 
	if pngpaste "$tmp" 2> /dev/null
	then
		kitty +kitten icat "$tmp"
		rm "$tmp"
	else
		echo "剪贴板没有图片"
	fi
}
z () {
	__zoxide_z "$@"
}
zi () {
	__zoxide_zi "$@"
}
# Shell Options
setopt nohashdirs
setopt login
# Aliases
alias -- icat='kitty +kitten icat'
alias -- run-help=man
alias -- which-command=whence
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  alias rg='/Users/comdir/SynologyDrive/0050Project/Tool.System/local-tools/lib/node_modules/\@anthropic-ai/claude-code/vendor/ripgrep/arm64-darwin/rg'
fi
export PATH=/Users/comdir/SynologyDrive/0050Project/Tool.System/local-tools/bin\:/Users/comdir/.npm-global/bin\:/opt/homebrew/opt/postgresql\@15/bin\:/opt/homebrew/bin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin\:/opt/pmk/env/global/bin\:/opt/homebrew/bin\:/Applications/Ghostty.app/Contents/MacOS
