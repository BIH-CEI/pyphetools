


class Disease:
    """
    Simple data object to hold ontology id/label for a disease diagnosis

    :param disease_id: a CURIE such as OMIM:600324
    :type disease_id: str
    :param disease_label: the name of the disease
    :type disease_label: str
    """

    def __init__(self, disease_id:str, disease_label):
        self._id = disease_id
        self._label = disease_label


    @property
    def id(self):
        return self._id

    @property
    def label(self):
        return self._label
