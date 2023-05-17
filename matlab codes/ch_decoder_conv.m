function [rxcbs] = ch_decoder_conv(rxdemod)
    
    rxdecod = double(2*rxdemod-1);    % convert to soft bits
    rxcbs = lteConvolutionalDecode(rxdecod);

end