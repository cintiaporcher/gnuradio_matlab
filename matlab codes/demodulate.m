function [rxdemod] = demodulate(rxsig, M) %#codegen
    rxdemod = qamdemod(rxsig,M,'OutputType','bit','UnitAveragePower',true);
    %rxdemod = qamdemod(rxsig,M,'UnitAveragePower',true);
end