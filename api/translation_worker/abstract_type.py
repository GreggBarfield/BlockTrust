from core.database.database import Database
from api.database.inserts_model import InsertsModel
from core.database.objects.match import Match
import abc


class AbstractType:

    def __init__(self, db: Database, inserts_model: InsertsModel, insert):
        self.db = db
        self.inserts_model = inserts_model
        self.block_value = None
        self.insert = insert

        self.emitted_blocks = []
        self.emitted_matches = []

    def emit_block(self, block_key, block_value):
        """Adds a block key-value pair to the list of blocks that need to be
        emitted. This is actually performed in insert_handler.py.

        Params:
            block_key: The block key
            block_value: The block value
        """
        self.emitted_blocks.append((block_key, block_value))

    def emit(self, match: Match):
        """Adds a match to the list of matches that need to be emitted.
        This is actually performed in insert_handler.py after processing
        is done with the blockchain.

        Params:
            match: A Match
        """
        self.emitted_matches.append(match)

    @abc.abstractmethod
    def block_key(self):
        """Checks to see if there is any outside information it needs.

        Returns:
            A block key, or None if not needed
        """
        pass

    @abc.abstractmethod
    def handle(self):
        """Handles an API Insert of this type.

        self.block_value has been set with a value if requested

        Returns: nothing
        """
        pass
