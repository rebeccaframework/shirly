import sys
import locale
import getpass
import logging
from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.command import Command
from pyramid.paster import bootstrap
import sqlahelper
from . import models as m

class AddUserCommand(Command):

    def get_parser(self, prog_name):
        parser = super(AddUserCommand, self).get_parser(prog_name)
        parser.add_argument('config')
        return parser

    def run(self, parsed_args):
        env = bootstrap(parsed_args.config)
        settings = env['registry'].settings
    
        user_name = unicode(raw_input('user name: '), locale.getpreferredencoding())
        password = getpass.getpass('password: ')
        user = m.User(user_name=user_name, password=password)
        m.DBSession.add(user)
        import transaction
        transaction.commit()

class ShirlyApp(App):
    log = logging.getLogger(__name__)

    def __init__(self):
        super(ShirlyApp, self).__init__(
            description='shirly manage command',
            version='0.0',
            command_manager=CommandManager('shirly.command'),
        )

    def initialize_app(self):
        self.log.debug('initialize app')

    def prepare_to_run_command(self, command):
        pass

    def clean_up(self, cmd, result, err):
        pass

def main(argv=sys.argv[1:]):
    myapp = ShirlyApp()
    return myapp.run(argv)
