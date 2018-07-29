if functions -q cork
	cork
end

function cork

	if set -q _OLD_WINEVERPATH
		set -gx WINEVERPATH $_OLD_WINEVERPATH
		set -e _OLD_WINEVERPATH
	else
		set -e WINEVERPATH
	end

	if set -q _OLD_PATH
		set -gx PATH $_OLD_PATH
		set -e _OLD_PATH
	end

	if set -q _OLD_WINESERVER
		set -gx WINESERVER $_OLD_WINESERVER
		set -e _OLD_WINESERVER
	else
		set -e WINESERVER
	end

	if set -q _OLD_WINELOADER
		set -gx WINELOADER $_OLD_WINELOADER
		set -e _OLD_WINELOADER
	else
		set -e WINELOADER
	end

	if set -q _OLD_WINEDLLPATH
		set -gx WINEDLLPATH $_OLD_WINEDLLPATH
		set -e _OLD_WINEDLLPATH
	else
		set -e WINEDLLPATH
	end

	if set -q _OLD_LD_LIBRARY_PATH
		set -gx LD_LIBRARY_PATH $_OLD_LD_LIBRARY_PATH
		set -e _OLD_LD_LIBRARY_PATH
	else
		set -e LD_LIBRARY_PATH
	end

	if set -q _OLD_WINEPREFIX
		set -gx WINEPREFIX $_OLD_WINEPREFIX
		set -e _OLD_WINEPREFIX
	else
		set -e WINEPREFIX
	end

	if set -q W
		set -e W
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

function goc
	cd $WINEPREFIX/drive_c
end
