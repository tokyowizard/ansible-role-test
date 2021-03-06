import click
import os
import sys


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.argument('path', default='.')
def init(path):
    """
    Create the test folder with a default test file
    """
    tasks_file = os.path.join(path, 'tasks/main.yml')
    meta_file = os.path.join(path, 'meta/main.yml')

    if not os.path.exists(tasks_file) and \
            not os.path.exists(meta_file):
        click.echo('error: no task or meta file found, aborting')
        sys.exit(2)

    tests_path = os.path.join(path, 'tests')
    tests_file = os.path.join(tests_path, 'main.yml')

    if os.path.exists(tests_file):
        click.echo('error: tests already exists, aborting')
        sys.exit(1)

    # derive role name from folder name or meta file
    role_name = os.path.basename(os.path.realpath(path))

    os.makedirs(tests_path)
    with open(tests_file, 'w') as fd:
        fd.write("""--- # Generated by ansible-role-test {version}
# The name of your test
name: "{role_name}"
# The containers you will use for this test, you could for example spawn a debian
# centos, ubuntu, etc... and run the tests on "all" hosts
# If skipped, tests will be run on every containers available
#containers:
#  master1: 'centos:6'
#  slave1:
#    image: 'centos:7'
#    vars:
#      host_var1: foobar # defines host_var1 on this host on particular
#  slave2: 'centos:7'
#  slave3: 'debian:wheezy'
# You can also setup custom inventory groups to be declared in the inventory, if
# no containers are declared above, they will be merged with the default groups.
# For exemple the following declaration will create 2 groups, master and slaves.
#groups:
#  masters:
#  - master1
#  slaves:
#  - slave1
#  - slave2
#  - slave3
# This is your test playbook
playbook:
- hosts: all
  sudo: true
# You should have your role called in roles, with the proper variables set, you
# can call the same role several times in a row but I'd rather recommend creating
# separate test files for each call to ensure that they run in a clean env
  roles:
# "@ROLE_NAME@" is a magic variable that will be replaced by the name of the role
# on your filesystem before running the tests
  - role: "@ROLE_NAME@"
# Some extra variables if necessary
#    var1: something
#    var2: something
# You should verify that your role executed properly here, using tasks
#  tasks:
#  - name: "Check that my-role did that thing properly"
#    module: do-something
""".format(
            version='0.1.0',
            role_name=role_name.capitalize()
        ))

    click.echo('Created empty test file in {tests_file}'.format(tests_file=tests_file))
