import os
import platform
import pytest

from hasek.__main__ import main
from hasek.core import MainCommand
from hasek.errors import *
from hasek.encrypt import *


@pytest.mark.usefixtures('tmpfiles')
class TestCommandLine(object):
    def test_print_help(self, mocker):
        # Should raise a SystemExit and cause help to print
        with pytest.raises(SystemExit):
            main()

    def test_config_not_found(self, mocker, tmpfiles):
        mock_prompt = mocker.patch('hasek.core.prompt_bool')
        mock_prompt.return_value = False
        mock_prompt.side_effect = ConfigNotFound("Did it!")
        with pytest.raises(ConfigNotFound):
            MainCommand().run(test_args=["secret", "test1", "--conf", tmpfiles.noconf])
