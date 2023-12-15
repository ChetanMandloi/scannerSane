Implementation of SANE api under a python wrapper and a PyQt GUI for scanning partial areas of flatbed in high resolution, stictch them together to output a full high resolution file for selected Region of Interest.


DONE:

    Created a dummy GUI interface.
    Testd SANE calls to get devices, options and open ports to issue commands etc.
    Created Classes to store settings for generating API calls and storing other scanner settings
    Export and import the above class objects to json to save and load settings selected.

    
TODO:

    Add application logic to pyqt elements in gui.
    Start binding SANE calls to the gui elements to be executed in seperate worker threads.
    Implement different output file types along with relevant settings needed. Implement the changes to gui
    Implement a method to select ROI from gui.
    Investigate the addition of progress feedback while scanning into gui.
    Weed out options that need not be implemented. Right now, we are storing in settingsClass settings that might be useless for our usecase like ADF modes, color correction profiles etc.



Current tracked settings:

    scanmode                          # Binary, Gray, Color
    depth                             # 8, 12, 14 bits colors per channel
    halftoning                        # Valid  options  are  "None",  "Halftone  A  (Hard  Tone)", "Halftone  B  (Soft Tone)", "Halftone C (Net Screen)", "Dither A(4x4 Bayer)", "Dither  B  (4x4  Spiral)",  "Dither  C  (4x4  Net Screen)",  "Dither  D (8x4 Net Screen)", "Text Enhanced Technology", "Download pattern A", and "Download pattern B".
    dropout                           # Dropout color used for monochrome scanning. The selected color is not scanned. Can be used to scan an original with a colored background
    brightness                        # integer range from -3 to 3
    sharpness                         # Integer -2(Defocus) to 2(Sharpen)
    gamma_correction                  # Valid options are "Default",  "User  defined", "High  density  printing"  "Low density printing" and "High contrast printing"
    color_correction                  # Valid options are "No Correction", "Impact-dot printers", "Thermal  printers",  "Ink-jet  printers" and "CRT monitors"
    out_resolution                    # use --help -d epnon with scanimage to get list of supported resolutions
    threshold                         # float from 0.0 to 100.0selects minimum brightness to get a white point
    mirror                            # If the image is laterally inverted or not
    auto_area_segmentation            # Image areas will be halftoned, text should be crispier with yes. read more
    wait_for_button                   # Start scan only when button on scanner is pressed
    cct                               # user defined color correction. cct-1 to cct-9 each with integers in range of -127 to 127
    preview                           # Requests a low resoltuion scan from frontend
    geometry                          # [l, t, x, y] Controls scan area. Rectangle from (l,t) to (x,y)
    source                            # Selects scan source. For our application, only flatbed shoudld be applicable as ADF won't support hexaboard
    auto_eject                        # Makes no difference as flatbed can't autoeject
    film_type                         # Should only activated if TPU is selected as source. Valid Options are "Negative Film" and "Positive Film"
    focus_position                    # Valid options are "Focus 2.5mm above glass" and "Focus on glass".  The  focus on the 2.5mm point above the glass is necessary for scans with the transparency unit, so that  the  scanner can  focus on the film if one of the film holders is used.  This option is only functional for selected scanners, all other scanners will ignore this option.
    bay                               # Select scan bay. Should not matter for our flatbed implementation
    eject                             # Options ejects the sheet in ADF. NA for flatbed scanning
    adf_mode                          # simplex or duplex for ADF scanning. Should not matter for flatbed scanning
    grid_size                         # If the grid of subscans is 2x2 or 3x3 or something. Increasing this would involve changing the UI on the fly. Currently only 2x2 is supported.
    output_type                       # Will implement only jpeg to start with. Planned Supported file types: jpeg, tiff, png or anything else
    jpeg_compression                  # Compression Quality Used if Jpeg is selected.
    self.scan_number = scan_number    # The number of scans that would need to be performed for the selected subscan grid
    self.json_export = json_export    # The export path for the exported json
  
