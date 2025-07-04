# GATE CSE AIR 1 Companion

A comprehensive Flask web application for GATE Computer Science Engineering preparation with AI-powered learning prompts, progress tracking, and motivational features.

## Features

- 🔐 **Secure Login System** with personalized access
- 🎯 **Interactive Learning Roadmap** for all GATE CSE subjects
- 🤖 **AI Prompt Generator** with one-click integration for ChatGPT, Claude, Grok, and Gemini
- 📊 **Progress Tracking** with concept mastery tracker
- 💾 **Persistent Storage** using localStorage
- 🎉 **Motivational Features** including celebration animations and progress visualization
- 📱 **Responsive Design** for desktop and mobile devices

## Login Credentials

- **Username:** `amma`
- **Password:** `Iloveyoumaa`

## Quick Start

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```
   Or use the batch file:
   ```bash
   run.bat
   ```

3. Open your browser and go to `http://localhost:5000`

### Deployment

#### Heroku
1. Create a new Heroku app
2. Connect your GitHub repository
3. Enable automatic deployments
4. The app will use the `Procfile` for deployment

#### Railway/Render
1. Connect your GitHub repository
2. Set the start command to: `python app.py`
3. Deploy automatically

#### Manual Server Deployment
1. Upload all files to your server
2. Install Python and pip
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python app.py`

## File Structure

```
├── app.py                 # Main Flask application
├── app_flask.py          # Original Flask file (backup)
├── credentials.json      # User authentication data
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── run.bat              # Local run script
├── static/
│   └── popup.PNG        # Motivational popup image
└── templates/
    ├── index.html       # Main application interface
    └── login.html       # Login page
```

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS with modern gradient designs
- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Poppins)

## Features Overview

### Subjects Covered
- Engineering Mathematics
- Digital Logic
- Computer Organization and Architecture
- Programming and Data Structures
- Algorithms
- Theory of Computation
- Compiler Design
- Operating System
- Databases
- Computer Networks

### AI Integration
- Auto-generated prompts for each topic
- One-click integration with popular AI platforms
- Topic-specific chat session management
- Copy/download functionality for prompts

### Progress Tracking
- Visual roadmap with checkpoints
- Concept mastery tracker for each topic
- Overall progress visualization
- Persistent progress storage

## Security Notes

- Session-based authentication
- Secure credential storage
- Protected routes with login required decorator

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is created for educational purposes to help GATE CSE aspirants achieve AIR 1.

---

**Made with ❤️ to help you reach GATE CSE AIR 1**
