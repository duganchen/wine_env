mkbottle() {

	case $# in
	1)
		mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

		mkuncorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc"
		mkcorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc"
		mkrunrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc"
		. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc"
		;;

	2)
		if [ -x $2 ]; then
			mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

			mkuncorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc"
			mkcorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc"
			mkrunrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc"
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc"

		else
			echo /path/to/wine must be the path to a Wine execuable
		fi
		;;
	*)
		echo mkbottle BottleName \[/path/to/wine\]
		echo e.g. mkbottle PvZ
		echo e.g. mkbottle PvZ ~/Software/wine-1.7.30/bin/wine
		;;

	esac
}


uncork() {

	case $# in
	1)
		if [ -f "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc" ]; then
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc"
			cd "$HOME/.local/share/wineprefixes/$1"
		else
			echo Invalid prefix
		fi
		;;
	*)
		echo uncork BottleName
		echo e.g. uncork PvZ
		;;

	esac
}


lsp() {
	ls $* "$HOME/.local/share/wineprefixes"
}
