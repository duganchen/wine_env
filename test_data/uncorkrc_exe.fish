set W /path/to/wine-1.7.3

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

if test -n "$WINESERVERPATH"
	if not set -q _OLD_WINESERVERPATH
		set -gx _OLD_WINESERVERPATH $WINESERVERPATH	
	end
end
set -gx WINESERVERPATH $W
if test -n "$PATH"
	if not set -q _OLD_PATH
		set -gx _OLD_PATH $PATH	
	end
end
set -gx PATH $W/bin $PATH
if test -n "$WINESERVER"
	if not set -q _OLD_WINESERVER
		set -gx _OLD_WINESERVER $WINESERVER	
	end
end
set -gx WINESERVER $W/bin/wineserver
if test -n "$WINELOADER"
	if not set -q _OLD_WINELOADER
		set -gx _OLD_WINELOADER $WINELOADER	
	end
end
set -gx WINELOADER $W/bin/wine
if test -n "$WINEDLLPATH"
	if not set -q _OLD_WINEDLLPATH
		set -gx _OLD_WINEDLLPATH $WINEDLLPATH	
	end
end
set -gx WINEDLLPATH $W/lib/wine/fakedlls
if test -n "$LD_LIBRARY_PATH"
	if not set -q _OLD_LD_LIBRARY_PATH
		set -gx _OLD_LD_LIBRARY_PATH $LD_LIBRARY_PATH	
	end
end
set -gx LD_LIBRARY_PATH $W/lib $LD_LIBRARY_PATH
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
