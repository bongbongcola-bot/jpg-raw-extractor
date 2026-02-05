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
        self.root.title("JPG Raw Select & Extract")
        self.root.geometry("750x550")
        self.root.resizable(True, True)
        
        # 변수 초기화
        self.jpg_folder = tk.StringVar()
        self.raw_folder = tk.StringVar()
        self.target_folder = tk.StringVar()
        self.extract_folder = tk.StringVar()
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
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """UI 위젯 생성"""
        # 탭 컨트롤
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 탭 1: 파일 복사
        self.tab_copy = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_copy, text="파일 복사")
        self.create_copy_tab(self.tab_copy)
        
        # 탭 2: 파일명 추출
        self.tab_extract = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_extract, text="파일명 추출")
        self.create_extract_tab(self.tab_extract)
    
    def create_copy_tab(self, parent):
        """파일 복사 탭 생성"""
        main_frame = ttk.Frame(parent, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 폴더 선택 섹션
        folder_frame = ttk.LabelFrame(main_frame, text="폴더 선택", padding="10")
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        # JPG 폴더
        self.create_folder_row(folder_frame, "jpg", self.jpg_folder, row=0)
        
        # RAW 폴더
        self.create_folder_row(folder_frame, "Raw_arw", self.raw_folder, row=1)
        
        # 복사 대상 폴더
        self.create_folder_row(folder_frame, "Copy_url", self.target_folder, row=2)
        
        # 파일 정보
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(file_frame, text="파일:", font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.current_file_label = ttk.Label(file_frame, text="", font=("Helvetica", 10))
        self.current_file_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 진행 바
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # 진행 정보
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.speed_label = ttk.Label(info_frame, text="속도: 0 MB/s", font=("Helvetica", 9))
        self.speed_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(info_frame, text="남은 시간: 계산 중...", font=("Helvetica", 9))
        self.time_label.pack(side=tk.LEFT, padx=(30, 0))
        
        self.count_label = ttk.Label(info_frame, text="남은 항목: 0개", font=("Helvetica", 9))
        self.count_label.pack(side=tk.RIGHT)
        
        # 버튼 섹션
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Start 버튼
        self.start_btn = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_copying,
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=(100, 20))
        
        # 초기화 버튼
        reset_btn = ttk.Button(
            button_frame,
            text="초기화",
            command=self.reset_copy_folders,
            width=15
        )
        reset_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Close 버튼
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            command=self.root.quit,
            width=15
        )
        close_btn.pack(side=tk.LEFT)
    
    def create_extract_tab(self, parent):
        """파일명 추출 탭 생성"""
        main_frame = ttk.Frame(parent, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 폴더 선택 섹션
        folder_frame = ttk.LabelFrame(main_frame, text="폴더 선택", padding="10")
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 선택 폴더
        row_frame = ttk.Frame(folder_frame)
        row_frame.pack(fill=tk.X)
        
        ttk.Label(row_frame, text="선택 폴더", width=10, font=("Helvetica", 10)).pack(side=tk.LEFT)
        
        entry = ttk.Entry(row_frame, textvariable=self.extract_folder, width=50, font=("Helvetica", 9))
        entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(
            row_frame, 
            text="찾아보기",
            command=lambda: self.select_folder(self.extract_folder)
        )
        browse_btn.pack(side=tk.LEFT)
        
        # 파일명 목록 표시 영역
        list_frame = ttk.LabelFrame(main_frame, text="파일명 목록", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 텍스트 영역과 스크롤바
        text_frame = ttk.Frame(list_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.filename_text = tk.Text(text_frame, wrap=tk.WORD, font=("Helvetica", 10), height=10)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.filename_text.yview)
        self.filename_text.configure(yscrollcommand=scrollbar.set)
        
        self.filename_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 진행 바
        self.extract_progress_var = tk.DoubleVar()
        self.extract_progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.extract_progress_var,
            maximum=100,
            mode='determinate'
        )
        self.extract_progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # 상태 표시
        self.extract_status_label = ttk.Label(main_frame, text="준비", font=("Helvetica", 10))
        self.extract_status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 버튼 섹션
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # 파일명 추출 버튼
        extract_btn = ttk.Button(
            button_frame,
            text="파일명 추출",
            command=self.extract_filenames,
            width=20
        )
        extract_btn.pack(side=tk.LEFT, padx=(150, 20))
        
        # 복사 버튼 (클립보드에 복사)
        copy_btn = ttk.Button(
            button_frame,
            text="클립보드 복사",
            command=self.copy_to_clipboard,
            width=15
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # 닫기 버튼
        close_btn = ttk.Button(
            button_frame,
            text="Close",
            command=self.root.quit,
            width=15
        )
        close_btn.pack(side=tk.LEFT)
    
    def create_folder_row(self, parent, label_text, var, row):
        """폴더 선택 행 생성"""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=5)
        
        # 레이블
        label = ttk.Label(row_frame, text=label_text, width=10, font=("Helvetica", 10))
        label.pack(side=tk.LEFT)
        
        # 경로 입력 필드
        entry = ttk.Entry(row_frame, textvariable=var, width=50, font=("Helvetica", 9))
        entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        # Browse 버튼
        browse_btn = ttk.Button(
            row_frame, 
            text=label_text.lower().replace("_", ""),
            command=lambda v=var: self.select_folder(v)
        )
        browse_btn.pack(side=tk.LEFT)
    
    def select_folder(self, var):
        """폴더 선택 대화"""
        folder = filedialog.askdirectory(title="폴더 선택")
        if folder:
            var.set(folder)
    
    def reset_copy_folders(self):
        """파일 복사 폴더 선택 초기화"""
        self.jpg_folder.set("")
        self.raw_folder.set("")
        self.target_folder.set("")
        self.progress_var.set(0)
        self.current_file_label.config(text="")
        self.speed_label.config(text="속도: 0 MB/s")
        self.time_label.config(text="남은 시간: 계산 중...")
        self.count_label.config(text="남은 항목: 0개")
    
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
        import time
        
        try:
            self.is_copying = True
            self.start_btn.config(state="disabled")
            
            jpg_folder = Path(self.jpg_folder.get())
            raw_folder = Path(self.raw_folder.get())
            target_folder = Path(self.target_folder.get())
            
            # JPG 파일 목록 가져오기
            jpg_files = list(jpg_folder.glob("*.jpg")) + list(jpg_folder.glob("*.JPG"))
            
            if not jpg_files:
                messagebox.showwarning("경고", "JPG 파일이 없습니다.")
                self.is_copying = False
                self.start_btn.config(state="normal")
                return
            
            total_files = len(jpg_files)
            copied_count = 0
            start_time = time.time()
            
            # 각 JPG에 대해 RAW 파일 찾아서 복사
            for idx, jpg_file in enumerate(jpg_files, 1):
                remaining = total_files - idx + 1
                self.count_label.config(text=f"남은 항목: {remaining}개")
                
                # 진행률 업데이트
                progress = (idx - 1) / total_files * 100
                self.progress_var.set(progress)
                self.current_file_label.config(text=jpg_file.name)
                
                # RAW 파일 찾기
                base_name = jpg_file.stem
                raw_extensions = [".raw", ".arw", ".CR2", ".CR3", ".nef", ".nrw", ".raf", ".rw2", ".orf", ".dng",
                                  ".RAW", ".ARW", ".NEF", ".NRW", ".RAF", ".RW2", ".ORF", ".DNG"]
                
                raw_file = None
                for ext in raw_extensions:
                    candidate = raw_folder / (base_name + ext)
                    if candidate.exists():
                        raw_file = candidate
                        break
                
                # RAW 파일 복사
                if raw_file:
                    try:
                        target_path = target_folder / raw_file.name
                        file_size = raw_file.stat().st_size
                        copy_start = time.time()
                        
                        shutil.copy2(raw_file, target_path)
                        
                        copy_time = time.time() - copy_start
                        if copy_time > 0:
                            speed = file_size / copy_time / 1024 / 1024  # MB/s
                            self.speed_label.config(text=f"속도: {speed:.1f} MB/s")
                        
                        copied_count += 1
                    except Exception as e:
                        print(f"복사 실패: {raw_file.name} - {str(e)}")
                
                # 남은 시간 계산
                elapsed = time.time() - start_time
                if idx > 0:
                    avg_time = elapsed / idx
                    remaining_time = avg_time * (total_files - idx)
                    mins, secs = divmod(int(remaining_time), 60)
                    self.time_label.config(text=f"남은 시간: {mins}분 {secs}초")
                
                self.root.update_idletasks()
            
            # 완료
            self.progress_var.set(100)
            self.count_label.config(text="남은 항목: 0개")
            self.time_label.config(text="남은 시간: 완료!")
            self.current_file_label.config(text="완료")
            
            messagebox.showinfo("완료", f"{copied_count}개/{total_files}개 파일 복사 완료!")
            
        except Exception as e:
            messagebox.showerror("오류", f"복사 중 오류 발생:\n{str(e)}")
        finally:
            self.is_copying = False
            self.start_btn.config(state="normal")
    
    def extract_filenames(self):
        """선택한 폴더에서 파일명 추출"""
        folder_path = self.extract_folder.get()
        
        if not folder_path:
            messagebox.showerror("오류", "폴더를 선택해주세요.")
            return
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("오류", "폴더가 존재하지 않습니다.")
            return
        
        try:
            self.extract_status_label.config(text="추출 중...")
            self.extract_progress_var.set(0)
            self.root.update_idletasks()
            
            # 이미지 파일 확장자
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.raw', '.arw', 
                              '.cr2', '.cr3', '.nef', '.orf', '.raf', '.dng', '.rw2'}
            
            folder = Path(folder_path)
            files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in image_extensions]
            
            total_files = len(files)
            if total_files == 0:
                messagebox.showwarning("경고", "이미지 파일이 없습니다.")
                self.extract_status_label.config(text="준비")
                return
            
            # 파일명만 추출 (확장자 제외)
            filenames = []
            for idx, f in enumerate(files):
                filenames.append(f.stem)
                progress = (idx + 1) / total_files * 100
                self.extract_progress_var.set(progress)
                self.root.update_idletasks()
            
            # 중복 제거 및 정렬
            filenames = sorted(set(filenames))
            
            # 텍스트 영역에 표시
            self.filename_text.delete(1.0, tk.END)
            self.filename_text.insert(tk.END, " ".join(filenames))
            
            self.extract_status_label.config(text=f"완료 - {len(filenames)}개 파일명 추출됨")
            self.extract_progress_var.set(100)
            
        except Exception as e:
            messagebox.showerror("오류", f"추출 중 오류 발생:\n{str(e)}")
            self.extract_status_label.config(text="오류 발생")
    
    def copy_to_clipboard(self):
        """파일명 목록을 클립보드에 복사"""
        text = self.filename_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("복사 완료", "파일명 목록이 클립보드에 복사되었습니다.")
        else:
            messagebox.showwarning("경고", "복사할 파일명이 없습니다.")


def main():
    root = tk.Tk()
    app = JPGRawExtractor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
