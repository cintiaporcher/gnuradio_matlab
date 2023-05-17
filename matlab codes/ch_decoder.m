%function [rxcbs] = ch_decoder(rxdemod, F, bgn, locs, itrMax) %#codegen
function [rxcbs] = ch_decoder(rxdemod, F, bgn, itrMax)
    % add filler bits
    %fillers = -1*ones(F, 1);
    %rxdemod = [rxdemod(1:locs(1)-1); fillers; rxdemod(locs(1):end)];
    
    rxdecod = double(1-2*rxdemod);    % convert to soft bits
    %FillerIndices = find(rxdemod(:,1) == -1);
    %rxdecod(FillerIndices,:) = 0;     % fillers have no LLT i
    [rxcbs, actualitr] = nrLDPCDecode(rxdecod,bgn,itrMax);
end