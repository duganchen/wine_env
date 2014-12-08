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


if [ -n "$BASH" ]; then
	. "$( dirname $( realpath "${BASH_SOURCE[0]}" ) )/wine_env_complete.sh"
elif [ -n "$ZSH" ]; then
	. "$( dirname $( realpath "$0" ) )/wine_env_complete.sh"
fi
