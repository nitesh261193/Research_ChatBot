import spacy

SESSION_END_MARKER = '============================================='
USER_MARKER = 'USER ++++ '
BOT_MARKER = 'TRUMP- THE BOT ASSISTANT ++++ '
ALLOWED_ENTITIES = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE',
                    'DATE',
                    'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL']


class HistorySaver:
    HISTORY_OUTPUT_FILE = 'output_convo.txt'

    def __init__(self):
        self.history_fh = None
        self.users_info = {}
        self.nlp = spacy.load("en_core_web_sm")

    def __enter__(self):
        self.history_fh = open(HistorySaver.HISTORY_OUTPUT_FILE, 'a+')
        self._load_past_conversations()
        return self

    def _load_past_conversations(self):
        with open(HistorySaver.HISTORY_OUTPUT_FILE, 'r+') as fh:
            session = []
            for line in fh.readlines():
                if line.strip() == SESSION_END_MARKER:
                    self._process_session(session)
                    session = []
                    continue
                session.append(line)

    def _process_session(self, session):
        if len(session) < 3:
            return
        # Second line in the session is supposed to be the intro line
        users = self._extract_persons_from_line(session[1])
        if not users:
            return

        user = users[0]
        curr_entities = {}
        # The third line is the bots' response according to history so we don't want to process that
        for line in session[3:]:
            processed_line = self.nlp(line)
            for token in processed_line:
                if token.ent_type_ not in ALLOWED_ENTITIES:
                    continue
                curr_entities[token.ent_type_] = token.text

        if curr_entities:
            self.users_info[user] = curr_entities

    def _extract_persons_from_line(self, line):
        processed_line = self.nlp(line)
        persons = [token.text for token in processed_line if token.ent_type_ == 'PERSON']

        return persons

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.update_end_session()
        self.history_fh.close()

    def update_user_response(self, response):
        self.history_fh.write(f'{USER_MARKER}{response}\n')

    def update_bot_response(self, response):
        self.history_fh.write(f'{BOT_MARKER}{response}\n')

    def update_end_session(self):
        self.history_fh.write(f'{SESSION_END_MARKER}\n')

    def get_history_based_response(self, intro_line):
        persons = self._extract_persons_from_line(intro_line)

        if not persons:
            print('WARN: No person name found in the intro line')
            return
        if persons[0] not in self.users_info:
            print(f'WARN: Person:[{persons[0]}] has not chatted with us previously')
            return

        return self.users_info[persons[0]]
