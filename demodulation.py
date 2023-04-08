"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import matlab.engine
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, M=4):
        gr.basic_block.__init__(self,
            name='Demodulation (MATLAB)',   # will show up in GRC
            in_sig=[np.csingle],
            out_sig=[np.byte]
        )
        self.M = M

        self.demod_message = None
        self.sent_count=0

        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r"G:\Meu Drive\UFRGS\PD\MATLABcodes\MATLABcoder")

    def demodulate(self, message):
        message = np.reshape(message,(-1,1))
        message = matlab.single(message, is_complex=True)
        rxdemod = self.eng.demodulate(message, self.M)
        rxdemod = np.asarray(rxdemod, dtype=np.byte).reshape(-1)
        return rxdemod

    def general_work(self, input_items, output_items):
        #buffer references
        #print('====== Demodulating ======')
        in0 = input_items[0]
        out = output_items[0]

        if self.sent_count==0:
            self.message_len = len(in0)
            self.demod_message = self.demodulate(in0)
        
        if self.sent_count + len(out) < len(self.demod_message):
            out[:] = self.demod_message[self.sent_count:self.sent_count+len(out)]
            out_len = len(out)
        else:
            to_send = self.demod_message[self.sent_count:]
            out_len = len(to_send)
            out[:out_len] = to_send
        
        self.sent_count += out_len

        if self.sent_count >= len(self.demod_message):
            self.sent_count = 0
            self.demod_message = None
            #print(f'Consuming {self.message_len} received bits...')
            self.consume(0, self.message_len)
            self.message_len = 0

        #print(f'Sending {out_len} demodulated bits...')

        return out_len
