# ScheduleSync
**ScheduleSync** is an open-source platform that helps students and academic groups manage and sync their class and exam timetables directly to Google Calendar. Designed for simplicity and collaboration, ScheduleSync makes it easy for students to stay organized and never miss an important lecture or exam.

### Still a work in progress

## Features

### MVP Features
- Join a class group via a personalized link
- Connect your Google Calendar
- Receive automatic calendar updates from your group’s schedule
- Admins can create and manage class schedules manually
- Support for recurring events
- Daily reminders sent the night before with the next day’s schedule

### Upcoming Features
- Custom reminder times
- Smart alerts for changes or overlaps in schedule
- Assignment tracker (admin-managed)
- Timetable scanner (image or PDF to calendar)
- Bulk entry for schedules

## How It Works
1. **Group Creation**: A group is created for a class or subject. 
2. **Invite & Approval**: Students join via a unique invite link and wait for admin approval.
3. **Calendar Sync**: Upon approval, the group’s timetable is synced to their Google Calendar.
4. **Reminders**: Users receive daily summaries of the next day’s schedule via email or notification.

## Tech Stack
- **Backend**: Django
- **Database**: PostgreSQL
- **OAuth & Calendar Integration**: Google Calendar API
- **Email Notifications**: SendGrid

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/steppacodes/schedulesync.git
cd schedulesync
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root and get the required variables from the (.env.example file)[.env.example]:

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Contributing

Contributions are welcome. To contribute:
1. Fork the repository
2. Create a new branch for your feature or fix
3. Submit a pull request with a clear description of your changes

Please read our `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` when available.

## License

This project is licensed under the [MIT License](LICENSE).
