import sys
import os
sys.path.append(snakemake.config['paths']['mcc_path'])
import scripts.mccutils as mccutils
import subprocess

def main():
    install_path = snakemake.config['paths']['install']+"/tools/"
    mccutils.remove(snakemake.params.zipfile)
    download_success = mccutils.download(snakemake.params.url, snakemake.params.zipfile, md5=snakemake.params.md5, max_attempts=3)

    if not download_success:
        print("temp download failed... exiting...")
        print("try running --install with --clean for clean installation")
        sys.exit(1)

    mccutils.remove(snakemake.config['paths']['install']+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1")
    command = ["unzip", snakemake.params.zipfile]
    mccutils.run_command(command, log=snakemake.params.log)

    mccutils.remove(install_path+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1")
    command = ["mv", snakemake.config['paths']['install']+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1", install_path]
    mccutils.run_command(command, log=snakemake.params.log)

    mccutils.remove(install_path+"temp")
    mccutils.mkdir(install_path+"temp")
    for f in os.listdir(install_path+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1"):
        command = ["mv", install_path+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1/"+f, install_path+"temp"]
        mccutils.run_command(command, log=snakemake.params.log)


    command = ["patch", "-i", snakemake.params.patch, install_path+"temp/scripts/TEMP_Absence.sh"]
    mccutils.run_command(command,log=snakemake.params.log) 

    mccutils.remove(install_path+"TEMP-d2500b904e2020d6a1075347b398525ede5feae1")
    mccutils.remove(snakemake.params.zipfile)

if __name__ == "__main__":                
    main()