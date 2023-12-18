"""
Chetan Mandloi

Define which parts of the api calls are active(Please note that only options that are enabled here will be parsed and
calls to SANE api.):
"""
SCANMODE_ON = True
DEPTH_ON = True
HALFTONING_ON = False
DROPOUT_ON = False
BRIGHTNESS = False
SHARPNESS = True
GAMMA_CORR_ON = False
OUT_RES_ON = True
THRESHOLD_ON = True
MIRROR_ON = False
AUTO_SEGMEN_ON = False
BUTTON_WAIT_ON = False
CCT_ON = False
#PREVIEW_ON = False
GEOMETRY_ON = True
SOURCE_ON = False
AUTO_EJECT_ON = False
FILM_TYPE_ON = False
FOCUS_ON = False
BAY_ON = False
EJECT_ON = False            # not an argument for scanning. Needs to implemented as a seperate command
ADFMODE_ON = False

import json
import sane
import numpy
from PIL import Image

class ScannerSettings:
    def __init__(self, sane_object=None,
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
        self.sane_object = sane_object
        self.scanmode = scanmode                    # Binary, Gray, Color , lineart, Monochrome Depending on scanner. check saneobject.opt after opening for details
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

    def set_scan_call_settings(self):
        """
            Generate pySane api calls based on current arguments and settings passed on to the object.
            A lot of options will have different parameter names. To get valid options, open a sane object connecting to
            the scanner and use saneobject.getoptions() and saneobject.opt variable output to know all valid active objects
            After checking there, update the variables here
            Non-selectable or non-existent options defined here will NOT generate an error but also WON"T WORK.
        """
        if self.sane_object == None:
            print("No Valid Opened sane port detected")
        if SCANMODE_ON:
            self.sane_object.mode = self.scanmode  # Exact Option name may vary a bit, check in cli using sane.opt
        if DEPTH_ON:
            self.sane_object.depth = self.depth
        if HALFTONING_ON:
            self.sane_object.halftoning = self.halftoning
        if DROPOUT_ON:
            self.sane_object.dropout = self.dropout
        if BRIGHTNESS:
            self.sane_object.brightness = self.brightness
        if SHARPNESS:
            self.sane_object.sharpness = self.sharpness
        if GAMMA_CORR_ON:
            self.sane_object.gamma_correction = self.gamma_correction
        if OUT_RES_ON:
            self.sane_object.resolution = self.out_resolution               # Some scanners might have seperate output and optical resoltuions. check in options for the scanner
        if THRESHOLD_ON:
            self.sane_object.threshold = self.threshold
        if MIRROR_ON:
            self.sane_object.mirror = self.mirror
        if AUTO_SEGMEN_ON:
            self.sane_object.auto_area_segmentation = self.auto_area_segmentation
        if BUTTON_WAIT_ON:
            self.sane_object.button_wait = self.wait_for_button
        if CCT_ON:
            self.sane_object.CCT = self.cct
        if GEOMETRY_ON:
            self.sane_object.tl_x = self.geometry[0]
            self.sane_object.tl_y = self.geometry[1]
            self.sane_object.br_x = self.geometry[2]
            self.sane_object.br_y = self.geometry[3]
        if SOURCE_ON:
            self.sane_object.source = self.source
        if AUTO_EJECT_ON:
            self.sane_object.autoEject = self.auto_eject
        if FILM_TYPE_ON:
            self.sane_object.film_type = self.film_type
        if FOCUS_ON:
            self.sane_object.focus = self.focus_position
        if BAY_ON:
            self.sane_object.bay = self.bay
        if ADFMODE_ON:
            self.sane_object.adf_mode = self.adf_mode

    def test_scan_pil(self):
        """
        Calls the set_scan_call_settings to apply current parameters to the sane port and save a test png image using
        python imaging library
        :return: 0 if no error, -1 if there is some error.
        """
        try:
            self.set_scan_call_settings()
            self.sane_object.start()
            test_img = self.sane_object.snap()
            test_img.save('test_image_pil.png')
            return 0
        except:
            return -1

    def test_scan_numpy(self):
        """
        Calls the set_scan_call_settings to apply current parameters to the sane port and save a test png image using
        numpy array parsing
        :return: 0 if no error, -1 if there is some error.
        """
        try:
            params = self.sane_object.get_parameters()
            self.sane_object.start()
            arr = self.sane_object.arr_snap()
            print("Array shape: %s, size: %d, type: %s, range: %d-%d, mean: %.1f, stddev: ""%.1f" % (repr(arr.shape),
                                                arr.size, arr.dtype, arr.min(), arr.max(), arr.mean(), arr.std()))
            if arr.dtype == numpy.uint16:
                arr = (arr / 255).astype(numpy.uint8)

            # reshape needed by PIL library
            arr = arr.reshape(arr.shape[2], arr.shape[1], arr.shape[0])
            if params[0] == 'color':
                im = Image.frombytes('RGB', arr.shape[1:], arr.tostring(), 'raw', 'RGB', 0,1)
            else:
                im = Image.frombytes('L', arr.shape[1:], arr.tostring(), 'raw', 'L', 0, 1)
            im.save('test_image_numpy.png')
            return 0

        except:
            return -1

    def close_sane_port(self):
        """
        Closes the sane port recieved and scanning or required transactions are done
        :return:
        """
        self.sane_object.close()



class AppSettings(ScannerSettings):
    """
    This class is for all the selections that can be done in the GUI. This should then be used to generate objects of
    ScannerSettings class that will be used to generate SANE api calls
    """
    def __init__(self, scanmode="Color", depth=8, halftoning="None", dropout="None", brightness=0, sharpness=0,
                 gamma_correction="Default", color_correction="No correction", out_resolution=4800,
                 threshold=100.0, mirror="no", auto_area_segmentation="yes", wait_for_button="no",
                 cct=None, preview="no", geometry=None, source="Flatbed",
                 auto_eject="no", film_type="Negative Film", focus_position="Focus on glass", bay=0, eject="no",
                 adf_mode="simplex", grid_size=2, output_type="jpeg", jpeg_compression=95, scan_number=4,
                 json_export="settings.json", roi=None
                 ):
        if roi is None:
            roi = [0, 0, 150, 150]
        self.scan_objs = None
        # Call Constructor of Parent class with inherited settings
        super().__init__(scanmode, depth, halftoning, dropout, brightness, sharpness, gamma_correction,
                         color_correction, out_resolution, threshold, mirror, auto_area_segmentation, wait_for_button,
                         cct, preview, geometry, source, auto_eject, film_type, focus_position, bay, eject, adf_mode)

        # ---------- Following Variables are for settings selected for output and other things ----------------------

        self.grid_size = grid_size  # If the grid of subscans is 2x2 or 3x3 or something. Increasing this would involve changing the UI on the fly. Currently only 2x2 is supported.
        self.output_type = output_type  # Will implement only jpeg to start with. Planned Supported file types: jpeg, tiff, png or anything else
        self.jpeg_compression = jpeg_compression  # Compression Quality Used if Jpeg is selected.
        # self.tiff_setting = "PLACEHOLDER"         # TODO After implementing tiff export
        # self.png_setting = "PLACEHOLDER"          # TODO After implementing PNG export
        self.scan_number = scan_number  # The number of scans that would need to be performed for the selected subscan grid
        self.json_export = json_export  # The export path for the exported json
        self.roi = roi


    def update_scan_number(self):
        self.scan_number = self.grid_size * self.grid_size

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

    def gen_scan_class(self):
        scan_obj_list = []
        if(self.scan_number == 4):      # implement for 9 or a general number of scan number later if needed
            for i in range(self.scan_number):
                if i == 0:
                    call_geometry = [self.roi[0], self.roi[1], self.roi[0] + (self.roi[2] - self.roi[0]) / 2, self.roi[1] + (self.roi[3] - self.roi[1]) / 2]
                elif i == 1:
                    call_geometry = [self.roi[0] + (self.roi[2] - self.roi[0]) / 2, self.roi[1], self.roi[2], self.roi[1] + (self.roi[3] - self.roi[0]) / 2]
                elif i == 2:
                    call_geometry = [self.roi[0], self.roi[0] + (self.roi[3] - self.roi[1]) / 2, self.roi[1] + (self.roi[2] - self.roi[0]) / 2, self.roi[3]]
                elif i == 3:
                    call_geometry = [self.roi[0] + (self.roi[2] - self.roi[0]) / 2, self.roi[1] + (self.roi[3] - self.roi[1]) / 2, self.roi[2], self.roi[3]]
                else:
                    call_geometry = None
                scan_obj_list.append(ScannerSettings(scanmode="Color", depth=8, halftoning="None", dropout="None", brightness=0, sharpness=0,
                 gamma_correction="Default", color_correction="No correction", out_resolution=4800,
                 threshold=100.0, mirror="no", auto_area_segmentation="yes", wait_for_button="no",
                 cct=None, preview="no", geometry=call_geometry, source="Flatbed",
                 auto_eject="no", film_type="Negative Film", focus_position="Focus on glass", bay=0, eject="no",
                 adf_mode="simplex"))
        self.scan_objs = scan_obj_list
        return scan_obj_list



test = AppSettings()
print(test.gen_scan_class()[0].geometry)
print(test.gen_scan_class()[1].geometry)
print(test.gen_scan_class()[2].geometry)
print(test.gen_scan_class()[3].geometry)


"""
test.exportConfiguration()
test.scanmode = "Grayscale"
print(test.__dict__)
testread = open("settings.json", 'r')
testjsonread = json.load(testread)
readobj = AppSettings(**testjsonread)
print(testjsonread)
print(readobj.__dict__)
test.scanmode = "Grayscale"
"""