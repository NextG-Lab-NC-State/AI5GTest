#############################################################

# Copyright 2025 North Carolina State University

# Authored by
# Pranshav Gajjar, Abiodun Ganiyu, and Vijay K. Shah
# NextG Wireless Lab, North Carolina State University

############################################################# 

import argparse
import subprocess
import ipaddress
import sys
import pyshark
import json
import signal
import os

class PacketCapture:
    def __init__(self, **kwargs):
        print("*" * 90)
        print("*" + " " * 88 + "*")
        print("*" + " " * 88 + "*")
        print("*" + " " * 13 + "Welcome to Anonymous Packet Capture/Processing Tool" + " " * 24 + "*")
        print("*" + " " * 12 + "Use --help to see the available options and usage type" + " " * 21 + " *")
        print("*" + " " * 88 + "*")
        print("*" + " " * 88 + "*")
        print("*" * 90)
        
        self.option = kwargs.get("option")
        self.du_ip = kwargs.get("du_ip", "")
        self.cu_ip = kwargs.get("cu_ip", "")
        self.amf_ip = kwargs.get("amf_ip", "") 
        self.output_file = kwargs.get("output")
        self.file_1 = kwargs.get("file_1")
        self.file_2 = kwargs.get("file_2", "")
        self.file_3 = kwargs.get("file_3", "")
        self.pcap_files = [f for f in [self.file_1, self.file_2, self.file_3] if f]
        
        if not self.option:
            raise ValueError("No option provided.")
        self.__execute_process()
        
    def __execute_process(self):
        if self.option.lower() == 'process':
            if not self.pcap_files:
                raise ValueError("Please provide at least one input pcap file using --file_1")
            self.process_pcap()
            
        elif self.option.lower() == 'capture':
            print("Live Capturing started. Capturing packets using tcpdump...")
            output_pcap = f"./record/{self.output_file}.pcap"
            # print(len(self.pcap_files), self.pcap_files)
            base_ports = (
                "udp port 9999 or udp port 2152 or sctp or "
                "port 38462 or port 38472 or port 38412 or port 2153"
            )
            
            host_filters = []
            for ip in [self.du_ip, self.cu_ip, self.amf_ip]:
                if ip:
                    host_filters.append(f"host {ip}")
            if host_filters:
                combined_filter = f"({' or '.join(host_filters)}) and ({base_ports})"
                print(f"Capturing filtered traffic to/from: {', '.join(host_filters)}")
            else:
                combined_filter = base_ports
                print("Capturing all matching traffic on any interface")
            
            tcpdump_cmd = [
                "sudo", "tcpdump", "-n", "-iany",
                combined_filter,
                "-w", output_pcap
            ]
            
            process = subprocess.Popen(" ".join(tcpdump_cmd), shell=True, preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN))
            try:
                user_input = input("\nCapture running. Enter 'yes' to stop: \n").strip().lower()
                while user_input != "yes":
                    user_input = input("Please type 'yes' to stop capture: \n").strip().lower()
            finally:
                print("Stopping tcpdump capture...")
                process.terminate()
                process.wait()

                print("Capture stopped. Processing captured packets...")
                self.file_1 = output_pcap
                self.pcap_files = [self.file_1]
                self.process_pcap()
            
    
    def process_pcap(self):
        if len(self.pcap_files) == 0:
            raise ValueError("No PCAP files to process.")
        capture_file = f"./record/merged_{os.path.splitext(self.output_file)[0]}.pcapng"

        # run mergecap with all of the specified input files
        mergecapResult = subprocess.run(["mergecap", "-w", capture_file] + self.pcap_files)

        if (mergecapResult.returncode != 0):
            print(mergecapResult.stderr)
            print("Mergecap error, exiting")
            sys.exit(1)
            
        cap = pyshark.FileCapture(capture_file, custom_parameters=[
            "-o", 'uat:user_dlts:"User 5 (DLT=152)","ngap","0","","0",""',
            "-o", 'uat:user_dlts:"User 7 (DLT=154)","f1ap","0","","0",""',
            "-o", 'uat:user_dlts:"User 2 (DLT=149)","udp","0","","0",""',
            "-o", "nas-5gs.null_decipher:TRUE",
            "-o", "mac-nr.attempt_rrc_decode:TRUE",
            "-o", "mac-nr.attempt_to_dissect_srb_sdus:TRUE",
            "-o", "mac-nr.lcid_to_drb_mapping_source:From configuration protocol",
            "--enable-heuristic", "mac_nr_udp"
        ])

        jsonArray = []
        escapeChars = ['\n', '\t']

        def removeEscapes(field):
            newField = field
            for escape in escapeChars:
                newField = newField.replace(escape, '')

            return newField

        for packet in cap:
                packetLayers = {}

                for layer in packet.layers:
                    layerFields = layer._get_all_field_lines()
                    layerFields = list(map(removeEscapes, layerFields))                
                    # print(layerFields)

                    packetLayers[layer.layer_name] = layerFields

                jsonArray.append(packetLayers)

        self.save_output(jsonArray)
            
    def save_output(self, jsonArr):
        with open(self.output_file if self.output_file.endswith('.json') else self.output_file + ".json", "w") as json_output:
            json.dump(jsonArr, json_output, indent=4)
        print(f"Output saved to: {self.output_file}.json")
        

def validate_ip(addr):
    try:
        ipaddress.ip_address(addr)
        return addr
    except ValueError:
        raise argparse.ArgumentError(f"Invalid IP address: {addr}")

parser = argparse.ArgumentParser(description="This is an automated packet capture and processing tool to capture/anaylze 5G protocol signaling interactions.")
parser.add_argument("-option", help="use `process` if you have the packet files and `capture` to capture live packet")
parser.add_argument("--output_file", default="output", help="path to save the processed file")
parser.add_argument("--du_ip", type=validate_ip, help="the IP address of the server hosting the DU (optional)")
parser.add_argument("--cu_ip", type=validate_ip, help="the IP address of the server hosting the CU (optional)")
parser.add_argument("--amf_ip", type=validate_ip, help="the IP address of the AMF (optional)")
parser.add_argument("--file_1", help="input pcap file 1")
parser.add_argument("--file_2", help="input pcap file 2")
parser.add_argument("--file_3", help="input pcap file 3")


args = parser.parse_args()

    
try:
    PacketCapture(
        option=args.option,
        output=args.output_file,
        file_1=args.file_1,
        file_2=args.file_2,
        file_3=args.file_3,
        du_ip=args.du_ip,
        cu_ip=args.cu_ip,
        amf_ip=args.amf_ip
    )
except Exception as e:
    print(f"{e}")
    sys.exit(1)