# BASH autocompletion for wine_env.

_bash_completion() {
	COMPREPLY=()
	if (( $COMP_CWORD == 1 )); then
		COMPREPLY=( $( compgen -W "$( _bottles )" -- "${COMP_WORDS[COMP_CWORD]}" ) )
	fi
}

complete -F _bash_completion uncork
complete -F _bash_completion bottle-run
complete -F _bash_completion bottle
