# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
__zoxide_cd () {
	\builtin cd -- "$@"
}
__zoxide_doctor () {
	[[ ${_ZO_DOCTOR:-1} -ne 0 ]] || return 0
	[[ ${chpwd_functions[(Ie)__zoxide_hook]:-} -eq 0 ]] || return 0
	_ZO_DOCTOR=0 
	\builtin printf '%s\n' 'zoxide: detected a possible configuration issue.' 'Please ensure that zoxide is initialized right at the end of your shell configuration file (usually ~/.zshrc).' '' 'If the issue persists, consider filing an issue at:' 'https://github.com/ajeetdsouza/zoxide/issues' '' 'Disable this message by setting _ZO_DOCTOR=0.' '' >&2
}
__zoxide_hook () {
	\command zoxide add -- "$(__zoxide_pwd)"
}
__zoxide_pwd () {
	\builtin pwd -L
}
__zoxide_z () {
	__zoxide_doctor
	if [[ "$#" -eq 0 ]]
	then
		__zoxide_cd ~
	elif [[ "$#" -eq 1 ]] && {
			[[ -d "$1" ]] || [[ "$1" = '-' ]] || [[ "$1" =~ ^[-+][0-9]+$ ]]
		}
	then
		__zoxide_cd "$1"
	elif [[ "$#" -eq 2 ]] && [[ "$1" = "--" ]]
	then
		__zoxide_cd "$2"
	else
		\builtin local result
		result="$(\command zoxide query --exclude "$(__zoxide_pwd)" -- "$@")"  && __zoxide_cd "${result}"
	fi
}
__zoxide_zi () {
	__zoxide_doctor
	\builtin local result
	result="$(\command zoxide query --interactive -- "$@")"  && __zoxide_cd "${result}"
}
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
  alias rg='/Users/comdir/SynologyDrive/0050Project/others/Tool.System/local-tools/lib/node_modules/\@anthropic-ai/claude-code/vendor/ripgrep/arm64-darwin/rg'
fi
export PATH=/Users/comdir/.local/bin\:/Users/comdir/SynologyDrive/0050Project/others/Tool.System/local-tools/bin\:/Users/comdir/.npm-global/bin\:/opt/homebrew/opt/postgresql\@15/bin\:/opt/homebrew/bin\:/usr/local/bin\:/System/Cryptexes/App/usr/bin\:/usr/bin\:/bin\:/usr/sbin\:/sbin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin\:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin\:/opt/pmk/env/global/bin\:/opt/homebrew/bin\:/Applications/Ghostty.app/Contents/MacOS
