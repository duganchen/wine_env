# wine_env

This is a command-line system to manage your installations of Wine and of
Wine software.

It's for shells with Bourne Shell syntax: bash, zsh, dash and ash.
Users of the fish shell can use [wine_env_fish](https://github.com/duganchen/wine_env_fish)
instead.

## Installation

Install it the way you would any Python application:

	python setup.py install

Then do the following to activate it:

	source /usr/bin/bottle.sh

If you're using bash or zsh, then also activate autocompletion:

	source /usr/bin/wine_env_complete.sh

## Usage

For the following example, let's say that you have Wine 1.7.31 installed as
follows:

	./configure --prefix=$HOME/wine-1.7.31
	make
	make install

Let's also say that you want to run the Diablo 3 installer, which you have
downloaded as:

	~/Downloads/Diablo-III-Setup-enUS.exe

Finally, note that Wine calls an isolated software installation (with its
own C drive, registry and DLL overrides) a *bottle*.

### Creating A Bottle

For Diablo 3, use the *bottle* command to create a Wine bottle named D3,
which will use your Wine 1.7.31 build:

	bottle D3 ~/wine-1.7.31/bin/wine

Creating a bottle automatically puts you in that *bottle environment*. Your
prompt will now start with "(D3)", and your current directory will be changed
to your new Wine bottle:

	~/.local/share/wineprefixes/D3

Running *wine* or *winecfg* from the D3 bottle environment will launch
version 1.7.31 of either tool. The WINEPREFIX variable will be set
so that they'll write to, and read from, the D3 bottle directory.

### Installing Software

Now you can install Diablo 3:

	wine ~/Downloads/Diablo-III-Setup-enUS.exe

That will invoke your custom Wine build to install Diablo 3 into the D3 bottle.

### Exiting the Bottle

To exit the bottle environment and go back to your normal one, simply:

	cork

That will restore your environment. Your prompt will be back to normal,
you'll be back in the directory you were once in, and the "wine" command
will now invoke the one normally in your PATH. WINEPREFIX will be
restored or cleared, as appropriate.

### Listing Bottles

You can list the bottles you've created with:

	lsp

This is the same command that winetricks recommends adding as a shortcut.

### Entering A Bottle

You can reenter the D3 bottle later with:

	uncork D3

### Switching to the C Drive

And when you're in the bottle, you can go to its C drive with:

	goc

This is another one recommended by Winetricks.

### Making A Launcher

If you want to add software to a menu, use *bottle-run*. On a 64-bit system,
Diablo 3's launch command is particulary hairy, but supported:

	setarch i386 -3 bottle-run D3 wine ~/.local/share/wineprefixes/D3/drive_c/Program\ Files/Diablo\ III/Diablo\ III.exe

### Editing Launchers

Wine, as normal part of software installation, installs menu items and desktop
icons. These need to be edited to use bottle-run.

For example, Diablo 3 installs the following desktop entry:

	$HOME/.local/share/applications/wine/Programs/Diablo\ III/Diablo\ III.desktop

It contains the following line:

	Exec=env WINEPREFIX="/home/dugan/.local/share/wineprefixes/D3" wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/dugan/.local/share/wineprefixes/D3/dosdevices/c:/users/Public/Start\\ Menu/Programs/Diablo\\ III/Diablo\\ III.lnk

Change the parts before "wine" so that it launches Diablo 3 in the D3 bottle:

	Exec=setarch i386 -3 bottle-run D3 wine C:\\\\windows\\\\command\\\\start.exe /Unix /home/dugan/.local/share/wineprefixes/D3/dosdevices/c:/users/Public/Start\\ Menu/Programs/Diablo\\ III/Diablo\\ III.lnk

The restart your desktop environment (log out and back in) so that it rereads the entry.

If there's a launcher on the desktop, you can edit it in the same way.

### Running Winetricks

To run Winetricks, I recommend passing it the --no-isolate flag from an
interactive bottle. To create a Bottle just for running Plants vs Zombies in
Steam, for example, do the following:

	bottle PvZ ~/wine-1.7.31
	winetricks --no-isolate steam

That will install Steam into the PvZ bottle.

### Other Notes

If you create a bottle without specifying a Wine executable, then it will
simply use your system's default Wine:

	bottle winzip

If you ever want a bottle to contain a different version of Wine, simple use
*bottle* to create the bottle again. The only files touched will be the
initialization files that wine_env's tools use when entering and exiting the
bottle.

Please regenerate your bottles whenever you upgrade wine_env.

If you don't want wine_env to modify the prompt, then do the following:

    export WINE_ENV_DISABLE_PROMPT=1

[Powerline](https://github.com/powerline/powerline) users can use my
[wine_env_powerline](https://github.com/duganchen/wine_env_powerline) project to integrate wine_env with Powerline.

