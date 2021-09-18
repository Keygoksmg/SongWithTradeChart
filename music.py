import numpy as np
from pydub import AudioSegment
from pydub.playback import play

class MakeSound:
    def __init__(self) -> None:
        self.audiofile_pos = 'Positive.wav' # change your own audiofile (wav format)
        self.audiofile_neg = 'Negative.wav' # change your own audiofile (wav format)


    def create_sound_timing(self, data):
        frec = np.array(data.Close.tolist(), dtype = float) - np.array(data.Open.tolist(), dtype = float)
        frec_binary = np.where(frec > 0, 1, -1)

        # sound status represented by 1 and -1
        sound_states = []
        initial_state = 0 if frec_binary[0] == -1 and frec_binary[1] == -1 else 1
        sound_states.append(initial_state)
        current_state = initial_state

        for i in range(1, len(frec_binary)-2):
            start = i
            end = start+1

            if frec_binary[start] == frec_binary[end] and current_state != frec_binary[start]:
                current_state = frec_binary[start]        
            sound_states.append(current_state)

        # determine timing to change sound
        keep_state_count = sound_states[0]
        sound_schedules = []

        for i in range(len(sound_states)-1):
            if sound_states[i] != sound_states[i+1]:
                sound_schedules.append(keep_state_count)
                keep_state_count = sound_states[i+1]
                
            else:
                if keep_state_count > 0:
                    keep_state_count += 1
                else:
                    keep_state_count -= 1

        return sound_schedules

    
    def create_music(self, sound_schedules, name):
        start_ms = 0 #start of clip in milliseconds
        end_ms = 1000 #end of clip in milliseconds 1000ms == 1s

        sound_pos = AudioSegment.from_file(self.audiofile_pos, format="wav")
        sound_neg = AudioSegment.from_file(self.audiofile_neg, format="wav")

        time_scale = 350
        result_music = sound_pos[start_ms:0]

        for time in sound_schedules:
            if time >= 0:
                result_music += sound_pos[0:time*time_scale]
            else:
                result_music += sound_neg[0:time*time_scale*-1]
            start_ms = end_ms

        result_music.export(f"{name}.mp3", format="mp3")