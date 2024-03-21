import typing

import phenopackets as pp202

from google.protobuf.message import Message

from ._base import File
from ._biosample import Biosample
from ._individual import Individual
from ._interpretation import Interpretation
from ._phenotypic_feature import PhenotypicFeature
from ._disease import Disease
from ._meta_data import MetaData
from .._api import MessageMixin
from ..parse import extract_message_scalar, extract_message_sequence, extract_pb_message_scalar, extract_pb_message_seq


class Phenopacket(MessageMixin):

    def __init__(
            self,
            id: str,
            meta_data: MetaData,
            subject: typing.Optional[Individual] = None,
            phenotypic_features: typing.Optional[typing.Iterable[PhenotypicFeature]] = None,

            biosamples: typing.Optional[typing.Iterable[Biosample]] = None,
            interpretations: typing.Optional[typing.Iterable[Interpretation]] = None,
            diseases: typing.Optional[typing.Iterable[Disease]] = None,

            files: typing.Optional[typing.Iterable[File]] = None,
    ):
        self._id = id
        self._subject = subject
        self._phenotypic_features = [] if phenotypic_features is None else list(phenotypic_features)
        self._biosamples = [] if biosamples is None else list(biosamples)
        self._interpretations = [] if interpretations is None else list(interpretations)
        self._diseases = [] if diseases is None else list(diseases)
        self._files = [] if files is None else list(files)
        self._meta_data = meta_data

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str):
        self._id = value

    @property
    def subject(self) -> typing.Optional[Individual]:
        return self._subject

    @subject.setter
    def subject(self, value: Individual):
        self._subject = value

    @subject.deleter
    def subject(self):
        self._subject = None

    @property
    def phenotypic_features(self) -> typing.MutableSequence[PhenotypicFeature]:
        return self._phenotypic_features

    @property
    def biosamples(self) -> typing.MutableSequence[Biosample]:
        return self._biosamples

    @property
    def interpretations(self) -> typing.MutableSequence[Interpretation]:
        return self._interpretations

    @property
    def diseases(self) -> typing.MutableSequence[Disease]:
        return self._diseases

    @property
    def files(self) -> typing.MutableSequence[File]:
        return self._files

    @property
    def meta_data(self) -> MetaData:
        return self._meta_data

    @meta_data.setter
    def meta_data(self, value: MetaData):
        self._meta_data = value

    @staticmethod
    def field_names() -> typing.Iterable[str]:
        return 'id', 'subject', 'phenotypic_features', 'biosamples', 'interpretations', 'diseases', 'files', 'meta_data'

    @staticmethod
    def from_dict(values: typing.Mapping[str, typing.Any]):
        if 'id' in values:
            return Phenopacket(
                # TODO: add the rest
                id=values['id'],
                subject=extract_message_scalar('subject', Individual, values),
                phenotypic_features=extract_message_sequence('phenotypic_features', PhenotypicFeature, values),
                biosamples=extract_message_sequence('biosamples', Biosample, values),
                interpretations=extract_message_sequence('interpretations', Interpretation, values),
                diseases=extract_message_sequence('diseases', Disease, values),
                files=extract_message_sequence('files', File, values),
                meta_data=MetaData.from_dict(values['meta_data']),
            )
        else:
            raise ValueError('Bug')  # TODO: better name

    def to_message(self) -> Message:
        return pp202.Phenopacket(
            id=self._id,
            subject=self._subject.to_message(),
            phenotypic_features=(pf.to_message() for pf in self._phenotypic_features),
            biosamples=(b.to_message() for b in self._biosamples),
            interpretations=(i.to_message() for i in self._interpretations),
            diseases=(d.to_message() for d in self._diseases),
            files=(f.to_message() for f in self._files),
            meta_data=self._meta_data.to_message(),
        )

    @classmethod
    def message_type(cls) -> typing.Type[Message]:
        return pp202.Phenopacket

    @classmethod
    def from_message(cls, msg: Message):
        if isinstance(msg, pp202.Phenopacket):
            return Phenopacket(
                id=msg.id,
                subject=extract_pb_message_scalar('subject', Individual, msg),
                phenotypic_features=extract_pb_message_seq('phenotypic_features', PhenotypicFeature, msg),
                biosamples=extract_pb_message_seq('biosamples', Biosample, msg),
                interpretations=extract_pb_message_seq('interpretations', Interpretation, msg),
                diseases=extract_pb_message_seq('diseases', Disease, msg),
                files=extract_pb_message_seq('files', File, msg),
                meta_data=extract_pb_message_scalar('meta_data', MetaData, msg),
            )
        else:
            cls.complain_about_incompatible_msg_type(msg)

    def __eq__(self, other):
        return isinstance(other, Phenopacket) \
            and self._id == other._id \
            and self._subject == other._subject \
            and self._phenotypic_features == other._phenotypic_features \
            and self._biosamples == other._biosamples \
            and self._interpretations == other._interpretations \
            and self._diseases == other._diseases \
            and self._files == other._files \
            and self._meta_data == other._meta_data

    def __repr__(self):
        return f'Phenopacket(' \
               f'id={self._id}, ' \
               f'subject={self._subject}, ' \
               f'phenotypic_features={self._phenotypic_features}, ' \
               f'biosamples={self._biosamples}, ' \
               f'interpretations={self._interpretations}, ' \
               f'diseases={self._diseases}, ' \
               f'files={self._files}, ' \
               f'meta_data={self._meta_data})'
