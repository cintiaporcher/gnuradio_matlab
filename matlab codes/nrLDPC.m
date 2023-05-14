%=================%
%    PARAMETERS   %
%=================% 
% coding
bgn = 1;    % base graph number
K = 2640;   % block length
%K = 120;
%K = 2560;
F = 0;     % filler bits
%F = 80;

% channel
EbNo = linspace(-2, 18, 21);

% decoder
itrMax = 6;

% bit error rate
Nblocks = 10^2;

%BER = zeros(4,length(EbNo));
Nbiterrs = zeros(4,length(EbNo));
Nblkerrs = zeros(4,length(EbNo));

%BER_uncoded = zeros(4,length(EbNo));
Nbiterrs_uncoded = zeros(4,length(EbNo));
Nblkerrs_uncoded = zeros(4,length(EbNo));

%=================%
%    SIMULATION   %
%=================%
tic 

for mod = 1:4  
    % modulation | 1: QPSK | 2: 16QAM | 3: 64QAM | 4: 256QAM |
    M = 4^mod;
    alphabet = qammod(0:M-1,M,'UnitAveragePower',true);
    sigpwr = pow2db(mean(abs(alphabet).^2));
    
    for block = 1:Nblocks
        %=================%
        %  CHANNEL CODER  %
        %=================% 
        txcbs = randi([0 1],K-F, 1); % code block segments
        %fillers = -1*ones(F, 1);
        %txcbs = [txcbs; fillers];
        txcodedcbs = nrLDPCEncode(txcbs, bgn);
    
        %=================%
        %    MODULATION   %
        %=================%
        % trim filler bits
        databit = txcodedcbs;
        %locs = find(databit == -1);
        %databit(locs) = [];
    
        txmodcbs = qammod(databit,M,'InputType','bit','UnitAveragePower',true);
        txmodcbs_uncoded = qammod(txcbs,M,'InputType','bit','UnitAveragePower',true);
        
        for n = 1:length(EbNo)
            %=================%
            %  AWGN CHANNEL   %
            %=================%
            awgn_ch = comm.AWGNChannel('EbNo',EbNo(n),'BitsPerSymbol',log2(M));
            %rxsig = awgn(txmodcbs,EbNo(n),sigpwr);
            rxsig = awgn_ch(txmodcbs);
            rxsig_uncoded = awgn_ch(txmodcbs_uncoded);
    
            %=================%
            %   DEMODULATION  %
            %=================%
            rxdemod = qamdemod(rxsig,M,'OutputType','bit','UnitAveragePower',true);
            rxdemod_uncoded = qamdemod(rxsig_uncoded,M,'OutputType','bit','UnitAveragePower',true);
             
            %=================%
            % CHANNEL DECODER %
            %=================%
            % add filler bits
            %rxdemod = [rxdemod(1:locs(1)-1); fillers; rxdemod(locs(1):end)];
            
            rxdecod = double(1-2*rxdemod);    % convert to soft bits
            %FillerIndices = find(rxdemod(:,1) == -1);
            %rxdecod(FillerIndices,:) = 0;     % fillers have no LLT info
    
            [rxcbs, actualitr] = nrLDPCDecode(rxdecod,bgn,itrMax);
    
            %txcbs(end-F+1:end,:) = 0;   % replace fillers bits with 0
        
            %=================%
            %     ANALYSIS    %
            %=================%
            Nerrs = sum(rxcbs ~= txcbs);
            if Nerrs > 0
                Nbiterrs(mod,n) = Nbiterrs(mod,n) + Nerrs;
                Nblkerrs(mod,n) = Nblkerrs(mod,n) + 1;
            end
    
            Nerrs = sum(rxdemod_uncoded ~= txcbs);
            if Nerrs > 0
                Nbiterrs_uncoded(mod,n) = Nbiterrs_uncoded(mod,n) + Nerrs;
                Nblkerrs_uncoded(mod,n) = Nblkerrs_uncoded(mod,n) + 1;
            end
        end
        
        if rem(block,Nblocks/2) == 0
            fprintf('%d %.0f%% ', mod, block/Nblocks*100)
        end
    end    

    %BER_uncod(mod,:) = berawgn(SNR-log2(M),'qam',M);
    %BER_uncod(mod,:) = berawgn(SNR,'qam',M);   
end

toc

BER = Nbiterrs./((K-F)*Nblocks);
BER_uncoded = Nbiterrs_uncoded./((K-F)*Nblocks);

f = figure;

semilogy(EbNo,BER_uncoded(1,:),'--','color','#0072BD','LineWidth',0.6);
hold on
semilogy(EbNo,BER(1,:),'*-','color','#0072BD','LineWidth',1.3);

semilogy(EbNo,BER_uncoded(2,:),'--','color','#D95319','LineWidth',0.6);
semilogy(EbNo,BER(2,:),'*-','color','#D95319','LineWidth',1.3);

semilogy(EbNo,BER_uncoded(3,:),'--','color','#EDB120','LineWidth',0.6);
semilogy(EbNo,BER(3,:),'*-','color','#EDB120','LineWidth',1.3);

semilogy(EbNo,BER_uncoded(4,:),'--','color','#7E2F8E','LineWidth',0.6);
semilogy(EbNo,BER(4,:),'*-','color','#7E2F8E','LineWidth',1.3);

xlabel("Eb/No (dB)");
ylabel("BER");
ylim([10^(-5) 10^(0.1)]);
xlim([min(EbNo) max(EbNo)]);
grid on;
legend("Uncoded QPSK","NR-LDPC QPSK","Uncoded 16-QAM","NR-LDPC 16-QAM","Uncoded 64-QAM","NR-LDPC 64-QAM","Uncoded 256-QAM","NR-LDPC 256-QAM");
hold off