import os

import click

from ftcli.Lib.Font import Font
from ftcli.Lib.utils import getFontsList, makeOutputFileName


@click.group()
def delAllNames():
    pass


@delAllNames.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   'name). By default, files are overwritten.')
def clean_nametable(input_path, output_dir, recalc_timestamp, overwrite):
    """Deletes all namerecords from the 'name' table.
    """

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            for name in font['name'].names:
                font.delNameRecord(nameID=name.nameID)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


@click.group()
def printLanguageCodes():
    pass


@printLanguageCodes.command()
def lang_help():
    """Prints available languages that can be used with the 'setname' and 'delname' commands
    """
    from fontTools.ttLib.tables._n_a_m_e import (_MAC_LANGUAGES, _WINDOWS_LANGUAGES)
    print('\n[WINDOWS LANGUAGES]')
    winlist = []
    for v in _WINDOWS_LANGUAGES.values():
        winlist.append(v)
    winlist.sort()
    print(winlist)
    print('\n[MAC LANGUAGES]')
    maclist = []
    for v in _MAC_LANGUAGES.values():
        maclist.append(v)
    maclist.sort()
    print(maclist)


@click.group()
def winToMac():
    pass


@winToMac.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   'name). By default, files are overwritten.')
def win_2_mac(input_path, output_dir, recalc_timestamp, overwrite):
    """Copies all namerecords from Windows table to Macintosh table.
    """

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.win2mac()
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


@click.group()
def deleteMacNames():
    pass


@deleteMacNames.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-ex', '--exclude-namerecord', type=click.IntRange(0, 32767), multiple=True,
              help="Name IDs to ignore. The specified name IDs won't be deleted. This option can be repeated "
                   "(example: -ex 3 -ex 5 -ex 6...).")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   'name). By default, files are overwritten.')
def del_mac_names(input_path, exclude_namerecord, output_dir, recalc_timestamp, overwrite):
    """Deletes all namerecords where platformID is equal to 1.

    According to Apple (https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6name.html), "names with
    platformID 1 were required by earlier versions of macOS. Its use on modern platforms is discouraged. Use names with
    platformID 3 instead for maximum compatibility. Some legacy software, however, may still require names with
    platformID 1, platformSpecificID 0".

    USAGE:

        ftcli names del-mac-names INPUT_PATH [OPTIONS]

    Use the -ex / --exclude-namerecord option to prevent certain namerecords to be deleted:

        ftcli names del-mac-names INPUT_PATH -ex 1

    The -ex / --exclude-namerecord option can be repeated to exclude from deletion more than one namerecord:

        ftcli names del-mac-names INPUT_PATH -ex 1 -ex 3 -ex 6

    INPUT_PATH can be a single font file or a folder containing fonts.
    """

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.delMacNames(exclude_namerecord=exclude_namerecord)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


# set-cff-name


@click.group()
def setCffName():
    pass


@setCffName.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('--font-name', type=str, default=None, help="Sets the CFF font name.")
@click.option('--full-name', type=str, default=None, help="Sets the CFF full name.")
@click.option('--family-name', type=str, default=None, help="Sets the CFF family name.")
@click.option('--weight', type=str, default=None, help="Sets the CFF weight.")
@click.option('--copyright', type=str, default=None, help="Sets the CFF copyright.")
@click.option('--notice', type=str, default=None, help="Sets the CFF notice.")
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def set_cff_name(input_path, font_name, full_name, family_name, weight, copyright, notice, output_dir,
                 recalc_timestamp, overwrite):
    """Sets names in the CFF table."""

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            if 'CFF ' not in font:
                click.secho(f'{f} is not a CFF font', fg='red')
                return

            count = font.setCFFName(fontNames=font_name, FullName=full_name, FamilyName=family_name, Weight=weight,
                                    Copyright=copyright, Notice=notice)

            if count > 0:
                output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
                font.save(output_file)
                click.secho(f'{output_file} --> saved', fg='green')
            else:
                click.secho(f'{os.path.basename(f)} --> no changes made.', fg='yellow')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


# set-name


@click.group()
def setNameRecord():
    pass


@setNameRecord.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--name-id', type=click.IntRange(0, 32767), help="nameID (Integer between 1 and 32767)")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If it's not specified, name will be written in both tables.")
@click.option('-l', '--language', default="en", show_default=True, help="language")
@click.option('-s', '--string', required=True, help='string')
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def set_name(input_path, name_id, platform, language, string, output_dir, recalc_timestamp, overwrite):
    """Writes the specified namerecord in the name table.

    If the namerecord is not present, it will be created. If it already exists, will be overwritten.

    If name_id parameter is not specified, the first available nameID will be used.

    By default, the namerecord will be written both in platformID 1 (Macintosh) and platformID 3 (Windows) tables. Use
    -p/--platform-id [win|mac] option to write the namerecord only in the specified platform.

    Use the -l/--language option to write the namerecord in a language different than 'en'. Use 'ftcli nametable
    langhelp' to display available languages.
    """

    windows = False if platform == "mac" else True
    mac = False if platform == "win" else True

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.setMultilingualName(nameID=name_id, language=language, string=string, windows=windows, mac=mac)

            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


# name-from-txt

@click.group()
def setNameRecordFromTxt():
    pass


@setNameRecordFromTxt.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--name-id', type=click.IntRange(0, 32767), help="nameID (Integer between 1 and 32767)")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If it's not specified, name will be written in both tables.")
@click.option('-l', '--language', default="en", show_default=True, help="language")
@click.option('-i', '--input-file', type=click.Path(exists=True, resolve_path=True), required=True,
              help="Path to the text file to read.")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, original timestamp is kept.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def name_from_txt(input_path, name_id, platform, language, input_file, output_dir, recalc_timestamp, overwrite):
    """Reads a text file and writes its content into the specified namerecord in the name table.

    If the namerecord is not present, it will be created. If it already exists, will be overwritten.

    If name_id parameter is not specified, the first available nameID will be used.

    By default, the namerecord will be written both in platformID 1 (Macintosh) and platformID 3 (Windows) tables. Use
    -p/--platform-id [win|mac] option to write the namerecord only in the specified platform.

    Use the -l/--language option to write the namerecord in a language different than 'en'. Use 'ftcli nametable
    langhelp' to display available languages.
    """

    windows = False if platform == "mac" else True
    mac = False if platform == "win" else True

    with open(input_file, 'r', encoding='utf-8-sig') as f:
        string = f.read()

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.setMultilingualName(nameID=name_id, language=language, string=string, windows=windows, mac=mac)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


# del-name

@click.group()
def delNameRecord():
    pass


@delNameRecord.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--name-id', type=click.IntRange(0, 32767), required=True,
              help="nameID (Integer between 0 and 32767)")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If no platform is specified, the namerecord will be deleted from both tables.")
@click.option('-l', '--language', default="en", show_default=True,
              help="Specify the name ID language (eg: 'de'), or use 'ALL' to delete the name ID from all languages.")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, timestamp is not recalculated.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def del_name(input_path, name_id, platform, language, output_dir, recalc_timestamp, overwrite):
    """Deletes the specified nemerecord from the name table.

    Use the -l/--language option to delete a namerecord in a language different than 'en'. Use 'ftcli nametable
    langhelp' to display available languages.

    Use '-l ALL' to delete the name ID from all languages.
    """
    windows = False if platform == "mac" else True
    mac = False if platform == "win" else True

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.delNameRecord(name_id, language=language, windows=windows, mac=mac)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


# find-replace
@click.group()
def findReplace():
    pass


@findReplace.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option("-os", "--old-string", required=True,
              help="old string")
@click.option('-ns', '--new-string', required=True,
              help="new string", show_default=True)
@click.option('-n', '--name-id', type=click.IntRange(0, 32767),
              help="nameID (Integer between 0 and 32767). If not specified, the string will be replaced in all"
                   "namerecords.")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If no platform is specified, the string will be replaced in both tables.")
@click.option('-cff', '--fix-cff', is_flag=True,
              help="Replaces the string in the CFF table.")
@click.option('-ex', '--exclude-namerecord', type=click.IntRange(0, 32767), multiple=True,
              help="Name IDs to ignore. The specified name IDs won't be changed. This option can be repeated "
                   "(example: -ex 3 -ex 5 -ex 6...).")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, timestamp is not recalculated.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def find_replace(input_path, old_string, new_string, name_id, platform, fix_cff, exclude_namerecord, output_dir,
                 recalc_timestamp, overwrite):
    """Replaces a string in the name table with a new string.

    If the '-cff' option is passed, the string will be replaced also in the 'CFF' table:

        ftcli names find-replace MyFont-Black.otf --os "Black" --ns "Heavy" --cff

    To simply remove a string, use an empty string as new string:

        ftcli names find-replace MyFont-Black.otf --os "RemoveMe" --ns ""

    To replace the string in a specific platform ('win' or 'mac'):

        ftcli names find-replace MyFont-Black.otf -os "Black" -ns "Heavy" -p win

    To replace the string in a specific namerecord:

        ftcli names find-replace MyFont-Black.otf -os "Black" -ns "Heavy" -n 6

    The -p / --platform and -n / --name-id options can be combined:

        ftcli names find-replace MyFont-Black.otf -os "Black" -ns "Heavy" -p win -n 6

    To exclude one or more namerecords, use the -ex / --exclude-namerecord option:

        ftcli names find-replace MyFont-Black.otf -os "Black" -ns "Heavy" -ex 1 -ex 6

    If a namerecord in explicitly included but also explicitly excluded, it wont be changed:

        ftcli names find-replace MyFont-Black.otf -os "Black" -ns "Heavy" -n 1 -ex 1 -ex 6

    The above command will replace the string only in nameID 6 in both platforms.
    """

    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            fix_count = font.findReplace(
                old_string, new_string, fixCFF=fix_cff, nameID=name_id, platform=platform,
                namerecords_to_ignore=exclude_namerecord)

            if fix_count > 0:
                output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
                font.save(output_file)
                click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
            else:
                click.secho(f'{os.path.basename(f)} --> no changes made', fg='yellow')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


@click.group()
def copyNameTable():
    pass


@copyNameTable.command()
@click.option('-s', '--source_font', required=True, type=click.Path(exists=True, resolve_path=True, dir_okay=False),
              help="Path to the source font.")
@click.option('-d', '--dest_font', required=True, type=click.Path(exists=True, resolve_path=True, dir_okay=False),
              help="Path to the destination font.")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, timestamp is not recalculated.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def copy_names(source_font, dest_font, output_dir, recalc_timestamp, overwrite):
    """Copies the 'name' table from source_font to dest_font.
    """

    try:
        s = Font(source_font)
        d = Font(dest_font, recalcTimestamp=recalc_timestamp)
        d['name'] = s['name']
        output_file = makeOutputFileName(dest_font, outputDir=output_dir, overWrite=overwrite)
        d.save(output_file)
        click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
    except Exception as e:
        click.secho(f'ERROR: {e}', fg='red')


@click.group()
def addPrefix():
    pass


@addPrefix.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('--prefix', required=True, type=str, help="The prefix string.")
@click.option('-n', '--name-ids', required=True, multiple=True, type=click.IntRange(0, 32767),
              help="nameID where to add the prefix (Integer between 0 and 32767)")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If no platform is specified, the prefix will be added in both tables.")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, timestamp is not recalculated.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def add_prefix(input_path, prefix, name_ids, platform, output_dir, recalc_timestamp, overwrite):
    """Adds a prefix to the specified namerecords.
    """
    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.addPrefix(prefix=prefix, name_ids=name_ids, platform=platform)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')
        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')

@click.group()
def addSuffix():
    pass


@addSuffix.command()
@click.argument('input_path', type=click.Path(exists=True, resolve_path=True))
@click.option('--suffix', required=True, type=str, help="The suffix string")
@click.option('-n', '--name-ids', required=True, multiple=True, type=click.IntRange(0, 32767),
              help="nameID where to add the suffix (Integer between 0 and 32767)")
@click.option("-p", "--platform", type=click.Choice(choices=["win", "mac"]),
              help="platform [win, mac]. If no platform is specified, the suffix will be added in both tables.")
@click.option('-o', '--output-dir', type=click.Path(file_okay=False, resolve_path=True), default=None,
              help='Specify the output directory where the output files are to be saved. If output_directory doesn\'t '
                   'exist, will be created. If not specified, files are saved to the same folder.')
@click.option('--recalc-timestamp/--no-recalc-timestamp', default=False, show_default=True,
              help='Keep the original font \'modified\' timestamp (head.modified) or set it to current time. By '
                   'default, timestamp is not recalculated.')
@click.option('--overwrite/--no-overwrite', default=True, show_default=True,
              help='Overwrite existing output files or save them to a new file (numbers are appended at the end of file'
                   ' name). By default, files are overwritten.')
def add_suffix(input_path, suffix, name_ids, platform, output_dir, recalc_timestamp, overwrite):
    """Adds a suffix to the specified namerecords.
    """
    files = getFontsList(input_path)

    for f in files:
        try:
            font = Font(f, recalcTimestamp=recalc_timestamp)
            font.addSuffix(suffix=suffix, name_ids=name_ids, platform=platform)
            output_file = makeOutputFileName(f, outputDir=output_dir, overWrite=overwrite)
            font.save(output_file)
            click.secho(f'{os.path.basename(output_file)} --> saved', fg='green')

        except Exception as e:
            click.secho(f'ERROR: {e}', fg='red')


cli = click.CommandCollection(sources=[
    setNameRecord, setNameRecordFromTxt, delNameRecord, setCffName, findReplace, winToMac, deleteMacNames,
    printLanguageCodes, delAllNames, copyNameTable, addPrefix, addSuffix],
    help="A command line tool to edit namerecords and CFF names.")
