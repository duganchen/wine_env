# BASH and ZSH autocompletion for wine_env.
# This file should be sourced by bottler.sh.

_bottles() {
	for prefix in "$HOME"/.local/share/wineprefixes/*/; do
		if [[ -f "$prefix/bin/uncorkrc.sh" ]]; then
			basename "$prefix"
		fi
	done
}

_bash_completion() {
	COMPREPLY=()
	if (( $COMP_CWORD == 1 )); then
		COMPREPLY=( $( compgen -W "$( _bottles )" -- "${COMP_WORDS[COMP_CWORD]}" ) )
	fi
}

_zsh_completion() {
	if (( CURRENT == 2 )); then
		compadd $( _bottles )
	fi
	return 0
}

if [[ -n "$BASH" ]]; then
	complete -F _bash_completion uncork
	complete -F _bash_completion bottle-run
	complete -F _bash_completion bottle
fi

if [[ -n "$ZSH" ]]; then
	compdef _zsh_completion uncork
	compdef _zsh_completion bottle-run
	compdef _zsh_completion bottle
fi
