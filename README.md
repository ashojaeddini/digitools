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

Although there are multiple steps involved, they are straight forward and quick steps that can be performed in a matter of seconds. Moreover, the additional steps are well worth it given that you just have to perfrom them once for an entire bank.

## Installation
Packaging the tool for easier consumption and installation is still in progress.

Manwhile, follow the steps below to use the tool:
1. Ensure Python 3.x is installed on your system
2. Downlowd the source code as an archive and unpack it
3. From the root source directory run the following command: `python digitone -h`

If you see the following help text, then you're all set.

    NAME
        digitone

    SYNOPSIS
        digitone COMMAND

    COMMANDS
        COMMAND is one of the following:

        print
        Prints the sounds in a SysEx file to the standard output.

        export
        Exports the sounds in a SysEx file to a CSV file.

        update
        Updates name and tags of sounds in a SysEx file from a CSV file.

Note that depending on how python is installed and setup on your system you may need to invoke Python using `python3` instead of `python`.

## Basic Usage
To see a list of available commands:
```
python digitone -h
```

To see more detailed information about the export command:
```
python digitone export -h
```

To list the sounds in a SysEx file:
```
python digitone print data/sounds.syx
```

To export the sounds in a SysEx file to a CSV file:
```
python digitone export data/sounds.syx data/sounds.csv
```

To update sounds in a SysEx file from a CSV file:
```
python digitone update data/sounds.syx data/sounds.csv
```

## Acknowledgment
This project has benefited immensely from the [libdigitone](https://gitlab.com/dhuck/libdigitone) project, and builds on the research and findings of its author.