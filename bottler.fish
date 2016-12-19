function _bottler_help
	printf "bottle BottleName [/path/to/wine]
	e.g. bottle PvZ
	e.g. bottle PvZ ~/wine-1.7.30/bin/wine"
end

function bottle

	switch (count $argv)
		case 1
			if echo $argv[1] | egrep -q '^[A-Za-z0-9]+$'
				mkdir -p $HOME/.local/share/wineprefixes/$argv[1]/bin

				mkuncorkrc $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish
				mkcorkrc $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/corkrc.fish
				mkrunrc $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/runrc.fish
				source $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish
			else
				_bottler_help
			end
		case 2
			if echo $argv[1] | egrep -q '^[A-Za-z0-9]+$'
				if [ -x $argv[2] ]
					mkdir -p $HOME/.local/share/wineprefixes/$argv[1]/bin

					mkuncorkrc --wine $argv[2] $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish
					mkcorkrc --wine $argv[2] $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/corkrc.fish
					mkrunrc --wine $argv[2] $argv[1] > $HOME/.local/share/wineprefixes/$argv[1]/bin/runrc.fish
					source $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish
				end
			else
				_bottler_help
			end
		case '*'
			_bottler_help

	end
end


function uncork

	switch (count $argv)
		case 1
			if [ -f $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish ]
				source $HOME/.local/share/wineprefixes/$argv[1]/bin/uncorkrc.fish
			else
				echo Invalid prefix
			end
		case '*'
			echo uncork BottleName
			echo e.g. uncork PvZ
	end
end


function lsp
	ls $argv "$HOME/.local/share/wineprefixes"
end

# Tab completions

function __bottles
	set cmd (commandline -opc)
	if test (count $cmd) -eq 1
		for prefix in $HOME/.local/share/wineprefixes/*
			if test -f $prefix/bin/uncorkrc.fish
				basename $prefix
			end
		end
	end
end

complete -e -c bottle
complete -c bottle --no-files --arguments "(__bottles)"

complete -e -c bottle-run
complete -c bottle-run --no-files --arguments "(__bottles)"

complete -e -c uncork
complete -c uncork --no-files --arguments "(__bottles)"
