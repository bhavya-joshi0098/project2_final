from flask import Flask, request, render_template , session , redirect, url_for , flash
from auth import signup_db, login_db
from functools import wraps
from models import User
import google.generativeai as genai
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your actual secret key

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper

# Configure Gemini AI
genai.configure(api_key="AIzaSyBjqSYnsr2Le7-QgX_eoATrrQ-Y9mGNS2U")
model = genai.GenerativeModel("gemini-1.5-flash")

def get_dicebear_avatar(name):
    # Create a hash of the name to get consistent avatar
    hash_object = hashlib.md5(name.encode())
    seed = hash_object.hexdigest()
    return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}"

# Function to send prompt to Gemini AI
def send_prompt(prompt_text):
    try:
        response = model.generate_content(prompt_text)
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return f"<!-- Failed to generate content: {str(e)} -->"

@app.route("/", methods=["GET", "POST"])
@login_required
def form():
    if request.method == "POST":
        data = request.form.to_dict()
        
        # Generate DiceBear avatar URL
        avatar_url = get_dicebear_avatar(data.get('name', 'Your Name'))
        data['avatar_url'] = avatar_url

        # === Improved Prompts for Creative Sections ===
        prompts = []

        # Navbar & Head
        prompts.append(f"""You are an expert in HTML, Bootstrap 5, and JavaScript. Generate only the <head> section and responsive navbar using Bootstrap 5 for a personal portfolio. Include Google Fonts (Poppins), Font Awesome icons, smooth scroll links, and a sticky top navbar. Do not include any explanation — return only raw HTML.

Name: {data.get('name', 'Your Name')}
Title: {data.get('title', 'Web Developer')}
Intro: {data.get('intro', 'Welcome to my personal portfolio!')}
""")

        # Hero Section with Avatar
        prompts.append(f"""Create a full-screen hero section with a gradient background, animated title using typed.js, and a call-to-action button. Include a profile image from {avatar_url}. Style it creatively using Bootstrap 5 and add parallax effect if possible. Do not include any explanation — return only raw HTML.""")

        # About Me, Education, Languages Known
        prompts.append(f"""Generate only the "About Me", "Education", and "Languages Known" sections using Bootstrap 5 cards or timeline style. Add padding, margin, and subtle shadow to each card. Use icons and a vibrant color scheme. Make it visually appealing. Do not include any explanation — return only raw HTML.

About: {data.get('about', '')}
Education: {data.get('education', '')}
Languages: {data.get('languages', '')}
""")

        # Skills, Certifications, Hobbies
        prompts.append(f"""Create only the "Skills", "Certifications", and "Hobbies" sections using Bootstrap 5. Use animated progress bars for skills, badges with icons for certifications, and icon-based list for hobbies. Style them with soft gradients and rounded corners. Do not include any explanation — return only raw HTML.

Skills: {data.get('skills', '')}
Certifications: {data.get('certifications', '')}
Hobbies: {data.get('hobbies', '')}
""")

        # Projects (Masonry Grid)
        prompts.append(f"""Add only the "Projects" section using a responsive masonry grid layout from Bootstrap 5. Each project should have a hover zoom effect, image, title, and short description. Use pastel backgrounds and border shadows. Do not include any explanation — return only raw HTML.

Projects: {data.get('projects', '')}
""")

        # Internships, Work Experience
        prompts.append(f"""Create only the "Internships" and "Work Experience" sections using vertical timeline design. Use icons and Bootstrap cards. Make it elegant and interactive. Do not include any explanation — return only raw HTML.

Internships: {data.get('internships', '')}
Experience: {data.get('experience', '')}
""")

        # Services Offered, Testimonials
        prompts.append(f"""Create only the "Services Offered" and "Testimonials" sections using Bootstrap 5. Use icons for services and a carousel with fade animation for testimonials. Apply soft borders, shadows, and glassmorphism. Make it elegant and user-friendly. Do not include any explanation — return only raw HTML.

Services: {data.get('services', '')}
Testimonials: {data.get('testimonials', '')}
""")

        # Contact and Footer
        prompts.append(f"""Generate only the "Contact" and "Footer" sections using Bootstrap 5. Use input fields with floating labels, social media buttons, and a stylish footer with copyright info. Style inputs with focus glow and rounded corners. Do not include any explanation — return only raw HTML.

Phone: {data.get('phone', '')}
Email: {data.get('email', '')}
Location: {data.get('location', '')}
Social Links: {data.get('social', '')}
""")

        # Generate HTML from all prompts
        sections = []
        for prompt in prompts:
            html_response = send_prompt(prompt)
            sections.append(html_response)

        return render_template("portfolio.html", 
                             sections=sections,
                             data=data)

    return render_template("form.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message, category, status, user = login_db(username, password)
        flash(message=message, category=category)
        if status == True:
            session["user_id"] = user.id
            # print(f"USER {session['user_id']} is now logged in")
            return redirect(url_for("form"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        message, category, status = signup_db(name, email, username, password)
        flash(message=message, category=category)
        if status == True:
            return redirect(url_for("login"))
        else:
            return redirect(url_for("signup"))
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)