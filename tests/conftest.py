import pytest


@pytest.fixture
def config(mocker):
    mock_config = mocker.patch("hasek.config.Config")
    mock_config().__enter__().get_connection.return_value = {
        "host": "db1",
        "username": "user123",
        "password": "pass456",
    }
    return mock_config


@pytest.fixture(scope="session")
def tmpfiles(tmpdir_factory):
    import hasek
    from collections import namedtuple

    tmpdir = tmpdir_factory.mktemp("data")
    conf = tmpdir.join(".hasekrc")
    key = tmpdir.join(".hasekpg")
    noconf = tmpdir.join("noconf.txt")
    load_file = tmpdir.join("load_file.txt")
    output_file = tmpdir.join("output.txt")
    result = hasek.Config.write_default(conf.strpath)
    hasek.encrypt.create_key_file(key.strpath)
    files = namedtuple("files", "conf key load_file noconf output_file")
    return files(
        conf.strpath,
        key.strpath,
        load_file.strpath,
        noconf.strpath,
        output_file.strpath,
    )
