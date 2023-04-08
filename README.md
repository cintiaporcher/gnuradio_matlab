# gnuradio_matlab

* Códigos em Python desenvolvidos para o meu TCC para integrar o GNU Radio com o Matlab. As funções utilizadas do Matlab são da toolbox de comunicação sem fio, mais especificamente para codificação para correção de erros em redes LTE e 5G NR, mas o código pode ser adaptado para outras aplicações.

* Os códigos foram criados para o bloco "Embedded Python Block" do GNU Radio.
  
* Para funcionar a versão do Python (foi utilizado o Python 3.10) precisa ser compatível com a versão do Matlab. Verifique as compatibildiades aqui: https://www.mathworks.com/support/requirements/python-compatibility.html.

* Os principais aspectos a serem considerados ao realizar a integração entre os dois softwares são os tipos das variáveis e o sistema de buffer de GNU Radio.
    * Por exemplo, no bloco de modulação a entrada é do tipo byte, mas para poder ser manipulada pelo Matlab ela precisa ser convertida para int8, e o vetor de saída do Matlab é convertido para csingle para poder ser utilizado no GNU Radio.
    * A arquitetura do buffer do GNU Radio é do tipo circular e apresentou algumas complicações com a integração, a função "general_work" dos códigos no geral era uma adatação dos vetores para poderem alimentar os buffers do GNU Radio de forma correta. Mais sobre a arquitetura de buffers do GNU Radio em: https://www.gnuradio.org/blog/2017-01-05-buffers/
