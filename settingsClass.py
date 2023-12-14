"""
Chetan Mandloi
"""
import json
import sane

class ScannerSettings:
    def __init__(self,
                 scanmode="Color", depth=8, halftoning="None", dropout="None", brightness=0, sharpness=0,
                 gamma_correction="Default", color_correction="No correction", out_resolution=4800,
                 threshold=100.0, mirror="no", auto_area_segmentation="yes", wait_for_button="no",
                 cct=None, preview="no", geometry=None, source="Flatbed",
                 auto_eject="no", film_type="Negative Film", focus_position="Focus on glass", bay=0, eject="no",
                 adf_mode="simplex"
                 ):
        if geometry is None:
            geometry = [0, 0, 75, 75]
        if cct is None:
            cct = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        # --------------------- These variables are for generating SANE api calls. ------------------------------
        self.scanmode = scanmode                    # Binary, Gray, Color
        self.depth = depth                          # 8, 12, 14 bits colors per channel
        self.halftoning = halftoning                # Valid  options  are  "None",  "Halftone  A  (Hard  Tone)", "Halftone  B  (Soft Tone)", "Halftone C (Net Screen)", "Dither A(4x4 Bayer)", "Dither  B  (4x4  Spiral)",  "Dither  C  (4x4  Net Screen)",  "Dither  D (8x4 Net Screen)", "Text Enhanced Technology", "Download pattern A", and "Download pattern B".
        self.dropout = dropout                      # Dropout color used for monochrome scanning. The selected color is not scanned. Can be used to scan an original with a colored background
        self.brightness = brightness                # integer range from -3 to 3
        self.sharpness = sharpness                  # Integer -2(Defocus) to 2(Sharpen)
        self.gamma_correction = gamma_correction    # Valid options are "Default",  "User  defined", "High  density  printing"  "Low density printing" and "High contrast printing"
        self.color_correction = color_correction    # Valid options are "No Correction", "Impact-dot printers", "Thermal  printers",  "Ink-jet  printers" and "CRT monitors"
        self.out_resolution = out_resolution        # use --help -d epnon with scanimage to get list of supported resolutions
        self.threshold = threshold                  # float from 0.0 to 100.0selects minimum brightness to get a white point
        self.mirror = mirror                        # If the image is laterally inverted or not
        self.auto_area_segmentation = auto_area_segmentation  # Image areas will be halftoned, text should be crispier with yes. read more
        # self.red_gamma_table = "PLACEHOLDER"      #TODO implement gamma table
        # self.green_gamma_table = "PLACEHOLDER"    #
        # self.blue_gamma_table = "PLACEHOLDER"     #
        self.wait_for_button = wait_for_button      # Start scan only when button on scanner is pressed
        self.cct = cct                              # user defined color correction. cct-1 to cct-9 each with integers in range of -127 to 127
        self.preview = preview                      # Requests a low resoltuion scan from frontend
        self.geometry = geometry                    # [l, t, x, y] Controls scan area. Rectangle from (l,t) to (x,y)
        self.source = source                        # Selects scan source. For our application, only flatbed shoudld be applicable as ADF won't support hexaboard
        self.auto_eject = auto_eject                # Makes no difference as flatbed can't autoeject
        self.film_type = film_type                  # Should only activated if TPU is selected as source. Valid Options are "Negative Film" and "Positive Film"
        self.focus_position = focus_position        # Valid options are "Focus 2.5mm above glass" and "Focus on glass".  The  focus on the 2.5mm point above the glass is necessary for scans with the transparency unit, so that  the  scanner can  focus on the film if one of the film holders is used.  This option is only functional for selected scanners, all other scanners will ignore this option.
        self.bay = bay                              # Select scan bay. Should not matter for our flatbed implementation
        self.eject = eject                          # Options ejects the sheet in ADF. NA for flatbed scanning
        self.adf_mode = adf_mode                    # simplex or duplex for ADF scanning. Should not matter for flatbed scanning


    def exportConfiguration(self):
        """
        Export JSON file with entire configuration of both the scanner and application side
        :return: 0 if access export is successful and -1 if there is an error.
        """
        try:
            jsonfile = open(self.json_export, 'w')
            jsonfile.write(json.dumps(self.__dict__))
            # print(json.dumps(self.__dict__))
            jsonfile.close()
        except:
            print("ERROR")


    def gen_scan_call(self, scan_set):
        """
            scan_set : ScanSettings object
            Generate pySane api calls based on received AppSettings objects and ScannerSettings Objects
        """
        # TODO
        pass
class AppSettings:
    """
    This class is for all the selections that can be done in the GUI. This should then be used to generate objects of
    ScannerSettings class that will be used to generate SANE api calls
    """
    def __init__(self, grid_size=2, output_type="jpeg", jpeg_compression=95, scan_number=4,
                 json_export="settings.json", roi=None
                 ):
        if roi is None:
            roi = [0, 0, 150, 150]

        # ---------- Following Variables are for settings selected for output and other things ----------------------

        self.grid_size = grid_size  # If the grid of subscans is 2x2 or 3x3 or something. Increasing this would involve changing the UI on the fly. Currently only 2x2 is supported.
        self.output_type = output_type  # Will implement only jpeg to start with. Planned Supported file types: jpeg, tiff, png or anything else
        self.jpeg_compression = jpeg_compression  # Compression Quality Used if Jpeg is selected.
        # self.tiff_setting = "PLACEHOLDER"         # TODO After implementing tiff export
        # self.png_setting = "PLACEHOLDER"          # TODO After implementing PNG export
        self.scan_number = scan_number  # The number of scans that would need to be performed for the selected subscan grid
        self.json_export = json_export  # The export path for the exported json

    def update_scan_number(self):
        self.scan_number = self.grid_size * self.grid_size



"""
test = HexScan()
test.exportConfiguration()
test.scanmode = "Grayscale"
print(test.__dict__)
testread = open("settings.json", 'r')
testjsonread = json.load(testread)
readobj = HexScan(**testjsonread)
print(testjsonread)
print(readobj.__dict__)
test.scanmode = "Grayscale"
"""