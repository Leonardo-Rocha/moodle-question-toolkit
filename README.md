# moodle-question-toolkit

Olá. O objetivo deste toolkit é permitir a **integração** de arquivos de provas com plataformas *moodle* e documentos *.tex*.

A ideia é simples : expandindo o uso das ferramentas gratuitas **pdftotext** e **pdfimages** do toolkit **xpdf-tools** nós extraimos as imagens e o texto das provas,
fazemos a marcação manualmente (esse processo será automatizado no futuro) das questões com "#Q(número da questão)" , das alternativas (quando tem) com "-(a-e)." e das
imagens inserindo ![Texto Alternativo](fig-(número da imagem).jpg "Titulo").

Uma vez com a marcação os arquivos txt podem ser convertidos para outros formatos, no momento estamos desenvolvendo o formato *.tex* mas no futuro será possível converter para outros como  o *GIFT*.

## TODO List : Objetivos de Implementação

[x]  Conversão de Equações

[ ]  Integração com as Imagens

[ ]  Conversão para *.tex*

[ ]  Conversão para *GIFT*

[ ]  Interface Gráfica

[ ]  Automação da marcação

[ ]  Multithreading
