from __future__ import with_statement
import os
from time import time
from io import StringIO
from tempfile import NamedTemporaryFile

from fabric.api import local, env, run, cd, get
from fabric.decorators import task
from fabric.contrib.files import exists, upload_template

env.use_ssh_config = True   # Hacer uso del archivo de configuración SSH
env.hosts = ['serial-macevedo'] # El nombre que indicamos en nuestro archivo ~/.ssh/config

releases_dir = "/var/www/blog/releases"
git_branch = "master"
git_repo = "git@github.com:maria-noel/blog.git"
repo_dir = "/var/www/blog/repo"
persist_dir = "/var/www/blog/persist"
next_release = "%(time).0f" % {'time': time()}
current_release = "/var/www/blog/current"
# Nuevas variables 
last_release_file = "/var/www/blog/LAST_RELEASE"
current_release_file = "/var/www/blog/CURRENT_RELEASE"

@task
def deploy():
    init()
    update_git()
    create_release()
    build_site()
    swap_symlinks()


# Creamos la tarea de rollback
@task
def rollback():
    last_release = get_last_release()
    current_release = get_current_release()

    rollback_release(last_release)

    write_last_release(current_release)
    write_current_release(last_release)


# Obtenemos el último release
def get_last_release():
    fd = StringIO()
    get(last_release_file, fd)
    return fd.getvalue()

# Obtenemos el release actual
def get_current_release():
    fd = StringIO()
    get(current_release_file, fd)
    return fd.getvalue()

# Guardamos el nombre de nuestro último release en la variable last_release_file
def write_last_release(last_release):
    last_release_tmp = NamedTemporaryFile(delete=False)
    last_release_tmp.write("%(release)s")
    last_release_tmp.close()

    upload_template(last_release_tmp.name, last_release_file, {'release':last_release}, backup=False)
    os.remove(last_release_tmp.name)

# Guardamos el nombre de nuestro release actual en la variable current_release_file
def write_current_release(current_release):
    current_release_tmp = NamedTemporaryFile(delete=False)
    current_release_tmp.write("%(release)s")
    current_release_tmp.close()

    upload_template(current_release_tmp.name, current_release_file, {'release':current_release}, backup=False)
    os.remove(current_release_tmp.name)

# Hacemos el rollback y apuntamos los symlinks hacia el release utilizado anteriormente
def rollback_release(to_release):
    release_into = "%s/%s" % (releases_dir, to_release)
    run("ln -nfs %s %s" % (release_into, current_release))
    run("sudo service php7.0-fpm reload")

# Inicializamos el build
def init():
    if not exists(releases_dir):
        run("mkdir -p %s" % releases_dir)

    if not exists(repo_dir):
        run("git clone -b %s %s %s" % (git_branch, git_repo, repo_dir))

    if not exists("%s/storage" % persist_dir):
        run("mk/var/www/blog/CURRENT_RELEASEdir -p %s/storage/app/public" % persist_dir)
        run("mkdir -p %s/storage/framework/cache" % persist_dir)
        run("mkdir -p %s/storage/framework/sessions" % persist_dir)
        run("mkdir -p %s/storage/framework/views" % persist_dir)
        run("mkdir -p %s/storage/logs" % persist_dir)

def update_git():
	with cd(repo_dir):
		run("git checkout %s" % git_branch)	
		run("git pull origin %s" % git_branch)

# Creamos directorio de release
def create_release():
    release_into = "%s/%s" % (releases_dir, next_release)
    # Creamos el directorio del release
    run("mkdir -p %s" % release_into)
    with cd(repo_dir):
        # Ponemos el contenido de github en el directorio del release
        run("git archive --worktree-attributes %s | tar -x -C %s" % (git_branch, release_into))


# Construimos nuestro sitio
def build_site():
    with cd("%s/%s" % (releases_dir, next_release)):
        # Instalamos dependencias de composer
        run("composer install")
 
# Actualizamos symlinks
def swap_symlinks():
    # Ruta de nuestro nuevo release
    release_into = "%s/%s" % (releases_dir, next_release)

    # Actualizamos symlinks
    run("ln -nfs %s/.env %s/.env" % (persist_dir, release_into))
    run("rm -rf %s/storage" % release_into)
    run("ln -nfs %s/storage %s/storage" % (persist_dir, release_into))

    run("ln -nfs %s %s" % (release_into, current_release))

    write_last_release(get_current_release())
    write_current_release(next_release)
    # Reiniciamos PHP
    run("sudo service php7.2-fpm reload")
