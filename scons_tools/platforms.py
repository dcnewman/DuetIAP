# platforms.py -- platform-specific build settings for firmware builds
#
#   To see a list of known platforms, issue the command
#
#      python platforms.py
#
#   Individuals can extend the list of known platforms by supplying
#   the file ~/.rrf_platforms.py containing additional entries
#   for the platforms{} dictionary.  In the following example, an
#   entry is defined for a platform named "franken-board"
#
#     % cat ~/.rrf_platforms.py
#     platforms['franken-board'] = {
#         'defines' : [ 'NETWORK' ]
#     }
#
#  It can then be built with the simple command
#
#     % scons platform=franken-board
#

from os.path import expanduser, isfile

platforms = {

# This is a dictionary of platform names to build.  The dictionary key
# is the platform name used when running scons,
#
#   scons platform=<dictionary-key>
#
# Each platform to build is itself a dictionary containing build settings.
# The settings are
#
#   board         -- Board name to use in C/C++ #define's to identify the
#                    board.  Will be converted to uppercase.
#
#   program_port  -- Which USB port to use for programming.
#
#   arduino_board -- Arduino platform (e.g., 'arduino_due_x')
#
#   arduino_libraries -- Arduino libraries needed by the main sources
#                        (as opposed to the local libraries used).
#
#   libraries     -- Local libraries to use out of src/Libraries/.
#                    Arduino libraries then needed by these local libraries
#                    are specified in scons_tools/libraries.py.
#
#   defines       -- List of #defines to establish for this board.  Any
#                    string prefixed with '-' will be removed from the list
#                    of #defines to establish.
#
    'duet' :
        { 'board' : 'Duet',
          'program_port' : 'native',
          'arduino_board' : 'arduino_due_x',
          'arduino_libraries' : [ 'core', 'Storage' ],
          'libraries' : [ 'Fatfs', 'Flash' ],
          'defines' : [ 'DUET' ]
        },

    'ng' :
        { 'board' : 'DuetNG',
          'program_port' : 'native',
          'arduino_board' : 'arduino_due_x',
          'arduino_libraries' : [ 'core', 'Storage' ],
          'libraries' : [ 'Fatfs', 'Flash' ],
          'defines' : [ 'DUET_NG' ]
        },

    'radds' :
        { 'board' : 'RADDS',
          'program_port' : 'native',
          'arduino_board' : 'arduino_due_x',
          'arduino_libraries' : [ 'core', 'Storage' ],
          'libraries' : [ 'Fatfs', 'Flash' ],
          'defines' : [ '__RADDS__', 'SD_MMC_SPI_MODE', 'SPI_PIN=77',
                        'SPI_CHAN=0', 'SD_SS=4', 'SD_DETECT_PIN=14',
                        'SD_DETECT_VAL=0', 'SD_DETECT_PIO_ID=ID_PIOD',
                        'USE_SAM3X_DMAC=1', 'DMA_TIMEOUT_COMPUTE' ]
        }
}

# Load data from ~/.rrf_platforms.py

tmp_dict = { 'platforms' : {} }
home = expanduser('~')
if home[-1] != '/':
    home += '/'
site_file = home + '.rrf_platforms.py'

if isfile(site_file):
    with open(site_file) as f:
        exec(f.read(), tmp_dict)

    if 'platforms' in tmp_dict:
        tmp_platforms = tmp_dict['platforms']
        for key in tmp_platforms:
            platforms[key] = tmp_platforms[key]

if __name__ == '__main__':
    list = ''
    for key in platforms:
        list += key + ' '
    print list[:-1]
