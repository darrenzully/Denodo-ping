import os
import subprocess

def ping(denodo_home_path: str, trust_path: str, hostname: str, timeout: str, vdbname: str, usr: str, passwd: str):
    lib_path_vdp = os.path.join(denodo_home_path, "lib")
    denodo_classpath = os.pathsep.join([
        os.path.join(lib_path_vdp, "vdp-client-core", "denodo-vdp-client.jar"),
        os.path.join(lib_path_vdp, "contrib", "denodo-asyncrmi.jar"),
        os.path.join(lib_path_vdp, "vdp-client-core", "denodo-vdp-tool.jar"),
        os.path.join(lib_path_vdp, "contrib", "commons-util.jar"),
        os.path.join(lib_path_vdp, "contrib", "commons-codec.jar"),
        os.path.join(lib_path_vdp, "contrib", "commons-collections4.jar"),
        os.path.join(lib_path_vdp, "contrib", "commons-lang3.jar"),
        os.path.join(lib_path_vdp, "contrib", "commons-pool2.jar"),
        os.path.join(lib_path_vdp, "contrib", "icu4j.jar"),
        os.path.join(lib_path_vdp, "contrib", "log4j-api.jar"),
        os.path.join(lib_path_vdp, "contrib", "log4j-core.jar")
    ])
    
    conf_path_vdp = os.path.join(denodo_home_path, "conf")
    dbtools_path = os.path.join(conf_path_vdp, "db-tools")
    if os.path.exists(conf_path_vdp) and not os.path.exists(dbtools_path):
        denodo_classpath = os.pathsep.join([denodo_classpath, conf_path_vdp])
    elif os.path.exists(dbtools_path):
        denodo_classpath = denodo_classpath = os.pathsep.join([denodo_classpath, dbtools_path])
    else:
        denodo_classpath = os.pathsep.join([denodo_classpath, dbtools_path])
 
    java_opts = "-Djavax.net.ssl.trustStore=" + trust_path
    ping_command = f"java {java_opts} -classpath {denodo_classpath} com.denodo.vdb.vdbinterface.client.tools.Ping -t {timeout} \
        -q SELECT_1 -l {usr} -p {passwd} -v {hostname}/{vdbname}"

    print(f"Pinging {hostname} - {vdbname}")
    p_commands = ping_command.split(" ")
    commands = [command.replace('SELECT_1', 'SELECT 1') for command in p_commands]
    completed_process = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if "ping OK!" in completed_process.stdout:
        response_time = completed_process.stdout.split("Response time:")[1]
        print(f"Ping to {vdbname}: OK!! {response_time}")
    else:
        ping_command_host = f"java {java_opts} -classpath {denodo_classpath} com.denodo.vdb.vdbinterface.client.tools.Ping -t {timeout} -v {hostname}"
        completed_process_host = subprocess.run(ping_command_host.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        if "ping OK!" in completed_process_host.stdout:
            response_time = completed_process_host.stdout.split("\n")[1]
            print(f"Ping to {hostname}: OK!! {response_time}")
        else:
            return f"{hostname} - {vdbname} is not responding."

    
