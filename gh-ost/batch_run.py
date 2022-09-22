

import sqlparse
import os
import argparse
from subprocess import Popen, PIPE, CalledProcessError

CUT_OVER_FLAG_FILE = '/tmp/ghost.cutover.flag'
CONTAINER_NAME = 'gh-ost'

def run_sql_by_gh_ost(sql, interactive_mode, db_infos):
    # Parse the SQL
    sql = sqlparse.format(sql, strip_comments=True).strip()
    sql = sql.replace('`', '')
    statements = sqlparse.parse(sql)
    for statement in statements:
        type = statement.get_type()
        if type == 'ALTER':
            query = str(statement).strip()
            tokens = query.strip().split(' ')
            table = tokens[2]
            command = ' '.join(tokens[3:])
            shell_command = generate_ghost_command(table, command,db_infos)
            if interactive_mode:
                ans = input(f'Going to run `{query}` by Github gh-ost, ready (Y/N) ?\n')
                if ans.strip() not in ('Y', 'y'):
                    print('Process terminated')
                    return 
            for line in run(shell_command):
                pass
        

def generate_ghost_command(table, command, db_infos):
    command = f"""
    docker run -i -t bonty/gh-ost:latest --name {CONTAINER_NAME}\\
        --host="{db_infos['repl_host']}" \\
        --port="{db_infos['repl_port']}" \\
        --initially-drop-old-table \\
        --initially-drop-ghost-table \\
        --max-load=Threads_running=25 \\
        --critical-load=Threads_running=1000 \\
        --chunk-size=1000 \\
        --max-lag-millis=1500 \\
        --user="{db_infos['user']}" \\
        --password="{db_infos['pwd']}" \\
        --database="{db_infos['db']}" \\
        --table="{table}" \\
        --verbose \\
        --alter="{command}" \\
        --assume-rbr \\
        --allow-master-master \\
        --cut-over=default \\
        --exact-rowcount \\
        --concurrent-rowcount \\
        --default-retries=120 \\
        --panic-flag-file=/tmp/ghost.panic.flag \\
        --assume-master-host="{db_infos['master_host']}:{db_infos['master_port']}" \\
    """
    if interactive_mode:
        command += f"    --postpone-cut-over-flag-file={CUT_OVER_FLAG_FILE} --execute"
    return command


"""
    Run the command in another process, and monitor its
    standard output. When output match the pattern, we 
    can decide corresponding action.    
"""
def run(shell_cmd):
    with Popen(shell_cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            yield line

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)


"""
    When gh-ost already prepare the copied table and ready to
    switch table, we can use this function to remove the flag
    then table will be switched by gh-ost
"""
def switch():
    command = f'docker run {CONTAINER_NAME} "rm {CUT_OVER_FLAG_FILE}"'
    os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script for batch running MySQL DDL')
    parser.add_argument('sql_file', type=str, help='The sql file which contain DDL(alter table commands)')
    parser.add_argument('-master-host', type=str, help='The host of master MySQL', required=True)
    parser.add_argument('-master-port', type=str, help='The port of master MySQL', required=True)
    parser.add_argument('-repl-host', type=str, help='The host of replica MySQL', required=True)
    parser.add_argument('-repl-port', type=str, help='The replica MySQL host', required=True)
    parser.add_argument('-db', type=str, help='The database to run DDL', required=True)
    parser.add_argument('-user', type=str, help='The user name of both MySQL', required=True)
    parser.add_argument('-pwd', type=str, help='The password of both MySQL', required=True)
    parser.add_argument('--no-interactive', action='store_true', default=False)

    args = parser.parse_args()
    sql_file = args.sql_file
    interactive_mode = not args.no_interactive
    db_infos = {
        'master_host': args.master_host,
        'master_port': args.master_port,
        'repl_host': args.repl_host,
        'repl_port': args.repl_port,
        'db': args.db,
        'user': args.user,
        'pwd': args.pwd,
    }

    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    run_sql_by_gh_ost(sql, interactive_mode, db_infos)
    