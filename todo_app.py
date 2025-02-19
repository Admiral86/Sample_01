import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import customtkinter as ctk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoリストアプリ")
        self.root.geometry("800x600")
        
        # データベースの初期化
        self.init_database()
        
        # UIの設定
        self.setup_ui()
        
        # タスクの読み込み
        self.load_tasks()
    
    def init_database(self):
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT DEFAULT '未完了',
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def setup_ui(self):
        # メインフレーム
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 入力フレーム
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # タスク入力
        self.task_entry = ctk.CTkEntry(input_frame, placeholder_text="新しいタスク")
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 追加ボタン
        add_button = ctk.CTkButton(input_frame, text="追加", command=self.add_task)
        add_button.pack(side=tk.LEFT, padx=5)
        
        # タスクリスト
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "タスク", "状態", "作成日"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("タスク", text="タスク")
        self.tree.heading("状態", text="状態")
        self.tree.heading("作成日", text="作成日")
        
        self.tree.column("ID", width=50)
        self.tree.column("タスク", width=300)
        self.tree.column("状態", width=100)
        self.tree.column("作成日", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ボタンフレーム
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 完了ボタン
        complete_button = ctk.CTkButton(button_frame, text="完了", command=self.complete_task)
        complete_button.pack(side=tk.LEFT, padx=5)
        
        # 削除ボタン
        delete_button = ctk.CTkButton(button_frame, text="削除", command=self.delete_task)
        delete_button.pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        title = self.task_entry.get()
        if not title:
            messagebox.showwarning("警告", "タスクを入力してください")
            return
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, status, created_at) VALUES (?, ?, ?)",
            (title, "未完了", datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        conn.close()
        
        self.task_entry.delete(0, tk.END)
        self.load_tasks()
    
    def complete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "タスクを選択してください")
            return
        
        task_id = self.tree.item(selected_item[0])['values'][0]
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            ("完了", task_id)
        )
        conn.commit()
        conn.close()
        
        self.load_tasks()
    
    def delete_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "タスクを選択してください")
            return
        
        if messagebox.askyesno("確認", "選択したタスクを削除しますか？"):
            task_id = self.tree.item(selected_item[0])['values'][0]
            
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            
            self.load_tasks()
    
    def load_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, status, created_at FROM tasks ORDER BY created_at DESC")
        tasks = cursor.fetchall()
        
        for task in tasks:
            self.tree.insert("", tk.END, values=task)
        
        conn.close()

if __name__ == "__main__":
    # メインウィンドウを作成
    root = ctk.CTk()
    # TodoAppクラスのインスタンスを作成
    app = TodoApp(root)
    # イベントループを開始
    root.mainloop() 