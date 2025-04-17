
import os

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from datetime import datetime
import csv
from kivy.logger import Logger

# Add this at the beginning of your app
Logger.setLevel('ERROR')  # Only show errors and above

Window.size = (1200, 800)


class AdminDashboard(Screen):
    current_user = ObjectProperty(None)
    status_message = StringProperty("")
    teacher_list = ListProperty([])
    student_list = ListProperty([])
    class_list = ListProperty([])
    subject_list = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'admin_dashboard'
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.load_sample_data()
        self.build_ui()

    def load_sample_data(self):
        # Sample data - replace with database calls
        self.teacher_list = [
            {'id': 1, 'name': 'John Smith', 'email': 'john@school.edu', 'role': 'Teacher', 'status': 'Active'},
            {'id': 2, 'name': 'Sarah Johnson', 'email': 'sarah@school.edu', 'role': 'DoS', 'status': 'Active'}
        ]

        self.student_list = [
            {'id': 1001, 'student_number': 'S2023001', 'name': 'Michael Brown', 'class': 'Grade 10A', 'fees_paid': 1500,
             'fees_due': 500},
            {'id': 1002, 'student_number': 'S2023002', 'name': 'Emily Davis', 'class': 'Grade 9B', 'fees_paid': 2000,
             'fees_due': 0}
        ]

        self.class_list = ['Grade 10A', 'Grade 10B', 'Grade 9A', 'Grade 9B']
        self.subject_list = ['Math', 'Science', 'English', 'History']

    def build_ui(self):
        self.clear_widgets()

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # Header
        header = self._build_header()
        main_layout.add_widget(header)

        # Tabbed interface
        self.tabs = TabbedPanel(
            do_default_tab=False,
            tab_width=dp(200),
            background_color=(0.95, 0.95, 0.95, 1)
        )

        # Add all required tabs
        self._add_tabs()

        main_layout.add_widget(self.tabs)

        # Status bar
        self.status_bar = Label(
            text=self.status_message,
            size_hint=(1, None),
            height=dp(30),
            color=(0.3, 0.3, 0.3, 1)
        )
        main_layout.add_widget(self.status_bar)

        self.add_widget(main_layout)

    def _build_header(self):
        header = BoxLayout(size_hint=(1, None), height=dp(80), spacing=dp(20))

        # User info
        user_box = BoxLayout(orientation='horizontal', spacing=dp(15))

        text_box = BoxLayout(orientation='vertical', spacing=dp(5))
        text_box.add_widget(Label(
            text=f"Welcome, {getattr(self.current_user, 'full_name', 'Administrator')}",
            font_size=dp(18),
            bold=True,
            halign='left'
        ))
        text_box.add_widget(Label(
            text="Admin Dashboard",
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1)
        ))

        user_box.add_widget(text_box)

        # Quick actions
        actions = BoxLayout(size_hint=(0.5, 1), spacing=dp(15))
        for action in [('Refresh Data', self.refresh_data),
                       ('View Reports', self.show_reports),
                       ('Logout', self.logout)]:
            btn = Button(
                text=action[0],
                size_hint=(None, None),
                size=(dp(120), dp(40))
            )
            btn.bind(on_press=action[1])
            actions.add_widget(btn)

        header.add_widget(user_box)
        header.add_widget(actions)
        return header

    def _add_tabs(self):
        # 1. User Management Tab
        user_tab = TabbedPanelItem(text='User Management')
        user_content = self._create_user_management_tab()
        user_tab.add_widget(user_content)
        self.tabs.add_widget(user_tab)

        # 2. Academic Management Tab
        academic_tab = TabbedPanelItem(text='Academic Management')
        academic_content = self._create_academic_management_tab()
        academic_tab.add_widget(academic_content)
        self.tabs.add_widget(academic_tab)

        # 3. Student Management Tab
        student_tab = TabbedPanelItem(text='Student Management')
        student_content = self._create_student_management_tab()
        student_tab.add_widget(student_content)
        self.tabs.add_widget(student_tab)

        # 4. Financial Management Tab
        finance_tab = TabbedPanelItem(text='Financial Management')
        finance_content = self._create_financial_management_tab()
        finance_tab.add_widget(finance_content)
        self.tabs.add_widget(finance_tab)

        # 5. Reports Tab
        reports_tab = TabbedPanelItem(text='Reports')
        reports_content = self._create_reports_tab()
        reports_tab.add_widget(reports_content)
        self.tabs.add_widget(reports_tab)

    # 1. User Management Functions
    def _create_user_management_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Teacher management section
        teacher_box = BoxLayout(orientation='vertical', spacing=dp(10))
        teacher_box.add_widget(Label(text='Teacher Accounts', size_hint=(1, None), height=dp(30)))

        # Teacher list
        scroll = ScrollView()
        self.teacher_grid = GridLayout(cols=4, size_hint_y=None, spacing=dp(5))
        self.teacher_grid.bind(minimum_height=self.teacher_grid.setter('height'))

        # Header row
        headers = ['Name', 'Email', 'Role', 'Actions']
        for header in headers:
            self.teacher_grid.add_widget(Label(text=header, size_hint_y=None, height=dp(40), bold=True))

        # Teacher rows
        for teacher in self.teacher_list:
            self.teacher_grid.add_widget(Label(text=teacher['name'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['email'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['role'], size_hint_y=None, height=dp(40)))

            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            edit_btn = Button(text='Edit',
                              size_hint_x=0.3,
                              background_color=(0.2, 0.6, 1, 1),  # Blue color
                              background_normal='',
                              color=(1, 1, 1, 1))  # White text
            disable_btn = Button(text='Disable',
                                 size_hint_x=0.3,
                                 background_color=(1, 0.4, 0.4, 1),  # Red color
                                 background_normal='',
                                 color=(1, 1, 1, 1))  # White text
            delete_btn = Button(text='Delete',
                                size_hint_x=0.3,
                                background_color=(1, 0.4, 0.4, 1),  # Red color
                                background_normal='',
                                color=(1, 1, 1, 1))  # White text

            edit_btn.bind(on_press=lambda x, t=teacher: self.edit_teacher(t))
            disable_btn.bind(on_press=lambda x, t=teacher: self.disable_teacher(t))
            delete_btn.bind(on_press=lambda x, t=teacher: self.delete_teacher(t))

            action_box.add_widget(edit_btn)
            action_box.add_widget(disable_btn)
            action_box.add_widget(delete_btn)
            self.teacher_grid.add_widget(action_box)

        # Add the grid to scroll view ONCE
        scroll.add_widget(self.teacher_grid)
        teacher_box.add_widget(scroll)

        # Add teacher controls
        add_teacher_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        self.new_teacher_name = TextInput(hint_text='Full Name', size_hint_x=0.3)
        self.new_teacher_email = TextInput(hint_text='Email', size_hint_x=0.3)
        self.new_teacher_role = Spinner(text='Teacher', values=['Teacher', 'DoS', 'Registrar'], size_hint_x=0.2)
        add_btn = Button(text='Add Teacher',
                         size_hint_x=0.2,
                         background_color=(0.2, 0.6, 1, 1),  # Blue color
                         background_normal='',
                         color=(1, 1, 1, 1))  # White text
        add_btn.bind(on_press=self.add_teacher)

        add_teacher_box.add_widget(self.new_teacher_name)
        add_teacher_box.add_widget(self.new_teacher_email)
        add_teacher_box.add_widget(self.new_teacher_role)
        add_teacher_box.add_widget(add_btn)

        teacher_box.add_widget(add_teacher_box)
        layout.add_widget(teacher_box)

        return layout

    def create_edit_teacher_dialog(self, teacher):
        # Create a popup dialog for editing teacher information
        popup = Popup(title=f"Edit Teacher: {teacher['name']}",
                      size_hint=(0.8, 0.6),
                      auto_dismiss=False)

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        # Form fields
        form_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.8)

        # Name field
        form_layout.add_widget(Label(text='Full Name:'))
        name_input = TextInput(text=teacher['name'], multiline=False)
        form_layout.add_widget(name_input)

        # Email field
        form_layout.add_widget(Label(text='Email:'))
        email_input = TextInput(text=teacher['email'], multiline=False)
        form_layout.add_widget(email_input)

        # Role field
        form_layout.add_widget(Label(text='Role:'))
        role_spinner = Spinner(text=teacher['role'],
                               values=['Teacher', 'DoS', 'Registrar'])
        form_layout.add_widget(role_spinner)

        # Status field (if you have this)
        form_layout.add_widget(Label(text='Status:'))
        status_spinner = Spinner(text=teacher.get('status', 'Active'),
                                 values=['Active', 'Disabled'])
        form_layout.add_widget(status_spinner)

        layout.add_widget(form_layout)

        # Button row
        button_box = BoxLayout(size_hint_y=0.2, spacing=dp(10))

        # Save button (blue)
        save_btn = Button(text='Save Changes',
                          background_color=(0.2, 0.6, 1, 1),
                          background_normal='',
                          color=(1, 1, 1, 1))

        # Cancel button (gray)
        cancel_btn = Button(text='Cancel',
                            background_color=(0.7, 0.7, 0.7, 1),
                            background_normal='',
                            color=(1, 1, 1, 1))

        button_box.add_widget(cancel_btn)
        button_box.add_widget(save_btn)
        layout.add_widget(button_box)

        # Set up button actions
        def save_changes(instance):
            # Update the teacher dictionary with new values
            teacher['name'] = name_input.text
            teacher['email'] = email_input.text
            teacher['role'] = role_spinner.text
            teacher['status'] = status_spinner.text

            # Here you would typically save to database
            self.update_teacher_in_database(teacher)

            # Refresh the teacher list display
            self.refresh_teacher_list()
            popup.dismiss()

        def cancel_edit(instance):
            popup.dismiss()

        save_btn.bind(on_press=save_changes)
        cancel_btn.bind(on_press=cancel_edit)

        popup.content = layout
        popup.open()

    def add_teacher(self, instance):
        new_teacher = {
            'id': len(self.teacher_list) + 1,
            'name': self.new_teacher_name.text,
            'email': self.new_teacher_email.text,
            'role': self.new_teacher_role.text,
            'status': 'Active'
        }
        self.teacher_list.append(new_teacher)
        self.refresh_teacher_list()
        self.status_message = f"Added teacher: {new_teacher['name']}"
        self.new_teacher_name.text = ''
        self.new_teacher_email.text = ''

    def edit_teacher(self, teacher):
        self.status_message = f"Editing teacher: {teacher['name']}"
        # Implement edit functionality

    def disable_teacher(self, teacher):
        self.status_message = f"Disabling teacher: {teacher['name']} for 30 days"
        # Implement disable functionality with time period

    def delete_teacher(self, teacher):
        self.status_message = f"Deleted teacher: {teacher['name']}"
        self.teacher_list = [t for t in self.teacher_list if t['id'] != teacher['id']]
        self.refresh_teacher_list()

    def refresh_teacher_list(self):
        self.teacher_grid.clear_widgets()
        headers = ['Name', 'Email', 'Role', 'Actions']
        for header in headers:
            self.teacher_grid.add_widget(Label(text=header, size_hint_y=None, height=dp(40), bold=True))

        for teacher in self.teacher_list:
            self.teacher_grid.add_widget(Label(text=teacher['name'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['email'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['role'], size_hint_y=None, height=dp(40)))

            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            edit_btn = Button(text='Edit', size_hint_x=0.3)
            disable_btn = Button(text='Disable', size_hint_x=0.3)
            delete_btn = Button(text='Delete', size_hint_x=0.3)

            edit_btn.bind(on_press=lambda x, t=teacher: self.edit_teacher(t))
            disable_btn.bind(on_press=lambda x, t=teacher: self.disable_teacher(t))
            delete_btn.bind(on_press=lambda x, t=teacher: self.delete_teacher(t))

            action_box.add_widget(edit_btn)
            action_box.add_widget(disable_btn)
            action_box.add_widget(delete_btn)
            self.teacher_grid.add_widget(action_box)

            # 2. Academic Management Functions




        # Rebuild the grid (you might want to reuse your existing code)
        headers = ['Name', 'Email', 'Role', 'Actions']
        for header in headers:
            self.teacher_grid.add_widget(Label(text=header, size_hint_y=None, height=dp(40), bold=True))

        for teacher in self.teacher_list:
            self.teacher_grid.add_widget(Label(text=teacher['name'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['email'], size_hint_y=None, height=dp(40)))
            self.teacher_grid.add_widget(Label(text=teacher['role'], size_hint_y=None, height=dp(40)))

            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            edit_btn = Button(text='Edit', size_hint_x=0.3,
                              background_color=(0.2, 0.6, 1, 1),
                              background_normal='',
                              color=(1, 1, 1, 1))
            disable_btn = Button(text='Disable', size_hint_x=0.3,
                                 background_color=(1, 0.4, 0.4, 1),
                                 background_normal='',
                                 color=(1, 1, 1, 1))
            delete_btn = Button(text='Delete', size_hint_x=0.3,
                                background_color=(1, 0.4, 0.4, 1),
                                background_normal='',
                                color=(1, 1, 1, 1))

            edit_btn.bind(on_press=lambda x, t=teacher: self.edit_teacher(t))
            disable_btn.bind(on_press=lambda x, t=teacher: self.disable_teacher(t))
            delete_btn.bind(on_press=lambda x, t=teacher: self.delete_teacher(t))

            action_box.add_widget(edit_btn)
            action_box.add_widget(disable_btn)
            action_box.add_widget(delete_btn)
            self.teacher_grid.add_widget(action_box)

    def _create_academic_management_tab(self):
        # Create main tab panel with custom styling
        tab_panel = TabbedPanel(do_default_tab=False,  # Disable the default tab
                                tab_width=Window.width / 2,  # Equal width tabs
                                background_color=(0.9, 0.9, 0.9, 1),  # Light gray background
                                tab_pos='top_mid')  # Center tabs

        # Class Management Tab
        class_tab = TabbedPanelItem(text='Class Management',
                                    background_normal='',
                                    background_color=(0.2, 0.6, 1, 1),  # Blue when inactive
                                    color=(1, 1, 1, 1))  # White text
        class_content = self._create_class_management_tab()
        class_tab.add_widget(class_content)
        tab_panel.add_widget(class_tab)

        # Subject Management Tab
        subject_tab = TabbedPanelItem(text='Subject Management',
                                      background_normal='',
                                      background_color=(0.2, 0.6, 1, 1),  # Blue when inactive
                                      color=(1, 1, 1, 1))  # White text
        subject_content = self._create_subject_management_tab()
        subject_tab.add_widget(subject_content)
        tab_panel.add_widget(subject_tab)

        # Set the first tab as active
        tab_panel.switch_to(class_tab)

        return tab_panel

    def _create_class_management_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Class list with header
        header = BoxLayout(size_hint_y=None, height=dp(40))
        header.add_widget(Label(text='Class Name', size_hint_x=0.6, bold=True))
        header.add_widget(Label(text='Actions', size_hint_x=0.4, bold=True))
        layout.add_widget(header)

        class_scroll = ScrollView()
        self.class_list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.class_list_grid.bind(minimum_height=self.class_list_grid.setter('height'))

        for class_name in self.class_list:
            class_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5), padding=(0, 0, dp(5), 0))
            class_row.add_widget(Label(text=class_name, size_hint_x=0.6))

            btn_box = BoxLayout(size_hint_x=0.4, spacing=dp(5))

            edit_btn = Button(text='Edit',
                              background_color=(0.2, 0.6, 1, 1),
                              background_normal='',
                              color=(1, 1, 1, 1))

            delete_btn = Button(text='Delete',
                                background_color=(1, 0.4, 0.4, 1),
                                background_normal='',
                                color=(1, 1, 1, 1))

            edit_btn.bind(on_press=lambda x, c=class_name: self.edit_class(c))
            delete_btn.bind(on_press=lambda x, c=class_name: self.delete_class(c))

            btn_box.add_widget(edit_btn)
            btn_box.add_widget(delete_btn)
            class_row.add_widget(btn_box)
            self.class_list_grid.add_widget(class_row)

        class_scroll.add_widget(self.class_list_grid)
        layout.add_widget(class_scroll)

        # Add class controls
        add_class_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        self.new_class_name = TextInput(hint_text='Enter Class Name', size_hint_x=0.7)

        add_btn = Button(text='Add Class',
                         size_hint_x=0.3,
                         background_color=(0.2, 0.6, 1, 1),
                         background_normal='',
                         color=(1, 1, 1, 1))

        add_btn.bind(on_press=self.add_class)
        add_class_box.add_widget(self.new_class_name)
        add_class_box.add_widget(add_btn)
        layout.add_widget(add_class_box)

        return layout

    def _create_subject_management_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Subject list with header
        header = BoxLayout(size_hint_y=None, height=dp(40))
        header.add_widget(Label(text='Subject Name', size_hint_x=0.6, bold=True))
        header.add_widget(Label(text='Actions', size_hint_x=0.4, bold=True))
        layout.add_widget(header)

        subject_scroll = ScrollView()
        self.subject_list_grid = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        self.subject_list_grid.bind(minimum_height=self.subject_list_grid.setter('height'))

        for subject in self.subject_list:
            subject_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(5), padding=(0, 0, dp(5), 0))
            subject_row.add_widget(Label(text=subject, size_hint_x=0.6))

            btn_box = BoxLayout(size_hint_x=0.4, spacing=dp(5))

            edit_btn = Button(text='Edit',
                              background_color=(0.2, 0.6, 1, 1),
                              background_normal='',
                              color=(1, 1, 1, 1))

            delete_btn = Button(text='Delete',
                                background_color=(1, 0.4, 0.4, 1),
                                background_normal='',
                                color=(1, 1, 1, 1))

            edit_btn.bind(on_press=lambda x, s=subject: self.edit_subject(s))
            delete_btn.bind(on_press=lambda x, s=subject: self.delete_subject(s))

            btn_box.add_widget(edit_btn)
            btn_box.add_widget(delete_btn)
            subject_row.add_widget(btn_box)
            self.subject_list_grid.add_widget(subject_row)

        subject_scroll.add_widget(self.subject_list_grid)
        layout.add_widget(subject_scroll)

        # Add subject controls
        add_subject_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        self.new_subject_name = TextInput(hint_text='Enter Subject Name', size_hint_x=0.7)

        add_btn = Button(text='Add Subject',
                         size_hint_x=0.3,
                         background_color=(0.2, 0.6, 1, 1),
                         background_normal='',
                         color=(1, 1, 1, 1))

        add_btn.bind(on_press=self.add_subject)
        add_subject_box.add_widget(self.new_subject_name)
        add_subject_box.add_widget(add_btn)
        layout.add_widget(add_subject_box)

        return layout



    def add_class(self, instance):
        if self.new_class_name.text:
            self.class_list.append(self.new_class_name.text)
            self.status_message = f"Added class: {self.new_class_name.text}"
            self.new_class_name.text = ''

    def add_subject(self, instance):
        if self.new_subject_name.text:
            self.subject_list.append(self.new_subject_name.text)
            self.status_message = f"Added subject: {self.new_subject_name.text}"
            self.new_subject_name.text = ''

    # 3. Student Management Functions
    def _create_student_management_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Search bar with styled buttons
        search_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        self.search_input = TextInput(hint_text='Search by name or student number', size_hint_x=0.7)

        # Blue search button
        search_btn = Button(text='Search',
                            size_hint_x=0.15,
                            background_color=(0.2, 0.6, 1, 1),  # Blue
                            background_normal='',
                            color=(1, 1, 1, 1))  # White text

        # Red clear button
        clear_btn = Button(text='Clear',
                           size_hint_x=0.15,
                           background_color=(1, 0.4, 0.4, 1),  # Red
                           background_normal='',
                           color=(1, 1, 1, 1))  # White text

        search_btn.bind(on_press=self.search_students)
        clear_btn.bind(on_press=self.clear_search)

        search_box.add_widget(self.search_input)
        search_box.add_widget(search_btn)
        search_box.add_widget(clear_btn)
        layout.add_widget(search_box)

        # Student list
        student_box = BoxLayout(orientation='vertical', spacing=dp(10))
        student_box.add_widget(Label(text='Student Records', size_hint=(1, None), height=dp(30)))

        scroll = ScrollView()
        self.student_grid = GridLayout(cols=6, size_hint_y=None, spacing=dp(5))
        self.student_grid.bind(minimum_height=self.student_grid.setter('height'))

        # Header row
        headers = ['ID', 'Student #', 'Name', 'Class', 'Fees Paid', 'Actions']
        for header in headers:
            label = Label(text=header, size_hint_y=None, height=dp(40), bold=True)
            self.student_grid.add_widget(label)

        # Student rows
        for student in self.student_list:
            # ID
            id_label = Label(text=str(student['id']), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(id_label)

            # Student Number
            num_label = Label(text=student.get('student_number', 'N/A'), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(num_label)

            # Name
            name_label = Label(text=student['name'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(name_label)

            # Class
            class_label = Label(text=student['class'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(class_label)

            # Fees Paid - Changed to KES
            fees_label = Label(text=f"KES {student['fees_paid']:,}",  # Format with commas
                               size_hint_y=None,
                               height=dp(40))
            self.student_grid.add_widget(fees_label)

            # Actions - Changed Edit to Disable
            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))

            # Red disable button
            disable_btn = Button(text='Disable' if student.get('active', True) else 'Enable',
                                 size_hint_x=0.4,
                                 background_color=(1, 0.4, 0.4, 1) if student.get('active', True) else (
                                 0.2, 0.7, 0.3, 1),
                                 background_normal='',
                                 color=(1, 1, 1, 1))

            # Blue assign class button
            assign_btn = Button(text='Assign Class',
                                size_hint_x=0.6,
                                background_color=(0.2, 0.6, 1, 1),
                                background_normal='',
                                color=(1, 1, 1, 1))

            disable_btn.bind(on_press=lambda x, s=student: self.toggle_student_status(s))
            assign_btn.bind(on_press=lambda x, s=student: self.assign_student_class(s))

            action_box.add_widget(disable_btn)
            action_box.add_widget(assign_btn)
            self.student_grid.add_widget(action_box)

        scroll.add_widget(self.student_grid)
        student_box.add_widget(scroll)

        # Student controls
        control_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        # Blue add student button
        manual_add_btn = Button(text='Add Student',
                                size_hint_x=0.3,
                                background_color=(0.2, 0.6, 1, 1),
                                background_normal='',
                                color=(1, 1, 1, 1))

        # Green bulk import button
        bulk_import_btn = Button(text='Bulk Import',
                                 size_hint_x=0.3,
                                 background_color=(0.2, 0.7, 0.3, 1),
                                 background_normal='',
                                 color=(1, 1, 1, 1))

        manual_add_btn.bind(on_press=self.show_add_student_popup)
        bulk_import_btn.bind(on_press=self.show_bulk_import_popup)

        control_box.add_widget(manual_add_btn)
        control_box.add_widget(bulk_import_btn)
        student_box.add_widget(control_box)

        layout.add_widget(student_box)
        return layout

    def search_students(self, instance):
        search_term = self.search_input.text.lower()
        if not search_term:
            self.refresh_student_list()
            return

        filtered_students = [
            s for s in self.student_list
            if (search_term in s['name'].lower() or
                search_term in s.get('student_number', '').lower())
        ]

        self.student_grid.clear_widgets()
        headers = ['ID', 'Student #', 'Name', 'Class', 'Fees Paid', 'Actions']
        for header in headers:
            label = Label(text=header, size_hint_y=None, height=dp(40), bold=True)
            self.student_grid.add_widget(label)

        for student in filtered_students:
            # ID
            id_label = Label(text=str(student['id']), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(id_label)

            # Student Number
            num_label = Label(text=student.get('student_number', 'N/A'), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(num_label)

            # Name
            name_label = Label(text=student['name'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(name_label)

            # Class
            class_label = Label(text=student['class'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(class_label)

            # Fees Paid
            fees_label = Label(text=f"${student['fees_paid']}", size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(fees_label)

            # Actions
            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            edit_btn = Button(text='Edit', size_hint_x=0.4)
            assign_btn = Button(text='Assign Class', size_hint_x=0.6)

            edit_btn.bind(on_press=lambda x, s=student: self.edit_student(s))
            assign_btn.bind(on_press=lambda x, s=student: self.assign_student_class(s))

            action_box.add_widget(edit_btn)
            action_box.add_widget(assign_btn)
            self.student_grid.add_widget(action_box)

    def clear_search(self, instance):
        self.search_input.text = ''
        self.refresh_student_list()

    def show_add_student_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        self.student_number = TextInput(hint_text='Student Number (e.g. S2023001)')
        self.student_name = TextInput(hint_text='Full Name')
        self.student_class = Spinner(text='Select Class', values=self.class_list)
        self.student_fees = TextInput(hint_text='Fees Paid', input_filter='float')

        btn_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        save_btn = Button(text='Save')
        cancel_btn = Button(text='Cancel')

        save_btn.bind(on_press=self.add_student)
        cancel_btn.bind(on_press=lambda x: self.popup.dismiss())

        content.add_widget(self.student_number)
        content.add_widget(self.student_name)
        content.add_widget(self.student_class)
        content.add_widget(self.student_fees)
        btn_box.add_widget(save_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        self.popup = Popup(title='Add New Student', content=content, size_hint=(0.8, 0.7))
        self.popup.open()

    def show_bulk_import_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # Create file chooser with filters
        self.file_chooser = FileChooserListView(
            filters=['*.csv'],  # Only show CSV files
            path=os.path.expanduser('~')  # Start at user's home directory
        )

        import_btn = Button(text='Import CSV', size_hint_y=None, height=dp(50))
        cancel_btn = Button(text='Cancel', size_hint_y=None, height=dp(50))

        import_btn.bind(on_press=self.import_students_csv)
        cancel_btn.bind(on_press=lambda x: self.popup.dismiss())

        content.add_widget(self.file_chooser)
        btn_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        btn_box.add_widget(import_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        self.popup = Popup(title='Import Students from CSV', content=content, size_hint=(0.9, 0.8))
        self.popup.open()

    def add_student(self, instance):
        try:
            fees_paid = float(self.student_fees.text) if self.student_fees.text else 0
            new_student = {
                'id': len(self.student_list) + 1,
                'student_number': self.student_number.text,
                'name': self.student_name.text,
                'class': self.student_class.text,
                'fees_paid': fees_paid,
                'fees_due': 2000 - fees_paid
            }
            self.student_list.append(new_student)
            self.refresh_student_list()
            self.status_message = f"Added student: {new_student['name']} ({new_student['student_number']})"
            self.popup.dismiss()
        except ValueError:
            self.status_message = "Invalid fees amount"

    def import_students_csv(self, instance):
        if not self.file_chooser.selection:
            self.status_message = "No file selected"
            return

        try:
            filepath = self.file_chooser.selection[0]
            if not filepath.lower().endswith('.csv'):
                self.status_message = "Please select a CSV file"
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        fees_paid = float(row.get('fees_paid', 0))
                        self.student_list.append({
                            'id': len(self.student_list) + 1,
                            'student_number': row.get('student_number', ''),
                            'name': row.get('name', ''),
                            'class': row.get('class', ''),
                            'fees_paid': fees_paid,
                            'fees_due': 2000 - fees_paid
                        })
                    except ValueError:
                        continue  # Skip rows with invalid data

            self.refresh_student_list()
            self.status_message = f"Imported {len(reader.fieldnames)} fields from CSV"
            self.popup.dismiss()
        except Exception as e:
            self.status_message = f"Import failed: {str(e)}"

    def edit_student(self, student):
        self.status_message = f"Editing student: {student['name']} ({student.get('student_number', '')})"

    def assign_student_class(self, student):
        self.status_message = f"Assigning class for: {student['name']} ({student.get('student_number', '')})"

    def refresh_student_list(self):
        self.student_grid.clear_widgets()
        headers = ['ID', 'Student #', 'Name', 'Class', 'Fees Paid', 'Actions']
        for header in headers:
            label = Label(text=header, size_hint_y=None, height=dp(40), bold=True)
            self.student_grid.add_widget(label)

        for student in self.student_list:
            # ID
            id_label = Label(text=str(student['id']), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(id_label)

            # Student Number
            num_label = Label(text=student.get('student_number', 'N/A'), size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(num_label)

            # Name
            name_label = Label(text=student['name'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(name_label)

            # Class
            class_label = Label(text=student['class'], size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(class_label)

            # Fees Paid
            fees_label = Label(text=f"${student['fees_paid']}", size_hint_y=None, height=dp(40))
            self.student_grid.add_widget(fees_label)

            # Actions
            action_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(5))
            edit_btn = Button(text='Edit', size_hint_x=0.4)
            assign_btn = Button(text='Assign Class', size_hint_x=0.6)

            edit_btn.bind(on_press=lambda x, s=student: self.edit_student(s))
            assign_btn.bind(on_press=lambda x, s=student: self.assign_student_class(s))

            action_box.add_widget(edit_btn)
            action_box.add_widget(assign_btn)
            self.student_grid.add_widget(action_box)

    def _create_financial_management_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Search bar
        search_box = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        self.fee_search_input = TextInput(hint_text='Search by student name or ID', size_hint_x=0.7)

        # Blue search button
        search_btn = Button(text='Search',
                            size_hint_x=0.15,
                            background_color=(0.2, 0.6, 1, 1),  # Blue
                            background_normal='',
                            color=(1, 1, 1, 1))  # White text

        # Red clear button
        clear_btn = Button(text='Clear',
                           size_hint_x=0.15,
                           background_color=(1, 0.4, 0.4, 1),  # Red
                           background_normal='',
                           color=(1, 1, 1, 1))  # White text

        search_btn.bind(on_press=self.search_fee_records)
        clear_btn.bind(on_press=self.clear_fee_search)
        search_box.add_widget(self.fee_search_input)
        search_box.add_widget(search_btn)
        search_box.add_widget(clear_btn)
        layout.add_widget(search_box)

        # Fee records
        fee_box = BoxLayout(orientation='vertical', spacing=dp(10))
        fee_box.add_widget(Label(text='Fee Records', size_hint=(1, None), height=dp(30)))

        scroll = ScrollView()
        self.fee_grid = GridLayout(cols=5, size_hint_y=None, spacing=dp(5))  # Added column for ID
        self.fee_grid.bind(minimum_height=self.fee_grid.setter('height'))

        # Header row
        headers = ['ID', 'Student', 'Class', 'Amount', 'Status']
        for header in headers:
            self.fee_grid.add_widget(Label(text=header, size_hint_y=None, height=dp(40), bold=True))

        # Fee rows
        for student in self.student_list:
            status = 'Paid' if student['fees_due'] <= 0 else 'Pending'
            status_color = (0.2, 0.7, 0.3, 1) if status == 'Paid' else (1, 0.4, 0.4, 1)  # Green/Red

            # Student ID
            self.fee_grid.add_widget(Label(text=student.get('student_id', 'N/A'),
                                           size_hint_y=None, height=dp(40)))

            # Student Name
            self.fee_grid.add_widget(Label(text=student['name'],
                                           size_hint_y=None, height=dp(40)))

            # Class
            self.fee_grid.add_widget(Label(text=student['class'],
                                           size_hint_y=None, height=dp(40)))

            # Amount (changed to KES)
            amount_text = f"KES {student['fees_paid']:,}/{student['fees_paid'] + student['fees_due']:,}"
            self.fee_grid.add_widget(Label(text=amount_text,
                                           size_hint_y=None, height=dp(40)))

            # Status with colored background
            status_btn = Button(text=status,
                                size_hint_y=None, height=dp(40),
                                background_color=status_color,
                                background_normal='',
                                color=(1, 1, 1, 1))  # White text
            status_btn.bind(on_press=lambda x, s=student: self.view_fee_details(s))
            self.fee_grid.add_widget(status_btn)

        scroll.add_widget(self.fee_grid)
        fee_box.add_widget(scroll)
        layout.add_widget(fee_box)

        # Reports section
        report_box = BoxLayout(orientation='vertical', spacing=dp(10))
        report_box.add_widget(Label(text='Financial Reports', size_hint=(1, None), height=dp(30)))

        report_btns = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))

        # Blue fee collection report button
        fee_collection_btn = Button(text='Fee Collection',
                                    background_color=(0.2, 0.6, 1, 1),
                                    background_normal='',
                                    color=(1, 1, 1, 1))

        # Red outstanding fees button
        outstanding_btn = Button(text='Outstanding Fees',
                                 background_color=(1, 0.4, 0.4, 1),
                                 background_normal='',
                                 color=(1, 1, 1, 1))

        # Green annual report button
        annual_report_btn = Button(text='Annual Report',
                                   background_color=(0.2, 0.7, 0.3, 1),
                                   background_normal='',
                                   color=(1, 1, 1, 1))

        fee_collection_btn.bind(on_press=lambda x: self.generate_report('Fee Collection'))
        outstanding_btn.bind(on_press=lambda x: self.generate_report('Outstanding Fees'))
        annual_report_btn.bind(on_press=lambda x: self.generate_report('Annual Report'))

        report_btns.add_widget(fee_collection_btn)
        report_btns.add_widget(outstanding_btn)
        report_btns.add_widget(annual_report_btn)

        report_box.add_widget(report_btns)
        layout.add_widget(report_box)

        return layout

    def search_fee_records(self, instance):
        query = self.fee_search_input.text.lower()
        # Filter self.student_list based on query
        # Then refresh the fee_grid display

    def clear_fee_search(self, instance):
        self.fee_search_input.text = ''
        # Reset to show all records
        # Refresh the fee_grid display

    def view_fee_details(self, student):
        # Show detailed fee information for the student
        pass

    def generate_report(self, report_type):
        # Generate the requested financial report
        pass

    def generate_report(self, report_type):
        self.status_message = f"Generating {report_type} report..."

    # 5. Reports Functions
    def _create_reports_tab(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        # Academic reports
        academic_box = BoxLayout(orientation='vertical', spacing=dp(10))
        academic_box.add_widget(Label(text='Academic Reports', size_hint=(1, None), height=dp(30)))

        academic_btns = BoxLayout(size_hint=(1, None), height=dp(50), spacing=dp(10))
        for report in ['Class Performance', 'Subject Analysis', 'Teacher Evaluation']:
            btn = Button(text=report)
            btn.bind(on_press=lambda x, r=report: self.view_academic_report(r))
            academic_btns.add_widget(btn)

        academic_box.add_widget(academic_btns)
        layout.add_widget(academic_box)

        # System logs
        log_box = BoxLayout(orientation='vertical', spacing=dp(10))
        log_box.add_widget(Label(text='System Logs', size_hint=(1, None), height=dp(30)))

        self.log_display = TextInput(readonly=True, size_hint=(1, 0.6))
        refresh_btn = Button(text='Refresh Logs', size_hint=(1, None), height=dp(40))
        refresh_btn.bind(on_press=self.refresh_logs)

        log_box.add_widget(self.log_display)
        log_box.add_widget(refresh_btn)
        layout.add_widget(log_box)

        return layout

    def view_academic_report(self, report_type):
        self.status_message = f"Viewing {report_type} report"
        # Sample log entries
        self.log_display.text = f"""=== {report_type} Report ===
Date: {datetime.now().strftime('%Y-%m-%d')}
Generated by: {getattr(self.current_user, 'full_name', 'Admin')}

Summary:
- Grade 10A: 85% pass rate
- Grade 9B: 78% pass rate
- Math: 92% average
- Science: 88% average"""

    def refresh_logs(self, instance):
        self.status_message = "Refreshed system logs"
        self.log_display.text = "System logs refreshed at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Common Functions
    def refresh_data(self, instance):
        self.status_message = "Refreshing all data..."
        Clock.schedule_once(self._finish_refresh, 1)

    def _finish_refresh(self, dt):
        self.load_sample_data()
        self.status_message = "All data refreshed successfully"
        Clock.schedule_once(lambda dt: setattr(self, 'status_message', ""), 2)

    def show_reports(self, instance):
        self.tabs.switch_to(self.tabs.tab_list[-1])  # Switch to Reports tab
        self.status_message = "Showing reports dashboard"

    def logout(self, instance):
        self.manager.current = 'login'


class AdminApp(App):
    def build(self):
        sm = ScreenManager()
        admin_dash = AdminDashboard(name='admin_dashboard')

        # Create a mock user object
        class User:
            username = "admin"
            full_name = "System Administrator"
            role = "Admin"

        admin_dash.current_user = User()
        sm.add_widget(admin_dash)
        return sm


if __name__ == '__main__':
    AdminApp().run()