# wine_env

This is a command-line system to manage your Wine installations and Wine
bottles.

## Installation

Install it the way you would any Python application:

	python setup.py install

Then source /usr/bin/bottle.sh to activate it.

## Usage

For the following example, let's say that you have Wine 1.7.31 installed as
follows:

	./configure --prefix=~/wine-1.7.31
	make
	make install

Let's also say that you want to run the Diablo 3 installer, which you have
downloaded as:

	~/Downloads/Diablo-III-Setup-enUS.exe

### Creating A Bottle

Use *bottle* to create a Wine bottle named D3, and have it use your Wine 1.7.31
build:

	bottle D3 ~/wine-1.7.31/bin/wine

Your prompt will now start with "(D3)", and your current directory to your new
Wine bottle:

	~/.local/share/wineprefixes/D3

### Installing Software

Now you can install Diablo 3:

	wine ~/Downloads/Diablo-III-Setup-enUS.exe

That will invoke your custom Wine build to install Diablo 3 into the D3 bottle.

### Exiting the Bottle

To exit the bottle environment and go back to your normal one, simply:

	cork

Your prompt will be back to normal, you'll be back in the directory you were
once in, and the "wine" command will now invoke the one normally in your PATH.

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

### Running Winetricks

To run Winetricks, I recommend passing it the --no-isolate flag from an
interactive bottle. To create a Bottle just for running Plants vs Zombies in
Steam, for example, do the following:

	bottle PvZ ~/wine-1.7.31
	winetricks --no-isolate steam

### Other Notes

If you create a bottle without specifying a Wine executable, then it will
simply use your system's default Wine:

	bottle winzip

If you ever want a bottle to contain a different version of Wine, simple use
*bottle* to create the bottle again. Only its initiation files will change.
