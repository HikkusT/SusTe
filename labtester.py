import sys
import os
import requests
import subprocess
from enum import Enum

#Sorry for the global variable! Xoxo
lab_num = None


class FileType(Enum):
  input_type = '.in'
  output_typ = '.out'


def lab_name():
  global lab_num
  if lab_num is None:
    if len(sys.argv) > 1:
      lab_num = '%02d' % int(sys.argv[1])
    else:
      lab_num = '%02d' % int(input('Qual lab voce deseja testar? '))
  
  return 'lab' + lab_num

def get_lab_folder(lab):
  parent_dir = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir, os.pardir))
  path = os.path.join(parent_dir, lab)

  if os.path.isdir(path):
    return path
  else:
    print("Diretorio {0} nao encontrado".format(lab))
    print("Procurando pelo arquivo")
    path = os.path.join(parent_dir, lab + '.py')
    if os.path.isfile(path):
      return parent_dir
    else:
      print('Nao foi possivel encontrar ')
      print('Encerrando o programa')
      quit()

def get_test_folder_path(lab_folder):
  test = os.path.join(lab_folder, 'tests')

  if not os.path.isdir(test):
    create_tests_folder(test)
    
  return test

def format_arq_name(i, file_type):
  return 'arq%02d' % i + file_type

def compose_base_url():
  return "https://susy.ic.unicamp.br:9999/mc102w/{0}/dados/".format(lab_num)

def create_tests_folder(folder_path):
  os.makedirs(folder_path)

  base_url = compose_base_url()
  download_tests(folder_path, base_url, 18)

def download_tests(path, base_url, num_tests):
  for i in range(1, num_tests + 1):
    for file_type in FileType:
      test_file = format_arq_name(i, file_type.value)
      url = base_url + test_file
      r = requests.get(url, verify=False)
      with open(os.path.join(path, test_file), 'wb') as f:
        f.write(r.content)

def compare_answers(i, folder_path):
  output_test_case = 'arq%02d.out' % i
  output = 'output%02d.out' % i
  a = open(os.path.join(folder_path, output_test_case), 'r')
  b = open(os.path.join(folder_path, output), 'r')
  equal = True
  for line1 in a:
    for line2 in b:
      if line1 != line2:
        equal = False
        print(line1 + line2)
      break
  
  print(equal)

if __name__ == "__main__":
  folder_path = get_lab_folder(lab_name())
  
  tests_folder = get_test_folder_path(folder_path)

  for i in range(1, 19):
    print('Analyzing test', i)
    input_test_case = 'arq%02d.in' % i
    output = 'output%02d.out' % i
    a = open(os.path.join(tests_folder, input_test_case), 'r')
    b = open(os.path.join(tests_folder, output), 'wb')
    subprocess.call(['python', os.path.join(folder_path, lab_name() + '.py')], stdin=a, stdout=b)
    compare_answers(i, tests_folder)
