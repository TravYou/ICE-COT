from relation import Relation
from wikidata.utils import get_label
from query import Query

# Essentially a S, R, O pair
class Fact:

    def __init__(self, subject_id, relation, target_id):
        self._subject_id = subject_id
        self._relation = relation
        self._target_id = target_id

    def get_subject_label(self):
        return get_label(self._subject_id)

    def get_target_label(self):
        return get_label(self._target_id)

    def get_relation_label(self):
        return self._relation.name.replace('_', ' ')

    def get_fact_query(self):
        return Query(self._subject_id, self._relation, self._target_id)

    def get_fact_prompt(self):
        return self._relation.phrase(get_label(self._subject_id))

    # Essentially returning the complete prompt give subject, relation, and target
    # It uses get_label to get wikidatalabel from id; use .phrase of relation to replace dummy <subject> with the actual label
    def get_fact_phrased(self):
        return self._relation.phrase(get_label(self._subject_id)) + f' {get_label(self._target_id)}.'

    # Get dictionary of prompt, s, r, o
    # Essentially returning itself as a dict with prompt
    def to_dict(self):
        return {
            'prompt': self.get_fact_phrased(),
            'subject_id': self._subject_id,
            'relation': self._relation.name,
            'target_id': self._target_id
        }

    @staticmethod
    def from_dict(d):
        return Fact(d['subject_id'], Relation[d['relation']], d['target_id'])

    def __str__(self):
        return f'({self.get_subject_label()}, {self.get_relation_label()}, {self.get_target_label()})'

