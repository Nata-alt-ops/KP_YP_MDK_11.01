import hashlib
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pyodbc
from datetime import datetime

# Подключение к базе данных
def connect_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-FSFCUVI\MSSQLSERVER01;"
            "DATABASE=Hotel;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

# Хэширование пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Авторизация
def authenticate_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        label_status.config(text="Введите логин и пароль")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            
            cursor.execute("SELECT user_id, user_type FROM Users WHERE username=? AND password=?", (username, hashed_password))
            result = cursor.fetchone()

            if result:
                user_id, user_type = result
                open_main_window(username, user_id, user_type)
            else:
                label_status.config(text="Неверный логин или пароль")
        except Exception as e:
            label_status.config(text=f"Ошибка: {e}")
        finally:
            conn.close()
    else:
        label_status.config(text="Нет подключения к БД")

# Регистрация
def register_user():
    def submit_registration():
        new_username = entry_new_username.get().strip()
        new_password = entry_new_password.get()
        new_first_name = entry_new_firstname.get().strip()
        new_last_name = entry_new_lastname.get().strip()
        new_phone = entry_new_phone.get().strip()
        new_email = entry_new_email.get().strip()
        
        if not new_username or not new_password:
            label_register_status.config(text="Заполните логин и пароль")
            return
            
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT user_id FROM Users WHERE username=?", (new_username,))
                if cursor.fetchone():
                    label_register_status.config(text="Пользователь уже существует")
                    return

                hashed_password = hash_password(new_password)

                cursor.execute(
                    "INSERT INTO Users (username, FirstName, LastName, password, Phone, Email, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_username, new_first_name, new_last_name, hashed_password, new_phone, new_email, 'user')
                )

                conn.commit()
                label_register_status.config(text="Регистрация успешна!", fg="green")
                entry_username.delete(0, END)
                entry_username.insert(0, new_username)
                registration.after(1500, registration.destroy)
                    
            except Exception as e:
                label_register_status.config(text=f"Ошибка: {e}")
            finally:
                conn.close()
        else:
            label_register_status.config(text="Нет подключения к БД")

    registration = Toplevel(root)
    registration.title("Регистрация")
    registration.configure(bg='lightblue')
    registration.geometry('400x400')  

    Label(registration, text="Регистрация", font=('Arial', 16), bg='lightblue').pack(pady=10)

    frame = Frame(registration, bg='lightblue')
    frame.pack(pady=10)

    Label(frame, text="Логин:*", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
    entry_new_username = Entry(frame, width=20)
    entry_new_username.grid(row=0, column=1, pady=5, padx=5)

    Label(frame, text="Пароль:*", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
    entry_new_password = Entry(frame, show='*', width=20)
    entry_new_password.grid(row=1, column=1, pady=5, padx=5)

    Label(frame, text="Имя:", bg='lightblue').grid(row=2, column=0, sticky=W, pady=5)
    entry_new_firstname = Entry(frame, width=20)
    entry_new_firstname.grid(row=2, column=1, pady=5, padx=5)

    Label(frame, text="Фамилия:", bg='lightblue').grid(row=3, column=0, sticky=W, pady=5)
    entry_new_lastname = Entry(frame, width=20)
    entry_new_lastname.grid(row=3, column=1, pady=5, padx=5)

    Label(frame, text="Телефон:", bg='lightblue').grid(row=4, column=0, sticky=W, pady=5)
    entry_new_phone = Entry(frame, width=20)
    entry_new_phone.grid(row=4, column=1, pady=5, padx=5)

    Label(frame, text="Email:", bg='lightblue').grid(row=5, column=0, sticky=W, pady=5)
    entry_new_email = Entry(frame, width=20)
    entry_new_email.grid(row=5, column=1, pady=5, padx=5)

    Button(frame, text="Зарегистрироваться", command=submit_registration, bg='lightgreen').grid(row=6, column=1, pady=10)
    Button(frame, text="Назад", command=registration.destroy, bg='lightcoral').grid(row=7, column=1, pady=5)

    label_register_status = Label(registration, text="", bg='lightblue')
    label_register_status.pack()

# Основное окно
def open_main_window(username, user_id, user_type):
    main_window = Toplevel(root)
    main_window.configure(bg='lightblue')
    main_window.geometry('800x600') 
    main_window.title(f"Добро пожаловать, {username}")

    root.withdraw()
    
    def logout():
        main_window.destroy()
        root.deiconify()  
        entry_password.delete(0, END)  
        label_status.config(text="Вы вышли из системы")

    main_frame = Frame(main_window, bg='lightblue')
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    left_frame = Frame(main_frame, bg='lightblue')
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)
    
    try:
        photo = PhotoImage(file="user.png")
        image_label = Label(left_frame, image=photo, bg='lightblue')
        image_label.pack(expand=True)
        main_window.photo = photo 
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")

  
    right_frame = Frame(main_frame, bg='lightblue')
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

  
    Label(right_frame, text="Меню", font=('Arial', 18, 'bold'), 
          bg='lightblue', fg='darkblue').pack(pady=20)

   
    Button(right_frame, text="🏨 Комнаты", width=25, height=2,
           command=lambda: view_all_rooms(user_type), font=('Arial', 12), 
           bg='#87CEEB', fg='black').pack(pady=10)
    
    Button(right_frame, text="🎯 Услуги отеля", width=25, height=2,
           command=view_services, font=('Arial', 12), 
           bg='#98FB98', fg='black').pack(pady=10)

    if user_type == 'user':
        Button(right_frame, text="📅 Мои бронирования", width=25, height=2,
               command=lambda: view_my_bookings(user_id), font=('Arial', 12), 
               bg='#FFD700', fg='black').pack(pady=10)
    
        Button(right_frame, text="👤 Редактировать профиль", width=25, height=2,
               command=lambda: edit_profile(user_id), font=('Arial', 12), 
               bg='#FFB6C1', fg='black').pack(pady=10)
        
        Button(right_frame, text="🗑️ Удалить учетную запись", width=25, height=2,
               command=lambda: delete_user_account(user_id, username), 
               font=('Arial', 12), bg='#FF6347', fg='white').pack(pady=10)

    if user_type == 'admin':

        Button(right_frame, text="📋 Управление бронированиями", width=25, height=2,
               command=manage_bookings, font=('Arial', 12), 
               bg='#DA70D6', fg='black').pack(pady=10)
        
        Button(right_frame, text="📊 Отчеты по таблицам", width=25, height=2,
           command=view_database_tables, font=('Arial', 12), 
           bg='#9370DB', fg='white').pack(pady=10)

    Button(right_frame, text="🚪 Выйти", command=logout, 
           width=20, height=2, font=('Arial', 12), 
           bg='#DC143C', fg='white').pack(pady=30)


def delete_user_account(user_id, username):
    if not messagebox.askyesno("Подтверждение удаления", 
                              f"Вы уверены, что хотите удалить свою учетную запись '{username}'?\n\n"
                              "Это действие невозможно отменить!"):
        return
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT BookingID FROM Bookings WHERE UserID = ?", (user_id,))
            bookings = cursor.fetchall()
            for booking in bookings:
                booking_id = booking[0]

                cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
            cursor.execute("""
                UPDATE Rooms 
                SET RoomStatus = 'Свободна' 
                WHERE RoomID IN (SELECT RoomID FROM Bookings WHERE UserID = ?)
            """, (user_id,))
            cursor.execute("DELETE FROM Bookings WHERE UserID = ?", (user_id,))
            cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            
            conn.commit()
            
            messagebox.showinfo("Успех", "Ваша учетная запись была успешно удалена.")
            
            for window in root.winfo_children():
                if isinstance(window, Toplevel):
                    window.destroy()
            
            root.deiconify()
            entry_username.delete(0, END)
            entry_password.delete(0, END)
            label_status.config(text="Учетная запись удалена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить учетную запись: {e}")
        finally:
            conn.close()

def view_all_rooms(user_type='user'):
    rooms_window = Toplevel()
    rooms_window.title("Доступные комнаты")
    rooms_window.configure(bg='lightblue')
    rooms_window.geometry('600x400')
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT RoomID, Room_number, RoomType, Price, RoomStatus FROM Rooms")
            rooms = cursor.fetchall()
         
            main_frame = Frame(rooms_window, bg='white')
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            canvas = Canvas(main_frame, bg='lightblue', highlightthickness=0)
            scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg='lightblue')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            try:
                room_photo = PhotoImage(file="rooms.png")
            except:
                room_photo = None
                print("Не удалось загрузить картинку комнаты")
            
            for room in rooms:
                room_id, room_number, room_type, price, status = room
                
                room_frame = Frame(scrollable_frame, relief=GROOVE, borderwidth=1, bg='white')
                room_frame.pack(fill=X, pady=5, padx=10)
                
                if room_photo:
                    image_label = Label(room_frame, image=room_photo, bg='white')
                    image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nw')
                else:
                    Label(room_frame, text="🏨", font=('Times New Roman', 24), bg='#e6f2ff', 
                          fg='#0066cc', width=4, height=3).grid(row=0, column=0, rowspan=2, 
                                                              padx=10, pady=10, sticky='nw')
                
                info_text = f"Комната №{room_number}\nТип: {room_type}\nЦена: {price} руб./ночь\nСтатус: {status}"
                info_label = Label(room_frame, text=info_text, font=('Times New Roman', 10, 'bold'), 
                                 bg='white', justify=LEFT, anchor='w')
                info_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
                
                if status == 'Свободна' and user_type != 'admin':
                    btn = Button(room_frame, text="Забронировать", bg='lightgreen', font=('Arial', 9),
                                command=lambda rid=room_id, rnum=room_number: book_room(rid, rnum))
                    btn.grid(row=1, column=1, padx=10, pady=5, sticky='e')
                else:
                    status_label = Label(room_frame, text="Занята", fg='red', 
                                       font=('Arial', 9, 'bold'), bg='white')
                    status_label.grid(row=1, column=1, padx=10, pady=5, sticky='e')
                
                room_frame.columnconfigure(1, weight=1)

            if room_photo:
                scrollable_frame.room_photo = room_photo

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            Button(rooms_window, text="Назад", command=rooms_window.destroy, 
                   bg='lightcoral', width=15).pack(pady=10)
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить комнаты: {e}")
        finally:
            conn.close()

# Бронирование комнаты
def book_room(room_id, room_number):
    booking_window = Toplevel()
    booking_window.title(f"Бронирование комнаты №{room_number}")
    booking_window.geometry('350x250')  
    booking_window.configure(bg='lightblue')
    
    Label(booking_window, text=f"Комната №{room_number}", font=('Arial', 14), bg='lightblue').pack(pady=10)
    
    frame = Frame(booking_window, bg='lightblue')
    frame.pack(pady=10)
    
    Label(frame, text="Дата заезда (ГГГГ-ММ-ДД):", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
    entry_checkin = Entry(frame, width=15)
    entry_checkin.insert(0, "2024-01-15")
    entry_checkin.grid(row=0, column=1, pady=5, padx=5)
    
    Label(frame, text="Дата выезда (ГГГГ-ММ-ДД):", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
    entry_checkout = Entry(frame, width=15)
    entry_checkout.insert(0, "2024-01-20")
    entry_checkout.grid(row=1, column=1, pady=5, padx=5)
    
    def confirm_booking():
        checkin = entry_checkin.get()
        checkout = entry_checkout.get()
        
        if not checkin or not checkout:
            messagebox.showerror("Ошибка", "Заполните даты")
            return
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT user_id FROM Users WHERE username = ?", (entry_username.get(),))
                user_result = cursor.fetchone()
                
                if user_result:
                    user_id = user_result[0]
                    
                    cursor.execute("SELECT RoomStatus FROM Rooms WHERE RoomID = ?", (room_id,))
                    room_status = cursor.fetchone()[0]
                    
                    if room_status != 'Свободна':
                        messagebox.showerror("Ошибка", "Комната уже занята")
                        return
                    
                    cursor.execute("""
                        INSERT INTO Bookings (UserID, RoomID, CheckInDate, CheckOutDate)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, room_id, checkin, checkout))
                    
                    cursor.execute("UPDATE Rooms SET RoomStatus = 'Занята' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", f"Комната №{room_number} забронирована!")
                    booking_window.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка бронирования: {e}")
            finally:
                conn.close()
    
    Button(booking_window, text="Подтвердить", command=confirm_booking, 
           bg='lightgreen', width=15).pack(pady=5)
    Button(booking_window, text="Назад", command=booking_window.destroy, 
           bg='lightcoral', width=15).pack(pady=5)

# Просмотр услуг отеля 
def view_services():
    services_window = Toplevel()
    services_window.title("Услуги отеля")
    services_window.configure(bg='lightblue')
    services_window.geometry('600x600')
    
    Label(services_window, text="Услуги отеля", font=('Arial', 12, 'bold'), 
          bg='lightblue', fg='darkblue').pack(pady=20)
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ServiceName, Price FROM Service")
            services = cursor.fetchall()
            
            main_frame = Frame(services_window, bg='lightblue')
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            canvas = Canvas(main_frame, bg='lightblue', highlightthickness=0)
            scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg='lightblue')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            grid_frame = Frame(scrollable_frame, bg='lightblue')
            grid_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)
            
            for i, service in enumerate(services):
                service_name, price = service
                
                row = i // 2  
                col = i % 2   
                
                service_frame = Frame(grid_frame, relief=RAISED, borderwidth=1, 
                                    bg='white', padx=10, pady=10)
                service_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                Label(service_frame, text=service_name, font=('Arial', 11, 'bold'), 
                      bg='white', fg='#333333').pack(anchor='w')
                
                Label(service_frame, text=f"{price} руб.", font=('Arial', 10), 
                      bg='white', fg='#006600').pack(anchor='w')
                
                grid_frame.columnconfigure(col, weight=1)
                grid_frame.rowconfigure(row, weight=1)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            Button(services_window, text="Назад", command=services_window.destroy, 
                   bg='lightcoral', width=15, font=('Arial', 10)).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки услуг: {e}")
        finally:
            conn.close()

# Просмотр бронирований пользователя 
def view_my_bookings(user_id):
    bookings_window = Toplevel()
    bookings_window.title("Мои бронирования")
    bookings_window.configure(bg='lightblue')  
    bookings_window.geometry('500x500')
    
   
    header_frame = Frame(bookings_window, bg='lightblue')
    header_frame.pack(fill=X, padx=20, pady=15)
    
    Label(header_frame, text="Мои бронирования", font=('Arial', 18, 'bold'), 
          bg='lightblue', fg='#000000').pack(side=LEFT, padx=10)
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.BookingID, r.Room_number, r.RoomType, r.Price, 
                       b.CheckInDate, b.CheckOutDate
                FROM Bookings b 
                JOIN Rooms r ON b.RoomID = r.RoomID 
                WHERE b.UserID = ?
            """, (user_id,))
            
            bookings = cursor.fetchall()
            
            if bookings:
               
                main_frame = Frame(bookings_window, bg="#ffffff")
                main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
                
                for booking in bookings:
                    booking_id, room_number, room_type, price, checkin, checkout = booking
                    
                    
                    card_frame = Frame(main_frame, bg='white', relief=RAISED, 
                                     borderwidth=2, highlightbackground='#bdc3c7')
                    card_frame.pack(fill=X, pady=8, padx=5)
                    
                    
                    top_frame = Frame(card_frame, bg='#ffffff')
                    top_frame.pack(fill=X)
                    
                    Label(top_frame, text=f"Комната №{room_number}", 
                          font=('Arial', 14, 'bold'), bg="#ffffff", fg='#000000',
                          padx=15, pady=8).pack(anchor='w')
                    
                
                    info_frame = Frame(card_frame, bg='white')
                    info_frame.pack(fill=X, padx=15, pady=12)
                    
                    
                    Label(info_frame, text="Тип:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=0, column=0, sticky='w')
                    Label(info_frame, text=room_type, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=0, column=1, sticky='w', padx=(5, 20))
                    
                  
                    Label(info_frame, text="Цена:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=0, column=2, sticky='w')
                    Label(info_frame, text=f"{price} руб.", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#27ae60').grid(row=0, column=3, sticky='w', padx=5)
                    
                   
                    Label(info_frame, text="Заезд:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=1, column=0, sticky='w', pady=(8, 0))
                    Label(info_frame, text=checkin, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=1, column=1, sticky='w', padx=5, pady=(8, 0))
                    
                    Label(info_frame, text="Выезд:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=1, column=2, sticky='w', pady=(8, 0))
                    Label(info_frame, text=checkout, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=1, column=3, sticky='w', padx=5, pady=(8, 0))
                    
                  
                    btn_frame = Frame(card_frame, bg='white')
                    btn_frame.pack(fill=X, padx=15, pady=(5, 12))
                    
                    Button(btn_frame, text="Отменить", 
                           command=lambda bid=booking_id, rnum=room_number: cancel_booking(bid, rnum),
                           bg="#ff270f", fg='white', font=('Arial', 9, 'bold'),
                           relief=RAISED, bd=2, padx=10, pady=4).pack(side=RIGHT)
            else:
               
                empty_frame = Frame(bookings_window, bg='#f0f8ff')
                empty_frame.pack(expand=True)
                
                Label(empty_frame, text="", font=('Arial', 48), 
                      bg='#f0f8ff', fg="#000000").pack(pady=10)
                Label(empty_frame, text="Нет активных бронирований", 
                      font=('Arial', 14), bg='#f0f8ff', fg='#7f8c8d').pack()
                Label(empty_frame, text="Забронируйте комнату в разделе 'Комнаты'", 
                      font=('Arial', 10), bg='#f0f8ff', fg='#95a5a6').pack()
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки бронирований: {e}")
        finally:
            conn.close()
    
   
    Button(bookings_window, text="Назад", command=bookings_window.destroy, 
           bg="#f8233f", fg='white', width=15, font=('Arial', 10),
           relief=RAISED, bd=2).pack(pady=15)

def cancel_booking(booking_id, room_number):
    if messagebox.askyesno("Подтверждение", f"Отменить бронирование комнаты №{room_number}?"):
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
                cursor.execute("SELECT RoomID FROM Bookings WHERE BookingID = ?", (booking_id,))
                room_result = cursor.fetchone()
                
                if room_result:
                    room_id = room_result[0]
                    
                    cursor.execute("DELETE FROM Bookings WHERE BookingID = ?", (booking_id,))
                    
                    cursor.execute("UPDATE Rooms SET RoomStatus = 'Свободна' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", f"Бронирование отменено!")
                    
                    for window in root.winfo_children():
                        if isinstance(window, Toplevel) and "Мои бронирования" in window.title():
                            window.destroy()
                            view_my_bookings(get_current_user_id())
                            break
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка отмены бронирования: {e}")
            finally:
                conn.close()

# поиск пользователя по ID (нужно для отмены бронирования)
def get_current_user_id():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (entry_username.get(),))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Ошибка получения ID пользователя: {e}")
            return None
        finally:
            conn.close()

# Редактирование профиля
def edit_profile(user_id):
    profile_window = Toplevel()
    profile_window.title("Редактирование профиля")
    profile_window.configure(bg='lightblue')
    profile_window.geometry('400x350')

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username, FirstName, LastName, Phone, Email FROM Users WHERE user_id=?", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                username, first_name, last_name, phone, email = user_data
                
                Label(profile_window, text="Редактирование профиля", font=('Arial', 16), bg='lightblue').pack(pady=10)
                
                frame = Frame(profile_window, bg='lightblue')
                frame.pack(pady=10)
                
                entries = {}
                fields = [
                    ("Логин:", "username", username),
                    ("Имя:", "firstname", first_name),
                    ("Фамилия:", "lastname", last_name),
                    ("Телефон:", "phone", phone),
                    ("Email:", "email", email)
                ]
                
                for i, (label, field, value) in enumerate(fields):
                    Label(frame, text=label, bg='lightblue').grid(row=i, column=0, sticky=W, pady=5)
                    entry = Entry(frame, width=20)
                    entry.insert(0, value)
                    entry.grid(row=i, column=1, pady=5, padx=5)
                    entries[field] = entry
                
                def save_profile():
                    save_conn = connect_db()
                    if save_conn:
                        try:
                            save_cursor = save_conn.cursor()
                            
                            new_username = entries['username'].get()
                            new_firstname = entries['firstname'].get()
                            new_lastname = entries['lastname'].get()
                            new_phone = entries['phone'].get()
                            new_email = entries['email'].get()
                            
                            if not new_username:
                                messagebox.showerror("Ошибка", "Заполните логин")
                                return
                            
                            save_cursor.execute("""
                                UPDATE Users 
                                SET username=?, FirstName=?, LastName=?, Phone=?, Email=?
                                WHERE user_id=?
                            """, (new_username, new_firstname, new_lastname, new_phone, new_email, user_id))
                            save_conn.commit()
                            messagebox.showinfo("Успех", "Профиль обновлен!")
                            profile_window.destroy()
                        except Exception as e:
                            messagebox.showerror("Ошибка", f"Ошибка обновления: {e}")
                        finally:
                            save_conn.close()
                
                Button(frame, text="Сохранить", command=save_profile, 
                       bg='lightgreen', width=10).grid(row=5, column=1, pady=10, sticky=E)
                Button(frame, text="Отмена", command=profile_window.destroy, 
                       bg='lightcoral', width=10).grid(row=5, column=0, pady=10, sticky=W)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки профиля: {e}")
        finally:
            conn.close()

# Управление бронированиями 
def manage_bookings():
    bookings_window = Toplevel()
    bookings_window.title("Управление бронированиями")
    bookings_window.configure(bg='lightblue')
    bookings_window.geometry('1000x600')
    
    Label(bookings_window, text="Управление бронирований", font=('Arial', 16), bg='lightblue').pack(pady=10)
    
    # Панель поиска
    search_frame = Frame(bookings_window, bg='lightblue')
    search_frame.pack(pady=5)
    
    Label(search_frame, text="Поиск:", bg='lightblue').pack(side=LEFT, padx=5)
    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var, width=30)
    search_entry.pack(side=LEFT, padx=5)
    
    Button(search_frame, text="Скачать отчет", bg='lightgrey',
           command=lambda: download_report()).pack(side=LEFT, padx=5)
    
    # Основной фрейм для таблицы
    main_frame = Frame(bookings_window, bg='lightblue')
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    # Хранилище для данных
    all_bookings_data = []
    
    def load_bookings():
        """Загружаем данные из БД"""
        nonlocal all_bookings_data
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.BookingID, u.username, r.Room_number, r.RoomType,
                           b.CheckInDate, b.CheckOutDate
                    FROM Bookings b
                    JOIN Users u ON b.UserID = u.user_id
                    JOIN Rooms r ON b.RoomID = r.RoomID
                    ORDER BY b.CheckInDate DESC
                """)
                all_bookings_data = cursor.fetchall()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки: {e}")
            finally:
                conn.close()
    
    def display_bookings():
        """Отображаем таблицу"""
        # Очищаем основной фрейм
        for widget in main_frame.winfo_children():
            widget.destroy()
        
        # Создаем прокручиваемую область
        canvas = Canvas(main_frame, bg='lightblue')
        scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='lightblue')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Заголовки таблицы
        headers = ["ID", "Пользователь", "Комната", "Тип", "Заезд", "Выезд", "Действия"]
        for i, header in enumerate(headers):
            bg_color = 'lightgray' if i < 6 else 'lightblue'
            Label(scrollable_frame, text=header, font=('Arial', 10, 'bold'), 
                  bg=bg_color, width=15).grid(row=0, column=i, padx=2, pady=2)
        
        # Поисковый текст
        search_text = search_var.get().strip().lower()
        found_count = 0
        
        # Данные таблицы
        for row_idx, booking in enumerate(all_bookings_data, 1):
            booking_id, username, room_number, room_type, checkin, checkout = booking
            
            # Форматируем даты
            checkin_str = checkin.strftime('%Y-%m-%d') if hasattr(checkin, 'strftime') else str(checkin)
            checkout_str = checkout.strftime('%Y-%m-%d') if hasattr(checkout, 'strftime') else str(checkout)
            
            # Проверяем поиск
            booking_str = f"{booking_id} {username} {room_number} {room_type} {checkin_str} {checkout_str}".lower()
            match_search = search_text in booking_str
            
            # Подсветка при совпадении
            bg_color = 'lightgrey' if match_search and search_text else 'white'
            
            if search_text and not match_search:
                continue  # Пропускаем если есть поиск и нет совпадения
            
            found_count += 1
            
            # Отображаем строку
            Label(scrollable_frame, text=booking_id, bg=bg_color, width=15).grid(row=row_idx, column=0, padx=2, pady=1)
            Label(scrollable_frame, text=username, bg=bg_color, width=15).grid(row=row_idx, column=1, padx=2, pady=1)
            Label(scrollable_frame, text=room_number, bg=bg_color, width=15).grid(row=row_idx, column=2, padx=2, pady=1)
            Label(scrollable_frame, text=room_type, bg=bg_color, width=15).grid(row=row_idx, column=3, padx=2, pady=1)
            Label(scrollable_frame, text=checkin_str, bg=bg_color, width=15).grid(row=row_idx, column=4, padx=2, pady=1)
            Label(scrollable_frame, text=checkout_str, bg=bg_color, width=15).grid(row=row_idx, column=5, padx=2, pady=1)
            
            Button(scrollable_frame, text="Удалить", bg='lightcoral', font=('Arial', 8), width=10,
                  command=lambda bid=booking_id: delete_booking(bid)).grid(row=row_idx, column=6, padx=2, pady=1)
        
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def delete_booking(booking_id):
        """Удаление бронирования"""
        if messagebox.askyesno("Подтверждение", "Удалить бронирование?"):
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Удаляем связанные записи
                    cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                    cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
                    
                    # Освобождаем комнату
                    cursor.execute("SELECT RoomID FROM Bookings WHERE BookingID = ?", (booking_id,))
                    room_result = cursor.fetchone()
                    
                    if room_result:
                        room_id = room_result[0]
                        cursor.execute("DELETE FROM Bookings WHERE BookingID = ?", (booking_id,))
                        cursor.execute("UPDATE Rooms SET RoomStatus = 'Свободна' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", "Бронирование удалено")
                    
                    # Обновляем отображение
                    load_bookings()
                    display_bookings()
                    
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")
                finally:
                    conn.close()
    
    def download_report():
        """Скачивание отчета"""
        search_text = search_var.get().strip()
        search_lower = search_text.lower() if search_text else ""
        
        # Фильтруем данные для отчета
        report_data = []
        for booking in all_bookings_data:
            booking_id, username, room_number, room_type, checkin, checkout = booking
            
            checkin_str = checkin.strftime('%Y-%m-%d') if hasattr(checkin, 'strftime') else str(checkin)
            checkout_str = checkout.strftime('%Y-%m-%d') if hasattr(checkout, 'strftime') else str(checkout)
            
            booking_str = f"{booking_id} {username} {room_number} {room_type} {checkin_str} {checkout_str}".lower()
            
            if not search_text or search_lower in booking_str:
                report_data.append((booking_id, username, room_number, room_type, checkin_str, checkout_str))
        
        if not report_data:
            messagebox.showinfo("Информация", "Нет данных для отчета")
            return
        
        # Создаем имя файла
        from datetime import datetime
        filename = f"отчет_бронирования_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Заголовок
                f.write("=" * 60 + "\n")
                f.write("ОТЧЕТ ПО БРОНИРОВАНИЯМ\n")
                f.write(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                if search_text:
                    f.write(f"Поиск: '{search_text}'\n")
                f.write(f"Записей: {len(report_data)}\n")
                f.write("=" * 60 + "\n\n")
                
                # Данные
                for data in report_data:
                    f.write(f"ID: {data[0]}\n")
                    f.write(f"Пользователь: {data[1]}\n")
                    f.write(f"Комната: {data[2]}\n")
                    f.write(f"Тип: {data[3]}\n")
                    f.write(f"Заезд: {data[4]}\n")
                    f.write(f"Выезд: {data[5]}\n")
                    f.write("-" * 40 + "\n\n")
            
            messagebox.showinfo("Успех", f"Отчет сохранен:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")
    
    def update_display(*args):
        """Обновляем отображение при изменении поиска"""
        display_bookings()
    
    # Привязываем события
    search_var.trace('w', update_display)  # Поиск в реальном времени
    
    # Загрузка и отображение
    load_bookings()
    display_bookings()
    
    Button(bookings_window, text="Назад", command=bookings_window.destroy, bg='lightcoral').pack(pady=5)
    
def view_database_tables():
    """Просмотр таблиц базы данных"""
    
    table_window = Toplevel()
    table_window.title("Отчеты по таблицам")
    table_window.geometry('1000x600')
    table_window.configure(bg='lightblue')
    
    # Глобальная переменная для хранения всех данных
    global all_table_data
    all_table_data = {}
    
    # Верхняя панель
    Label(table_window, text="Таблица:", bg='lightblue').place(x=10, y=10)
    table_var = StringVar()
    table_combo = ttk.Combobox(table_window, textvariable=table_var, width=15)
    table_combo.place(x=70, y=10)
    
    Label(table_window, text="Поиск:", bg='lightblue').place(x=200, y=10)
    search_var = StringVar()
    search_entry = Entry(table_window, textvariable=search_var, width=20)
    search_entry.place(x=250, y=10)
    
    # Таблица с прокруткой
    tree = ttk.Treeview(table_window, show="headings")
    scrollbar = ttk.Scrollbar(table_window, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.place(x=10, y=50, width=980, height=500)
    scrollbar.place(x=990, y=50, height=500)
    
    # Кнопки
    Button(table_window, text="Скачать отчет", 
           command=lambda: download_report(tree, table_var.get())).place(x=10, y=560)
    Button(table_window, text="Назад", command=table_window.destroy).place(x=120, y=560)

    def load_tables():
        """Загружаем список таблиц"""
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sys.tables")
                tables = [row[0] for row in cursor.fetchall()]
                table_combo['values'] = tables
                if tables:
                    table_combo.set(tables[0])
                    load_table_data(tables[0])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки таблиц: {e}")
            finally:
                conn.close()

    def load_table_data(table_name):
        """Загружаем данные таблицы с сохранением"""
        global all_table_data
        
        if not table_name:
            return
            
        conn = connect_db()
        if conn:
            try:
                tree.delete(*tree.get_children())
                
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name} WHERE 1=0")
                columns = [column[0] for column in cursor.description]
                
                tree['columns'] = columns
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120)
                
                cursor.execute(f"SELECT * FROM {table_name}")
                all_data = []
                for row in cursor.fetchall():
                    formatted_row = []
                    for value in row:
                        if hasattr(value, 'strftime'):
                            formatted_row.append(value.strftime('%Y-%m-%d %H:%M'))
                        else:
                            formatted_row.append(str(value) if value is not None else '')
                    all_data.append(formatted_row)
                
                # Сохраняем все данные
                all_table_data[table_name] = all_data
                
                # Отображаем все данные
                display_filtered_data(table_name)
                
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
            finally:
                conn.close()

    def display_filtered_data(table_name, search_text=""):
        """Отображаем отфильтрованные данные"""
        tree.delete(*tree.get_children())
        
        if table_name not in all_table_data:
            return
        
        data = all_table_data[table_name]
        displayed_count = 0
        
        if not search_text:
            # Показываем все данные
            for row in data:
                tree.insert("", END, values=row)
                displayed_count = len(data)
        else:
            # Фильтруем данные
            search_text_lower = search_text.lower()
            for row in data:
                if any(search_text_lower in str(value).lower() for value in row):
                    tree.insert("", END, values=row, tags=('found',))
                    displayed_count += 1
            
            tree.tag_configure('found', background='lightgrey')
        

    def search_data(event=None):
        """Поиск по таблице"""
        search_text = search_var.get()
        table_name = table_var.get()
        
        if not table_name:
            messagebox.showwarning("Предупреждение", "Сначала выберите таблицу")
            return
        
        if not search_text:
            # Если поиск пустой, показываем все данные
            load_table_data(table_name)
            return
        
        # Отображаем отфильтрованные данные
        display_filtered_data(table_name, search_text)

    def download_report(tree, table_name):
        """Скачиваем отчет - либо полный, либо по результатам поиска"""
        try:
            if not table_name:
                messagebox.showwarning("Предупреждение", "Сначала выберите таблицу")
                return
                
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Сохранить отчет"
            )
            if file_path:
                # Получаем ВИДИМЫЕ в данный момент элементы в treeview
                visible_items = tree.get_children()
                count = len(visible_items)
                search_text = search_var.get()

                with open(file_path, 'w', encoding='utf-8') as file:
                    # Заголовок отчета с учетом поиска
                    file.write("=" * 60 + "\n")
                    if search_text:
                        file.write(f"ОТЧЕТ ИЗ ТАБЛИЦЫ: {table_name}\n")
                    else:
                        file.write(f"ПОЛНЫЙ ОТЧЕТ ИЗ ТАБЛИЦЫ: {table_name}\n")
                    
                    file.write(f"Дата формирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"Количество записей: {count}\n")
                    file.write("=" * 60 + "\n\n")
                    
                    # Получаем названия колонок
                    columns = tree['columns']
                    
                    # Записываем данные в красивом формате
                    for i, item in enumerate(visible_items, 1):
                        values = tree.item(item)['values']
                        file.write("-" * 50 + "\n")
                        file.write(f"ЗАПИСЬ #{i}\n")
                        file.write("-" * 50 + "\n")
                        
                        # Выводим каждое поле в формате "Название: значение"
                        for col_name, value in zip(columns, values):
                            # Подсветка найденного текста в отчете
                            if search_text and search_text.lower() in str(value).lower():
                                file.write(f"{col_name}: **{value}**\n")
                            else:
                                file.write(f"{col_name}: {value}\n")
                        
                        file.write("\n")  # Пустая строка между записями
                    
                    file.write("=" * 60 + "\n")
                    if search_text:
                        file.write(f"Всего найдено записей: {count}\n")
                    else:
                        file.write(f"Всего записей в таблице: {count}\n")
                    file.write("=" * 60 + "\n")
                    
                messagebox.showinfo("Успех", 
                    f"Отчет сохранен:\n{file_path}\n\n")
            else:
                messagebox.showinfo("Отмена", "Сохранение отменено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении отчета: {e}")

    # Привязываем события
    table_combo.bind('<<ComboboxSelected>>', lambda e: load_table_data(table_var.get()))
    search_entry.bind('<KeyRelease>', search_data)
    search_entry.bind('<Return>', search_data)  # Поиск по Enter
    
    # Загружаем таблицы при открытии окна
    load_tables()

# Основное окно авторизации
root = Tk()
root.title("Авторизация")
root.configure(bg='lightblue')
root.geometry('350x300')

Label(root, text="Вход в аккаунт", font=('Arial', 16), bg='lightblue').pack(pady=10)

frame = Frame(root, bg='lightblue')
frame.pack(pady=10)

Label(frame, text="Логин:", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
entry_username = Entry(frame, width=20)
entry_username.grid(row=0, column=1, pady=5, padx=5)

Label(frame, text="Пароль:", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
entry_password = Entry(frame, show='*', width=20)
entry_password.grid(row=1, column=1, pady=5, padx=5)

Button(root, text="Войти", command=authenticate_user, bg='lightgrey', width=10).pack(pady=5)
Button(root, text="Регистрация", command=register_user, bg='lightgreen', width=10).pack(pady=5)

label_status = Label(root, text="Введите данные для входа", fg='black', bg='lightblue')
label_status.pack(pady=10)

root.mainloop()