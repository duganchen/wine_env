bottle() {

	case $# in
	1)
		mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

		mkuncorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
		mkcorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.sh"
		mkrunrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.sh"
		. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
		;;

	2)
		if [ -x $2 ]; then
			mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

			mkuncorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
			mkcorkrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.sh"
			mkrunrc --wine "$2" "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.sh"
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"

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
		if [ -f "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh" ]; then
			. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
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
