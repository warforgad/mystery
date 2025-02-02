import importlib
import json
import pathlib
import tempfile
import typing

import findimports

import mystery

ALLOWED_IMPORTS = ['sys']


def teardown_module(_):
    # Load the configuration file.
    config_path = pathlib.Path('config.json')
    config = json.load(config_path.open('r'))
    dep_lock_path = pathlib.Path(tempfile.gettempdir()).joinpath(
        config['lockfile_name']
    )
    try:
        dep_lock_path.unlink()
    except FileNotFoundError:
        pass


def test_mystery_package():
    package_imports: typing.List[findimports.ImportInfo] = findimports.find_imports(
        mystery.__mystery_init_py__
    )
    print(f'mystery_file: {mystery.__file__}')
    print(f'mystery_name: {mystery.__name__}')
    print(f'mystery_package_name: {mystery.__mystery_package_name__}')
    for package_import in package_imports:
        if package_import.name in ALLOWED_IMPORTS:
            continue
        print(f'package_import_name: {package_import.name}')
        try:
            _ = importlib.import_module(package_import.name)
        except ModuleNotFoundError:
            print('MODULE_NOT_FOUND!!')
            assert package_import.name == mystery.__mystery_package_name__
        else:
            assert package_import.name == mystery.__name__
