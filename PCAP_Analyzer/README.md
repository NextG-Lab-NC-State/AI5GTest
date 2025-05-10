# Anonymous Lab Packet Capture & Processing Tool

This tool enables automated packet capture and processing of 5G O-RAN protocol traffic.  
It supports both live capture (via `tcpdump`) and offline `.pcap` file processing, decoding essential protocol layers like F1AP, NGAP, NAS-5GS, and MAC-NR, and exporting results in structured JSON format.

---

## ✅ Features

- Live packet capture using `tcpdump`, with user-controlled stop
- Merge and process up to 3 `.pcap` files
- Decode key 5G protocol layers using Wireshark and PyShark
- Export captured/decoded data to a structured JSON file
- Flexible support for both disaggregated (multi-system) and loopback (single-host) 5G setups

---

## ⚙️ Requirements

**System Tools**  
- Python 3.7+
- `tcpdump`
- `mergecap` (Wireshark CLI utility)

**Python Packages**  
Install using pip:


---

## 🔐 Running with Root Permissions

To capture packets on network interfaces, this script **must be run with sudo**:


Alternatively, you may grant `tcpdump` special permissions using `setcap` or by editing `/etc/sudoers`, but running the script with `sudo` is the simplest and safest approach.

---

## 🧰 Usage

### 1. Process Existing `.pcap` Files

To decode previously captured files:

```bash 
sudo python3 packet_capture.py -option process --file_1 /path_to_file/f1ap.pcap --output_file decoded.json
```
 You may also merge up to three `.pcap` files:

```bash
sudo python3 packet_capture.py -option process --file_1 f1ap.pcap --file_2 ngap.pcap --file_3 mac.pcap --output_file full.json
```

---

### 2. Live Capture from Network Interface

Capture live traffic on key O-RAN/5G interfaces and ports:

```bash
sudo python3 packet_capture.py -option capture --output_file live.json
```

You will be prompted to type `yes` when you're ready to stop capturing. The captured packets will then be processed and decoded into a JSON file.

---

### 3. Live Capture Filtered by CU/DU/CN IPs

If your DU, CU, or CN are hosted on different machines, you can limit the capture to those IPs:

```bash
sudo python3 packet_capture.py -option capture --du_ip 10.10.1.2 --cu_ip 10.10.1.3 --amf_ip 10.10.1.4 --output_file filtered.json
```

This improves performance by capturing only relevant traffic.

---

## 📁 Output

The processed output is saved as a JSON file (named via `--output_file`).  
Each JSON entry represents one packet with all its decoded protocol layers.
Example:
```json
[{
        "user_dlt": [],
        "ngap": [
            "NGAP-PDU: initiatingMessage (0)",
            "initiatingMessage",
            "procedureCode: id-NGSetup (21)",
            "criticality: reject (0)",
            "value",
            "NGSetupRequest",
            "protocolIEs: 4 items",
            "Item 0: id-GlobalRANNodeID",
            "ProtocolIE-Field",
            "id: id-GlobalRANNodeID (27)",
            "GlobalRANNodeID: globalGNB-ID (0)",
            "globalGNB-ID",
            "pLMNIdentity: 00f110",
            "Mobile Country Code (MCC): Unknown (1)",
            "Mobile Network Code (MNC): Unknown (01)",
            "gNB-ID: gNB-ID (0)",
            "gNB-ID: 00066c [bit length 22, 2 LSB pad bits, 0000 0000  0000 0110  0110 11.. decimal value 411]",
            "RANNodeName: cu_cp_01",
            "SupportedTAList: 1 item",
            "SupportedTAItem",
            "tAC: 7 (0x000007)",
            "broadcastPLMNList: 1 item",
            "BroadcastPLMNItem",
            "tAISliceSupportList: 1 item",
            "SliceSupportItem",
            "s-NSSAI",
            "sST: 01",
            "PagingDRX: v256 (3)",
            "criticality: reject (0)",
            "criticality: ignore (1)",
            "criticality: reject (0)",
            "criticality: ignore (1)",
            "value",
            "value",
            "value",
            "value",
            "Item 1: id-RANNodeName",
            "Item 2: id-SupportedTAList",
            "Item 0",
            "Item 0",
            "Item 0",
            "Item 3: id-DefaultPagingDRX",
            "ProtocolIE-Field",
            "ProtocolIE-Field",
            "ProtocolIE-Field",
            "id: id-RANNodeName (82)",
            "id: id-SupportedTAList (102)",
            "id: id-DefaultPagingDRX (21)",
            "pLMNIdentity: 00f110",
            "Mobile Country Code (MCC): Unknown (1)",
            "Mobile Network Code (MNC): Unknown (01)"
        ]
    }
]

```
Temporary .pcapng files used during processing are stored in ```./record``` and may be removed manually.


