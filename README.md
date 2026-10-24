# My Technology Story Notebook

A personal notebook for tracking what you know about technology and turning that knowledge into confident interview answers.

## Objective

Help people capture their understanding of technologies, reflect on their experience, and prepare for interviews. Instead of scattered notes, keep a story for each technology: what you know, how you have used it, what problems you have solved, and what you still want to learn.

## Project at a glance

```text
My Technology Story Notebook

Technologies             My Linux story
-------------------      ------------------------------------
Linux                    What I know:
Ansible                  Processes, permissions, and networking.
Kubernetes
Python                   My experience:
+ Add a technology       Diagnosing a service startup failure.

Drag entries to reorder  Interview preparation:
                         Explain the problem, approach, result,
                         and lessons learned.

                         Words: 30               [Save story]
```

## Features

- Organize notes by technology.
- Write and revise your technology stories.
- See a live word count.
- Drag technology entries to arrange them in your preferred order.
- Remember the order between launches.
- Receive a warning before leaving with unsaved stories.
- Add technologies directly in the browser version.

## Run the browser version

Open [index.html](index.html) in a modern browser. No installation or build step is needed.

The browser version runs without a subscription, account, or paid hosting.

Click a technology, write your notes, and choose **Save story**. Drag a technology entry to change its position. Use **Add a technology** to create another category.

Stories and technology order are stored in that browser's local storage. They are not uploaded to a server or synchronized across browsers or devices. Clearing browser storage removes the saved notebook data.

## Publish with GitHub Pages

1. Push the project to the `main` branch of a public GitHub repository.
2. In the repository, open **Settings > Pages** and select **GitHub Actions** as the source.
3. Open **Actions > Deploy notebook to GitHub Pages** and choose **Run workflow** if the initial deployment has not succeeded.
4. Once deployment finishes, open the website link shown in **Settings > Pages**.

The included workflow publishes only the browser app. Personal desktop notes in `stories` are excluded from Git.

## Run the desktop version

With Python and Tkinter installed:

```powershell
python start.py
```

The desktop app saves each story in a `stories\<technology>\story.txt` file and the sidebar order in `stories\.technology_order.json`. The default technologies are Linux, Ansible, Kubernetes, and Python. To add another desktop category, create a folder with its name inside `stories` and reopen the app.

**The browser and desktop versions use separate storage. They do not currently synchronize or import each other's notes.**

## Suggested interview preparation template

```text
Technology:

What I understand:
Key concepts I can explain in my own words.

Where I have used it:
Projects, tasks, and real-world experience.

A problem I solved:
Situation, approach, outcome, and lessons learned.

Questions to practice:
Topics I should be ready to discuss.

What I want to learn next:
Gaps and next steps.
```

Revisit your stories regularly, add concrete examples, and practice explaining them aloud before an interview.
