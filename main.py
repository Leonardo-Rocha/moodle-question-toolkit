import os
import re
import sys
from typing import List 

# MUST IMPORT \usepackage{enumitem}
def convert_to_tex(filename: str):
  # equação -> $equation$
  print("Converting to TeX...")
  
  preamble_filename = 'provas/preamble.tex'
  converted_filename = filename.replace(".txt", ".tex")
  output_file = open(converted_filename, "w")
  output_list = []

  # filename = "provas/Enade/CC_2005/CC_2005_Marcado.txt"
  paths = re.split("/", filename)
  test_type = paths[1] if len(paths) >= 1 else 'ENADE' 
  test_year = paths[2].split('_')[1] if len(paths) >= 2 else 'ANO'
  test_course = paths[2].split('_')[0] if len(paths) >= 2 else 'CURSO'
  document_title = f"\\LARGE \\textbf{{Prova {test_type} {test_year}\\\{test_course} \\\}}"

  with open(preamble_filename) as file:
    lines = file.readlines()
    lines[20] = document_title
    output_file.writelines(lines)

  alternative_regex = "(-[a-e].)"
  question_regex = "(#Q)\d+"
  image_regex = "!\[[\w\sà-úÀ-Ú\d/./:/-]+\]\(fig-\d+.jpg \"[\w\sà-úÀ-Ú\d/./:/-]+\"\)"

  should_close_enumerate = False
  is_enumerate_open = False

  output_list.append("\n\\begin{questions}\n")

  with open(filename) as file:
    lines = file.readlines()
    
    index = 0
    line = ""
    while index < len(lines):
      line = lines[index]
      # para cada marcação de questão, escrever um \question
      if re.match(question_regex, line):
        # TODO: escape backslash
        output_list.append(f"\n\\question (\\textbf{{{test_type}}}$|$\\textbf{{{test_course}}}-\\textbf{{{test_year}}}) ")
        index += 1

      # para cada imagem, adicionar um include graphics
      # ![Texto Alternativo](fig-0000.jpg "Legenda")
      elif re.match(image_regex, line):
        parsed_string = line.split('(')[1]
        filename_and_caption = parsed_string.split('\"')
        figure_filename = filename_and_caption[0]
        figure_caption = filename_and_caption[1].split("\")")[0]
        figure_fullpath = f'{paths[3].split(".")[0] if len(paths) >= 3 else "figuras"}_figuras/{figure_filename}'.strip()

        output_list.extend([
          '\\begin{figure}[H]\n',
          '\t\\begin{center}\n',
          f'\t\t\\includegraphics[width=0.5\\textwidth]{{{figure_fullpath}}}\n',
          f'\t\t\\caption{{{figure_caption}}}\n',
          '\t\\end{center}\n',
          '\\end{figure}\n'
        ])
        index += 1

      # para cada marcação de alternativa adicionar um item do enumerate
      elif re.match(alternative_regex, line):
        # se é a primeira questão, abrir um enumerate
        if re.match("(-a.)", line):
          is_enumerate_open = True
          output_list.append("\t\\begin{enumerate}[label=\\alph*)]\n")

        string_to_append = ""
        # remove -a.
        string_to_append = re.sub(alternative_regex, "", line)
        line = lines[index + 1]
        index += 1
        while index < (len(lines) - 1) and not re.match(alternative_regex, lines[index + 1]) and not re.match(question_regex, line):
          string_to_append += line
          line = lines[index + 1]
          index += 1

        # se a próxima linha é uma questão, fechar o enumerate
        if index < (len(lines) - 1) and re.match(question_regex, line):
          should_close_enumerate = True 
        else:
          should_close_enumerate = False
          string_to_append += line
          index += 1
          
        # substitute \n for whitespace
        string_to_append = re.sub("(\n)", " ", string_to_append)
        output_list.append(f"\t\t\\item {string_to_append}\n")

        if should_close_enumerate:
          should_close_enumerate = False
          output_list.append("\t\\end{enumerate}\n")
      else:
        # caso não tenha marcação, apenas escrever diretamente
        output_list.append(line)
        index += 1
  
  if is_enumerate_open:
    is_enumerate_open = False
    output_list.append("\t\\end{enumerate}\n")

  output_list.append("\n\\end{questions}\n")
  output_list.append("\\end{document}\n")

  output_file.writelines(output_list)
  output_file.close()


def convert_to_GIFT():
  print("Converting to GIFT...")

def is_64bits():
  return sys.maxsize > 2**32
  
def main():
  # test = "provas/Enade/CC_2005/CIENCIA_DA_COMPUTACAO_Prova2005.pdf"

  # TODO: fazer download da versão mais recente do xpdf-tools pelo site.
  #os.system(f"./xpdf-tools-linux-4.03/bin64/pdftotext -raw {test}")
  #os.system(f"mkdir $PWD/provas/Enade/CC_2005/CIENCIA_DA_COMPUTACAO_Prova2005_figuras")
  #os.system(f"./xpdf-tools-linux-4.03/bin64/pdfimages -j {test} $PWD/provas/Enade/CC_2005/CIENCIA_DA_COMPUTACAO_Prova2005_figuras/fig")

  markdown_file_path = "provas/Enade/CC_2005/CIENCIA_DA_COMPUTACAO_Prova2005-utf8.txt"

  convert_to_tex(markdown_file_path)


if __name__ == "__main__":
  main()
