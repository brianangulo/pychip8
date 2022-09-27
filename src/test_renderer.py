from renderer import Renderer
import pytest

def test_run_launches_loop():
    def mock_screen_loop():
        raise SystemExit(1)
    renderer = Renderer()
    # simple test checking that run starts the main loop
    renderer.screen_loop = mock_screen_loop
    with pytest.raises(SystemExit):
        renderer.run()

def test_setting_pixels():
    renderer = Renderer()
    # setting a few pixels for testing
    renderer.set_pixel(0, 0, 1)
    renderer.set_pixel(1, 1, 1)
    renderer.set_pixel(2, 2, 1)
    assert renderer.pixel_map[0][0] == 1
    assert renderer.pixel_map[1][1] == 1
    assert renderer.pixel_map[2][2] == 1

def test_clear_pixels():
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
