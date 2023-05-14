"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Coded BER (PYTHON)',   # will show up in GRC
            in_sig=[np.byte, np.byte],
            out_sig=[np.float32]
        )

        self.bit_count = 0
        self.error_count = 0

    def general_work(self, input_items, output_items):
        #buffer references
        print('====== BER ======')
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]

        print(f'(BER) Original size: {len(in0)}, Received size: {len(in1)}')

        inlen = min([len(in0), len(in1)])

        in0_use = in0[:inlen]
        in1_use = in1[:inlen]

        self.bit_count += inlen
        self.error_count += np.sum(in0_use^in1_use)

        print(f'{self.error_count} errors in {self.bit_count} bits...')

        self.consume(0, inlen)
        self.consume(1, inlen)

        out[0] = self.error_count/self.bit_count

        print(f'Coded BER: {out[0]*100:.6f}%')

        return 1
