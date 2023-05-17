function [txcoded] = ch_coder(txcbs, F, bgn)
%function [txcoded] = ch_coder(K, F, bgn) %#codegen
%txcbs = randi([0 1],K-F, 1); % code block segments
fillers = -1*ones(F, 1);
txcbs = [txcbs; fillers];
txcoded = nrLDPCEncode(txcbs, bgn);

% remove filler bits
locs = (txcoded == -1);
txcoded(locs) = [];
end