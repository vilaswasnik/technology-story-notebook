import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText


def main():
    window = tk.Tk()
    window.title("My Technology Story Notebook")
    window.geometry("900x600")

    heading = tk.Label(
        window,
        text="My Technology Story Notebook",
        font=("Arial", 20, "bold"),
    )
    heading.pack(pady=20)

    welcome = tk.Label(
        window,
        text="Write what you know. Reflect, revise, and prepare.",
        font=("Arial", 12),
    )
    welcome.pack()
    content = tk.Frame(window)
    content.pack(fill="both", expand=True, padx=20, pady=20)

    sidebar = tk.Frame(content)
    sidebar.pack(side="left", fill="y")

    technology_heading = tk.Label(
        sidebar,
        text="Technologies",
        font=("Arial", 14, "bold"),
    )
    technology_heading.pack(anchor="w", pady=(0, 10))

    technology_list = tk.Listbox(
        sidebar,
        font=("Arial", 12),
        width=22,
        exportselection=False,
    )
    technology_list.pack(fill="y", expand=True)

    technologies = ["Linux", "Ansible", "Kubernetes", "Python"]
    stories_folder = Path(__file__).resolve().parent / "stories"
    order_path = stories_folder / ".technology_order.json"

    try:
        for technology in technologies:
            technology_folder = stories_folder / technology
            technology_folder.mkdir(parents=True, exist_ok=True)

        known_names = {name.casefold() for name in technologies}

        for folder in sorted(
            stories_folder.iterdir(),
            key=lambda path: path.name.casefold(),
        ):
            if folder.is_dir() and folder.name.casefold() not in known_names:
                technologies.append(folder.name)
                known_names.add(folder.name.casefold())

    except OSError as error:
        messagebox.showerror(
            "Folder setup failed",
            f"Could not prepare the technology folders:\n{error}",
            parent=window,
        )
        window.destroy()
        return

    try:
        saved_order = json.loads(order_path.read_text(encoding="utf-8"))
        if not isinstance(saved_order, list) or any(
            not isinstance(name, str) for name in saved_order
        ):
            raise ValueError("The saved technology order must be a list of names.")
    except FileNotFoundError:
        saved_order = []
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        messagebox.showerror(
            "Technology order failed",
            f"Could not read the saved technology order:\n{error}",
            parent=window,
        )
        window.destroy()
        return

    available_technologies = technologies
    technology_by_name = {
        technology.casefold(): technology for technology in available_technologies
    }
    ordered_technologies = []
    ordered_names = set()
    for name in saved_order:
        normalized_name = name.casefold()
        technology = technology_by_name.get(normalized_name)
        if technology is not None and normalized_name not in ordered_names:
            ordered_technologies.append(technology)
            ordered_names.add(normalized_name)
    technologies = ordered_technologies + [
        technology
        for technology in available_technologies
        if technology.casefold() not in ordered_names
    ]

    for technology in technologies:
        technology_list.insert(tk.END, technology)
    editor_panel = tk.Frame(content)
    editor_panel.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(20, 0),
    )

    story_heading = tk.Label(
        editor_panel,
        text="Write your technology story",
        font=("Arial", 14, "bold"),
    )
    story_heading.pack(anchor="w", pady=(0, 10))

    story_editor = ScrolledText(
        editor_panel,
        wrap="word",
        font=("Arial", 12),
        undo=True,
    )
    story_editor.pack(fill="both", expand=True)

    word_count_label = tk.Label(
        editor_panel,
        text="Words: 0",
        font=("Arial", 10),
    )
    word_count_label.pack(anchor="w", pady=(5, 0))

    def update_word_count(event=None):
        text = story_editor.get("1.0", "end-1c")
        word_count = len(text.split())
        word_count_label.config(text=f"Words: {word_count}")

    def on_story_modified(event):
        if story_editor.edit_modified():
            update_word_count()
            story_editor.edit_modified(False)

    story_editor.edit_modified(False)
    story_editor.bind("<<Modified>>", on_story_modified)

    drafts = {technology: "" for technology in technologies}
    try:
        for technology in technologies:
            story_path = stories_folder / technology / "story.txt"

            try:
                drafts[technology] = story_path.read_text(encoding="utf-8")
            except FileNotFoundError:
                drafts[technology] = ""
    except (OSError, UnicodeError) as error:
        messagebox.showerror(
            "Loading failed",
            f"Could not read a story:\n{error}",
            parent=window,
        )
        window.destroy()
        return
    current_technology = None

    saved_stories = drafts.copy()
    current_technology = None

    story_editor.config(state="disabled")

    drag_source = None
    order_changed = False

    def begin_technology_drag(event):
        nonlocal drag_source, order_changed

        index = technology_list.nearest(event.y)
        drag_source = index if 0 <= index < len(technologies) else None
        order_changed = False

    def drag_technology(event):
        nonlocal drag_source, order_changed

        if drag_source is None:
            return "break"

        target = technology_list.nearest(event.y)
        if not 0 <= target < len(technologies) or target == drag_source:
            return "break"

        technology = technologies.pop(drag_source)
        technologies.insert(target, technology)
        technology_list.delete(drag_source)
        technology_list.insert(target, technology)

        if current_technology is not None:
            current_index = technologies.index(current_technology)
            technology_list.selection_clear(0, tk.END)
            technology_list.selection_set(current_index)
            technology_list.activate(current_index)

        drag_source = target
        order_changed = True
        return "break"

    def save_technology_order():
        temporary_path = order_path.with_suffix(".tmp")
        try:
            temporary_path.write_text(
                json.dumps(technologies, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary_path.replace(order_path)
        except (OSError, UnicodeError) as error:
            messagebox.showerror(
                "Order save failed",
                f"Could not save the technology order:\n{error}",
                parent=window,
            )

    def end_technology_drag(event):
        nonlocal drag_source

        if order_changed:
            save_technology_order()
        drag_source = None

    def select_technology(event):
        nonlocal current_technology

        selected_items = technology_list.curselection()

        if not selected_items:
            return

        technology = technology_list.get(selected_items[0])

        if technology == current_technology:
            return

        if current_technology is not None:
            drafts[current_technology] = story_editor.get("1.0", "end-1c")

        current_technology = technology

        story_editor.config(state="normal")
        story_editor.delete("1.0", tk.END)
        story_editor.insert("1.0", drafts[technology])
        story_editor.edit_reset()

        story_heading.config(text=f"My {technology} story")
        story_editor.focus_set()

    def save_story():
        if current_technology is None:
            messagebox.showwarning(
                "Choose a technology",
                "Select a technology before saving.",
                parent=window,
            )
            return

        text = story_editor.get("1.0", "end-1c")
        story_path = stories_folder / current_technology / "story.txt"
        temporary_path = story_path.with_suffix(".tmp")

        try:
            temporary_path.write_text(text, encoding="utf-8")
            temporary_path.replace(story_path)
        except (OSError, UnicodeError) as error:
            messagebox.showerror(
                "Saving failed",
                f"Could not save your story:\n{error}",
                parent=window,
            )
            return

        drafts[current_technology] = text
        saved_stories[current_technology] = text

        messagebox.showinfo(
            "Story saved",
            f"Your {current_technology} story was saved.",
            parent=window,
        )

    def close_notebook():
        if current_technology is not None:
            drafts[current_technology] = story_editor.get("1.0", "end-1c")

        unsaved_technologies = [
            technology
            for technology in technologies
            if drafts[technology] != saved_stories[technology]
        ]

        if unsaved_technologies:
            technology_names = ", ".join(unsaved_technologies)

            should_close = messagebox.askokcancel(
                "Unsaved stories",
                f"Unsaved changes in: {technology_names}\n\n"
                "OK: discard unsaved changes and close.\n"
                "Cancel: return to the notebook to save.",
                parent=window,
            )

            if not should_close:
                return

        window.destroy()

    technology_list.bind("<ButtonPress-1>", begin_technology_drag)
    technology_list.bind("<B1-Motion>", drag_technology)
    technology_list.bind("<ButtonRelease-1>", end_technology_drag)
    technology_list.bind("<<ListboxSelect>>", select_technology)
    save_button = tk.Button(
        editor_panel,
        text="Save Story",
        command=save_story,
    )
    save_button.pack(anchor="e", pady=(10, 0))
    window.protocol("WM_DELETE_WINDOW", close_notebook)

    window.mainloop()


if __name__ == "__main__":
    main()