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

complete -e -c bottle-run
complete -c bottle-run --no-files --arguments "(__bottles)"

complete -e -c uncork
complete -c uncork --no-files --arguments "(__bottles)"
