import tkinter
import customtkinter
from FYPdatabaseFuncs import *
import tkinter.filedialog
from PIL import Image, ImageTk
import cv2
from io import BytesIO
global img_name
global users_window
global records_window
global policies_window
global add_new_window

policy_activites_list = ["smoking", "phone", "fighting", "free_time"]
week_days = ["saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


def admin_check(user, pas):
    if user == "admin" and pas == "pass":
        return True
    else:
        return False


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x400")
app.title("Policy Based Employee Monitoring System - User")

user_text = tkinter.StringVar()
pas_text = tkinter.StringVar()

# ---------- Open Admin Dashboard ------------------


def login_function():
    user = username_entry.get()
    pas = password_entry.get()

    if check_admin(user, pas):
        login_label.configure(text="Login Successful!")
        open_dashboard()
    else:
        login_label.configure(text="Please enter correct credentials")
    # open_dashboard()


def open_dashboard():

    # ----------------- Open new window ------------
    global main_window
    global add_new_window
    try:
        main_window.destroy()
    except:
        pass
    try:
        app.destroy()
    except:
        pass
    try:
        add_new_window.destroy()
    except:
        pass
    try:
        users_window.destroy()
    except:
        pass

    main_window = customtkinter.CTk()
    main_window.title("Policy Based Employee Monitoring System")
    main_window.state("zoomed")

    main_window.grid_columnconfigure((0), weight=1)
    main_window.grid_rowconfigure(0, weight=1)
    #
    # lb = customtkinter.CTkLabel(main_window, text=".")
    # lb.grid(row=0, column=1)

    # scrollbar = customtkinter.CTkScrollbar(main_window, command=)

    # this method will open new window and show all POLICIES

    def open_all_policies(start_index):

        print("start_index ", start_index)
        try:
            main_window.destroy()
        except:
            print("Main window not destroyed")
        global policies_window

        try:
            print("In try")
            policies_window.destroy()
        except:
            print("records window not destroyed")

        policies_window = customtkinter.CTk()
        policies_window.title("All Users")
        policies_window.state("zoomed")

        def next_page(index):
            index = index + 10
            # users_window.destroy()
            print("Index ", index)
            open_all_policies(index)

        def pre_page(index):
            # users_window.destroy()
            index -= 10
            if index < 0:
                index = 0
            open_all_policies(index)

        def back_to_dash():
            policies_window.destroy()
            open_dashboard()

        def delete_function(id_delete, index):
            # Configure and connect to Postgres
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )
            # Create a cursor
            c = conn.cursor()

            print("connection established")
            query = f"DELETE FROM policies WHERE id={id_delete}"

            try:
                c.execute(query)
                conn.commit()
                conn.close()
                print("Query id: ", query)

            except:
                print("Query not done")

            open_all_policies(index)

        policies_window.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        policies_window.grid_rowconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(master=policies_window)
        frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20, columnspan=10)

        frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=2)

        all_policies_title_label = customtkinter.CTkLabel(master=frame, text="All Policies", text_font=("Roboto Medium", -28))
        all_policies_title_label.grid(row=0, column=1, pady=10, padx=10, columnspan=9)

        back_label = customtkinter.CTkButton(master=frame, text="Back", command=back_to_dash, fg_color="white")
        back_label.grid(row=0, column=0, pady=10, padx=10)

        # Headings

        id_label = customtkinter.CTkLabel(master=frame, text="ID", text_font=("Roboto Medium", -16))
        id_label.grid(row=1, column=0, pady=10, padx=0, columnspan=2)

        name_label = customtkinter.CTkLabel(master=frame, text="Activity Name", text_font=("Roboto Medium", -16))
        name_label.grid(row=1, column=2, pady=10, padx=0, columnspan=2)

        allowed_label = customtkinter.CTkLabel(master=frame, text="Allowed / Not Allowed", text_font=("Roboto Medium", -16))
        allowed_label.grid(row=1, column=4, pady=10, padx=0, columnspan=2)

        duration_label = customtkinter.CTkLabel(master=frame, text="Duration", text_font=("Roboto Medium", -16))
        duration_label.grid(row=1, column=6, pady=10, padx=0, columnspan=2)

        # Bottom Buttons

        # delete_entry = customtkinter.CTkEntry(master=policies_window, placeholder_text="Record ID to delete")
        # delete_entry.grid(row=1, column=0, pady=10, columnspan=2)
        #
        # delete_button = customtkinter.CTkButton(master=policies_window, text="Delete", command=lambda: delete_function(delete_entry.get(), start_index))
        # delete_button.grid(row=1, column=2, pady=10)

        pre_page_button = customtkinter.CTkButton(master=policies_window, text="Previous Page", command=lambda: pre_page(start_index))
        pre_page_button.grid(row=1, column=4, pady=10)

        next_page_button = customtkinter.CTkButton(master=policies_window, text="Next Page", command=lambda: next_page(start_index))
        next_page_button.grid(row=1, column=5, pady=10)

        # Headings done

        # Data Showing

        try:
        # Configure and connect to Postgres
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )

            # Create a cursor
            c = conn.cursor()

            print("connection established")

            sql_fetch_blob_query = f"SELECT * FROM policies LIMIT 10 OFFSET {start_index}"

            print("query done: ", sql_fetch_blob_query)

            c.execute(sql_fetch_blob_query)

            record = c.fetchall()
            count_records = len(record)
            n = 0
            for row_number in range(count_records):
                for col_number in range(4):

                    text = record[row_number][col_number]

                    if (row_number % 2) == 0:
                        color = "#4d4dff"
                        f_color = "#ffffff"
                    else:
                        color = "#b3b3ff"
                        f_color = "#000000"

                    if col_number == 2:
                        # print("text: ", type(text))
                        if text:
                            text = "Allowed"
                        else:
                            text = "Not Allowed"
                    customtkinter.CTkLabel(master=frame, text=text, fg_color=color, text_color=f_color).grid(
                        row=row_number + 2, column=col_number * 2, padx=10, pady=10, columnspan=2)

            conn.commit()
            conn.close()
        except:
            customtkinter.CTkLabel(frame, text="Check your internet connection, can not connect to database",
                               text_font=("Roboto Medium", -18)).grid(row=4, column=1, columnspan=4, pady=5)

        policies_window.mainloop()


    # this method will open new window and show all users

    def open_all_users(start_index):

        print("start_index ", start_index)
        try:
            main_window.destroy()
        except:
            print("Main window not destroyed")
        global users_window

        try:
            print("In try")
            users_window.destroy()
        except:
            print("records window not destroyed")

        users_window = customtkinter.CTk()
        users_window.title("All Users")
        users_window.state("zoomed")

        def next_page(index):
            index = index + 10
            # users_window.destroy()
            print("Index ", index)
            open_all_users(index)

        def pre_page(index):
            # users_window.destroy()
            index -= 10
            if index < 0:
                index = 0
            open_all_users(index)

        def back_to_dash():

            open_dashboard()

        def delete_function(id_delete, index):
            # Configure and connect to Postgres
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )

            # Create a cursor
            c = conn.cursor()

            print("connection established")
            query = f"DELETE FROM users WHERE id={id_delete}"

            try:
                c.execute(query)
                conn.commit()
                conn.close()
                print("Query id: ", query)

            except:
                print("Query not done")

            open_all_users(index)

        users_window.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        users_window.grid_rowconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(master=users_window)
        frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20, columnspan=10)

        frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=2)

        all_records_title_label = customtkinter.CTkLabel(master=frame, text="All Users", text_font=("Roboto Medium", -28))
        all_records_title_label.grid(row=0, column=1, pady=10, padx=10, columnspan=9)

        back_label = customtkinter.CTkButton(master=frame, text="Back", command=back_to_dash, fg_color="white")
        back_label.grid(row=0, column=0, pady=10, padx=10)

        # Headings

        id_label = customtkinter.CTkLabel(master=frame, text="ID", text_font=("Roboto Medium", -16))
        id_label.grid(row=1, column=0, pady=10, padx=0, columnspan=2)

        name_label = customtkinter.CTkLabel(master=frame, text="Username", text_font=("Roboto Medium", -16))
        name_label.grid(row=1, column=2, pady=10, padx=0, columnspan=2)

        password_label = customtkinter.CTkLabel(master=frame, text="Password", text_font=("Roboto Medium", -16))
        password_label.grid(row=1, column=4, pady=10, padx=0, columnspan=2)

        # Bottom Buttons

        # delete_entry = customtkinter.CTkEntry(master=users_window, placeholder_text="Record ID to delete")
        # delete_entry.grid(row=1, column=0, pady=10, columnspan=2)
        #
        # delete_button = customtkinter.CTkButton(master=users_window, text="Delete", command=lambda: delete_function(delete_entry.get(), start_index))
        # delete_button.grid(row=1, column=2, pady=10)

        pre_page_button = customtkinter.CTkButton(master=users_window, text="Previous Page", command=lambda: pre_page(start_index))
        pre_page_button.grid(row=1, column=4, pady=10)

        next_page_button = customtkinter.CTkButton(master=users_window, text="Next Page", command=lambda: next_page(start_index))
        next_page_button.grid(row=1, column=5, pady=10)

        # Headings done

        # Data Showing

        try:
        # Configure and connect to Postgres
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )

            # Create a cursor
            c = conn.cursor()

            print("connection established")

            sql_fetch_blob_query = f"SELECT * FROM users LIMIT 10 OFFSET {start_index}"

            print("query done: ", sql_fetch_blob_query)

            c.execute(sql_fetch_blob_query)

            record = c.fetchall()
            count_records = len(record)
            n = 0
            for row_number in range(count_records):
                for col_number in range(3):

                    text = record[row_number][col_number]

                    if (row_number % 2) == 0:
                        color = "#4d4dff"
                        f_color = "#ffffff"
                    else:
                        color = "#b3b3ff"
                        f_color = "#000000"
                    customtkinter.CTkLabel(master=frame, text=text, fg_color=color, text_color=f_color).grid(
                        row=row_number + 2, column=col_number * 2, padx=10, pady=10, columnspan=2)

            conn.commit()
            conn.close()
        except:
            customtkinter.CTkLabel(frame, text="Check your internet connection, can not connect to database",
                               text_font=("Roboto Medium", -18)).grid(row=4, column=1, columnspan=4, pady=5)

        users_window.mainloop()

    def open_all_employees(start_index):

        print("start_index ", start_index)
        try:
            main_window.destroy()
        except:
            print("Main window not destroyed")
        global employees_window

        try:
            print("In try")
            employees_window.destroy()
        except:
            print("records window not destroyed")

        employees_window = customtkinter.CTk()
        employees_window.title("All Uploaded Records")
        employees_window.state("zoomed")

        def next_page(index):
            index = index + 5
            # employees_window.destroy()
            print("Index ", index)
            open_all_employees(index)

        def pre_page(index):
            # employees_window.destroy()
            index -= 5
            if index < 0:
                index = 0
            open_all_employees(index)

        def back_to_dash():
            employees_window.destroy()
            open_dashboard()

        def delete_function(id_delete, index):
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )

            # Create a cursor
            c = conn.cursor()

            print("connection established")
            query = f"DELETE FROM employees WHERE id={id_delete}"

            try:
                c.execute(query)
                conn.commit()
                conn.close()
                print("Query id: ", query)

            except:
                print("Query not done")

            employees_window(index)

        employees_window.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=2)
        employees_window.grid_columnconfigure(0, weight=1)
        employees_window.grid_columnconfigure(9, weight=4)
        employees_window.grid_rowconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(master=employees_window)
        frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20, columnspan=10)
        # frame.configure(scrollcommand=)

        # for col in range(2, 10):
        #     frame.grid_columnconfigure(col, weight=2)
        # frame.grid_columnconfigure(1, weight=1)
        # frame.grid_columnconfigure(10, weight=4)

        frame.columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=2)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(9, weight=4)

        # frame.rowconfigure()

        all_records_title_label = customtkinter.CTkLabel(master=frame, text="All Employees", text_font=("Roboto Medium", -28))
        all_records_title_label.grid(row=0, column=1, pady=10, padx=10, columnspan=9)

        back_label = customtkinter.CTkButton(master=frame, text="Back", command=back_to_dash, fg_color="gray")
        back_label.grid(row=0, column=0, pady=10, padx=10)

        # Headings

        id_label = customtkinter.CTkLabel(master=frame, text="ID", text_font=("Roboto Medium", -16))
        id_label.grid(row=1, column=0, pady=10, padx=0)

        name_label = customtkinter.CTkLabel(master=frame, text="Name", text_font=("Roboto Medium", -16))
        name_label.grid(row=1, column=1, pady=10, padx=0)

        contact_name_label = customtkinter.CTkLabel(master=frame, text="Duty", text_font=("Roboto Medium", -16))
        contact_name_label.grid(row=1, column=2, pady=10, padx=0)

        contact_phone_label = customtkinter.CTkLabel(master=frame, text="Off Day", text_font=("Roboto Medium", -16))
        contact_phone_label.grid(row=1, column=3, pady=10, padx=0)

        gd_label = customtkinter.CTkLabel(master=frame, text="Office ID", text_font=("Roboto Medium", -16))
        gd_label.grid(row=1, column=4, pady=10, padx=0)

        off_name_label = customtkinter.CTkLabel(master=frame, text="Duty Start \nTime", text_font=("Roboto Medium", -16))
        off_name_label.grid(row=1, column=5, pady=10, padx=0)

        bp_label = customtkinter.CTkLabel(master=frame, text="Policies \nApplicable", text_font=("Roboto Medium", -16))
        bp_label.grid(row=1, column=6, pady=10, padx=0)

        off_phone_label = customtkinter.CTkLabel(master=frame, text="Department", text_font=("Roboto Medium", -16))
        off_phone_label.grid(row=1, column=7, pady=10, padx=0)

        remarks_label = customtkinter.CTkLabel(master=frame, text="Break Time", text_font=("Roboto Medium", -16))
        remarks_label.grid(row=1, column=8, pady=10, padx=0)

        photo_label = customtkinter.CTkLabel(master=frame, text="Photo", text_font=("Roboto Medium", -16))
        photo_label.grid(row=1, column=10, pady=10, padx=0)

        # Bottom Buttons

        # delete_entry = customtkinter.CTkEntry(master=employees_window, placeholder_text="Record ID to delete")
        # delete_entry.grid(row=1, column=1, pady=10, columnspan=2)
        #
        # delete_button = customtkinter.CTkButton(master=employees_window, text="Delete", command=lambda: delete_function(delete_entry.get(), start_index))
        # delete_button.grid(row=1, column=3, pady=10)

        pre_page_button = customtkinter.CTkButton(master=employees_window, text="Previous Page", command=lambda: pre_page(start_index))
        pre_page_button.grid(row=1, column=6, pady=10)

        next_page_button = customtkinter.CTkButton(master=employees_window, text="Next Page", command=lambda: next_page(start_index))
        next_page_button.grid(row=1, column=8, pady=10)

        # Headings done
        # Data Showing

        try:
            conn = psycopg2.connect(
                host="localhost",
                database="rao_pbems_db",
                user="postgres",
                password="rao123",
                port="5432",
            )
            # Create a cursor
            c = conn.cursor()

            print("connection established")

            sql_fetch_blob_query = f"SELECT * FROM employees LIMIT 5 OFFSET {start_index}"

            print("query done: ", sql_fetch_blob_query)

            c.execute(sql_fetch_blob_query)

            record = c.fetchall()
            count_records = len(record)
            n = 0
            blobs = []
            for row_number in range(count_records):
                for col_number in range(9):

                    text = record[row_number][col_number]

                    # if type(text)==type("str"):
                    #     text = add_LB(text)

                    if (row_number % 2) == 0:
                        color = "#4d4dff"
                        f_color = "#ffffff"
                    else:
                        color = "#b3b3ff"
                        f_color = "#000000"
                    customtkinter.CTkLabel(master=frame, text=text, fg_color=color, text_color=f_color).grid(
                        row=row_number + 2, column=col_number, padx=1, pady=10)
                # image_name = str(row_number) + '.jpg'
                # print("image_name: ", image_name)

                blobs.append(ImageTk.PhotoImage(Image.open(BytesIO(record[row_number][-1])).resize((100, 100))))
                customtkinter.CTkLabel(frame, image=blobs[-1]).grid(row=row_number + 2, column=10, pady=5)

            conn.commit()
            conn.close()
        except:
            customtkinter.CTkLabel(frame, text="Check your internet connection, can not connect to database",
                               text_font=("Roboto Medium", -18)).grid(row=4, column=1, columnspan=5, pady=5)

        employees_window.mainloop()

    def logout_function():
        logout_window = customtkinter.CTkToplevel()
        logout_window.title("Log out - Lost and Found User")
        logout_window.geometry("400x230")

        frame_right = customtkinter.CTkFrame(master=logout_window)
        frame_right.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        label = customtkinter.CTkLabel(master=frame_right, text="Do you really want to log out?",
                                       text_font=("Roboto Medium", -22))
        label.grid(row=0, column=0, pady=40, padx=10, rowspan=2, columnspan=2)

        cancel_button = customtkinter.CTkButton(master=frame_right, text="Cancel",
                                                command=lambda: logout_window.destroy())
        cancel_button.grid(row=2, column=0, pady=20, padx=20)

        rlogout_button = customtkinter.CTkButton(master=frame_right, text="Log Out",
                                                 command=lambda: main_window.destroy())
        rlogout_button.grid(row=2, column=1, pady=20, padx=20)

    def add_new_function():
        # print("start_index ", start_index)
        try:
            main_window.destroy()
        except:
            print("Main window not destroyed")
        global records_window

        try:
            print("In try")
            records_window.destroy()
        except:
            print("records window not destroyed")

        add_new_window = customtkinter.CTk()
        add_new_window.title("Add New")
        add_new_window.state("zoomed")

        def back_to_dash():
            add_new_window.destroy()
            open_dashboard()

        add_new_window.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        # add_new_window.grid_rowconfigure(0, weight=1)

        frame = customtkinter.CTkFrame(master=add_new_window)
        frame.grid(row=0, column=0, sticky="nswe", padx=20, pady=20, columnspan=12)

        # for col in range(2, 10):
        #     frame.grid_columnconfigure(col, weight=2)
        # frame.grid_columnconfigure(1, weight=1)
        # frame.grid_columnconfigure(10, weight=4)

        frame.columnconfigure((1, 2, 3), weight=2)
        # frame.columnconfigure((8, 10), weight=4)
        frame.columnconfigure(0, weight=1)

        # frame.rowconfigure()

        # all_records_title_label = customtkinter.CTkLabel(master=frame, text="All Filed Reports",
        #                                                  text_font=("Roboto Medium", -28))
        # all_records_title_label.grid(row=0, column=1, pady=10, padx=10, columnspan=9)

        back_label = customtkinter.CTkButton(master=frame, text="Back", command=back_to_dash, fg_color="gray")
        back_label.grid(row=0, column=0, pady=20, padx=10)

        status_label = customtkinter.CTkLabel(master=frame, text="")
        status_label.grid(row=0, column=3, pady=20, padx=10)


        # Add employee section

        sec2 = customtkinter.CTkFrame(master=frame)
        sec2.grid(row=1, column=0, sticky="nswe", padx=20, pady=20, columnspan=12)

        sec2.columnconfigure((1, 2, 3), weight=2)
        sec2.columnconfigure(0, weight=1)

        add_emp_label = customtkinter.CTkLabel(master=sec2, text="Add Employee",
                                                  text_font=("Roboto Medium", -22))
        add_emp_label.grid(row=1, column=0, pady=10, padx=10)

        image_label = customtkinter.CTkLabel(master=sec2, text="",
                                                  text_font=("Roboto Medium", -22))
        image_label.grid(row=2, column=0, pady=10, padx=10, rowspan=3)

        def upload_picture():
            global img2
            global img_name
            img_name = tkinter.filedialog.askopenfilename()
            img2 = ImageTk.PhotoImage(file=img_name)
            # lost_filename_label.config(text=filename)
            img2 = Image.open(img_name)
            width, height = img2.size
            # aspect_ratio = width / height
            if width > height:

                scale_factor = 140 / width
                width = 140
                height = height * scale_factor
            else:
                scale_factor = 150 / height
                height = 150
                width = width * scale_factor
            img_resized = img2.resize((int(width), int(height)))  # new width & height
            img2 = ImageTk.PhotoImage(img_resized)
            image_label.configure(image=img2)
            status_label.configure(text_color="green", text="Image loaded")

        #

        sec2a = customtkinter.CTkFrame(master=sec2)
        sec2a.grid(row=1, column=1, sticky="nswe", padx=20, pady=20, columnspan=3, rowspan=4)

        sec2a.columnconfigure((0, 1, 2), weight=2)
        # sec2a.columnconfigure(0, weight=1)

        name_entry = customtkinter.CTkEntry(sec2a, placeholder_text="Name of Employee")
        name_entry.grid(row=1, column=0, sticky="nswe", pady=10, padx=10)

        id_entry = customtkinter.CTkEntry(sec2a, placeholder_text="ID of Employee")
        id_entry.grid(row=1, column=1, sticky="nswe", pady=10, padx=10)

        dpt_entry = customtkinter.CTkEntry(sec2a, placeholder_text="Department of Employee")
        dpt_entry.grid(row=1, column=2, sticky="nswe", pady=10, padx=10)

        #

        duty_entry = customtkinter.CTkOptionMenu(sec2a, values=["Duty", "Knitting", "bleaching"])
        duty_entry.grid(row=2, column=0, sticky="nswe", pady=10, padx=10)

        timing_entry = customtkinter.CTkOptionMenu(sec2a, values=["Duty Starts at", "8 AM", "9 AM", "4 PM", "5 PM", "12 AM", "1 AM"],
                                                   hover=True)
        timing_entry.grid(row=2, column=1, sticky="nswe", pady=10, padx=10)

        break_entry = customtkinter.CTkOptionMenu(sec2a, values=["Break Starts at", "12 PM", "1 PM"])
        break_entry.grid(row=2, column=2, sticky="nswe", pady=10, padx=10)

        #

        off_days_entry = customtkinter.CTkOptionMenu(sec2a, values=["Off Day"] + week_days)
        off_days_entry.grid(row=3, column=0, sticky="nswe", pady=10, padx=10)

        policy_select_entry = customtkinter.CTkOptionMenu(sec2a, values=["All Policies Applied", "No Policies Applied"])
        policy_select_entry.grid(row=3, column=1, sticky="nswe", pady=10, padx=10)

        add_img_button = customtkinter.CTkButton(master=sec2a, text="Select Image", command=upload_picture)
        add_img_button.grid(row=3, column=2, sticky="nswe", pady=10, padx=30)

        #


        # image = customtkinter.CTkFrame(master=sec2)
        # image.grid(row=6, column=0, sticky="nswe", padx=10, pady=10, rowspan=3)
        #
        # im = customtkinter.CTkLabel(image, text=".")
        # im.grid(row=0, col=0, rowspan=3)

        def add_employee_function():
            print("Entering emp function")
            status_label.configure(text_color="purple", text="in add emp function")
            global img_name
            img = img_name
            print(img)
            name = name_entry.get()
            id = id_entry.get()
            department = dpt_entry.get()
            start_time = timing_entry.get()
            offday = off_days_entry.get()
            policy = policy_select_entry.get()
            break_time_start = break_entry.get()
            duty = duty_entry.get()
            photo = img_name

            print("start:" + str(start_time))

            is_any_entry_empty = False

            # Check if entries are filled
            details = [name, id, department, start_time, offday, policy, break_time_start, duty]
            for item in details:
                if len(item) == 0:
                    is_any_entry_empty = True
                    status_label.configure(text_color="red", text=details.index(item) + " is empty")
                    print(item + " is empty")
                    return 0

            status_label.configure(text_color="blue", text="All entries are non-zero")

            print("off day problem")
            print("offday[0] == 'O' " + str(offday[0] == 'O'))
            print("offday not in week_days  " + str(offday not in week_days))
            print('offday.split(" ")[0] == "Off" ' + str(offday.split(" ")[0] == "Off"))

            if len(start_time) > 5 or len(break_time_start) > 5 or offday[0] == 'O' or str(duty) == "Duty":
                status_label.configure(text_color="blue", text="problem with time or duty or offday")
                print("error in this if")
                is_any_entry_empty = True

            start_time = int(str(start_time).split(" ")[0])
            break_time_start = int(str(break_time_start).split(" ")[0])

            status_label.configure(text_color="blue", text="start time and break time are OK")

            # image check here
            image_uploaded = True
            img_check = cv2.imread(img_name)

            status_label.configure(text_color="blue", text="image is ok")

            if img_check is None:
                image_uploaded = False
                status_label.configure(text_color="red", text="Image not uploaded")

            if image_uploaded and not is_any_entry_empty:
                cid = add_employee(name, id, department, duty, offday, start_time, break_time_start, policy, photo)
                status_label.configure(text_color="green", text="Success! Employee Added : " + str(cid))
                add_dr(cid, 0, 0, [], 0, "", "", 0)
                status_label.configure(text_color="green", text="Success! daily report row added " + str(cid))
                add_mr(cid, 0, 0, 0, 0, 0, 0, 0)
                status_label.configure(text_color="green", text="Success! monthly report row added " + str(cid))

            # else:
                # status_label.configure(text_color="red", text="Not successful")

            # print("name, name_contact, phone_contact, gd, officer_name, bp, officer_contact, remarks, photo: "
            #       , name, name_contact, phone_contact, gd, officer_name, bp, officer_contact, remarks, photo)

            name_entry.delete(0, tkinter.END)
            id_entry.delete(0, tkinter.END)
            dpt_entry.delete(0, tkinter.END)
            timing_entry.delete(0, tkinter.END)
            off_days_entry.delete(0, tkinter.END)
            policy_select_entry.delete(0, tkinter.END)
            break_entry.delete(0, tkinter.END)
            # duty_entry.delete(0, tkinter.END)
            image_label.configure(image="")

        add_emp_button = customtkinter.CTkButton(master=sec2a, text="Add Employee", command=add_employee_function)
        add_emp_button.grid(row=4, column=0, sticky="nswe", pady=10, padx=30, columnspan=3)


        # Add New Policy Section

        # This is section 3

        sec3 = customtkinter.CTkFrame(master=frame)
        sec3.grid(row=5, column=0, sticky="nswe", padx=20, pady=20, columnspan=5)

        sec3.columnconfigure((1, 2, 3), weight=2)
        sec3.columnconfigure(0, weight=1)

        add_policy_label = customtkinter.CTkLabel(master=sec3, text="Add Policy",
                                                  text_font=("Roboto Medium", -22))
        add_policy_label.grid(row=5, column=0, sticky="nswe", pady=10, padx=10, rowspan=2)

        #
        sec3a = customtkinter.CTkFrame(master=sec3)
        sec3a.grid(row=5, column=1, sticky="nswe", padx=10, pady=20, columnspan=3)

        sec3a.columnconfigure((0, 1, 2), weight=2)
        # sec3a.columnconfigure(0, weight=1)

        policy_activity_entry = customtkinter.CTkOptionMenu(sec3a, values=["Activity"] + policy_activites_list)
        policy_activity_entry.grid(row=5, column=0, sticky="nswe", pady=10, padx=10)

        # activity_allowed_entry = customtkinter.CTkEntry(sec3a, placeholder_text="Allowed / Not Allowed")

        activity_allowed_entry = customtkinter.CTkOptionMenu(master=sec3a, values=["Allowed", "Not Allowed"])
        activity_allowed_entry.grid(row=5, column=1, sticky="nswe", pady=10, padx=10)

        duration_entry = customtkinter.CTkEntry(sec3a, placeholder_text="Duration (Minutes)")
        duration_entry.grid(row=5, column=2, sticky="nswe", pady=10, padx=10)

        def add_policy_function():

            activity_name = policy_activity_entry.get()
            activity_allowed = activity_allowed_entry.get()
            activity_duration = duration_entry.get()
            if len(str(activity_duration)) == 0:
                activity_duration = 0

            status_label.configure(text_color="red", text="Adding Policy")

            is_policy_valid = True

            if policy_exists(activity_name):
                status_label.configure(text_color="red", text="%s Policy Already exists, Delete existing first"
                                                              % activity_name)
                is_policy_valid = False

            elif len(activity_name) == 0:
                status_label.configure(text_color="red", text="Must Enter Activity Name")
                is_policy_valid = False

            elif activity_name not in policy_activites_list:
                status_label.configure(text_color="red", text="Activity name is not valid")
                is_policy_valid = False
            elif not activity_duration.isnumeric():
                status_label.configure(text_color="red", text="Activity Duration must be a positive number",
                                       text_font=("Roboto Medium", -18))
                is_policy_valid = False
            elif activity_allowed == "Allowed" and int(activity_duration) == 0:
                status_label.configure(text_color="red", text="Activity is allowed but duration is 0",
                                       text_font=("Roboto Medium", -18))
                is_policy_valid = False

            if is_policy_valid:
                # policy_activity_entry.insert(0, "")
                duration_entry.insert(0, "")
                if activity_allowed == "Allowed":
                    is_allowed = "true"
                else:
                    is_allowed = "false"
                try:
                    print("activity parameters")
                    print(activity_name, is_allowed, abs(int(activity_duration)))
                    add_policy(activity_name, is_allowed, abs(int(activity_duration)))
                    print("Policy added")
                    try:
                        status_label.configure(text_color="Green", text="Policy Added",
                                               text_font=("Roboto Medium", -26))
                    except:

                        print("Policy added 2")
                except:
                    status_label.configure(text_color="red", text="Policy Not Added something went wrong",
                                           text_font=("Roboto Medium", -26))
            else:
                status_label.configure(text_color="red", text="Issue with data entered",
                                       text_font=("Roboto Medium", -26))

        add_new_policy_button = customtkinter.CTkButton(master=sec3a, text="Add New Policy", command=add_policy_function)
        add_new_policy_button.grid(row=6, column=0, columnspan=3, sticky="nswe", pady=10, padx=30)

        # Add New user Section

        sec4 = customtkinter.CTkFrame(master=frame)
        sec4.grid(row=7, column=0, sticky="nswe", padx=20, pady=20, columnspan=4)

        sec4.columnconfigure((1, 2, 3), weight=2)
        sec4.columnconfigure(0, weight=1)

        add_user_label = customtkinter.CTkLabel(master=sec4, text="Add User",
                                                  text_font=("Roboto Medium", -22))
        add_user_label.grid(row=7, column=0, sticky="nswe", pady=10, padx=10, rowspan=2)

        #

        sec4a = customtkinter.CTkFrame(master=sec4)
        sec4a.grid(row=7, column=1, sticky="nswe", padx=20, pady=20, columnspan=3)

        sec4a.columnconfigure((0, 1, 2), weight=2)
        # sec4a.columnconfigure(0, weight=1)

        new_username_entry = customtkinter.CTkEntry(sec4a, placeholder_text="Enter Username")
        new_username_entry.grid(row=7, column=0, sticky="nswe", pady=10, padx=10)

        new_password_entry = customtkinter.CTkEntry(sec4a, placeholder_text="Enter Password")
        new_password_entry.grid(row=8, column=0, sticky="nswe", pady=10, padx=10)

        # Generation of credentials and creation of user

        def generate_username():
            username = get_random_username()
            status_label.configure(text_color="blue", text="Username Generated - " + username)
            print("username: ", username)
            # while not username_available(username):
            #     username = get_random_username()
            #     print(username)
            # user_text.set(username)
            new_username_entry.delete(0, tkinter.END)
            new_username_entry.insert(0, username)

        def generate_password():
            password = get_random_password()
            print("password: ", password)
            status_label.configure(text_color="blue", text="Password Generated - " + password)
            new_password_entry.delete(0, tkinter.END)
            new_password_entry.insert(0, password)

        def add_user_function():
            user = new_username_entry.get()
            pas = new_password_entry.get()

            print("user: ", user)
            print("pas: ", pas)

            if len(user) == 0 or len(pas) == 0:
                print("This username or password is not good")
                if not username_available(user):
                    status_label.configure(text_color="red", text="Username not available")
                else:
                    status_label.configure(text_color="red", text="Enter username and password of 8 characters",
                                           text_font=("Roboto Medium", -18))
            else:

                add_user(user, pas)
                new_username_entry.insert(0, "")
                new_password_entry.insert(0, "")
                print("User is generated and created in db")
                status_label.configure(text_color="green", text="User Created", text_font=("Roboto Medium", -26))


        # Buttons

        generate_username_button = customtkinter.CTkButton(master=sec4a, text="Generate Username", command=generate_username)
        generate_username_button.grid(row=7, column=1, sticky="nswe", pady=10, padx=30)

        generate_password_button = customtkinter.CTkButton(master=sec4a, text="Generate Password", command=generate_password)
        generate_password_button.grid(row=8, column=1, sticky="nswe", pady=10, padx=30)

        add_user_button = customtkinter.CTkButton(master=sec4a, text="Add New user", command=add_user_function)
        add_user_button.grid(row=7, column=2, rowspan=2, sticky="we", pady=10, padx=30)

        records_window.mainloop()



    #  ------- Make frame in window --------

    frame_right = customtkinter.CTkFrame(master=main_window)
    frame_right.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

    frame_right.columnconfigure((0, 3, 4), weight=1)
    frame_right.columnconfigure((1, 2), weight=2)

    # scrollbar = customtkinter.CTkScrollbar(main_window, command=frame_right.yview)
    # scrollbar.grid(row=0, column=5, sticky="ns")


    # ----------- Dash Label on Top Left ---------------

    admin_label = customtkinter.CTkLabel(master=frame_right, text="User Panel", text_font=("Roboto Medium", -16))
    admin_label.grid(row=1, column=0, pady=5, padx=10)

    #     ----------------- Make Center Frame in Dashboard ---------

    frame_center = customtkinter.CTkFrame(master=frame_right)
    frame_center.grid(row=2, column=0, sticky="nswe", padx=20, pady=30, columnspan=12)

    frame_center.columnconfigure((1, 2), weight=4)
    frame_center.columnconfigure(0, weight=8)
    frame_center.columnconfigure((3, 4), weight=1)

    num_employees = get_num_employees()
    num_polices = get_num_policies()
    num_users = get_num_users()

    total_emps_label = customtkinter.CTkLabel(master=frame_center, text="Total Employees: " + str(num_employees), text_font=("Roboto Medium", -22))
    total_emps_label.grid(row=3, column=0, pady=10, padx=10)

    on_duty_label = customtkinter.CTkLabel(master=frame_center, text="Total Polices: " + str(num_polices), text_font=("Roboto Medium", -22))
    on_duty_label.grid(row=4, column=0, pady=10, padx=10)

    total_emps_label = customtkinter.CTkLabel(master=frame_center, text="Total Policies: " + str(num_users), text_font=("Roboto Medium", -22))
    total_emps_label.grid(row=5, column=0, pady=10, padx=10)

    max_overtime_allowed = get_max_overtime()

    overtime_label = customtkinter.CTkLabel(master=frame_center,
                                                text="Max Overtime Allowed: " + str(max_overtime_allowed) + " Hours",
                                                text_font=("Roboto Medium", -22))
    overtime_label.grid(row=3, column=3, pady=10, padx=10, rowspan=2, columnspan=2)

    # overtime_change_label = customtkinter.CTkLabel(master=frame_center, text="Change max allowed overtime (hours) to ",
    #                                             text_font=("Roboto Medium", -18),
    #                                                text_color="#aaaaaa")
    # overtime_change_label.grid(row=4, column=3, pady=10, padx=10, rowspan=2)
    #
    # overtime_change_button = customtkinter.CTkOptionMenu(master=frame_center, values=[str(i) for i in range(0, 4)])
    # overtime_change_button.grid(row=4, column=4, pady=20, padx=20, rowspan=2)

    # --------- Make Frame within Center Frame ------------------------

    frame_bottom = customtkinter.CTkFrame(master=frame_center)
    frame_bottom.grid(row=3, column=1, sticky="nswe", padx=20, pady=30, columnspan=2, rowspan=3)
    frame_bottom.columnconfigure((0, 1), weight=1)
    # frame_bottom.rowconfigure((0, 1), weight=1)
    #
    # add_user_entry = customtkinter.CTkEntry(master=frame_bottom, placeholder_text="Add Username")
    # add_user_entry.grid(row=5, column=0, pady=20, padx=20)
    #
    # add_password_entry = customtkinter.CTkEntry(master=frame_bottom, placeholder_text="Add Password")
    # add_password_entry.grid(row=6, column=0, pady=20, padx=20)
    #
    # generate_username_button = customtkinter.CTkButton(master=frame_bottom, text="Generate Username", command=generate_username)
    # generate_username_button.grid(row=5, column=1, pady=20, padx=20)
    #
    # generate_password_button = customtkinter.CTkButton(master=frame_bottom, text="Generate Password", command=generate_password)
    # generate_password_button.grid(row=6, column=1, pady=20, padx=20)
    #
    # add_user_button = customtkinter.CTkButton(master=frame_bottom, text="Add User", command=add_user_function)
    # add_user_button.grid(row=7, column=0, pady=20, padx=20, columnspan=2)

    # all_users_button = customtkinter.CTkButton(master=frame_bottom, text="View All Users", command=lambda: open_all_users(0))
    # all_users_button.grid(row=3, column=0, pady=20, padx=20)

    all_emp_button = customtkinter.CTkButton(master=frame_bottom, text="View All Employees", command=lambda: open_all_employees(0))
    all_emp_button.grid(row=3, column=1, pady=20, padx=20)

    all_policies_button = customtkinter.CTkButton(master=frame_bottom, text="View All Policies",
                                                command=lambda: open_all_policies(0))
    all_policies_button.grid(row=4, column=0, pady=20, padx=20)

    all_reports_button = customtkinter.CTkButton(master=frame_bottom, text="View Previous Reports", command=None)
    all_reports_button.grid(row=4, column=1, pady=20, padx=20)

    # ----------- Admin Label on Top Right with Buttons ---------------

    title_text_label = customtkinter.CTkLabel(master=frame_right, text="Policy Based Employee Monitoring System", text_font=("Roboto Medium", -26))
    title_text_label.grid(row=0, column=0, columnspan=12, pady=30, padx=10)

    logout_button = customtkinter.CTkButton(master=frame_right, text="Logout", command=logout_function, fg_color="#bb0000")
    logout_button.grid(row=1, column=10, pady=5, padx=20)

    status_label = customtkinter.CTkLabel(master=frame_right, text="", text_font=("Roboto Medium", -14))
    status_label.grid(row=7, column=2, pady=10, padx=10, columnspan=1)

    # This is section 2

    sec2 = customtkinter.CTkFrame(master=frame_right)
    sec2.grid(row=5, column=0, sticky="nswe", padx=20, pady=30, columnspan=12)

    sec2.columnconfigure((0, 1, 2, 3), weight=4)
    # frame_center.columnconfigure(0, weight=8)
    # frame_center.columnconfigure(3, weight=1)

    # new_admin_password_entry = customtkinter.CTkEntry(sec2
    #                                                   , placeholder_text="Enter new password")
    # new_admin_password_entry.grid(row=5, column=0, pady=20, padx=10)

    # change_password_button = customtkinter.CTkButton(master=sec2, text="Change Password",
    #                                                  command=lambda: change_admin_password_function(
    #                                                      new_admin_password_entry.get()))
    # change_password_button.grid(row=6, column=0, pady=20, padx=10)

    # apply_button = customtkinter.CTkButton(master=sec2, text="Apply Changes", command=apply_changes_function)
    # apply_button.grid(row=5, column=3, pady=20, padx=20)

    # exit_button = customtkinter.CTkButton(master=sec2, text="Exit", command=None, fg_color="#bb0000")
    # exit_button.grid(row=6, column=3, pady=20, padx=20)

    # --------- Make Frame within Center Frame ------------------------

    # frame_bottom2 = customtkinter.CTkFrame(master=sec2)
    # frame_bottom2.grid(row=5, column=1, sticky="nswe", padx=20, pady=20, columnspan=2, rowspan=2)
    # frame_bottom2.columnconfigure((0, 1), weight=1)

    # add_users_button = customtkinter.CTkButton(master=frame_bottom2, text="Add New User", command=add_new_function)
    # add_users_button.grid(row=5, column=0, pady=20, padx=20)
    #
    # add_emp_button = customtkinter.CTkButton(master=frame_bottom2, text="Add New Employee", command=add_new_function)
    # add_emp_button.grid(row=5, column=1, pady=20, padx=20)
    #
    # add_policy_button = customtkinter.CTkButton(master=frame_bottom2, text="Add New Policy",
    #                                              command=add_new_function)
    # add_policy_button.grid(row=6, column=0, pady=20, padx=20, columnspan=2)

    # frame_right.configure(yscrollcommand=scrollbar.set)


# -------------  login window ------------------

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=20, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, text="User Login", text_font=("Roboto Medium", -20), justify=tkinter.LEFT)
label_1.pack(pady=40, padx=10)

username_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Username")
username_entry.pack(pady=12, padx=0)

password_entry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Password")
password_entry.pack(pady=12, padx=10)

login_button = customtkinter.CTkButton(master=frame_1, text="Login", command=login_function)
login_button.pack(pady=12, padx=10)

login_label = customtkinter.CTkLabel(master=frame_1, text="", text_font=("Roboto Medium", -20), justify=tkinter.LEFT)
login_label.pack(pady=12, padx=10)

#   ------------------------- Keep Loop Running ------------------

app.mainloop()