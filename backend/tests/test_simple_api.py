import unittest
from pathlib import Path
from fastapi import HTTPException
from unittest.mock import patch

import preliminary.simple_api
from preliminary.simple_api import _open_vid_or_404, list_videos, _meta, VideoMetaData, video, video_frame, \
    video_frame_ocr, video_file, VIDEOS

from starlette.responses import FileResponse


class TestVideoPlayback(unittest.TestCase):
    def test_404_if_file_does_not_exist(self):
        mock_path = Path("/this/is/my/fake/path.mp4")
        VIDEOS["missing_file"] = mock_path

        with patch.object(Path, "is_file", return_value=False):
            with self.assertRaises(HTTPException) as response:
                _open_vid_or_404("missing_file")

        self.assertEqual(response.exception.status_code, 404)
        self.assertEqual(response.exception.detail, "Video not found")


class TestListVideos(unittest.TestCase):
    def test_list_videos_structure(self):
        test_sample_videos = {
            "demo": Path("this/is/a/test/video.mp4"),
            "demo2": Path("this/is/a/test/video2.mp4")
        }
        with patch("preliminary.simple_api.VIDEOS", test_sample_videos):
            response = list_videos()
            self.assertEqual(response["count"], 2)
            self.assertEqual(len(response["videos"]), 2)

            first = response["videos"][0]
            self.assertIn("id", first)
            self.assertIn("path", first)
            self.assertIn("description", first)
            self.assertIn("_links", first)


class TestMeta(unittest.TestCase):
    def test_meta_returns_metadata(self):
        class ExampleVideo:
            fps = 30
            frame_count = 400
            duration = 20.0

        video = ExampleVideo()
        meta = _meta(video)

        self.assertIsInstance(meta, VideoMetaData)
        self.assertEqual(meta.fps, 30)
        self.assertEqual(meta.frame_count, 400)
        self.assertEqual(meta.duration_seconds, 20.0)


class TestVideoFunction(unittest.TestCase):
    def test_video_returns_metadata(self):
        test_path = Path("/this/is/a/test/video_path.mp4")
        VIDEOS["test_video"] = test_path

        class MockCodingVideo:
            fps = 30
            frame_count = 400
            duration = 30.0

            def __init__(self, path):
                self.path = path

            class capture:
                @staticmethod
                def release():
                    pass

        with patch("preliminary.simple_api.CodingVideo", MockCodingVideo), \
                patch("preliminary.simple_api.Path.is_file", return_value=True):
            result = video("test_video")

        self.assertEqual(result.fps, 30)
        self.assertEqual(result.frame_count, 400)
        self.assertEqual(result.duration_seconds, 30.0)
        self.assertIn("self", result._links)
        self.assertIn("frames", result._links)


class TestVideoFrame(unittest.TestCase):
    def test_video_frame_returns_bytes(self):
        fake_path = Path("/fake/test/video_path.mp4")
        VIDEOS["fake_video"] = fake_path

        class MockCodingVideo:
            def __init__(self, path):
                self.path = path

                class Capture:
                    @staticmethod
                    def release():
                        pass

                self.capture = Capture()

            def get_image_as_bytes(self, t):
                return b"fake_image_bytes"

        with patch("preliminary.simple_api.CodingVideo", MockCodingVideo), \
                patch("preliminary.simple_api.Path.is_file", return_value=True):
            result = video_frame("fake_video", 1.0)

        self.assertEqual(result.body, b"fake_image_bytes")
        self.assertEqual(result.media_type, "image/png")

        del VIDEOS["fake_video"]


class TestVideoFrameOCR(unittest.TestCase):
    def test_video_frame_ocr(self):
        fake_path = Path("/fake/test/video_path.mp4")
        VIDEOS["fake_video"] = fake_path

        class MockCodingVideo:
            def __init__(self, path):
                self.path = path

                class Capture:
                    @staticmethod
                    def release():
                        pass

                self.capture = Capture()

            def get_text_from_frame_at_time(self, t):
                return "test text for OCR"

        with patch("preliminary.simple_api.CodingVideo", MockCodingVideo), \
                patch("preliminary.simple_api.Path.is_file", return_value=True):
            result = video_frame_ocr("fake_video", 1)

        self.assertIsInstance(result, dict)
        self.assertIn("text", result)
        self.assertEqual(result["text"], "test text for OCR")

        del VIDEOS["fake_video"]


class TestVideoFile(unittest.TestCase):
    def test_video_file_response(self):
        fake_path = Path("/fake/test/video_path.mp4")
        VIDEOS["fake_video"] = fake_path

        with patch("preliminary.simple_api.Path.is_file", return_value=True):
            result = video_file("fake_video")

        self.assertIsInstance(result, FileResponse)
        self.assertEqual(result.path, fake_path)
        self.assertEqual(result.media_type, "video/mp4")

        del VIDEOS["fake_video"]




if __name__ == '__main__':
    unittest.main()
