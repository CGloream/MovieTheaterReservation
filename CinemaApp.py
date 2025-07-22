from models.Cinema import Cinema
from models.Movie import Movie
from models.ScreeningRoom import ScreeningRoom
from models.Screening import Screening
from models.Reservation import Reservation

from data_storage.DataStorage import DataStorage

from logics.ReservationManager import ReservationManager
from logics.AdminManager import AdminManager

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime, timedelta


class CinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHENG Movie Reservation System")
        self.root.geometry("1200x800")
        
        self.cinema = Cinema("CHENG Movie Theater")
        self.data_storage = DataStorage("cinema_data.json")
        
        self.reservation_manager = ReservationManager(self.cinema)
        self.admin_manager = AdminManager(self.cinema)
        self.load_data()
        
        self.create_widgets()
        self.show_main_menu()
    
    def load_data(self):
        loaded_cinema = self.data_storage.load_data()
        if loaded_cinema:
            self.cinema = loaded_cinema
            # Update next IDs
            if self.cinema.movies:
                self.admin_manager.next_movie_id = max(m.id for m in self.cinema.movies) + 1
            if self.cinema.screenings:
                self.admin_manager.next_screening_id = max(s.id for s in self.cinema.screenings) + 1
            if self.cinema.reservations:
                self.reservation_manager.next_reservation_id = max(r.id for r in self.cinema.reservations) + 1
    
    def save_data(self):
        self.data_storage.save_data(self.cinema)
    
    def create_widgets(self):
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # create navigation bar
        self.navbar = tk.Frame(self.main_frame, bg="#333")
        self.navbar.pack(fill=tk.X)
        
        self.user_btn = tk.Button(self.navbar, text="User Mode", command=self.show_main_menu, bg="#333", fg="white", padx=20, pady=10, relief=tk.FLAT)
        self.user_btn.pack(side=tk.LEFT)
        
        self.admin_btn = tk.Button(self.navbar, text="Admin Mode", command=self.show_admin_login, bg="#333", fg="white", padx=20, pady=10, relief=tk.FLAT)
        self.admin_btn.pack(side=tk.LEFT)
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def clear_content(self):
        # clear all widgets
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Welcome To CHENG Movie Reservation System", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # list hot movies
        movies_frame = tk.LabelFrame(self.content_frame, text="Movies Now Showing", font=("Arial", 14))
        movies_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        if not self.cinema.movies:
            no_movies_label = tk.Label(movies_frame, text="Currently No Movie Showing", font=("Arial", 12))
            no_movies_label.pack(pady=20)
        else:
            for movie in self.cinema.movies:
                movie_frame = tk.Frame(movies_frame, bd=1, relief=tk.SOLID, padx=10, pady=10)
                movie_frame.pack(fill=tk.X, pady=5)
                
                title_label = tk.Label(movie_frame, text=movie.title, font=("Arial", 14, "bold"))
                title_label.pack(anchor=tk.W)
                
                info_label = tk.Label(movie_frame, text=f"{movie.rating} | {movie.duration} min")
                info_label.pack(anchor=tk.W)
                
                desc_label = tk.Label(movie_frame, text=movie.description, wraplength=800)
                desc_label.pack(anchor=tk.W, pady=5)
                
                book_btn = tk.Button(movie_frame, text="Reserve", command=lambda m=movie: self.show_screenings(m.id))
                book_btn.pack(side=tk.RIGHT, padx=10)
    
    def show_screenings(self, movie_id):
        self.clear_content()
        
        movie = next((m for m in self.cinema.movies if m.id == movie_id), None)
        if not movie:
            messagebox.showerror("Error", "Movie not exists")
            self.show_main_menu()
            return
        
        title = tk.Label(self.content_frame, text=f"{movie.title} - Choose Screening", font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        screenings = self.cinema.get_screenings_by_movie(movie_id)
        
        if not screenings:
            no_screenings_label = tk.Label(self.content_frame, text="No Screening", font=("Arial", 12))
            no_screenings_label.pack(pady=20)
        else:
            for screening in screenings:
                room = next((r for r in self.cinema.screening_rooms if r.id == screening.room_id), None)
                if not room:
                    continue
                
                screening_frame = tk.Frame(self.content_frame, bd=1, relief=tk.SOLID, padx=10, pady=10)
                screening_frame.pack(fill=tk.X, pady=5)
                
                time_label = tk.Label(screening_frame, text=f"Time: {screening.start_time.strftime('%Y-%m-%d %H:%M')}", font=("Arial", 12))
                time_label.pack(anchor=tk.W)
                
                room_label = tk.Label(screening_frame, text=f"Screening room: {room.name}", font=("Arial", 12))
                room_label.pack(anchor=tk.W)
                
                price_label = tk.Label(screening_frame, text=f"Ticket price: ¥{screening.price}", font=("Arial", 12))
                price_label.pack(anchor=tk.W)
                
                available_seats = screening.get_available_seats(room)
                seat_count_label = tk.Label(screening_frame, text=f"Seats available: {len(available_seats)}/{room.get_total_seats()}", font=("Arial", 12))
                seat_count_label.pack(anchor=tk.W)
                
                book_btn = tk.Button(screening_frame, text="Select Seats", command=lambda s=screening, r=room: self.show_seat_selection(s.id, r.id))
                book_btn.pack(side=tk.RIGHT, padx=10)
    
    def show_seat_selection(self, screening_id, room_id):
        self.clear_content()
        
        screening = self.cinema.get_screening_by_id(screening_id)
        room = next((r for r in self.cinema.screening_rooms if r.id == room_id), None)
        
        if not screening or not room:
            messagebox.showerror("Error", "Screening or room doesn't exist")
            self.show_main_menu()
            return
        
        title = tk.Label(self.content_frame, text=f"Select Seats - {screening.start_time.strftime('%Y-%m-%d %H:%M')} | {room.name}", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Display screen
        screen_frame = tk.Frame(self.content_frame, height=30, bg="lightgray")
        screen_frame.pack(fill=tk.X, padx=100, pady=20)
        screen_label = tk.Label(screen_frame, text="Screen", font=("Arial", 14, "bold"), bg="lightgray")
        screen_label.pack(pady=5)
        
        # Create seat selection area
        seats_frame = tk.Frame(self.content_frame)
        seats_frame.pack(pady=20)
        
        # Store selected seats
        self.selected_seats = []
        self.seat_buttons = {}
        
        available_seats = screening.get_available_seats(room)
        
        for row in range(1, room.rows + 1):
            row_frame = tk.Frame(seats_frame)
            row_frame.pack()
            
            for col in range(1, room.cols + 1):
                seat = (row, col)
                if seat in available_seats:
                    btn = tk.Button(row_frame, text=f"{row}-{col}", width=3, height=1,
                                   bg="green", fg="white",
                                   command=lambda s=seat: self.toggle_seat(s))
                else:
                    btn = tk.Button(row_frame, text=f"{row}-{col}", width=3, height=1,
                                   bg="red", fg="white", state=tk.DISABLED)
                
                btn.grid(row=row, column=col, padx=2, pady=2)
                self.seat_buttons[seat] = btn
        
        # Display selected seats
        selected_frame = tk.LabelFrame(self.content_frame, text="Selected Seats")
        selected_frame.pack(fill=tk.X, pady=10)
        
        self.selected_seats_label = tk.Label(selected_frame, text="No seats selected")
        self.selected_seats_label.pack(anchor=tk.W, padx=10)
        
        # Create booking button
        book_frame = tk.Frame(self.content_frame)
        book_frame.pack(pady=20)
        
        book_btn = tk.Button(book_frame, text="Confirm Selection", command=lambda: self.show_booking_form(screening_id, room_id),
                           bg="blue", fg="white", padx=20, pady=10)
        book_btn.pack()
    
    def toggle_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            self.seat_buttons[seat].config(bg="green")
        else:
            self.selected_seats.append(seat)
            self.seat_buttons[seat].config(bg="yellow", fg="black")
        
        if self.selected_seats:
            self.selected_seats_label.config(text=", ".join([f"{s[0]}-{s[1]}" for s in self.selected_seats]))
        else:
            self.selected_seats_label.config(text="No seats selected")
    
    def show_booking_form(self, screening_id, room_id):
        if not self.selected_seats:
            messagebox.showerror("Error", "Please select seats")
            return
        
        self.clear_content()
        
        screening = self.cinema.get_screening_by_id(screening_id)
        room = next((r for r in self.cinema.screening_rooms if r.id == room_id), None)
        
        if not screening or not room:
            messagebox.showerror("Error", "Screening or room not found")
            self.show_main_menu()
            return
        
        title = tk.Label(self.content_frame, text="Booking Information", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Display booking summary
        summary_frame = tk.LabelFrame(self.content_frame, text="Booking Summary")
        summary_frame.pack(fill=tk.X, pady=10)
        
        movie = next((m for m in self.cinema.movies if m.id == screening.movie_id), None)
        movie_title = movie.title if movie else "Unknown Movie"
        
        tk.Label(summary_frame, text=f"Movie: {movie_title}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(summary_frame, text=f"Time: {screening.start_time.strftime('%Y-%m-%d %H:%M')}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(summary_frame, text=f"Screening Room: {room.name}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(summary_frame, text=f"Seats: {', '.join([f'{s[0]}-{s[1]}' for s in self.selected_seats])}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(summary_frame, text=f"Total Price: ¥{len(self.selected_seats) * screening.price}", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=10)
        
        # Create form
        form_frame = tk.LabelFrame(self.content_frame, text="Personal Information")
        form_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = tk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        email_entry = tk.Entry(form_frame, width=30)
        email_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Submit button
        submit_btn = tk.Button(self.content_frame, text="Submit Booking", 
                             command=lambda: self.process_booking(screening_id, name_entry.get(), email_entry.get()),
                             bg="blue", fg="white", padx=20, pady=10)
        submit_btn.pack(pady=20)
    
    def process_booking(self, screening_id, name, email):
        if not name or not email:
            messagebox.showerror("Error", "Please enter name and email")
            return
        
        success, result = self.reservation_manager.make_reservation(
            screening_id, name, email, self.selected_seats
        )
        
        if success:
            self.save_data()
            self.show_booking_confirmation(result)
        else:
            messagebox.showerror("Error", result)
    
    def show_booking_confirmation(self, reservation):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Booking Confirmation", font=("Arial", 18, "bold"), fg="green")
        title.pack(pady=20)
        
        screening = self.cinema.get_screening_by_id(reservation.screening_id)
        movie = next((m for m in self.cinema.movies if m.id == screening.movie_id), None)
        movie_title = movie.title if movie else "Unknown Movie"
        
        confirmation_frame = tk.Frame(self.content_frame)
        confirmation_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(confirmation_frame, text=f"Booking ID: {reservation.id}", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Movie: {movie_title}", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Time: {screening.start_time.strftime('%Y-%m-%d %H:%M')}", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Seats: {', '.join([f'{s[0]}-{s[1]}' for s in reservation.seats])}", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Total Price: ¥{reservation.get_total_price(screening)}", font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Customer: {reservation.customer_name} ({reservation.customer_email})", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        tk.Label(confirmation_frame, text=f"Booking Time: {reservation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)
        
        home_btn = tk.Button(self.content_frame, text="Return to Home", command=self.show_main_menu,
                           bg="blue", fg="white", padx=20, pady=10)
        home_btn.pack(pady=20)
    
    def show_admin_login(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Admin Login", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        form_frame = tk.Frame(self.content_frame)
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        username_entry = tk.Entry(form_frame, width=30)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        password_entry = tk.Entry(form_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        login_btn = tk.Button(self.content_frame, text="Login", 
                           command=lambda: self.check_admin_login(username_entry.get(), password_entry.get()),
                           bg="blue", fg="white", padx=20, pady=10)
        login_btn.pack(pady=20)
    
    def check_admin_login(self, username, password):
        # Simple authentication (replace with proper authentication in a real application)
        if username == "admin" and password == "admin123":
            self.show_admin_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def show_admin_menu(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Admin Dashboard", font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        btn_frame = tk.Frame(self.content_frame)
        btn_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        add_movie_btn = tk.Button(btn_frame, text="Add Movie", command=self.show_add_movie_form,
                                 width=20, height=2, font=("Arial", 12))
        add_movie_btn.pack(pady=10)
        
        add_screening_btn = tk.Button(btn_frame, text="Add Screening", command=self.show_add_screening_form,
                                     width=20, height=2, font=("Arial", 12))
        add_screening_btn.pack(pady=10)
        
        view_reservations_btn = tk.Button(btn_frame, text="View Reservations", command=self.show_view_reservations,
                                         width=20, height=2, font=("Arial", 12))
        view_reservations_btn.pack(pady=10)
        
        logout_btn = tk.Button(btn_frame, text="Logout", command=self.show_main_menu,
                             width=20, height=2, font=("Arial", 12), fg="red")
        logout_btn.pack(pady=10)
    
    def show_add_movie_form(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Add New Movie", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        form_frame = tk.LabelFrame(self.content_frame, text="Movie Details")
        form_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        title_entry = tk.Entry(form_frame, width=50)
        title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Duration (min):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        duration_entry = tk.Entry(form_frame, width=20)
        duration_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Rating:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        rating_entry = tk.Entry(form_frame, width=20)
        rating_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Description:").grid(row=3, column=0, sticky=tk.NW, padx=10, pady=5)
        desc_text = tk.Text(form_frame, width=50, height=5)
        desc_text.grid(row=3, column=1, padx=10, pady=5)
        
        submit_btn = tk.Button(self.content_frame, text="Add Movie", 
                             command=lambda: self.process_add_movie(title_entry.get(), 
                                                                  duration_entry.get(), 
                                                                  rating_entry.get(), 
                                                                  desc_text.get("1.0", tk.END)),
                             bg="blue", fg="white", padx=20, pady=10)
        submit_btn.pack(pady=20)

        home_btn = tk.Button(self.content_frame, text="Return to Home", command=self.show_admin_menu,
                           bg="blue", fg="white", padx=20, pady=10)
        home_btn.pack(pady=20)
    
    def process_add_movie(self, title, duration, rating, description):
        if not title or not duration or not rating:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            duration = int(duration)
        except ValueError:
            messagebox.showerror("Error", "Duration must be an integer")
            return
        
        movie = self.admin_manager.add_movie(title, duration, rating, description.strip())
        self.save_data()
        
        messagebox.showinfo("Success", f"Movie '{movie.title}' added successfully")
        self.show_admin_menu()
    
    def show_add_screening_form(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="Add Screening", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        form_frame = tk.LabelFrame(self.content_frame, text="Screening Details")
        form_frame.pack(fill=tk.X, pady=10)
        
        # Movie selection
        tk.Label(form_frame, text="Movie:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        movie_var = tk.StringVar()
        movie_combo = ttk.Combobox(form_frame, textvariable=movie_var, width=47)
        
        movie_options = []
        movie_id_map = {}
        for movie in self.cinema.movies:
            movie_options.append(f"{movie.title} ({movie.rating})")
            movie_id_map[movie.title] = movie.id
        
        movie_combo['values'] = movie_options
        if movie_options:
            movie_combo.current(0)
        movie_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Screening room selection
        tk.Label(form_frame, text="Screening Room:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        room_var = tk.StringVar()
        room_combo = ttk.Combobox(form_frame, textvariable=room_var, width=47)
        
        room_options = []
        room_id_map = {}
        for room in self.cinema.screening_rooms:
            room_options.append(f"{room.name} ({room.rows}x{room.cols} seats)")
            room_id_map[room.name] = room.id
        
        room_combo['values'] = room_options
        if room_options:
            room_combo.current(0)
        room_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Date and time
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        date_entry = tk.Entry(form_frame, width=20)
        date_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(form_frame, text="Time (HH:MM):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        time_entry = tk.Entry(form_frame, width=20)
        time_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Ticket price
        tk.Label(form_frame, text="Ticket Price:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        price_entry = tk.Entry(form_frame, width=20)
        price_entry.grid(row=4, column=1, padx=10, pady=5)
        
        submit_btn = tk.Button(self.content_frame, text="Add Screening", 
                             command=lambda: self.process_add_screening(movie_var.get(), 
                                                                       room_var.get(), 
                                                                       date_entry.get(), 
                                                                       time_entry.get(), 
                                                                       price_entry.get(),
                                                                       movie_id_map,
                                                                       room_id_map),
                             bg="blue", fg="white", padx=20, pady=10)
        submit_btn.pack(pady=20)

        home_btn = tk.Button(self.content_frame, text="Return to Home", command=self.show_admin_menu,
                           bg="blue", fg="white", padx=20, pady=10)
        home_btn.pack(pady=20)
    
    def process_add_screening(self, movie_text, room_text, date_str, time_str, price_str, movie_id_map, room_id_map):
        if not movie_text or not room_text or not date_str or not time_str or not price_str:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            movie_title = movie_text.split(" (")[0]
            movie_id = movie_id_map[movie_title]
            
            room_name = room_text.split(" (")[0]
            room_id = room_id_map[room_name]
            
            datetime_str = f"{date_str} {time_str}"
            start_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            price = float(price_str)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return
        
        screening = self.admin_manager.add_screening(movie_id, room_id, start_time, price)
        self.save_data()
        
        messagebox.showinfo("Success", f"Screening added successfully: {screening.start_time.strftime('%Y-%m-%d %H:%M')}")
        self.show_admin_menu()
    
    def show_view_reservations(self):
        self.clear_content()
        
        title = tk.Label(self.content_frame, text="View Reservations", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Movie selection
        tk.Label(self.content_frame, text="Select Movie:").pack(anchor=tk.W, padx=10, pady=5)
        movie_var = tk.StringVar()
        movie_combo = ttk.Combobox(self.content_frame, textvariable=movie_var, width=47)
        
        movie_options = []
        movie_id_map = {}
        for movie in self.cinema.movies:
            movie_options.append(f"{movie.title} ({movie.rating})")
            movie_id_map[movie.title] = movie.id
        
        movie_combo['values'] = movie_options
        screening_var = tk.StringVar()
        screening_combo = ttk.Combobox(self.content_frame, textvariable=screening_var, width=47)

        if movie_options:
            movie_combo.current(0)
            movie_combo.bind("<<ComboboxSelected>>", 
                        lambda event, sv=screening_var, sc=screening_combo: 
                        self.update_screening_combo(event, movie_id_map, sv, sc))
        movie_combo.pack(anchor=tk.W, padx=10, pady=5)
        
        # Screening selection
        tk.Label(self.content_frame, text="Select Screening:").pack(anchor=tk.W, padx=10, pady=5)
        screening_var = tk.StringVar()
        screening_combo = ttk.Combobox(self.content_frame, textvariable=screening_var, width=47)
        screening_combo.pack(anchor=tk.W, padx=10, pady=5)
        
        # Initialize screening combobox
        if movie_options:
            selected_movie_title = movie_options[0].split(" (")[0]
            selected_movie_id = movie_id_map[selected_movie_title]
            self.update_screening_combo(None, movie_id_map, screening_var, screening_combo)
        
        # View button
        view_btn = tk.Button(self.content_frame, text="View Reservations", 
                            command=lambda: self.display_reservations(movie_id_map.get(movie_var.get().split(" (")[0]), 
                                                                     screening_combo.get()),
                            bg="blue", fg="white", padx=20, pady=10)
        view_btn.pack(pady=20)

        home_btn = tk.Button(self.content_frame, text="Return to Home", command=self.show_admin_menu,
                           bg="blue", fg="white", padx=20, pady=10)
        home_btn.pack(pady=20)

    def update_screening_combo(self, event, movie_id_map, screening_var, screening_combo):
        if event:
            selected_movie_title = event.widget.get().split(" (")[0]
        else:
            if movie_id_map:
                selected_movie_title = next(iter(movie_id_map))
            else:
                return
        
        movie_id = movie_id_map.get(selected_movie_title)
        if not movie_id:
            return
        
        screenings = self.cinema.get_screenings_by_movie(movie_id)
        screening_options = []
        screening_id_map = {}
        
        for screening in screenings:
            room = next((r for r in self.cinema.screening_rooms if r.id == screening.room_id), None)
            room_name = room.name if room else "Unknown Room"
            screening_options.append(f"{screening.start_time.strftime('%Y-%m-%d %H:%M')} | {room_name}")
            screening_id_map[screening.start_time.strftime('%Y-%m-%d %H:%M')] = screening.id
        
        screening_combo['values'] = screening_options
        if screening_options:
            screening_combo.current(0)
    
    def display_reservations(self, movie_id, screening_info):
        self.clear_content()
        
        if not movie_id or not screening_info:
            messagebox.showerror("Error", "Please select both movie and screening")
            self.show_view_reservations()
            return
        
        # Parse screening time from the combo box selection
        screening_time_str = screening_info.split(" | ")[0]
        screenings = self.cinema.get_screenings_by_movie(movie_id)
        
        screening = next((s for s in screenings if s.start_time.strftime('%Y-%m-%d %H:%M') == screening_time_str), None)
        
        if not screening:
            messagebox.showerror("Error", "Selected screening not found")
            self.show_view_reservations()
            return
        
        movie = next((m for m in self.cinema.movies if m.id == screening.movie_id), None)
        room = next((r for r in self.cinema.screening_rooms if r.id == screening.room_id), None)
        
        # Display screening information
        info_frame = tk.LabelFrame(self.content_frame, text="Screening Information")
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, text=f"Movie: {movie.title if movie else 'Unknown Movie'}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(info_frame, text=f"Time: {screening.start_time.strftime('%Y-%m-%d %H:%M')}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        tk.Label(info_frame, text=f"Screening Room: {room.name if room else 'Unknown Room'}", font=("Arial", 12)).pack(anchor=tk.W, padx=10)
        
        # Display reservations list
        reservations_frame = tk.LabelFrame(self.content_frame, text="Reservations List")
        reservations_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        reservations = self.cinema.get_reservations_by_screening(screening.id)
        
        if not reservations:
            tk.Label(reservations_frame, text="No reservations found", font=("Arial", 12)).pack(pady=20)
        else:
            # Create table
            columns = ("Reservation ID", "Customer Name", "Customer Email", "Seats", "Total Price", "Reservation Time")
            tree = ttk.Treeview(reservations_frame, columns=columns, show="headings")
            
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor=tk.CENTER)
            
            for reservation in reservations:
                seat_str = ", ".join([f"{s[0]}-{s[1]}" for s in reservation.seats])
                total_price = reservation.get_total_price(screening)
                tree.insert("", tk.END, values=(
                    reservation.id,
                    reservation.customer_name,
                    reservation.customer_email,
                    seat_str,
                    f"¥{total_price}",
                    reservation.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                ))
            
            tree.pack(fill=tk.BOTH, expand=True)
        
        back_btn = tk.Button(self.content_frame, text="Back", command=self.show_view_reservations,
                           bg="blue", fg="white", padx=20, pady=10)
        back_btn.pack(pady=20)

        home_btn = tk.Button(self.content_frame, text="Return to Home", command=self.show_admin_menu,
                           bg="blue", fg="white", padx=20, pady=10)
        home_btn.pack(pady=20)


def initialize_demo_data(cinema):
    # Add screening rooms
    room1 = ScreeningRoom(1, "Room 1", 10, 15)
    room2 = ScreeningRoom(2, "Room 2", 8, 12)
    room3 = ScreeningRoom(3, "Room 3", 12, 20)
    
    cinema.add_screening_room(room1)
    cinema.add_screening_room(room2)
    cinema.add_screening_room(room3)
    
    # Add movies
    movie1 = Movie(1, "Avengers: Endgame", 181, "PG-13", "The final chapter in the Marvel Cinematic Universe, where the remaining heroes must band together to reverse the damage caused by Thanos.")
    movie2 = Movie(2, "Titanic", 194, "PG-13", "A fictionalized account of the sinking of the RMS Titanic, and the love story between two passengers from different social classes.")
    movie3 = Movie(3, "Avatar", 162, "PG-13", "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.")
    
    cinema.add_movie(movie1)
    cinema.add_movie(movie2)
    cinema.add_movie(movie3)
    
    # Add screenings
    today = datetime.now()
    
    screening1 = Screening(1, 1, 1, today + timedelta(hours=2), 80.0)
    screening2 = Screening(2, 1, 1, today + timedelta(hours=5), 80.0)
    screening3 = Screening(3, 2, 2, today + timedelta(hours=1), 75.0)
    screening4 = Screening(4, 2, 2, today + timedelta(hours=4), 75.0)
    screening5 = Screening(5, 3, 3, today + timedelta(hours=3), 90.0)
    screening6 = Screening(6, 3, 3, today + timedelta(hours=6), 90.0)
    
    cinema.add_screening(screening1)
    cinema.add_screening(screening2)
    cinema.add_screening(screening3)
    cinema.add_screening(screening4)
    cinema.add_screening(screening5)
    cinema.add_screening(screening6)


if __name__ == "__main__":
    root = tk.Tk()
    app = CinemaApp(root)
    
    # If no data, initialize demo data
    if not app.cinema.movies:
        initialize_demo_data(app.cinema)
        app.save_data()
    
    root.mainloop()