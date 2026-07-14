import os
import json
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from generate import build_dist

class BuzlGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buzl Client Manager & Compiler")
        self.root.geometry("900x650")
        self.root.minsize(800, 550)
        
        self.vendors_file = 'vendors.json'
        self.vendors = []
        self.selected_index = None
        self.uploaded_image_path = None
        
        self.load_vendors()
        self.setup_ui()

    def load_vendors(self):
        if os.path.exists(self.vendors_file):
            try:
                with open(self.vendors_file, 'r', encoding='utf-8') as f:
                    self.vendors = json.load(f)
            except Exception as e:
                messagebox.showerror("File Error", f"Could not load vendors.json:\n{e}")
                self.vendors = []
        else:
            self.vendors = []

    def save_vendors(self):
        try:
            with open(self.vendors_file, 'w', encoding='utf-8') as f:
                json.dump(self.vendors, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to save vendors.json:\n{e}")

    def setup_ui(self):
        # Configure fonts
        default_font = ("Segoe UI", 10)
        title_font = ("Segoe UI", 11, "bold")
        btn_font = ("Segoe UI", 10, "bold")
        
        self.root.option_add("*Font", default_font)

        # Configure Grid weight
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=5)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        # --- LEFT PANEL: Client List ---
        left_frame = tk.LabelFrame(self.root, text="Registered Clients", font=title_font, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.client_listbox = tk.Listbox(left_frame, selectmode=tk.SINGLE, font=("Segoe UI", 10), bd=1, relief="solid")
        self.client_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.client_listbox.bind('<<ListboxSelect>>', self.on_client_select)

        scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.client_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.client_listbox.config(yscrollcommand=scrollbar.set)

        self.refresh_listbox()

        # Left panel controls
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=(8, 0))
        tk.Button(btn_frame, text="✚ Add New Client", bg="#F3F4F6", fg="#111827", relief="groove", pady=4, command=self.add_new_client).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        tk.Button(btn_frame, text="🗑 Delete", bg="#FEE2E2", fg="#991B1B", relief="groove", pady=4, command=self.delete_client).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4, 0))

        # --- RIGHT PANEL: Details Form ---
        right_frame = tk.LabelFrame(self.root, text="Client Information Form", font=title_font, padx=15, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        right_frame.columnconfigure(1, weight=1)

        # Form Entries
        fields = [
            ("Location ID:", "locationId", "e.g., locn-dev-409 (Backend DB ID)"),
            ("Short ID:", "shortId", "e.g., 409 (For URL routing)"),
            ("Business Name:", "locationName", "e.g., Santhiya Chandran Academy"),
            ("Google Place ID:", "placeId", "Google maps place ID for review link"),
            ("Analytics ID:", "googleAnalyticsId", "e.g., G-XXXXXXXXXX (Optional)"),
            ("OG Title:", "ogTitle", "Share card title (Optional)"),
            ("OG Description:", "ogDescription", "Share card description (Optional)")
        ]
        
        self.entries = {}
        row_idx = 0
        for label_text, field_name, tooltip in fields:
            # Label
            tk.Label(right_frame, text=label_text).grid(row=row_idx, column=0, sticky="w", pady=4)
            # Entry
            entry = tk.Entry(right_frame, bd=1, relief="solid")
            entry.grid(row=row_idx, column=1, sticky="ew", pady=4, padx=(5, 0))
            self.entries[field_name] = entry
            
            # Tooltip/Instruction
            tk.Label(right_frame, text=tooltip, fg="gray", font=("Segoe UI", 8)).grid(row=row_idx+1, column=1, sticky="w", padx=(5, 0))
            row_idx += 2
        # Image Upload Row
        tk.Label(right_frame, text="OG Share Image:").grid(row=row_idx, column=0, sticky="w", pady=8)
        img_frame = tk.Frame(right_frame)
        img_frame.grid(row=row_idx, column=1, sticky="ew", pady=8, padx=(5, 0))
        
        self.img_label_text = tk.StringVar(value="No custom image (defaults to logo)")
        tk.Label(img_frame, textvariable=self.img_label_text, fg="#4B5563", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(img_frame, text="Browse Image...", bg="#E5E7EB", command=self.browse_image).pack(side=tk.RIGHT)
        row_idx += 1

        # Active Status Row
        tk.Label(right_frame, text="Active Status:").grid(row=row_idx, column=0, sticky="w", pady=8)
        self.active_var = tk.BooleanVar(value=True)
        self.active_check = tk.Checkbutton(right_frame, text="Enabled (will generate static site folders)", variable=self.active_var, activebackground="#EFF6FF")
        self.active_check.grid(row=row_idx, column=1, sticky="w", pady=8, padx=(5, 0))
        row_idx += 2

        # Save Button
        self.save_btn = tk.Button(right_frame, text="✓ Save / Update Client Details", bg="#2563EB", fg="white", font=btn_font, pady=6, command=self.save_client_form)
        self.save_btn.grid(row=row_idx, column=0, columnspan=2, pady=(15, 0), sticky="ew")

        # --- BOTTOM PANEL: Actions ---
        bottom_frame = tk.Frame(self.root, pady=12, bg="#F9FAFB")
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.compile_btn = tk.Button(bottom_frame, text="▶ COMPILE STATIC SITES (BUILD DIST/)", bg="#059669", fg="white", font=("Segoe UI", 12, "bold"), pady=8, command=self.compile_sites)
        self.compile_btn.pack(fill=tk.X, padx=15)

    def refresh_listbox(self):
        self.client_listbox.delete(0, tk.END)
        for vendor in self.vendors:
            status = "" if vendor.get('active', True) else " (Disabled)"
            self.client_listbox.insert(tk.END, f"[{vendor.get('shortId', '??')}] {vendor.get('locationName', 'Unnamed')}{status}")

    def on_client_select(self, event):
        selection = self.client_listbox.curselection()
        if not selection:
            return
        self.selected_index = selection[0]
        vendor = self.vendors[self.selected_index]

        # Populate form
        for field, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, vendor.get(field, ''))
            
        self.img_label_text.set(vendor.get('ogImage', 'No custom image (defaults to logo)'))
        self.active_var.set(vendor.get('active', True))
        self.uploaded_image_path = None

    def add_new_client(self):
        self.selected_index = None
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.img_label_text.set("No custom image (defaults to logo)")
        self.active_var.set(True)
        self.uploaded_image_path = None
        self.client_listbox.selection_clear(0, tk.END)

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Share Card Thumbnail Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")]
        )
        if file_path:
            self.uploaded_image_path = file_path
            self.img_label_text.set(os.path.basename(file_path))

    def save_client_form(self):
        # Validate required fields
        data = {}
        for field, entry in self.entries.items():
            val = entry.get().strip()
            if field in ["locationId", "shortId", "locationName", "placeId"] and not val:
                messagebox.showerror("Validation Error", f"Field '{field}' is required to save client details.")
                return
            data[field] = val

        data['active'] = self.active_var.get()

        # Handle Image Upload Copying
        if self.uploaded_image_path:
            assets_dir = 'assets'
            os.makedirs(assets_dir, exist_ok=True)
            
            # Save using shortId filename convention
            ext = os.path.splitext(self.uploaded_image_path)[1]
            dest_filename = f"og-{data['shortId']}{ext}"
            dest_path = os.path.join(assets_dir, dest_filename)
            
            try:
                shutil.copy(self.uploaded_image_path, dest_path)
                data['ogImage'] = f"/assets/{dest_filename}"
            except Exception as e:
                messagebox.showerror("Upload Error", f"Failed to save uploaded image:\n{e}")
                return
        elif self.selected_index is not None:
            # Keep previous image if no new upload
            data['ogImage'] = self.vendors[self.selected_index].get('ogImage', 'https://gobuzl.com/assets/og-image-default.png')
        else:
            # Default placeholder image
            data['ogImage'] = 'https://gobuzl.com/assets/og-image-default.png'

        # Insert or Update in Registry
        if self.selected_index is not None:
            self.vendors[self.selected_index] = data
            messagebox.showinfo("Saved", f"Client '{data['locationName']}' updated successfully.")
        else:
            self.vendors.append(data)
            messagebox.showinfo("Saved", f"New client '{data['locationName']}' added successfully.")

        self.save_vendors()
        self.refresh_listbox()

    def delete_client(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Please select a client from the list to delete.")
            return
        vendor = self.vendors[self.selected_index]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete client '{vendor['locationName']}'?")
        if confirm:
            self.vendors.pop(self.selected_index)
            self.save_vendors()
            self.refresh_listbox()
            self.add_new_client()

    def compile_sites(self):
        try:
            # Run generator compiler logic
            build_dist()
            messagebox.showinfo("Build Completed", "Static sites compiled and deployed successfully inside the /dist/ directory!")
        except Exception as e:
            messagebox.showerror("Build Error", f"Static site compilation failed:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = BuzlGeneratorApp(root)
    root.mainloop()
