# Robustness Evaluation Benchmark

A benchmark platform for measuring CNN robustness against adversarial attacks: 6 models tested against 13 attacks, with a portal for researchers to submit their own.

🔗 **Live demo:** https://robustness-evaluation-benchmark.onrender.com

🎓 **Background:** Website for a team research project on adversarial robustness, advised by Prof. Sy-Yen Kuo, National Taiwan University, 2020

📄 **Paper:** [Evaluating Robustness of AI Models against Adversarial Attacks](https://doi.org/10.1145/3385003.3410920), ACM SPAI 2020

![Benchmark heatmap](static/images/1.png)

---

## Features

- **Benchmark** — compare how 6 CNN models on MNIST, CIFAR-10 and ImageNet hold up against 13 adversarial attacks in a colour-coded heatmap
- **About** — read plain-language explainers on adversarial attacks and how robustness is scored
- **Submit** — send a model or an attack by URL for the lab to evaluate

---

## How It Works

- **Attack-agnostic scoring** — each attack is weighted by how well it separates the models, so no single attack type dominates
- **Models and attacks** — Simple CNN, the C&W model, All-CNN, VGG19, ResNet50 and InceptionV3, attacked with Foolbox, ART and CleverHans
- **Benchmark heatmap** — built directly in HTML and CSS with each cell coloured by attack success rate
- **Submissions** — the server checks every field, then emails the lab through the AgentMail API

---

## Security

The live demo is public, so the code covers the main OWASP Top 10 risks:

- **Cross-site scripting** — Jinja2 escapes everything users type before it appears on a page
- **Cross-site request forgery** — the submission form carries a secret token that Flask-WTF checks
- **Security misconfiguration** — debug mode is off, secrets live only in environment variables, and Render generates the session key

---

## Tech Stack

| Layer | Tools |
|---|---|
| Backend | Flask 3.1, Jinja2 |
| Forms & security | Flask-WTF, WTForms |
| Email delivery | AgentMail HTTP API via `requests` |
| WSGI server | gunicorn |
| Frontend | Bootstrap, jQuery, Owl Carousel, Magnific Popup, Stellar.js, animate.css |
| Hosting | Render |

---

## Running Locally

Requires Python 3.14.

```bash
git clone https://github.com/cassielo/robustness-evaluation-benchmark.git
cd robustness-evaluation-benchmark
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

---

## Project Structure

```
app.py               Flask app: routes, form validation, notification email
templates/           pages: index, about, benchmark, submit
static/              css, js, images, fonts, videos
resource/            sample analysis report
requirements.txt     pinned dependencies
.python-version      Python version for the host
render.yaml          Render deployment config
```

---

## Project Status

Live and maintained: the lab evaluates each submission by running the 13 attacks and emails back the robustness score. Next, this evaluation will run automatically on every submission.
