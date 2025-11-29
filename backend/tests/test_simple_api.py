import unittest
from pathlib import Path
from fastapi import HTTPException
from unittest.mock import patch

import preliminary.simple_api
from preliminary.simple_api import _open_vid_or_404, list_videos, _meta, VideoMetaData, VIDEOS


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
        self.assertEqual(meta.fps,30)
        self.assertEqual(meta.frame_count, 400)
        self.assertEqual(meta.duration_seconds,20.0)

if __name__ == '__main__':
    unittest.main()
