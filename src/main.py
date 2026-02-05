#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
from pathlib import Path
import threading
from typing import List, Tuple

class JPGRawExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG & RAW Extractor")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 변수 초기화
        self.jpg_folder = tk.StringVar()
        self.raw_folder = tk.StringVar()
        self.target_folder = tk.StringVar()
        self.is_copying = False
        
        # UI 스타일 설정
        self.setup_styles()
        
        # UI 구성
        self.create_widgets()
    
    def setup_styles(self):
        """UI 스타일 설정"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 색상 정의
        self.bg_color = "#f0f0f0"
        self.button_color = "#0078d4"
        self.button_hover = "#005a9e"
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(
            main_frame, 
            text="JPG & RAW 파일 추출기",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # 폴더 선택 섹션
        self.create_folder_section(main_frame)
        
        # 버튼 섹션
        self.create_button_section(main_frame)
        
        # 진행률 섹션
        self.create_progress_section(main_frame)
    
    def create_folder_section(self, parent):
        """폴더 선택 섹션 생성"""
        folder_frame = ttk.LabelFrame(parent, text="폴더 선택", padding="10")
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        # JPG 폴더
        self.create_folder_row(folder_frame, "JPG 폴더", self.jpg_folder, row=0)
        
        # RAW 폴더
        self.create_folder_row(folder_frame, "RAW 폴더", self.raw_folder, row=1)
        
        # 복사 대상 폴더
        self.create_folder_row(folder_frame, "복사 대상", self.target_folder, row=2)
    
    def create_folder_row(self, parent, label_text, var, row):
        """폴더 선택 행 생성"""
        # 레이블
        label = ttk.Label(parent, text=label_text, width=12, font=("Helvetica", 10))
        label.grid(row=row, column=0, padx=(0, 10), pady=8, sticky="w")
        
        # 경로 입력 필드
        entry = ttk.Entry(parent, textvariable=var, width=50, font=("Helvetica", 9))
        entry.grid(row=row, column=1, padx=(0, 10), pady=8, sticky="ew")
        
        # Browse 버튼
        browse_btn = ttk.Button(
            parent, 
            text="Browse",
            command=lambda v=var: self.select_folder(v)
        )
        browse_btn.grid(row=row, column=2, padx=0, pady=8)
        
        parent.columnconfigure(1, weight=1)
    
    def create_button_section(self, parent):
        """버튼 섹션 생성"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 복사 시작 버튼
        self.copy_btn = ttk.Button(
            button_frame,
            text="복사 시작",
            command=self.start_copying
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 초기화 버튼
        reset_btn = ttk.Button(
            button_frame,
            text="초기화",
            command=self.reset_folders
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def create_progress_section(self, parent):
        """진행률 섹션 생성"""
        progress_frame = ttk.LabelFrame(parent, text="진행 상황", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # 진행 바
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # 진행 정보 레이블
        info_frame = ttk.Frame(progress_frame)
        info_frame.pack(fill=tk.X)
        
        # 파일 복사 진행 정보
        self.status_label = ttk.Label(
            info_frame,
            text="준비 완료",
            font=("Helvetica", 10)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 백분율
        self.percent_label = ttk.Label(
            info_frame,
            text="0%",
            font=("Helvetica", 10, "bold")
        )
        self.percent_label.pack(side=tk.RIGHT)
        
        # 상세 정보
        self.detail_label = ttk.Label(
            progress_frame,
            text="",
            font=("Helvetica", 9),
            foreground="gray"
        )
        self.detail_label.pack(fill=tk.X, pady=(5, 0))
    
    def select_folder(self, var):
        """폴더 선택 대화"""
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            var.set(folder)
    
    def reset_folders(self):
        """폴더 선택 초기화"""
        self.jpg_folder.set("")
        self.raw_folder.set("")
        self.target_folder.set("")
        self.progress_var.set(0)
        self.status_label.config(text="준비 완료")
        self.percent_label.config(text="0%")
        self.detail_label.config(text="")
    
    def validate_folders(self) -> bool:
        """폴더 선택 유효성 검사"""
        if not self.jpg_folder.get():
            messagebox.showerror("오류", "JPG 폴더를 선택해주세요.")
            return False
        if not self.raw_folder.get():
            messagebox.showerror("오류", "RAW 폴더를 선택해주세요.")
            return False
        if not self.target_folder.get():
            messagebox.showerror("오류", "복사 대상 폴더를 선택해주세요.")
            return False
        
        # 폴더 존재 여부 확인
        if not os.path.isdir(self.jpg_folder.get()):
            messagebox.showerror("오류", "JPG 폴더가 존재하지 않습니다.")
            return False
        if not os.path.isdir(self.raw_folder.get()):
            messagebox.showerror("오류", "RAW 폴더가 존재하지 않습니다.")
            return False
        if not os.path.isdir(self.target_folder.get()):
            messagebox.showerror("오류", "복사 대상 폴더가 존재하지 않습니다.")
            return False
        
        return True
    
    def start_copying(self):
        """복사 시작"""
        if not self.validate_folders():
            return
        
        if self.is_copying:
            messagebox.showwarning("경고", "이미 복사 중입니다.")
            return
        
        # 백그라운드 스레드에서 복사 작업 수행
        thread = threading.Thread(target=self.copy_files)
        thread.daemon = True
        thread.start()
    
    def copy_files(self):
        """JPG와 매칭되는 RAW 파일을 복사"""
        try:
            self.is_copying = True
            self.copy_btn.config(state="disabled")
            
            jpg_folder = Path(self.jpg_folder.get())
            raw_folder = Path(self.raw_folder.get())
            target_folder = Path(self.target_folder.get())
            
            # JPG 파일 목록 가져오기
            jpg_files = list(jpg_folder.glob("*.jpg")) + list(jpg_folder.glob("*.JPG"))
            
            if not jpg_files:
                messagebox.showwarning("경고", "JPG 파일이 없습니다.")
                self.is_copying = False
                self.copy_btn.config(state="normal")
                return
            
            total_files = len(jpg_files)
            copied_count = 0
            
            # 각 JPG에 대해 RAW 파일 찾아서 복사
            for idx, jpg_file in enumerate(jpg_files, 1):
                # 진행률 업데이트
                progress = (idx - 1) / total_files * 100
                self.update_progress(progress, idx, total_files, jpg_file.name)
                
                # RAW 파일 찾기 (여러 확장자 지원: .raw, .arw, .CR2, .nef 등)
                base_name = jpg_file.stem
                raw_extensions = [".raw", ".arw", ".CR2", ".CR3", ".nef", ".nrw", ".raf", ".rw2", ".orf", ".dng"]
                
                raw_file = None
                for ext in raw_extensions:
                    candidate = raw_folder / (base_name + ext)
                    if candidate.exists():
                        raw_file = candidate
                        break
                    # 대문자도 확인
                    candidate = raw_folder / (base_name + ext.upper())
                    if candidate.exists():
                        raw_file = candidate
                        break
                
                # RAW 파일 복사
                if raw_file:
                    try:
                        target_path = target_folder / raw_file.name
                        shutil.copy2(raw_file, target_path)
                        copied_count += 1
                    except Exception as e:
                        print(f"복사 실패: {raw_file.name} - {str(e)}")
            
            # 완료
            self.progress_var.set(100)
            self.percent_label.config(text="100%")
            self.status_label.config(text="복사 완료!")
            self.detail_label.config(text=f"총 {total_files}개 중 {copied_count}개 파일 복사됨")
            
            messagebox.showinfo("완료", f"{copied_count}개/{total_files}개 파일 복사 완료!")
            
        except Exception as e:
            messagebox.showerror("오류", f"복사 중 오류 발생:\n{str(e)}")
        finally:
            self.is_copying = False
            self.copy_btn.config(state="normal")
    
    def update_progress(self, progress, current, total, filename):
        """진행률 업데이트"""
        self.progress_var.set(progress)
        self.percent_label.config(text=f"{int(progress)}%")
        self.status_label.config(text=f"복사 중... ({current}/{total})")
        self.detail_label.config(text=f"파일: {filename}")
        self.root.update_idletasks()


def main():
    root = tk.Tk()
    app = JPGRawExtractor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
