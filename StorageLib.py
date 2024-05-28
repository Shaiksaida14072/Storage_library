import re
import time
from connect import SSHClient
client=SSHClient('192.168.0.111','winteck','Winteck@2024')

class Storage_cmds:

    def list_drives(self):
        try:
            drives_list=[]
            exec_cmd=client.exec_command('lsblk')
            out_drives=re.findall('sd[a-z]+',exec_cmd)
            out_drives=set(out_drives)
            for drives in out_drives:
                drives_list.append('/dev/'+drives)
            return (f'The list of drives :: {drives_list}')
        except Exception as err:
            print(f'error found \n{err}')




    def list_firmware_version_of_all_drives(self):
        try:
            drives_list = []
            exec_cmd = client.exec_command('lsblk')
            out_cmd = re.findall('sd[a-z]+', exec_cmd)
            out_cmd = set(out_cmd)
            for drives in out_cmd:
                drives_list.append('/dev/' + drives)
            for drives in drives_list:
                exec_cmd=client.exec_command('smartctl -a '+drives)
                Firmware_version=re.search('F[a-z]+ V[a-z]+:\s+\w+',exec_cmd)
                Revision=re.search('R[a-z]+:\s+\w+',exec_cmd)
                if Firmware_version:
                    print('The firmware version of\t'+drives+' :: '+Firmware_version.group())
                elif Revision:
                    print('The firmware version of\t'+drives+' :: '+Revision.group())
        except Exception as errinfo:
            print(f'error found \n{errinfo}')



    def list_partitions(self):
        try:
            exec_cmd=client.exec_command('lsblk -l')
            out_drive=re.findall('sd[a-z][0-9]',exec_cmd)
            return (f'The partitions on drives are :: {out_drive}')
        except Exception as errinfo:
            print(f"error found \n{errinfo}")


    def create_partition(self):
        try:
            drive_name=input('Enter drive name :: ')
            partition_on_this_drive=client.exec_command('lsblk -l')
            prtns=re.findall(f'{drive_name}[0-9]+',partition_on_this_drive)
            if prtns!=[]:
                 print(f'The partitions on this drive\t{prtns}')
            elif prtns==[]:
                print(f'There are no partitions on this {drive_name} drive')
            time.sleep(2)
            type_partition=input('Please enter new partition or delete partition :: ')
            if 'n' in type_partition:
                pri_exn=input('please enter primary or extended partition :: ')
                partition_num=input('Enter partition number :: ')
                size=input('Enter your size of partiton :: ')
                exec_cmd=client.exec_command(f"echo -e '{type_partition}\n{pri_exn}\n{partition_num}\n\n{size}\nw\n' | fdisk /dev/{drive_name}")
                print('created partitions')
            elif 'd' in type_partition:
                exec_cmd=client.exec_command(f"echo -e '{type_partition}\n\n\n\n\nw\n' | fdisk /dev/{drive_name}")
                print('Partitions on this drive are deleted')
            else:
                print(f'Please enter :: n for new prtition\n\t\t\t :: d for delete partition')
            return
        except Exception as errinfo:
            print(f'error found :: {errinfo}')




    def create_file_system(self):
        drive_name=input('To make filesystem enter drive name :: ')
        file_type=input('Enter filesystem format :: ')
        exec_cmd=client.exec_command(f'mkfs{file_type} /dev/{drive_name}')
        mkdir=input('create a directory to mount :: ')
        exec_cmd_mkdir=client.exec_command(f'mkdir {mkdir}')
        exec_cmd_mnt=client.exec_command(f'mount /dev/{drive_name} {mkdir}')
        check=input('Do you want to check the filesystem is created or not :: [Y] for yes :: [N] for no : ')
        if check =='Y':
            exec_cmd1=client.exec_command('df -Th')
            print(exec_cmd1)
        elif check =='N':
            pass
        else:
            print('please give [Y] for yes :: [N] for no')
        return


    def get_cpu_model(self):
        exec_cmd=client.exec_command('lscpu')
        match=re.search('M[a-z]+ [a-z]+:\s+[A-Z][a-z]+\([A-Z]\) [A-Z][a-z]+\([A-Z]\) [A-Z]+ [A-Z][0-9]-[0-9]+ [0-9] @ [0-9].[0-9]+[A-Z]+[a-z]',exec_cmd)
        return (f'The CPU model name is ::\n{match.group()}')


    def get_pci_card_model(self):
        exec_cmd=client.exec_command('lspci -vmm')
        print(exec_cmd)
        return


    def get_free_ram(self):
        exec_cmd=client.exec_command('free -h')
        free_ram=re.findall('[0-9]+Gi',exec_cmd)
        return (f'free ram :: {free_ram[2]}')


    def get_used_ram(self):
        exec_cmd=client.exec_command('free -h')
        free_ram=re.findall('[0-9]+Gi|[0-9]+.[0-9]+Gi',exec_cmd)
        return (f'used ram :: {free_ram[1]}')

    def create_raid(self,raid_array,raid_level,*no_of_drives):
        from create_raid import creation_raid
        exec_cmd=client.exec_command(f'echo -e y | mdadm -C /dev/{raid_array} -l{raid_level} -n{no_of_drives} {no_of_drives}')
        print(exec_cmd)

    def check_raid_arrays(self):
        client.exec_command('Winteck@2024 | sudo su root')
        exec_cmd=client.exec_command('cat /proc/mdstat')
        out = re.findall("md\d+\s+:\s+[a-z]+\s+[a-z]+\d+\s+sd[a-z]\[\d+\]", exec_cmd)
        if out:
            print (f'raid arrays {out}')
        else:
            print ('No Raid arrays are there')

    def stop_raid(self):
        exec_cmd = client.exec_command('cat /proc/mdstat')
        out = re.findall("md\d+|md\s+:\s+[a-z]+\s+[a-z]+\d+\s+sd[a-z]\[\d+\]", exec_cmd)
        if out:
            print(f'created raids are :: {out}')
            i=input('If u want to stop the raid array give raid array-name\t::\t')
            if i:
                ecec_cmd1=client.exec_command(f'mdadm -S /dev/{i}')
            else:
                print(f'please enter correct raid_aray\t::\t{i}')
        else:
            print('There are no raids created')

    def check_processor(self):
        exec_cmd=client.exec_command('dmidecode -t processor')
        print(exec_cmd)

a=Storage_cmds()
a.stop_raid()
# a.create_raid('md5','5','3','/dev/sdf /dev/sdg /dev/sdh')
# a.get_free_ram()
# / dev / sdf, / dev / sdg, and / dev / sdh.



