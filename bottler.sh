uncork() {

	case $# in
	(1)
		if [ -f "$HOME/.config/wine_env/$1/uncorkrc.sh" ]; then
			. "$HOME/.config/wine_env/$1/uncorkrc.sh"
		else
			echo "Bottle $1 not found."
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

