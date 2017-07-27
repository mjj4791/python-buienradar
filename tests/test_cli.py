"""Basic testing for CLI."""
from buienradar.__main__ import main


def test_main_info():
    """Test if we can call the main function."""
    # use simulation interface
    args = ['-v']

    # test calling results in the loop close cleanly
    assert main(args) is None


def test_main_debug():
    """Test if we can call the main function."""
    # use simulation interface
    args = ['-vv']

    # test calling results in the loop close cleanly
    assert main(args) is None
