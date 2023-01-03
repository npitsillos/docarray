from typing import TypeVar

from docarray.typing.tensor.audio.abstract_audio_tensor import AbstractAudioTensor
from docarray.typing.tensor.audio.audio_ndarray import MAX_INT_16
from docarray.typing.tensor.torch_tensor import TorchTensor, metaTorchAndNode

T = TypeVar('T', bound='AudioTorchTensor')


class AudioTorchTensor(AbstractAudioTensor, TorchTensor, metaclass=metaTorchAndNode):
    """
    Subclass of TorchTensor, to represent an audio tensor.
    Adds audio-specific features to the tensor.


    EXAMPLE USAGE

    .. code-block:: python

        from typing import Optional

        import torch
        from pydantic import parse_obj_as

        from docarray import Document
        from docarray.typing import AudioTorchTensor, AudioUrl


        class MyAudioDoc(Document):
            title: str
            audio_tensor: Optional[AudioTorchTensor]
            url: Optional[AudioUrl]


        doc_1 = MyAudioDoc(
            title='my_first_audio_doc',
            audio_tensor=torch.randn(size=(1000, 2)),
        )

        doc_1.audio_tensor.save_to_wav_file(file_path='path/to/file_1.wav')


        doc_2 = MyAudioDoc(
            title='my_second_audio_doc',
            url='https://www.kozco.com/tech/piano2.wav',
        )

        doc_2.audio_tensor = parse_obj_as(AudioTorchTensor, doc_2.url.load())
        doc_2.audio_tensor.save_to_wav_file(file_path='path/to/file_2.wav')

    """

    _PROTO_FIELD_NAME = 'audio_torch_tensor'

    def to_audio_bytes(self):
        import torch

        tensor = (self * MAX_INT_16).to(dtype=torch.int16)
        return tensor.cpu().detach().numpy().tobytes()