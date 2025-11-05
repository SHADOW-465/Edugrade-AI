# 🤖 EduGrade AI: The Super-Smart Grading Robot!

Welcome to EduGrade AI! Imagine you have a friendly robot helper who can read and grade homework for every student, from tiny kindergarteners to super-smart college students. That's what EduGrade AI is! It's a magical tool that looks at pictures of handwritten homework and grades it, giving helpful feedback, all by itself.

## ✨ Key Features

-   **🧠 Adapts to Any Grade Level**: Just like a chameleon changes colors, EduGrade AI changes how it grades based on the student's age. It's gentle with little kids and super detailed with college students.
-   **✍️ Reads All Kinds of Handwriting**: From simple block letters to fancy cursive and even tricky math equations, our robot can read it all.
-   **✅ Smart Grading**: It doesn't just check for right or wrong. It understands the *meaning* behind the answers.
-   **👍 Helpful Feedback**: Gives feedback that is just right for the student—encouraging words for younger kids and scholarly advice for older students.
-   **🔒 Safe and Secure**: Uses a special database called Convex to keep all the grades safe. It even has a backup plan (using a local SQLite database) in case the internet gets sleepy.
-   **🧑‍🏫 Teacher's Best Friend**: Teachers can easily review all the grades and make changes if they want.

---

## 🚀 Getting Started: Let's Bring Your Robot to Life!

Follow these simple steps to get your own EduGrade AI running. It's like building with LEGOs!

### Part 1: What You'll Need (Your Toolbox)

Make sure you have these tools installed on your computer before you start:

1.  **Python**: The language our robot speaks. (Version 3.9 or newer)
2.  **Docker**: A magic box that runs our app perfectly every time.
3.  **Git**: A time machine for code, so you can get the latest version.
4.  **A Code Editor**: Like VS Code or Cursor, a place to look at the code.

### Part 2: Setting Up the Project

#### Step 1: Get the Code

First, you need to copy the project to your computer. Open your computer's command line (like Terminal or PowerShell) and type this:

```bash
git clone <repository-url>
cd edugrade-ai
```

#### Step 2: Your Secret Keys! (Environment Variables)

Our robot needs some secret keys to connect to its brain and other magical internet services. We'll keep these in a special file called `.env`.

1.  Find the file named `env.example`.
2.  Make a copy of it and name the copy `.env`.
3.  Open the new `.env` file and fill in your secret keys!

Here’s what each key does and where to get it:

| Variable                  | What it is                                      | Where to Get It                                                                                                                                                                |
| ------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GEMINI_API_KEY`          | The key to Google's AI brain (Gemini).          | Go to the [Google AI Studio](https://aistudio.google.com/app/apikey) and click "Create API key". Copy the key and paste it here.                                                 |
| `CONVEX_DEPLOYMENT_URL`   | The address of your Convex database.            | 1. Go to [Convex](https://www.convex.dev/) and create a new project. <br> 2. Follow their instructions to deploy the schema from `backend/convex/`. <br> 3. Copy the Deployment URL from your project settings. |
| `PADDLEOCR_MODEL_PATH`    | Path to the advanced OCR model.                 | This will be set up automatically by the Docker container, you can often leave this blank or as a default path.                                                                  |
| `PLAGIARISM_API_KEY`      | Key for checking college papers for copying.    | Sign up for a plagiarism detection service (like Turnitin or a similar API) and get your key from their website.                                                                 |

Your `.env` file should look something like this:

```
GEMINI_API_KEY="a_very_long_secret_key_from_google"
CONVEX_DEPLOYMENT_URL="https://your-cool-project.convex.site"
PLAGIARISM_API_KEY="another_secret_key"
```

#### Step 3: Start the Magic! (Run with Docker)

This is the easiest and best way to run everything. Docker will build all the parts of our app in special containers, so you don't have to worry about installing a million things.

Make sure Docker is running on your computer, then open your command line in the project folder and run:

```bash
docker-compose up --build
```

That's it! You're done! Your EduGrade AI is now alive and running.

-   **Backend API**: You can talk to the robot's brain at `http://localhost:8000`
-   **Streamlit Dashboard**: See the teacher's dashboard at `http://localhost:8501`

---

## 🏗️ Project Structure (A Map of the Robot)

Here’s a map to help you find your way around the code.

```
edugrade-ai/
├── backend/          # The Engine Room (where the robot's brain lives)
│   ├── app/
│   │   ├── agents/     # The different "mini-bots" for each task
│   │   ├── api/        # How the outside world talks to the robot
│   │   ├── core/       # The robot's personality and settings
│   │   ├── graph/      # The master plan that the agents follow
│   │   └── services/   # Special tools the robot uses (like the Grade Detector)
│   ├── convex/       # The blueprint for the robot's memory (database)
│   └── tests/        # A gym to make sure the robot is working correctly
│
├── frontend/         # The Face of the Robot (what users see)
│   └── streamlit_dashboard.py # The dashboard for teachers and parents
│
├── data/             # Where the robot stores its files and models
│
├── docker-compose.yml # The instruction manual for Docker
└── README.md          # You are here!
```

## 🧪 Testing (Giving the Robot a Check-up)

To make sure all the parts of our robot are working perfectly, we have tests. You can run them with this command:

```bash
pytest backend/tests
```

This will run a series of check-ups to make sure the robot can still think, read, and grade correctly.

---

Happy Grading! 🎓
