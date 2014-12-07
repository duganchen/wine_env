bottle() {

	case $# in
	(1)
		mkdir -p "$HOME/.local/share/wineprefixes/$1/bin"

		mkuncorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
		mkcorkrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/corkrc.sh"
		mkrunrc "$1" > "$HOME/.local/share/wineprefixes/$1/bin/runrc.sh"
		. "$HOME/.local/share/wineprefixes/$1/bin/uncorkrc.sh"
		;;

	(2)
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
		echo bottle BottleName \[/path/to/wine\]
		echo e.g. bottle PvZ
		echo e.g. bottle PvZ ~/Software/wine-1.7.30/bin/wine
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


_bottles() {
	for prefix in "$HOME"/.local/share/wineprefixes/*/; do
		basename "$prefix"
	done
}

_bash_completion() {
	COMPREPLY=()
	if [ $COMP_CWORD = 1 ]; then
		COMPREPLY=( $( compgen -W "$( _bottles )" -- "${COMP_WORDS[COMP_CWORD]}" ) )
	fi
}

_zsh_completion() {
	if (( CURRENT == 2 )); then
		compadd $( _bottles )
	fi
	return 0
}

if [ -n "$BASH" ]; then
	complete -F _bash_completion uncork
	complete -F _bash_completion bottle-run
fi

if [ -n "$ZSH" ]; then
	compdef _zsh_completion uncork
	compdef _zsh_completion bottle-run
fi


