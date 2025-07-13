import requests
from bs4 import BeautifulSoup
from readability import Document
from fpdf import FPDF
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import webbrowser

def scrape_website_to_pdf(url, output_pdf, progress_callback):
    try:
        progress_callback(10)
        response = requests.get(url, timeout=10)
        progress_callback(30)

        # Use readability-lxml to extract main content
        doc = Document(response.text)
        title = doc.title()
        main_html = doc.summary()

        soup = BeautifulSoup(main_html, "html.parser")
        paragraphs = soup.find_all(["p", "h1", "h2", "h3"])
        text = "\n\n".join([p.get_text(strip=True) for p in paragraphs])
        progress_callback(70)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, title)
        pdf.ln()

        for line in text.split("\n"):
            pdf.multi_cell(0, 10, line)

        pdf.output(output_pdf)
        progress_callback(100)

    except Exception as e:
        messagebox.showerror("Error", str(e))

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Improved Website Scraper")
        self.root.geometry("500x300")
        self.root.configure(bg="#222831")

        self.title = tk.Label(root, text="🌐 Better Website to PDF Scraper 🌐",
                              font=("Helvetica", 18, "bold"), fg="#00ADB5", bg="#222831")
        self.title.pack(pady=20)

        self.url_entry = tk.Entry(root, width=50, font=("Helvetica", 12))
        self.url_entry.pack(pady=10)
        self.url_entry.insert(0, "https://example.com")

        self.process_btn = tk.Button(root, text="🚀 Click Process 🚀",
                                     font=("Helvetica", 12, "bold"),
                                     bg="#00ADB5", fg="white",
                                     command=self.start_scrape_thread)
        self.process_btn.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.animation_label = tk.Label(root, text="", font=("Helvetica", 14),
                                        fg="#EEEEEE", bg="#222831")
        self.animation_label.pack()

    def start_scrape_thread(self):
        url = self.url_entry.get().strip()
        if not url.startswith("http"):
            messagebox.showwarning("Invalid URL", "Please enter a valid website URL.")
            return

        self.process_btn.config(state="disabled")
        self.animation_label.config(text="✨ Extracting article content... ✨")
        threading.Thread(target=self.scrape_process, args=(url,), daemon=True).start()

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()

    def scrape_process(self, url):
        output_pdf = "output.pdf"
        scrape_website_to_pdf(url, output_pdf, self.update_progress)

        self.animation_label.config(text="✅ 100% Done! Opening output folder...")
        self.process_btn.config(state="normal")

        output_folder = os.path.abspath(os.path.dirname(output_pdf))
        if os.name == 'nt':
            os.startfile(output_folder)
        else:
            webbrowser.open(f'file://{output_folder}')

        self.root.after(3000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()
