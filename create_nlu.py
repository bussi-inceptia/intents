# create_nlu.py

import os
import glob
import yaml
import argparse

parser = argparse.ArgumentParser(description="""***EXPERIMENTAL***
                                 Script que permite crear archivo nlu 
                                 basandose en los intents limpios y recolectados de 
                                 los distintos bots.""")

#parser.add_argument("nombre", help="Nombre de la persona")
parser.add_argument("-p","--path",        
                    help = "Path de donde se leerá el domain.yml")
parser.add_argument("-r","--regex",       
                    help = "Archivo que contenga la lista de regex a utilizar")
parser.add_argument("-R","--use-regex",   
                    help = "usar el archivo de regex en -p ")
parser.add_argument("-l","--lookup",      
                    help = "Archivo que contenga la lista de lookups a utilizar")
parser.add_argument("-L","--use-lookup",  
                    help = "usar el archivo de lookup en -p ")
parser.add_argument("-s","--synonym",     
                    help = "Archivo que contenga la lista de synonyms a utilizar")
parser.add_argument("-S","--use-synonym", 
                    help = "usar el archivo de regex en -p ")
parser.add_argument("-y","--replace-nlu", action="store_true",
                    help = "flag que si se setea, reemplaza el nlu sin promptear warning")


args = parser.parse_args()
#print(args)

#--------------------------------
#parsing de arguentos
base_path  = args.path
if base_path is None:
    print(Warning("no se proporcionó path. Saliendo"))
    exit(1)

regex_file   = f"{base_path}/regex"   if args.use_regex   is not None else args.regex
lookup_file  = f"{base_path}/lookup"  if args.use_lookup  is not None else args.lookup
synonym_file = f"{base_path}/synonym" if args.use_synonym is not None else args.synonym


replace = args.replace_nlu

#--------------------------------

#paths de intents, domain y nlu
intents_base_path = 'intents/clean/'
all_intents = glob.glob(f"{intents_base_path}/*")

domain_file = f'{base_path}/domain.yml'
output_path = f'{base_path}/data/'
#--------------------------------


#----------- Funciones de utilidad -----------------
def get_intents_in_domain(domain_file):
    print(f"intentando abrir {domain_file}")
    print(f"full_path: {os.full_path(domain_file)}")
    with open(domain_file, 'r') as file:
        data = yaml.safe_load(file)

    intents = []
    for i, d in enumerate(data['intents']):
        if isinstance(d, dict):
            intents.append(*list(d.keys()))
        else:
            intents.append(d)
    intents = [i.lower() for i in intents]  # por las dudas paso a lower
    return intents


def get_regex(regex_file):
    raise(NotImplementedError('Todavía no implementé get_regex'))
    # with open(regex_file,'r') as file:


def get_synonyms(synonyms_file):
    raise(NotImplementedError("Todavía no implementé get_synonyms"))

#--------------------------------

#-----------Checkeo de archivos y path de salida--------------

# si no existe el path de salida, lo creo
if not os.path.exists(output_path):
    os.mkdir(output_path)

# checkeo si existe el archivo, y prompteo si se desea reemplazar
output_file = f"{output_path}nlu2.md"

if os.path.exists(output_file):
    if not replace:
        print(Warning(f"El archivo \"{output_file}\" ya existe"))
        replace = input(f'el archivo {output_file} ya existe, desea remplazarlo? (y/N)')
        replace = replace.lower() == 'y'
    if replace:
        os.remove(output_file)
    else:
        # acá iría un return porque no debería hacer el resto
        print(f"el archivo de NLU ya existe y no se reemplaza, saltando procesamiento")
        exit(1)
#-----------------------------------------------------------

# TODO, checkear clean nlu hay paréntesis sin cerrar en weekday de ya_pague

def write_elems_to_file(elems, type='intent'):
    for el in elems:
        with open(f"{intents_base_path}{type}:{el}") as file:
            sentences_in_elem = file.readlines()

        with open(output_file, 'a') as file:
            file.writelines(f'## {type}:{el}\n')
            file.writelines('- ' + '- '.join(sentences_in_elem) + '\n\n')


intents = get_intents_in_domain(domain_file)
write_elems_to_file(intents, type='intent')

if regex_file is not None:
    try:
        regex = get_regex(regex_file)
        write_elems_to_file(regex, type='regex')
    except Exception as e:
        print(e)
        exit(1)
if synonym_file is not None:
    try:
        synonym = get_synonyms(synonym_file)
        write_elems_to_file(synonym, type='synonym')
    except NotImplementedError as e:
        print(e)
        exit(1)

if lookup_file is not None:
    try:
        lookup = get_regex(lookup_file)
        write_elems_to_file(lookup, type='lookup')
    except NotImplementedError as e:
        print(e)
        exit(1)

