#! /usr/bin/env python 
from ast import NotIn
import os
import string
import tempfile
import yaml

def readcmd(cmd):
    ftmp = tempfile.NamedTemporaryFile(suffix='.out', prefix='tmp', delete=False)
    fpath = ftmp.name
    if os.name=="nt":
        fpath = fpath.replace("/","\\") # forwin
    ftmp.close()
    os.system(cmd + " > " + fpath)
    data = ""
    with open(fpath, 'r') as file:
        data = file.read()
        file.close()
    os.remove(fpath)
    return data
default_ns = ["default", "kube-system", "kube-public", "kube-node-lease"]
print (type(default_ns))
ns= readcmd ("kubectl get ns | awk {'print $1'} | tail -n +2 ").split("\n")[:-1]
x= set(ns)-set(default_ns)
custom_ns= list(x)
os.system("kubeseal --fetch-cert > cert.pem")
print(custom_ns)  
for ns in custom_ns:
    os.system("kubectl config set-context --current --namespace="+ ns) 
    liste_secrets =readcmd("kubectl get secret | awk {'print $1'}  | tail -n +2 ").split("\n")[:-1]
    for secret in liste_secrets:
            # current_secret=os.system("kubectl get secret "+ secret +" -o yaml > "+ ns+"_"+secret+".yaml"  )
            # os.system("kubeseal < "+ns+"_"+secret+".yaml --cert cert.pem -o yaml > selead_"+ns+"_"+secret+".yaml")
            os.system("kubeseal --cert cert.pem -o yaml <<< $(kubectl get secret "+secret +" -n "+ ns +" -o yaml) > sealed_"+secret+"_"+ns+".yaml")

secret_files_found=readcmd("grep --exclude=secret.py -r -i 'kind: Secret' .").split("\n")[:-1]
for secret_file in secret_files_found:
    secret_filepath=secret_file.split(':')[0]
    # print("path:", secret_filepath)
    with open(secret_filepath, "r") as f:
        try:
            secret_yaml=yaml.safe_load(f)
            if(secret_yaml['kind'] == 'Secret'):
                # print(secret_yaml)
                name=secret_yaml['metadata']['name']
                ns=secret_yaml['metadata']['namespace']
                os.system("kubeseal --cert cert.pem -o yaml < "+ secret_filepath +"> sealed_"+name+"_"+ns+".yaml")

        except yaml.YAMLError as exc:
            print("yo")
            print(secret_filepath)

   # print (ll)
    # while l < len(ll):
    #     if (l== ""):
    #         ll.remove(l)
    #     print (ll)
        # l=l+1
    #     os.system("kubectl get secret "+liste[l] +" -o yaml > secret"+str(p)+".yaml")
    #     p=p+1
    # print (liste)
    # # while l < len(liste):
    # #         os.system("kubectl get secret "+liste[l]+" -o yaml > secret"+str(l)+".yaml")
    # #         l=l+1
# list_ns={}

# class my_dictionary(dict): 
  
#     # __init__ function 
#     def __init__(self): 
#         self = dict() 
          
#     # Function to add key:value 
#     def add(self, key, value): 
#         self[key] = value 
  
# dict_obj = my_dictionary() 
  
# Taking input key = 1, value = Geek

# for i in custom_ns:
#     print(i)
#     liste =readcmd("kubectl get secret -n "+i+"| awk {'print $1'}  | tail -n +2 ").split("\n")
#     print("namespace    "+i)
#     for j in liste:
#         print("secret   "+ j)
#         dict_obj.add(i, liste)

# print(dict_obj)
# for k in dict_obj:
#     if(dict_obj[k].count()>1):
#         liste=[]

# # {
#     'test': {
#         testsecret
#     },
#     'test': {
#         secret2
#     },
#     'farouk': {
#         farouk
#     }
# }

# list_of_secret= list(liste)
# print ( list_of_secret)

# for i in custom_ns:
#     print("in")
#     os.system( "kubectl get secret -n "+i  )

#         for z in custom_ns:
#             # for l in list_of_secret:
#             #     i=0
#             #     os.system(f"kubectl get secrets "+l+ " -n "+z+ " -o yaml > "+" secret"+str(i)+".yaml")
#             #     i=i+1
#             os.system

#" -o yaml > "+" secret"+str(i)+".yaml"