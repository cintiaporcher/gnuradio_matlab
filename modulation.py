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
    def __init__(self, M=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(self,
            name='Modulation (MATLAB)',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.csingle]
        )
        self.M = M

        self.mod_message = None
        self.sent_count=0

        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r"G:\Meu Drive\UFRGS\PD\MATLABcodes\MATLABcoder")

    def modulate(self, message):
        message = np.reshape(message,(-1,1))
        message = matlab.int8(message)
        txmod = self.eng.modulate(message, self.M)
        txmod = np.asarray(txmod, dtype=np.csingle).reshape(-1)
        return txmod

    def general_work(self, input_items, output_items):
        #buffer references
        print('====== Modulating ======')
        in0 = input_items[0]
        out = output_items[0]

        if self.sent_count==0:
            self.message_len = len(in0)
            #self.mod_message = self.modulate(in0)
            self.mod_message = self.modulate(np.reshape(in0,(-1,1)))
        
        if self.sent_count + len(out) < len(self.mod_message):
            out[:] = self.mod_message[self.sent_count:self.sent_count+len(out)]
            out_len = len(out)
        else:
            to_send = self.mod_message[self.sent_count:]
            out_len = len(to_send)
            out[:out_len] = to_send
        
        self.sent_count+=out_len

        if self.sent_count >= len(self.mod_message):
            self.sent_count = 0
            self.mod_message = None
            print(f'Consuming {self.message_len} coded bits...')
            self.consume(0, self.message_len)
            self.message_len = 0

        print(f'Sending {out_len} modulated bits...')
        #return produced
        return out_len
