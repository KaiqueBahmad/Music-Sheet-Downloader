# Music-Sheet-Downloader
Web-Scraping script, searches music sheet, find it and download.

Open finder.py, instanciate the class Finder, then call 'get_sheet' method, required argument is the name of the song, it don't need to be exactally the name,
optional argument is 'folder_name', if None is given, then the name of the folder where sheets will be downloaded is the same than the name music.

"""Example on how to use
Bot = Finder()

Bot.get_sheet('Moonlight Sonata', folder_name = 'sheets')\n
"""
