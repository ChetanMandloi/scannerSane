Implementation of SANE api under a python wrapper and a PyQt GUI for scanning partial areas in high resolution, stictch them together to output a Full high resolution file.

DONE:
  Create a GUI framework
  Test SANE calls to get devices, options and open ports to issue commands.
  Created Classes to store settings for generating API calls and storing other scanner settings
  Export and import the above class objects to json to save and load settings essentially
TODO:
  Add application logic to pyqt elements in gui
  Start binding SANE calls to the gui elements to be executed in seperate worker threads
  Implement a method to select ROI from gui
  Investigate the addition of progress feedback while scanning into gui
  
