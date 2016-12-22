_bottler_help() {
	cat <<- EOF
	bottle BottleName [/path/to/wine]
	e.g. bottle PvZ
	e.g. bottle PvZ ~/wine-1.7.30/bin/wine
	EOF
}

bottle() {

	case $# in
	(1)
		if echo "$1" | egrep -q "^[A-Za-z0-9]+$"; then
			mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

			mkuncorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
			mkcorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.sh"
			mkrunrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.sh"
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"

			mkuncorkrc_fish "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.fish"
			mkcorkrc_fish "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.fish"
			mkrunrc_fish "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.fish"
		else
			_bottler_help
		fi
		;;

	(2)
		if echo "$1" | egrep -q "^[A-Za-z0-9]+$" && [ -x $2 ]; then
			mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

			mkuncorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
			mkcorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.sh"
			mkrunrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.sh"
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"

			mkuncorkrc_fish --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.fish"
			mkcorkrc_fish --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.fish"
			mkrunrc_fish --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.fish"
		else
			_bottler_help
		fi
		;;
	(*)
		_bottler_help
		;;

	esac
}


uncork() {

	case $# in
	(1)
		if [ -f "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh" ]; then
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
		else
			echo Invalid prefix
		fi
		;;
	(*)
		echo uncork BottleName
		echo e.g. uncork PvZ
		;;

	esac
}


lsp() {
	ls $* "$HOME/.local/share/wineprefixes"
}


# Used by the autocompletion scripts.
_bottles() {
	for prefix in "$HOME"/.local/share/wineprefixes/*/; do
		if [[ -f "$prefix/bin/uncorkrc.sh" ]]; then
			basename "$prefix"
		fi
	done
}

