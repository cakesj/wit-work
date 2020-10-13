from shutil import copyfile, rmtree
import matplotlib.pyplot as plt 
import networkx as graph_maker
from typing import List
from PIL import Image
import datetime
import random
import sys
import os

def Isthereperent(fun):
    "\t\tfor a file, chacks if it has the .wit program inside it, if not, raises WitNotFoundError"
    def wrapper(*args, **kwargs):
        TOwhere: str = '~None~'
        perent_list: List[str] = str(sys.argv[0]).split('\\')
        for ancastor_n in range(len(perent_list)):  
            ancastor: str = '/'.join(perent_list[:ancastor_n + 1])
            if not (os.path.isdir(ancastor)):
                break
            elif '.wit' in os.listdir(ancastor):
                TOwhere = ancastor + '/.wit'
        if TOwhere == '~None~':
            raise WitNotFoundError("you havn't installed wit yet in any of the parenting files")
        return fun(TOwhere ,*args, **kwargs) # remember to put "place at any decorated function to get "TOwhere"
    return wrapper
    
class WitNotFoundError(Exception):
    pass

class FileNotEcceptableError(Exception):
    pass

class NameNotValid(Exception):
    pass

class Wit:

    def init(self, where: str) -> None:
        "\t\tcreates all the needed filework for oparation"
        os.mkdir(f'{where}/.wit')
        os.mkdir(f'{where}/.wit/images')
        os.mkdir(f'{where}/.wit/staging_area')
        with open(f'{where}/.Wit/info.txt', 'w') as TXT:
            TXT.write("\n")
        with open(f'{where}/.Wit/refrences.txt', 'w') as TXT:
            TXT.write(f"|HEAD=None\n|master(active)=None")



    def _HEAD_HUNTER(self, PLACE: str, branch: str="HEAD"):
        '''\t\tfinds the most reacent file inside the file "images", out of a certin branch
        
        \tinputs:
        PLACE: the place where the .wit file is
        branch: the branch to search in'''
        with open(f'{PLACE}/refrences.txt', 'r') as branches:
            branches = branches.read()
            start_O_branch = branches.find(f'|{branch}')
            end_O_branch = branches[start_O_branch:].find('\n') + start_O_branch
            perent = branches[end_O_branch - 20: end_O_branch]
            if start_O_branch == -1:
                return None
            return perent.strip('\n')



    def add(self, from_where: str, to_where: str=False, onion: bool=True) -> None:
        """\t\tcopies one file outside the .wit file, and copys it and all its belonging to .wit/staging area
        
            inputs:
        from_where: the place from which to take the file
        to_where: the place to copy to the file
        onion: if the original file is inside layers of folders, says if to copy all the unnacacary layers, recommended to keep at true"""
        if to_where == False:
            perent_list: List[str] = from_where.split('/')
            isdirectory, remembrer = True, True   #just to sure          
            for ancastor_n in range(len(perent_list)):
                ancastor: str = '/'.join(perent_list[:ancastor_n + 1])
                isdirectory = True
                try:
                    if '.wit' in os.listdir(ancastor):
                        to_where: str = ancastor + '/.wit'
                        remembrer: int = ancastor_n
                except NotADirectoryError:
                    isdirectory = False
            with open(f'{to_where}/info.txt', 'r') as TXT:
                text: str = TXT.read().split('\n')
            with open(f'{to_where}/info.txt', 'w') as TXT:
                text[0] += f'{from_where.split("/")[-1]}, '
                text[1] += f'~{from_where}'
                TXT.write('\n'.join(text))

            to_where += '/staging_area'
            if to_where == False:
                raise WitNotFoundError("you havn't installed wit yet in any of the parenting files")
            Remembrer: List[str] = from_where.split('/')[remembrer + 1:]
            
            if isdirectory and onion:
                for itam in Remembrer:
                    if not os.path.isdir(f'{to_where}/{itam}'):
                        try:
                            os.mkdir(f'{to_where}/{itam}')
                        except FileExistsError:
                            pass
                        to_where += f'/{itam}'
  
        if os.path.isdir(from_where):
            for file in os.listdir(from_where):
                new_file: str = f'{to_where}/{file}'
                if os.path.isdir('/'.join([from_where,file])):
                    try:   
                        os.mkdir(new_file)
                    except FileExistsError:
                        pass
                    self.add(from_where='/'.join([from_where, file]), to_where=new_file)

                else:
                    copyfile(f'{from_where}/{file}', f'{to_where}/{file}')
        else:
            copyfile(from_where, f'{to_where}/{from_where.split("/")[-1]}')



    @Isthereperent
    def commit(place: str, self, MESSEGE: str, branch: str='HEAD', jenus: str='') -> None:
        """\t\tcopies the files from staging area to a memmory of the files, from which .wit works
        
        \tinputs:
        MESSEGE: the maggage that you want to put in the commit
        branch: in which branch it is working"""
        
        
        addition: str = ''
        length_of_random_string: int = 20
        for UNIMPORTENT in range(length_of_random_string):
            addition += random.choice('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')        
        name: str = f'{place}/images/{addition}'
        HEAD = self._HEAD_HUNTER(place, branch)
        os.mkdir(name)
        self.add(from_where=place + '/staging_area', to_where=name, onion=True)
        with open(f"{name}/{addition}.txt", "w") as file:
            if jenus != '':
                message = f"parent={jenus}\ndate={str(datetime.datetime.now()).strip('aqbcdefghijklmnopqrstuvwxyz[]')}\nmessage={MESSEGE}"  
            else:
                message = f"parent={HEAD}\ndate={str(datetime.datetime.now()).strip('aqbcdefghijklmnopqrstuvwxyz[]')}\nmessage={MESSEGE}"  
            file.write(message)
        with open(f'{place}/info.txt', 'r') as TXT:
            text: str = TXT.read().split('\n')[-1]
        with open(f'{place}/info.txt', 'w') as TXT:
            TXT.write(f'\n{text}')
        with open(f'{place}/refrences.txt', 'r') as quark:
            all_REF = quark.read()
        list_for_message = []
        all_REF = all_REF.replace('=', '\n').split('\n')
        head_HEAD: str = ""
        for line in range(len(all_REF) // 2):
            if all_REF[line * 2] == "|HEAD" or all_REF[line * 2][-8:] == '(active)' and (head_HEAD == all_REF[line * 2 + 1] or all_REF[line * 2 + 1] == 'None'):
                if all_REF[line * 2 + 1] != "None":
                    head_HEAD = all_REF[line * 2 + 1]
                all_REF[line * 2 + 1] = addition
            list_for_message.append(f"{all_REF[line * 2]}={all_REF[line * 2 + 1]}")
        with open(f'{place}/refrences.txt', 'w') as quark:
            quark.write('\n'.join(list_for_message))



    def _check_if_files_equal(self, path_1: str, path_2: str) -> bool:
        """\t\tchacks if two files are eqaual at content.
        
        \tinputs:
        path_1: the first path to the comperison
        path_2: the second path to the comperison"""
        pak = open(path_1, 'rb')
        tack = open(path_2, 'rb')
        return (pak.read() == tack.read())



    def _master_compare(self, PLACE: str) -> str:
        "\t\tchecks if the files in staging area are the same as the ones outside .wit"
        with open(f'{PLACE}/info.txt', 'r') as TXT:
            all_paths: str = TXT.read().split('\n')[1].split('~')
        PLACE = f'{PLACE}/staging_area'
        for path in all_paths:
            for root, UNIMPORTENT, names in os.walk(PLACE):
                for name in names:        
                    if name == path.split('/')[-1]:
                        kath: str = (path + '/' + '/'.join(root.split('\\')[2:])).strip('/')
                        if not self._check_if_files_equal(f'{root}/{name}', f'{kath}'):
                            yield f'{kath}'



    @Isthereperent
    def status(place: str, self) -> None:
        "\t\tprints the status of the current .wit"
        changed_files: str = ''
        for itam in self._master_compare(place):
            changed_files += f'{itam}, '        
        with open(f'{place}/info.txt', 'r') as TXT:
            text: str = TXT.read().split('\n')[0]
        messeage = f"""
        commit ID - {self._HEAD_HUNTER(place)}
        Canges to be commited - {text}
        Changes not staged for commit - {changed_files}
        """
        print(messeage)



    @Isthereperent
    def chackout(place: str, self, branch: str="HEAD", commit_id: str='None') -> None:
        """\t\ttakes all the files from a certin folder inside 'images' and copys it to the needed places
        
        \tinputs:
        branch: the branch in which to do the chackout, if HEAD is entred does the most reacent
        commit_id: if wants a specific file, can put the name of it as commit id and it will chackout as the commit id respective file
        """
        if commit_id == 'None':
            commit_id = self._HEAD_HUNTER(place, branch)
            if commit_id == 'None':
                raise FileNotEcceptableError('you need to do at least one "commit" before doing the chackout function')
        with open(f'{place}/info.txt', 'r') as text:     
            file_content = text.read()
        not_saved: str = file_content.split('\n')[0]
        all_of_perents: str = file_content.split('~')[1:]
        if len(not_saved) > 0:
            if  not str(input('files have not been saved, do you want to continue?')) == 'yeah':
                return None
        for perent in all_of_perents:
            if os.path.isdir(perent):
                for root, dir, files in os.walk(f'{place}/images/{commit_id}'):
                    for Root, Dir, Files in os.walk(perent):
                        for file in files:
                            for File in Files: 
                                if file != f'{commit_id}.txt':
                                    if f'{file}' == f'{File}' and f"{root}/{file}" != f"{Root}/{File}":
                                        copyfile(f"{root}/{file}", f"{Root}/{File}")
            else:
                copyfile(f"{place}/images/{commit_id}/{perent.split('/')[-1]}", perent)

        rmtree(f'{place}/staging_area')
        os.makedirs(f'{place}/staging_area')
        self.add(from_where=f'{place}/images/{commit_id}', to_where=f'{place}/staging_area', onion=False)
        os.remove(f'{place}/staging_area/{commit_id}.txt')
        


    @Isthereperent
    def remove(place: str, self, removing: str) -> None:
        """\t\tremoves a file from staging area without creating probloms
        
        \tinputs:
        removing: the name of the file to remove"""
        removing_end = []
        for krup in removing.split('/')[::-1]:
            if krup == place.split('/')[-2]: # -1 is only getting ".wit" so we use -2
                break
            removing_end.append(krup)
        removing_end = f"{place}/staging_area/{'/'.join(removing_end[::-1])}"
        removing_total = []
        for kurp in range(len(removing_end.split('/')) - 1):
            if len(os.listdir('/'.join(removing_end.split('/')[:kurp + 1]))) <= 1 or kurp in place.split('/'):
                removing_total.append(removing_end.split('/')[kurp + 1])
        removing_total.remove(removing_total[0])
        removing_end = removing_end.split('/')
        for kurp in removing_total:
            removing_end.remove(kurp)
        rmtree('/'.join(removing_end))



    @Isthereperent
    def graph(place: str, self) -> None:
        "\t\tmakes a graph out of all the images"
        Graph = graph_maker.Graph()
        length_of_node_name: int = 6 # must be lower then 21
        for file in os.listdir(f"{place}/images"):
            with open(f'{place}/images/{file}/{file}.txt', 'r') as commit_file:
                commit_file: List[str] = commit_file.read().split('\n')
                perent: str = commit_file[0][7:]
                if perent == 'None':
                    perent = 'origin' # can be whatever you want, recommended that the length of it is lowerthen "length_of_node_name"
                elif len(perent) > 20:
                    perent = perent.split(',')
                    Graph.add_edge(file[:length_of_node_name], perent[1][:length_of_node_name])
                    perent = perent[0]
                Graph.add_edge(file[:length_of_node_name], perent[:length_of_node_name])
        graph_maker.draw(Graph, node_color='cyan', edge_color='navy', with_labels=True)
        plt.savefig(f'{place}/graph.png')
        image = Image.open(f'{place}/graph.png')
        image.show()



    @Isthereperent
    def branch(place: str, self, name: str) -> None:
        """\t\tcreates a branch of which can the images be divided into groups
        
        \tinputs:
        name: the name of the branch, can only be a string which is not already in"""
        if not isinstance(name, str):
            raise NameNotValid('that name is not a string')
        with open(f'{place}/refrences.txt', 'r') as reading_brench:
            content_red: str = reading_brench.read()
        content: List[str] = content_red.replace('\n', '=').split('=')
        for one in range(len(content) // 2):
            if content[one * 2] == name:
                raise NameNotValid('that name is already taken') 
        with open(f"{place}/refrences.txt", 'a') as newpath:
            path: str = self._HEAD_HUNTER(place)
            newpath.write(f'\n|{name}(active)={path}')



    @Isthereperent
    def deactivate_branch(place: str, self, branch: str) -> None:
        """\t\tdeactivates a certin branch so the head of the branch stays the same
        
        \tinputs:
        branch: the branch to disactivate"""
        with open(f'{place}/refrences.txt', 'r') as reading_brench:
            content_of_refrances: str = reading_brench.read()
        list_for_message: List[str] = []
        content: List[str] = content_of_refrances.replace('=', '\n').split('\n')
        for line in range(len(content) // 2):
            if content[line * 2][-8:] == '(active)' and content[line * 2][:-8] == f"|{branch}":
                content[line * 2] = content[line * 2][:-8]
            list_for_message.append(f"{content[line * 2]}={content[line * 2 + 1]}")
        mess: str = '\n'.join(list_for_message)
        with open(f'{place}/refrences.txt', 'w') as quark:
            quark.write(mess)


    @Isthereperent
    def reactivate_branch(place: str, self, branch: str) -> None:
        """\t\treactivates a certin branch so the head of the branch could change
        
        \tinputs:
        branch: the branch to reactivate"""
        with open(f'{place}/refrences.txt', 'r') as reading_brench:
            content_of_refrances: str = reading_brench.read()
        list_for_message: List[str] = []
        content: List[str] = content_of_refrances.replace('=', '\n').split('\n')
        for line in range(len(content) // 2):
            if '(active)' not in content[line * 2] and content[line * 2][:-8] == f"|{branch}":
                content[line * 2] += "(active)"
            list_for_message.append(f"{content[line * 2]}={content[line * 2 + 1]}")
        mess: str = '\n'.join(list_for_message)
        with open(f'{place}/refrences.txt', 'w') as quark:
            quark.write(mess)
        


    def _find_base(self, side_1: str, side_2: str) -> str:
        side1_list: List[str] = [side_1]
        side2_list: List[str] = [side_2]
        reached: str = side_1
        while True:
            with open(side1_list[-1], 'r') as head_search:
                side1_list.append(reached)
                reached = reached.split('/')[:-2]
                perent = head_search.read().replace('\n', '=').split('=')[1]
                reached.append(f"{perent}/{perent}.txt")
                if reached[-1] == '/.txt':
                    break
                reached = '/'.join(reached)
        reached = side_2
        while True:
            with open(side2_list[-1], 'r') as head_search:
                side2_list.append(reached)
                reached = reached.split('/')[:-2]
                perent = head_search.read().replace('\n', '=').split('=')[1]
                reached.append(f"{perent}/{perent}.txt")
                if reached[-1] == '/.txt':
                    break
                reached = '/'.join(reached)
        side1_list = side1_list[::2]
        side2_list = side2_list[::2]
        base: str = ''
        base_score = 0
        for legacy in range(len(side1_list)):
            for Legacy in range(len(side2_list)):
                if side1_list[legacy] == side2_list[Legacy]:
                    if Legacy + legacy <= base_score:
                        base = side1_list[legacy]
                        base_score = Legacy + legacy
        return '/'.join(base.split('/')[:-1])
                         
                         
                         
    @Isthereperent
    def merge(place: str, self, branch_name: str):
        branch_2 = f'{place}/images/{self._HEAD_HUNTER(place)}/{self._HEAD_HUNTER(place)}.txt'
        branch_1 = f'{place}/images/{self._HEAD_HUNTER(place, branch_name)}/{self._HEAD_HUNTER(place, branch_name)}.txt'
        if branch_1.split('/')[-2] == 'None':
            return None
        base: str = self._find_base(branch_1, branch_2)
        HEAD = '/'.join(branch_2.split('/')[:-1])
        branch_path = '/'.join(branch_1.split('/')[:-1])
        rmtree(f'{place}/staging_area')
        os.makedirs(f'{place}/staging_area')
        self.add(from_where=base, to_where=False, onion=False)
        self.add(from_where=branch_path, to_where=False, onion=False)
        os.remove(f'{place}/staging_area/{branch_1.split("/")[-1]}')
        self.commit(MESSEGE='', branch='HEAD', jenus=f'{HEAD.split("/")[-1]},{branch_path.split("/")[-1]}')
        with open(f'{place}/refrences.txt', 'r') as abastos:
            content_of_REF: str = abastos.read()
        start_branch_REF: str = content_of_REF.find(branch_name) 
        end_branch_REF: str = content_of_REF[start_branch_REF:].find('\n')
        if end_branch_REF == -1:
            end_branch_REF = len(content_of_REF)
        branch_all_REF: str = content_of_REF[start_branch_REF - 1:end_branch_REF + 1] #it's - 1 because at start didn't conclude "|" and + 1 in the end because must have +1 to have the full line
        mess_L: List[str] = content_of_REF.split('\n')
        mess_L.remove(branch_all_REF)
        mess: str = '\n'.join(mess_L)
        with open(f'{place}/refrences.txt', 'w') as abastos:
            abastos.write(mess)










            


        

#input('bfv_________')


wheat = Wit()
