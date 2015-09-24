𝚃𝚛𝚎𝚊𝚜𝚞𝚛𝚎 𝙲𝚘𝚕𝚞𝚖𝚗
---------------

This is the code that runs [Treasure Column](https://www.youtube.com/channel/UCKNW6jeGUfPUg_UsyAsTaPA), a Youtube bot I run
that harvests publicly available imagery and sets it to the finest in uptempo dance music.

More info on the project can be found [here](https://medium.com/@derekarnold/remote-viewing-5cb161cdef4a).

Requirements: See setup.py, but you'll also need a Wordnik API key, as well as Google credentials.
Default search path for credential files is the current directory. You must copy the config defaults file and put in your
Wordnik API key. It'll search (curdir)/config.ini and ~/.treasurecolumn/config.ini for a config file.

You'll also need a url or file with a url on each line pointing at MJPEG streams. Obtaining those is an exercise left
to the reader.
