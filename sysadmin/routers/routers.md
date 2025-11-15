
**Ubiquiti UniFi / UDM / UDM Pro** can add local DNS hostnames so that it returns custom names mapped to internal IP addresses. The exact features depend on the model and firmware version, but the functionality exists.

---

# ✔️ Can the UDM Pro respond with custom internal DNS names?

Yes — it can, using **Static DNS Entries** via **DNS Forwarding** (previously called “DNS Host Records”).

This allows you to map:

- hostname → internal IP  
    Example:
    
    ```
    nas.home.lan → 192.168.1.50
    git.lan → 192.168.1.60
    myserver.internal → 10.0.0.5
    ```
    

The UDM Pro is _not_ a full authoritative DNS server like BIND or Technitium, but for LAN usage it works well.

---

# 🔧 Where to enable this

On **UDM Pro (UniFi OS 3.x and newer):**

1. Open **UniFi Network → Settings**
    
2. Go to **Networks → Local Networks → DNS**
    
3. Enable **DNS Forwarding**
    
4. Click **Add Hostname**
    
5. Fill in:
    
    - **Hostname**: `nas`
        
    - **Domain**: `home.lan` (or your custom internal domain)
        
    - **IP Address**: `192.168.1.50`
        

After saving, the entire LAN will use this entry automatically (via DHCP or direct DNS queries).

---

# ✔️ Result

UDM Pro will now reply:

```
nslookup nas.home.lan 192.168.1.1
→ 192.168.1.50
```

---

# 🧩 Limitations

To give you a precise picture:

- **No wildcard DNS** (*.example.lan)
    
- **No full DNS zone management**
    
- **No manual PTR records** (reverse DNS)
    
- **No split-horizon control per interface**
    

If you need more advanced DNS features, run a DNS server on a Raspberry Pi:

✔️ Technitium DNS  
✔️ dnsmasq  
✔️ Bind9

Then configure UDM Pro to use that server as your DHCP DNS provider.

---

