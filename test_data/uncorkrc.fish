if functions -q cork
	cork
end

function cork
	source $HOME/.local/share/wineprefixes/bottle/bin/corkrc.fish
	cd "$_OLD_PWD"
		set -e _OLD_PWD
	if set -q W		set -e W
	end
	if set -q BOTTLE
		set -e BOTTLE
	end
	functions -e goc
	functions -e cork
end

if test -n "$WINEVERPATH"
	if not set -q _OLD_WINEVERPATH
		set -gx _OLD_WINEVERPATH $WINEVERPATH	
	end
end
if test -n "$PATH"
	if not set -q _OLD_PATH
		set -gx _OLD_PATH $PATH	
	end
end
if test -n "$WINESERVER"
	if not set -q _OLD_WINESERVER
		set -gx _OLD_WINESERVER $WINESERVER	
	end
end
if test -n "$WINELOADER"
	if not set -q _OLD_WINELOADER
		set -gx _OLD_WINELOADER $WINELOADER	
	end
end
if test -n "$WINEDLLPATH"
	if not set -q _OLD_WINEDLLPATH
		set -gx _OLD_WINEDLLPATH $WINEDLLPATH	
	end
end
if test -n "$LD_LIBRARY_PATH"
	if not set -q _OLD_LD_LIBRARY_PATH
		set -gx _OLD_LD_LIBRARY_PATH $LD_LIBRARY_PATH	
	end
end
if test -n "$WINEPREFIX"
	if not set -q _OLD_WINEPREFIX
		set -gx _OLD_WINEPREFIX $WINEPREFIX	
	end
end
set -gx WINEPREFIX $HOME/.local/share/wineprefixes/bottle

set -gx _OLD_PWD $PWD
cd $HOME/.local/share/wineprefixes/bottle

function goc
	cd $WINEPREFIX/drive_c
end
