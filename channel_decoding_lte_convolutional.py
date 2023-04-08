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
    def __init__(self, out_msgLen=2560):        
        self.received_count = 0
        self.sent_count = 0

        self.msg_len = out_msgLen*3 
        self.buffer_out = np.zeros(out_msgLen*3 , dtype=np.byte)
        self.decoded_msg = np.zeros(out_msgLen, dtype=np.byte)

        gr.basic_block.__init__(self,
            name="Channel Decoding (MATLAB)",
            in_sig=[np.byte],
            out_sig=[np.byte])

        self.eng = matlab.engine.start_matlab()
        self.eng.cd(r"G:\Meu Drive\UFRGS\PD\MATLABcodes\MATLABcoder")
        #print('matlab ok')

    def decode(self, message):
        message = np.reshape(message,(-1,1))
        message = matlab.int8(message)
        rxdecod = self.eng.ch_decoder_conv(message)
        rxdecod = np.asarray(rxdecod, dtype=np.byte).reshape(-1)
        return rxdecod

    def general_work(self, input_items, output_items):
        #buffer references
        #print('====== Decoding ======')
        in0 = input_items[0]
        out = output_items[0]

        # se ainda não começou a enviar o out
        if self.sent_count == 0:
            # Se espero receber mais bytes
            if self.received_count + len(in0) <= self.msg_len:
                # Popula buffer
                self.buffer_out[self.received_count:self.received_count+len(in0)] = in0[:]
                # Incrementa contador de bytes recebidos
                self.received_count += len(in0)
            
            if self.received_count != self.msg_len:
                #print(f'Consuming {len(in0)} coded bits...')
                self.consume(0, len(in0))
            
            # se já recebi todos os bytes, decodifica e começa a transissão
            if self.received_count == self.msg_len:
                self.received_count = 0
                #print('Decoding...')
                self.decoded_msg[:] = self.decode(self.buffer_out)

                out[:] = self.decoded_msg[:len(out)]
                self.sent_count += len(out)
                #print(f'Sendin: {self.sent_count} uncoded bits...')

                return len(out)
            else:
                return 0

        # se a transmissão já foi iniciada, sent_count != 0
        else:
            if self.sent_count + len(out) < len(self.decoded_msg):
                out[:] = self.decoded_msg[self.sent_count : self.sent_count + len(out)]
                self.sent_count += len(out)
            # se len(out) é maior que o restante da mensagem
            else:
                out[:len(self.decoded_msg)-self.sent_count] = self.decoded_msg[self.sent_count:]
                self.sent_count += len(self.decoded_msg) - self.sent_count
            
            #print(f'Sending {self.sent_count} uncoded bits...')
            
            if self.sent_count == len(self.decoded_msg):
                #print(f'Consuming {len(in0)} coded bits...')
                self.consume(0, len(in0))

            return len(out)