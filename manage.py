import unittest

from settings import APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE, DST_ABSPATH, DATABASE_URL
from tests.test_data_access import UnitTestDataAccess, UnitTestDataAccessExceptions
from vk_music.app import MusicApp
from vk_music.models import Base
from vk_music.services.data_access import DataAccessObject

import click


@click.group(name='run', invoke_without_command=False)
def run():
    pass


@run.command(name='init_db')
def init_db():
    """Invokes database according to models"""
    data_access_object = DataAccessObject(DATABASE_URL)
    Base.metadata.create_all(data_access_object.engine)


@run.command(name='sync')
def sync():
    """Syncs VK audios with database and file system"""
    music_app = MusicApp(APP_ID, USER_LOGIN, USER_PASSWORD, SCOPE)
    path = DST_ABSPATH
    music_app.synchronize_files(path)


@click.group(name='test', invoke_without_command=False)
def test():
    pass


@test.command(name='test_dao')
def test_data_access():
    """Tests implemented data access"""
    suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestDataAccess)
    unittest.TextTestRunner(verbosity=2).run(suite)
    exc_suite = unittest.TestLoader().loadTestsFromTestCase(UnitTestDataAccessExceptions)
    unittest.TextTestRunner(verbosity=2).run(exc_suite)


manage = click.CommandCollection(sources=[run, test])

if __name__ == '__main__':
    manage()
