# Audio

DocArray supports many different modalities including `Audio`.
This section will show you how to use DocArray to load and handle audio data in DocArray.

Moreover, we will introduce DocArray's audio specific types, to represent your audio data ranging from [`AudioUrl`][docarray.typing.url.AudioUrl] to [`AudioBytes`][docarray.typing.bytes.AudioBytes] and [`AudioNdArray`][docarray.typing.tensor.audio.audio_ndarray.AudioNdArray].

!!! note
    This requires a `pydub` dependency. You can install all necessary dependencies via:
    ```cmd 
    pip install "docarray[audio]"
    ```

## Load audio file

First, let's define our class `MyAudio`, which extends [`BaseDoc`][docarray.base_doc.doc.BaseDoc] and has an `url` attribute of type [`AudioUrl`][docarray.typing.url.AudioUrl], and an optional `tensor` attribute of type `AudioTensor`.

Next, we can instantiate a `MyAudio` object with a local or remote url. 

```python
from docarray import BaseDoc
from docarray.typing import AudioUrl, AudioNdArray


class MyAudio(BaseDoc):
    url: AudioUrl
    tensor: AudioNdArray = None
    frame_rate: int = None


doc = MyAudio(
    url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.mp3?raw=true'
)
```

Loading the content of the audio file is as easy as calling [`.load()`][docarray.typing.url.AudioUrl] on the [`AudioUrl`][docarray.typing.url.AudioUrl] instance. 

This will return:

- an [`AudioNdArray`][docarray.typing.tensor.audio.AudioNdArray] representing the audio file content 
- the corresponding frame rate, which describes the number of signals for a certain period of time.

```python
doc.tensor, doc.frame_rate = doc.url.load()
doc.summary()
```
``` { .text .no-copy }
📄 MyAudio : 2015696 ...
╭──────────────────────┬───────────────────────────────────────────────────────╮
│ Attribute            │ Value                                                 │
├──────────────────────┼───────────────────────────────────────────────────────┤
│ url: AudioUrl        │ https://github.com/docarray/docarray/blob/feat-rew    │
│                      │ ... (length: 90)                                      │
│ tensor: AudioNdArray │ AudioNdArray of shape (30833,), dtype: float64        │
│ frame_rate: int      │ 44100                                                 │
╰──────────────────────┴───────────────────────────────────────────────────────╯
```


## AudioTensor

DocArray offers several AudioTensors to store your data to:

- [`AudioNdArray`][docarray.typing.tensor.audio.audio_ndarray.AudioNdArray]
- `AudioTorchTensor`
- `AudioTensorFlowTensor`

If you specify the type of your tensor to one of the above, it will be cast to that automatically:

```python hl_lines="7 8 15 16"
from docarray import BaseDoc
from docarray.typing import AudioTensorFlowTensor, AudioTorchTensor, AudioUrl


class MyAudio(BaseDoc):
    url: AudioUrl
    tf_tensor: AudioTensorFlowTensor = None
    torch_tensor: AudioTorchTensor = None


doc = MyAudio(
    url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.mp3?raw=true'
)

doc.tf_tensor, _ = doc.url.load()
doc.torch_tensor, _ = doc.url.load()

assert isinstance(doc.tf_tensor, AudioTensorFlowTensor)
assert isinstance(doc.torch_tensor, AudioTorchTensor)
```


## AudioBytes

Alternatively, you can load your [`AudioUrl`][docarray.typing.url.AudioUrl] instance to [`AudioBytes`][docarray.typing.bytes.AudioBytes], and your [`AudioBytes`][docarray.typing.bytes.AudioBytes] instance to an `AudioTensor` of your choice:

```python hl_lines="15 16"
from docarray import BaseDoc
from docarray.typing import AudioBytes, AudioTensor, AudioUrl


class MyAudio(BaseDoc):
    url: AudioUrl = None
    bytes_: AudioBytes = None
    tensor: AudioTensor = None


doc = MyAudio(
    url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.mp3?raw=true'
)

doc.bytes_, _ = doc.url.load_bytes()  # type(doc.bytes_) = AudioBytes
doc.tensor, _ = doc.bytes_.load()  # type(doc.tensor) = AudioNdarray
```
 
Vice versa, you can also transform an AudioTensor to AudioBytes:

```python
from docarray.typing import AudioBytes

bytes_from_tensor = doc.tensor.to_bytes()

assert isinstance(bytes_from_tensor, AudioBytes)
```

## Save audio to file
You can save your AudioTensor to an audio file of any format as follows:
```python
tensor_reversed = doc.tensor[::-1]
tensor_reversed.save(
    file_path='olleh.mp3',
    format='mp3',
)
```
## Play audio in notebook

You can play your audio sound in a notebook from its url as well as its tensor, by calling `.display()` on either one:

```python
doc.url.display()
```

<table>
  <tr>
    <td><b>hello.mp3</b></td>
  </tr>
  <tr>
    <td><audio controls><source src="../hello.mp3" type="audio/mp3"></audio></td>
  </tr>
</table>

```python
tensor_reversed.display()
```
<table>
  <tr>
    <td><b>olleh.mp3</b></td>
  </tr>
  <tr>
    <td><audio controls><source src="../olleh.mp3" type="audio/mp3"></audio></td>
  </tr>
</table>




## Get started - Predefined AudioDoc

To get started and play around with your audio data, DocArray provides a predefined [`AudioDoc`][docarray.documents.audio.AudioDoc], which includes all of the previously mentioned functionalities:

```python
class AudioDoc(BaseDoc):
    url: Optional[AudioUrl]
    tensor: Optional[AudioTensor]
    embedding: Optional[AnyEmbedding]
    bytes_: Optional[AudioBytes]
    frame_rate: Optional[int]
```

You can use this class directly or extend it to your preference:
```python
from docarray.documents import AudioDoc
from typing import Optional


# extend AudioDoc
class MyAudio(AudioDoc):
    name: Optional[str]


audio = MyAudio(
    url='https://github.com/docarray/docarray/blob/feat-rewrite-v2/tests/toydata/hello.mp3?raw=true'
)
audio.name = 'My first audio doc!'
audio.tensor, audio.frame_rate = audio.url.load()
model = MyEmbeddingModel()
audio.embedding = model(audio.tensor)
```
