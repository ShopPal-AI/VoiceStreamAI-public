import gradio as gr
import numpy as np
from src.buffering_strategy.buffering_strategy_factory import BufferingStrategyFactory
from scipy.io.wavfile import write
import sys


strategy_config = {"language": None,
                       "processing_strategy": "silence_at_end_of_chunk", 
                       "processing_args": {
                           "chunk_length_seconds": 3, 
                           "chunk_offset_seconds": 0.1
                           }
                    }

#strategy = BufferingStrategyFactory.create_buffering_strategy(strategy_config['processing_strategy'], **strategy_config['processing_args'])  

history = []
async def transcribe(new_chunk):
    global history
    sampling_rate, y = new_chunk
    history.append(y)
    print(len(history))

    if len(history) == 2:
        history = np.concatenate(history)
        await write('output.wav', sampling_rate, history)
        sys.exit(0)
    # print(sampling_rate, y.shape, y.dtype, y.max(), y.min())
    # y = y.astype(np.float32)
    # y /= np.max(np.abs(y))

    #text = strategy.process_audio(new_chunk)
    # text = None
    # if text is not None:
    #     history.append(text)
    
    return "test"


demo = gr.Interface(
    transcribe,
    [gr.Audio(sources=["microphone"], streaming=True)],
    ["text"],
    live=True,
)

demo.launch()
