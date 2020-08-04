# Digitools
Digitools is a collection of tools intended to help Elektron Digitakt/Digitone users.

Currently, the only functionality provided is viewing and modifying basic Digitone sound information (i.e. name and tags)

With this tool you can ...
- List the name and tags of sounds in a Digitone SysEx file
- Export the name and tags of sounds in a Digitone SysEx file to a CSV file
- Update name and tags of sounds in a Digitone SysEx file from a CSV file

The combination of these capabilities provides a faster and easier way to rename and tag Digitone sounds outside the hardware itself.

Here is what the workflow would look like:
1. Export a SysEx dump of the sound bank you want to edit from Digitone
2. Export the information from the SysEx file to a CSV file using Digitools
3. Open the CSV file with a spreadsheet application (e.g. Excel) and modify sound names and tags
4. Apply the data in the CSV file back to the SysEx file using Digitools
5. Finally, import the updated SysEx file back into Digitone

Although there are multiple steps involved, most are straightforward and quick steps that can be performed in a matter of seconds. Moreover, the additional steps are well worth taking given they only need to be done once for each bank.

Other possible usages of the tool include:
- Printing a catalog of your sounds and using it as a reference
- Renaming all sounds in a Sound Pack to add a prefix for easy identification
- Correcting obvious tagging errors in Sound Packs before installing them (e.g. I have seen sounds in packs that have the __MINE__ tag)

## Installation
There are many different ways to distribute and install Python libraries and applications. The approach I've outlined below is what I believe is the best option for most users. Those who are familiar with Python or technically inclined may choose a different approach that better suits them.

### Step 1: Install _Python_
If you don't already have a recent version of Python (3.6+) installed, follow the links below to install/upgrade your Python.

__Windows / macOS:__<br>
Download and install the latest release for your OS from [here](https://www.python.org/downloads)

__macOS__:<br>
If you use _Homebrew_ (you should, it's great), I recommend installing Python using the [Homebrew Python formula](https://docs.brew.sh/Homebrew-and-Python) by executing this command:<br>
```
brew python
```

Otherwise, download and install the latest release for your OS from [here](https://www.python.org/downloads)

__Note:__
Depending on how python is installed and setup on your system, you may need to use `python3` and `pip3` instead of the `python` and `pip` commands shown below. The installation process should provide this information.

### Step 2: Install _pipx_
If you would like to learn what _pipx_ is and what it's good for please see: [Installing stand alone command line tools](https://packaging.python.org/guides/installing-stand-alone-command-line-tools) and [pipxproject / pipx](https://github.com/pipxproject/pipx)

Here are the commands I use to install and configure _pipx_, which are slightly different from those listed on the above pages. Both would work.
```
pip install pipx
pipx ensurepath
```

### Step 3: Install _digitools_ using _pipx_
Once you have both _Python_ and _pipx_ set up, you can install _digitools_ using _pipx_.

First, download the `.whl` file from the release assets (choose the latest release to view the included assets).

Next, simply execute the following command, replacing `<path>` with the actual path to where you downloaded the file:
```
pipx install <path>
```

## Basic Usage
To see a list of available commands:
```
digitools -h
```

To see more detailed information about the export command:
```
digitools export -h
```

To list the sounds in a SysEx file:
```
digitools print data/sounds.syx
```

To export the sounds in a SysEx file to a CSV file:
```
digitools export data/sounds.syx data/sounds.csv
```

To update sounds in a SysEx file from a CSV file:
```
digitools update data/sounds.syx data/sounds.csv
```

## Acknowledgment
This project has benefited immensely from the [libdigitone](https://gitlab.com/dhuck/libdigitone) project, and builds on the research and findings of its author.