function [txmod, locs] = modulate(data, M) %#codegen
    %locs = (data == -1);
    %data(locs) = [];
    txmod = qammod(data,M,'InputType','bit','UnitAveragePower',true);
end