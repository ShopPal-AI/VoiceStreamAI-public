import os
import json
import time
from src.asr.asr_factory import ASRFactory
from src.vad.vad_factory import VADFactory
from src.agent.llm import chat, nonstream_chat
from src.tts.coqui_tts import tts



class SilenceAtEndOfChunk():

    def __init__(self, **kwargs):

        self.chunk_length_seconds = os.environ.get('BUFFERING_CHUNK_LENGTH_SECONDS')
        if not self.chunk_length_seconds:
            self.chunk_length_seconds = kwargs.get('chunk_length_seconds')
        self.chunk_length_seconds = float(self.chunk_length_seconds)

        self.chunk_offset_seconds = os.environ.get('BUFFERING_CHUNK_OFFSET_SECONDS')
        if not self.chunk_offset_seconds:
            self.chunk_offset_seconds = kwargs.get('chunk_offset_seconds')
        self.chunk_offset_seconds = float(self.chunk_offset_seconds)

        self.error_if_not_realtime = os.environ.get('ERROR_IF_NOT_REALTIME')
        if not self.error_if_not_realtime:
            self.error_if_not_realtime = kwargs.get('error_if_not_realtime', False)
        
        self.processing_flag = False

        vad_args = {"auth_token": "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"}
        self.vad_pipeline = VADFactory.create_vad_pipeline("pyannote", **vad_args)
        asr_args = {"model_size": "large-v3"}
        self.asr_pipeline = ASRFactory.create_asr_pipeline("faster_whisper", **asr_args)
        self.agent = nonstream_chat
        self.tts = tts
        self.chunk_stack = bytearray()

    def process_audio(self, new_chunk):
        sampling_rate, y = new_chunk
        y = y.astype(np.float32)
        y /= np.max(np.abs(y))
        chunk_length_in_bytes = self.chunk_length_seconds * self.client.sampling_rate * self.client.samples_width
        if len(new_chunk) > chunk_length_in_bytes:
            if self.processing_flag:
                exit("Error in realtime processing: tried processing a new chunk while the previous one was still being processed")

            self.chunk_stack += new_chunk
            self.processing_flag = True
            # Schedule the processing in a separate task
            return self.process_audio_aux()
    
    def process_audio_aux(self):  
        
        start = time.time()
        vad_results =  vad_pipeline.detect_activity(self.chunk_stack)

        if len(vad_results) == 0:
            self.chunk_stack.clear()
            self.processing_flag = False
            return 

        last_segment_should_end_before = ((len(self.chunk_stack) / (self.client.sampling_rate * self.client.samples_width)) - self.chunk_offset_seconds)
        if vad_results[-1]['end'] < last_segment_should_end_before:
            #print("asr start")
            transcription = asr_pipeline.transcribe(self.chunk_stack)
            #print("asr end")
            if transcription['text'] != '' and transcription['language'] == 'en' and transcription['language_probability']>0.5 :
                new_question = transcription['text']
                end = time.time()
                transcription['processing_time'] = end - start
                json_transcription = json.dumps(transcription) 

                return json_transcription
                # await websocket.send(json_transcription)

                # #print("agent start")
                # new_answer = agent(transcription['text'], chat_history)
                # #print("agent end")
                # agent_time = time.time()
                # answer = {"text":new_answer, "processing_time":agent_time-end}
                # json_answer = json.dumps(answer)
                # await websocket.send(json_answer)

                # #print("tts start")
                # tts_bytes = tts(text=new_answer)
                # if tts_bytes is not None:
                #     tts_time = time.time()
                #     tts_result = {"processing_time":tts_time-agent_time, "tts": list(tts_bytes)}
                #     tts_result = json.dumps(tts_result)
                #     #print("tts end")
                #     await websocket.send(tts_result)

            self.chunk_stack.clear()
        
        self.processing_flag = False