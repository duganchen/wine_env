# ZSH autocompletion for wine_env.

_zsh_completion() {
	if (( CURRENT == 2 )); then
		compadd $( _bottles )
	fi
	return 0
}

compdef _zsh_completion uncork
compdef _zsh_completion bottle-run
compdef _zsh_completion bottle
