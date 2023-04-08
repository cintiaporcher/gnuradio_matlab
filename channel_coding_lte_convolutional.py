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
    def __init__(self):
        self.coded_message = None
        self.sent_count = 0

        gr.basic_block.__init__(self,
            name="Channel Coding (MATLAB)",
            in_sig=[np.byte],
            out_sig=[np.byte])

        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r"G:\Meu Drive\UFRGS\PD\MATLABcodes\MATLABcoder")

    def encode(self, message):
        message = np.reshape(message,(-1,1))
        message = matlab.int8(message)
        txcoded = self.eng.ch_coder_conv(message)
        txcoded = np.asarray(txcoded, dtype=np.byte).reshape(-1)
        return txcoded

    def general_work(self, input_items, output_items):
        #buffer references
        #print('====== Coding ======')

        in0 = input_items[0]
        out = output_items[0]

        # Se não tem mensagem pra enviar, ou se terminou de enviar a mensagem
        if self.sent_count==0:
            # Coda a mensagem e deixa ela na fila de entrada
            self.message_len = len(in0)
            self.coded_message = self.encode(in0)
        
        # Se ainda tem mais do que len(out) bits pra enviar
        if self.sent_count + len(out) < len(self.coded_message):
            # envia len(out) bits
            out[:] = self.coded_message[self.sent_count:self.sent_count+len(out)]
            out_len = len(out)
        else: # Se sobram 0< bits < len(out) bits, (finalzinho da msg), manda os bits que sobraram
            to_send = self.coded_message[self.sent_count:]
            out_len = len(to_send)
            out[:out_len] = to_send
        
        # Vou enviar esse tanto de bits
        self.sent_count+=out_len

        # Se eu enviei todos os bits da mensagem
        if self.sent_count >= len(self.coded_message):
            # Reseta a contagem de bits
            self.sent_count = 0
            self.coded_message = None
            #print(f'Consuming {self.message_len} uncoded bits...')
            # Tira a mensagem da fila de entrada SÓ AGORA
            self.consume(0, self.message_len)
            self.message_len = 0

        #print(f'Sending {out_len} coded bits...')
        #return produced
        return out_len
