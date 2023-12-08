#!/usr/bin/python3
"""
script that distributes archive to webservers
"""
import os.path
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import datetime


env.hosts = ['100.26.214.3', '54.165.188.189']
env.user = 'ubuntu'

#!/usr/bin/python3
"""
file to practice use of Fabric
"""
from fabric.api import *
from datetime import datetime


def do_pack():
    """ generates a .tgz archive from the contents of the web_static

    All files in the folder web_static must be added to the final archive.
    All archives must be stored in the folder versions.
    The name of the archive created must be:
        web_static_<year><month><day><hour><minute><second>.tgz
    The function do_pack must return the archive path if the archive has
    been correctly generated. Otherwise, it should return None.

    Returns:
        fabric.operations._AttributeString: archive path.
    """
    timestr = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        # create folder versions if it doesn’t exist
        local("mkdir -p versions")
        # extract the contents of a tar archive
        local(f"tar -cvzf versions/web_static_{timestr}.tgz web_static/")
        return ("versions/web_static_{}.tgz".format(timestr))
    except BaseException:
        return None
    
def do_deploy(archive_path):
    """distributes an archive to your web servers.

    Args:
        archive_path (string): path to archive

    Returns:
        Boolean: whether the archive is distributed or not
    """
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        # Uncompress the archive to the folder,
        # /data/web_static/releases/<archive filename without extension>
        # on the web server
        new_comp = archive_path.split("/")[-1]
        new_folder = ("/data/web_static/releases/" + new_comp.split(".")[0])
        # upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Create new directory for release
        run("sudo mkdir -p {}".format(new_folder))
        # Untar archive
        run("sudo tar -xzf /tmp/{} -C {}".
            format(new_comp, new_folder))
        # Delete the archive from the web server
        run("sudo rm /tmp/{}".format(new_comp))
        # Move extraction to proper directory
        run("sudo mv {}/web_static/* {}/".format(new_folder, new_folder))
        # Delete first copy of extraction after move
        run("sudo rm -rf {}/web_static".format(new_folder))
        # Delete the symbolic link /data/web_static/current from the web server
        run('sudo rm -rf /data/web_static/current')
        # Create new the symbolic link /data/web_static/current on web server,
        # linked to the new version of your code,
        # (/data/web_static/releases/<archive filename without extension>
        run("sudo ln -s {} /data/web_static/current".format(new_folder))

        print('New version deployed!')
        return True
    except Exception:
        return False
