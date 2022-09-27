from renderer import Renderer
from unittest import mock
import pytest

@mock.patch('renderer.Filedialog')
@mock.patch('renderer.pygame')
def test_run_launches_loop(mock, pygame_mock):
    def mock_screen_loop():
        raise SystemExit(1)
    renderer = Renderer()
    # simple test checking that run starts the main loop
    renderer.screen_loop = mock_screen_loop
    with pytest.raises(SystemExit):
        renderer.run()

@mock.patch('renderer.Filedialog')
@mock.patch('renderer.pygame')
def test_setting_pixels(mock, pygame_mock):
    renderer = Renderer()
    # setting a few pixels for testing
    renderer.set_pixel(0, 0, 1)
    renderer.set_pixel(1, 1, 1)
    renderer.set_pixel(2, 2, 1)
    assert renderer.pixel_map[0][0] == 1
    assert renderer.pixel_map[1][1] == 1
    assert renderer.pixel_map[2][2] == 1

@mock.patch('renderer.Filedialog')
@mock.patch('renderer.pygame')
def test_clear_pixels(mock, pygame_mock):
    renderer = Renderer()
    # setting a few pixels for testing
    renderer.set_pixel(0, 0, 1)
    renderer.set_pixel(1, 1, 1)
    renderer.set_pixel(2, 2, 1)
    renderer.clear_pixels()
    # pixel map should be all 0s now
    assert renderer.pixel_map[0][0] == 0
    assert renderer.pixel_map[1][1] == 0
    assert renderer.pixel_map[2][2] == 0
