"""A basic introduction to Open CV

Instructions
------------

Implement the functions below based on their docstrings.

Notice some docstrings include references to third-party documentation
Some docstrings **require** you to add references to third-party documentation.

Make sure you read the docstrings C.A.R.E.F.U.L.Y (yes, I took the L to check that you are awake!)
"""

# imports - add all required imports here
from pathlib import Path
import cv2, os
import numpy as np
from PIL import Image
import platform
import pytesseract

system = platform.system()
if system == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
elif system == "Linux":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

VID_PATH = Path("resources/oop.mp4")

class CodingVideo:
    capture: cv2.VideoCapture

    def __init__(self, video: Path | str):
        self.capture = cv2.VideoCapture(str(video))
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = self.capture.get(cv2.CAP_PROP_FRAME_COUNT)
        self.duration: float = (self.frame_count / self.fps) if self.fps > 0 else 0.0


    def __str__(self) -> str:
        """Displays key metadata from the video

        Specifically, the following information is shown:
            FPS - Number of frames per second rounded to two decimal points
            FRAME COUNT - The total number of frames in the video
            DURATION (minutes) - Calculated total duration of the video given FPS and FRAME COUNT

        Reference
        ----------
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        """
        duration_minutes = 0
        if self.fps > 0: 
            duration_minutes = (self.frame_count / self.fps / 60)
            

        return (f'FPS: {self.fps:.2f} \n') + (f'Frame Count: {self.frame_count}\n') + (f"Duration: {duration_minutes:.2f} minutes \n")


    def get_frame_number_at_time(self, seconds: int) -> int:
        """Given a time in seconds, returns the value of the nearest frame"""
        #get an approximate index based on seconds
        idx = int(round(float(seconds) * self.fps))
        #non 0 frame count
        if self.frame_count > 0:
            idx = max(0, min(idx, self.frame_count - 1)) 
        return idx
    
    def get_frame_rgb_array(self, frame_number: int) -> np.ndarray:
        """Returns a numpy N-dimensional array (ndarray)

        The array represents the RGB values of each pixel in a given frame

        Note: cv2 defaults to BGR format, so this function converts the color space to RGB

        Reference
        ---------
        https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html

        """
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_number))
        ok, frame_bgr = self.capture.read()
        if not ok or frame_bgr is None:
            raise ValueError(f"Invalid frame at frame num {frame_number} ")
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return frame_rgb
    
    def get_text_from_frame_at_time(self, seconds: int):
        """wrapper method that calls relevant functions, completing OCR pipeline from timestamp to output text"""
        if self.fps <= 0:
            raise ValueError("FPS is zero; cannot map time to frame.")

        # get frame from time -> get rgb frame at time in video -> perform OCR
        frame_idx = self.get_frame_number_at_time(seconds)
        frame_rgb = self.get_frame_rgb_array(frame_idx)
        text = pytesseract.image_to_string(frame_rgb)
        return text.strip()
    
    def get_image_as_bytes(self, seconds: int) -> bytes:
        """input timestamp, output a series of bytes representing the frame at that timestamp"""
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.get_frame_number_at_time(seconds))
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target location")
        ok, buf = cv2.imencode(".png", frame)
        if not ok:
            raise ValueError("Failed to encode frame")
        return buf.tobytes()

    def save_as_image(self, seconds: int, output_path: Path | str = 'resources/output.png') -> None:
      """Saves the given frame as a png image"""
      png_bytes = self.get_image_as_bytes(seconds)
      if not png_bytes:
        raise ValueError(f"Could not obtain image bytes at {seconds}s")

      out = Path(output_path)
      out.parent.mkdir(parents=True, exist_ok=True)
      with open(out, "wb") as f:
          f.write(png_bytes)

def test():
    coding_vid = CodingVideo("resources/oop.mp4")
    print(coding_vid)
    
    #getting frame from video (no OCR)
    coding_vid.get_image_as_bytes(42)
    coding_vid.save_as_image(42)

    # getting frame, and 'OCRing' it 
    print(coding_vid.get_text_from_frame_at_time(42))

if __name__ == '__main__':
    test()
