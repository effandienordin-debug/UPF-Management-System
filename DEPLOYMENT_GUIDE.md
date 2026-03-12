# Windows Server 2025 Deployment Guide
## UPF Management System

This guide provides instructions for deploying the **UPF Management System** to a production environment on **Windows Server 2025**.

---

### **Prerequisites**
1.  **Python 3.9+**: Download and install from [python.org](https://www.python.org/).
2.  **PostgreSQL**: Install locally or use a cloud database (like Supabase).
3.  **Git**: For cloning the repository.
4.  **Visual C++ Build Tools**: Required for some Python dependencies (like `pyroaring`).

---

### **Step 1: System Configuration**
1.  **Environment Variables**: 
    Copy the template `.env` file to the server's root directory. Update it with production values:
    ```env
    DATABASE_URL=postgresql://your_user:your_pass@your_host:5432/your_db
    SECRET_KEY=generate_a_strong_random_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```

2.  **Firewall Configuration**:
    Open the following ports in Windows Defender Firewall:
    - **8000**: Backend API (FastAPI)
    - **8501**: Frontend Dashboard (Streamlit)
    - **5432**: PostgreSQL (if running locally)

---

### **Step 2: Database Migration**
1.  Initialize your database by running the SQL scripts:
    - `database/schema.sql` (to create tables)
    - `database/seed_data.sql` (to populate initial data)

---

### **Step 3: Service Setup (Production Recommended)**
To run the system as a background service (so it stays running after logging off), we recommend using **NSSM (Non-Sucking Service Manager)**:

1.  Download NSSM from [nssm.cc](https://nssm.cc/).
2.  **Backend Service**:
    ```cmd
    nssm install UPF_Backend "C:\Path\To\venv\Scripts\uvicorn.exe" "backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4"
    ```
3.  **Frontend Service**:
    ```cmd
    nssm install UPF_Frontend "C:\Path\To\venv\Scripts\streamlit.exe" "run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"
    ```

---

### **Step 4: Using IIS as a Reverse Proxy (Optional)**
For professional deployment with a custom domain (e.g., `upf.my-org.com`):
1.  Install **IIS** (Internet Information Services) on Windows Server 2025.
2.  Install **URL Rewrite** and **Application Request Routing (ARR)** modules.
3.  Configure IIS to forward traffic from Port 80/443 to Port 8501 (Streamlit).

---

### **Step 5: Quick Startup Script**
For manual startup or testing, you can use the provided [run_upf_system.bat](file:///c:/Users/effan/Downloads/asm-evaluation-system-1.0-main/UPF%20Facility%20Management%20System/UPF%20Management%20System/run_upf_system.bat):
1.  Double-click `run_upf_system.bat`.
2.  It will automatically create a virtual environment, install dependencies, and launch both servers.

---

### **Maintenance & Logs**
- **Static Files**: All generated QR codes are stored in the `static/qr_codes/` directory.
- **Troubleshooting**: Check the console output of the `run_upf_system.bat` for error messages during startup.
- **Python Path**: Ensure `python` is added to the system's Environment Variables (PATH).
