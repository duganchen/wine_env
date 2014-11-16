function mkbottle {

	case $# in
	1)
		mkdir -p $HOME/.local/share/wineprefixes/$1/bin

		mkrunner $1 > $HOME/.local/share/wineprefixes/$1/bin/wine
		chmod +x $HOME/.local/share/wineprefixes/$1/bin/wine

		mkopener $1 > $HOME/.local/share/wineprefixes/$1/bin/uncork
		source $HOME/.local/share/wineprefixes/$1/bin/uncork
		;;

	2)
		if [ -x $2 ]; then
			mkdir -p $HOME/.local/share/wineprefixes/$1/bin

			mkrunner --wine $2 $1 > $HOME/.local/share/wineprefixes/$1/bin/wine
			chmod +x $HOME/.local/share/wineprefixes/$1/bin/wine

			mkopener --wine $2 $1 > $HOME/.local/share/wineprefixes/$1/bin/uncork
			source $HOME/.local/share/wineprefixes/$1/bin/uncork

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


function bottle {

	case $# in
	1)
		if [ -f $HOME/.local/share/wineprefixes/$1/bin/uncork ]; then
			source $HOME/.local/share/wineprefixes/$1/bin/uncork
			cd $HOME/.local/share/wineprefixes/$1
		else
			echo Invalid prefix
		fi
		;;
	*)
		echo bottle BottleName
		echo e.g. bottle PvZ
		;;

	esac
}
